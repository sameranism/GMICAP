"""P05/S02-004 raw-news repository with idempotent upsert.

Identity is the ``news_id`` derived from source and canonical URL, so re-polling
the same feed cannot create duplicates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Mapping, Sequence

from backend.core.contracts import validate_payload


@dataclass
class RawNewsRepository:
    """Fixture repository; production writes ``domestic.raw_news`` in PostgreSQL."""

    _by_id: dict[str, dict[str, Any]] = field(default_factory=dict, repr=False)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def upsert(self, record: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
        """Store a validated record; returns (record, created)."""
        validate_payload("raw_news", record)
        news_id = str(record["news_id"])
        with self._lock:
            existing = self._by_id.get(news_id)
            if existing is not None:
                return dict(existing), False
            stored = dict(record)
            self._by_id[news_id] = stored
            return dict(stored), True

    def upsert_many(self, records: Sequence[Mapping[str, Any]]) -> tuple[int, int]:
        """Returns (created, skipped) after validating every record first."""
        created = skipped = 0
        for record in records:
            _, was_created = self.upsert(record)
            if was_created:
                created += 1
            else:
                skipped += 1
        return created, skipped

    def get(self, news_id: str) -> dict[str, Any] | None:
        with self._lock:
            record = self._by_id.get(news_id)
            return dict(record) if record is not None else None

    def list(self, *, stream: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            values = [dict(record) for record in self._by_id.values()]
        values.sort(key=lambda item: str(item["collected_at"]), reverse=True)
        if stream is not None:
            values = [value for value in values if value["stream"] == stream]
        return values[:limit]

    def __len__(self) -> int:
        with self._lock:
            return len(self._by_id)
