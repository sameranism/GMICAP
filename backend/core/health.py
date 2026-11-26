"""B01/P27 health: liveness plus dependency usability.

Health answers two different questions: is the process alive (always true when
it answers) and are its dependencies usable. It never returns secrets or URLs
with credentials. Logging helpers live in ``observability.py`` and are re-exported
here for convenience only.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Mapping

from backend.core.db import DatabaseRegistry
from backend.core.observability import configure_logging, log_event

__all__ = ["configure_logging", "health_report", "log_event"]


def _probe(callable_: Callable[[], bool]) -> tuple[str, str]:
    try:
        return ("ok" if callable_() else "degraded"), ""
    except Exception as exc:  # noqa: BLE001 - a probe must never break health
        return "unavailable", type(exc).__name__


def health_report(
    *,
    databases: DatabaseRegistry | None = None,
    probes: Mapping[str, Callable[[], bool]] | None = None,
    version: str = "0.1.0",
) -> dict[str, Any]:
    """Aggregate dependency state into a safe, machine-readable report."""
    checks: dict[str, dict[str, str]] = {}

    if databases is not None:
        for role, described in databases.describe().items():
            state = "not_configured" if described == "not_configured" else "configured"
            checks[f"db.{role}"] = {"state": state, "detail": described}

    for name, probe in (probes or {}).items():
        state, detail = _probe(probe)
        checks[name] = {"state": state, "detail": detail}

    degraded = [name for name, check in checks.items() if check["state"] in {"degraded", "unavailable"}]
    return {
        "status": "degraded" if degraded else "ok",
        "version": version,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "degraded": degraded,
    }
