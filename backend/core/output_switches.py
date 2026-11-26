"""B01/P02 output decisions; callers must check again immediately before effects."""

from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from typing import Any

from backend.core.contracts import validate_payload

OUTPUTS = frozenset(
    {
        "public_analysis",
        "studio.audio",
        "studio.video",
        "publishing.domestic",
        "publishing.foreign",
        "publishing.public_reports",
    }
)
_CONTINUOUS = frozenset({"ingest", "archive", "private_report"})


class OutputBlocked(PermissionError):
    """The current control revision does not permit this output."""


def require_output_enabled(
    load_controls: Callable[[], Mapping[str, Any]],
    output: str,
    *,
    classification: str = "internal",
    held: bool = False,
    deadline_at: datetime | None = None,
    expected_revision: int | None = None,
    revalidate: Callable[[], bool] | None = None,
    now: datetime | None = None,
) -> int:
    """Load current controls on every call, including immediately before dispatch.

    This decision does not replace actor authorization or rights checks.
    A held job needs a fresh policy/rights callback and an unexpired deadline.
    """
    if output not in OUTPUTS | _CONTINUOUS:
        raise OutputBlocked("Unknown output")
    if classification == "executive_private" and output != "private_report":
        raise OutputBlocked("Private reports cannot enter output or general archive paths")

    controls = load_controls()
    validate_payload("output_controls", controls)
    revision = controls["revision"]

    if held:
        current_time = now or datetime.now(timezone.utc)
        if (
            deadline_at is None
            or deadline_at.tzinfo is None
            or deadline_at <= current_time
            or expected_revision is None
            or expected_revision != revision
            or revalidate is None
            or not revalidate()
        ):
            raise OutputBlocked("Held job requires current authorization and deadline")

    if output in _CONTINUOUS:
        return revision
    if output == "public_analysis":
        allowed = controls["public_analysis"]["enabled"]
    elif output.startswith("studio."):
        key = "audio_enabled" if output == "studio.audio" else "video_enabled"
        allowed = controls["studio"]["enabled"] and controls["studio"][key]
    else:
        key = output.split(".", 1)[1] + "_enabled"
        allowed = controls["publishing"]["enabled"] and controls["publishing"][key]

    if not allowed:
        raise OutputBlocked("Output disabled")
    return revision
