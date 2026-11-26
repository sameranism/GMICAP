"""B01/P03 source registry management.

A source is usable only when it is both enabled and rights-cleared. Registration
validates the whole ``source_registry`` document, so a malformed source cannot
be enabled by a side door.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Mapping

from backend.core.contracts import validate_payload

BLOCKED_SCOPE = "unknown"


class SourceNotFound(KeyError):
    """The requested source id is not registered."""


class SourceNotAllowed(RuntimeError):
    """The source exists but may not be used for this stream or rights scope."""


@dataclass
class SourceService:
    """In-memory registry fixture; the authoritative store is PostgreSQL."""

    registry_id: str = "default"
    _sources: dict[str, dict[str, Any]] = field(default_factory=dict, repr=False)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def register(self, source: Mapping[str, Any]) -> dict[str, Any]:
        candidate = dict(source)
        self._validate_with([candidate])
        with self._lock:
            self._sources[str(candidate["source_id"])] = candidate
        return dict(candidate)

    def set_enabled(self, source_id: str, enabled: bool) -> dict[str, Any]:
        with self._lock:
            source = self._sources.get(source_id)
            if source is None:
                raise SourceNotFound(source_id)
            updated = dict(source)
            updated["enabled"] = bool(enabled)
            self._sources[source_id] = updated
        self._validate_with(list(self._sources.values()))
        return dict(updated)

    def get(self, source_id: str) -> dict[str, Any]:
        with self._lock:
            source = self._sources.get(source_id)
        if source is None:
            raise SourceNotFound(source_id)
        return dict(source)

    def list(self, *, enabled_only: bool = False) -> list[dict[str, Any]]:
        with self._lock:
            values = [dict(item) for item in self._sources.values()]
        values.sort(key=lambda item: item["source_id"])
        if enabled_only:
            values = [item for item in values if item["enabled"]]
        return values

    def require_usable(self, source_id: str, stream: str | None = None) -> dict[str, Any]:
        source = self.get(source_id)
        if not source["enabled"]:
            raise SourceNotAllowed(f"source {source_id} is disabled")
        if source["license_scope"] == BLOCKED_SCOPE:
            raise SourceNotAllowed(f"source {source_id} has no reuse right")
        if stream is not None and source["stream"] not in (stream, "both"):
            raise SourceNotAllowed(f"source {source_id} does not serve stream {stream!r}")
        return source

    def document(self) -> dict[str, Any]:
        """The full ``source_registry`` record, validated before return."""
        record = {
            "schema_version": "1.0",
            "registry_id": self.registry_id,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "sources": self.list(),
        }
        validate_payload("source_registry", record)
        return record

    def _validate_with(self, sources: list[dict[str, Any]]) -> None:
        validate_payload(
            "source_registry",
            {
                "schema_version": "1.0",
                "registry_id": self.registry_id,
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "sources": sources,
            },
        )
