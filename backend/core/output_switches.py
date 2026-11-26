"""B01/P02 the three independent output switches (ADR-004).

Turning an output off must never stop ingestion, archiving or the private EIC
reports. Each switch is read before a side effect, never cached per process.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from backend.core.contracts import validate_payload

PUBLIC_ANALYSIS = "public_analysis"
STUDIO = "studio"
PUBLISHING = "publishing"
OUTPUTS = (PUBLIC_ANALYSIS, STUDIO, PUBLISHING)

_STUDIO_CHANNELS = {"audio": "audio_enabled", "video": "video_enabled"}
_PUBLISHING_STREAMS = {
    "domestic": "domestic_enabled",
    "foreign": "foreign_enabled",
    "public_report": "public_reports_enabled",
    "public_reports": "public_reports_enabled",
}


class OutputDisabled(Exception):
    """A side effect was requested while its output switch is off."""


@dataclass(frozen=True)
class OutputSwitches:
    """A validated ``output_controls`` record."""

    record: Mapping[str, Any]

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "OutputSwitches":
        validate_payload("output_controls", record)
        return cls(record=dict(record))

    @property
    def revision(self) -> int:
        return int(self.record["revision"])

    def enabled(self, output: str) -> bool:
        if output not in OUTPUTS:
            raise KeyError(f"unknown output: {output!r}")
        section = self.record[output]
        if not isinstance(section, Mapping) or not section.get("enabled"):
            return False
        return True

    def studio_channel_enabled(self, channel: str) -> bool:
        if channel not in _STUDIO_CHANNELS:
            raise KeyError(f"unknown studio channel: {channel!r}")
        if not self.enabled(STUDIO):
            return False
        return bool(self.record[STUDIO].get(_STUDIO_CHANNELS[channel]))

    def publishing_stream_enabled(self, stream: str) -> bool:
        field = _PUBLISHING_STREAMS.get(stream)
        if field is None:
            raise KeyError(f"unknown publishing stream: {stream!r}")
        if not self.enabled(PUBLISHING):
            return False
        return bool(self.record[PUBLISHING].get(field))

    def require(self, output: str) -> None:
        if not self.enabled(output):
            raise OutputDisabled(f"output {output!r} is disabled")


def default_off_switches() -> OutputSwitches:
    """Fail-safe baseline: every output off, valid against the contract."""
    record = {
        "schema_version": "1.0",
        "revision": 1,
        "updated_at": "1970-01-01T00:00:00Z",
        "updated_by": "system-default",
        "public_analysis": {"enabled": False},
        "studio": {"enabled": False, "audio_enabled": False, "video_enabled": False},
        "publishing": {
            "enabled": False,
            "domestic_enabled": False,
            "foreign_enabled": False,
            "public_reports_enabled": False,
        },
    }
    return OutputSwitches.from_record(record)
