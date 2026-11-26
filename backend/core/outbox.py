"""B01/P29 transactional outbox.

The outbox is the only bridge between a database change and an event publish:
append the envelope in the same unit of work, then dispatch it. Dispatch is
idempotent, so a crash between append and publish re-delivers exactly once.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Callable, Mapping
from uuid import uuid4

from backend.core.events import dedupe_key, validate_shared_event


@dataclass
class OutboxEntry:
    entry_id: str
    event: dict[str, Any]
    created_at: str
    dispatched_at: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "event": dict(self.event),
            "created_at": self.created_at,
            "dispatched_at": self.dispatched_at,
        }


class Outbox:
    """Fixture outbox; production uses a table in the owning database."""

    def __init__(self) -> None:
        self._entries: dict[str, OutboxEntry] = {}
        self._lock = Lock()

    def append(self, event: Mapping[str, Any]) -> OutboxEntry:
        envelope = validate_shared_event(event)
        entry = OutboxEntry(
            entry_id=str(uuid4()),
            event=envelope,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        with self._lock:
            self._entries[entry.entry_id] = entry
        return entry

    def pending(self) -> list[OutboxEntry]:
        with self._lock:
            return [entry for entry in self._entries.values() if entry.dispatched_at is None]

    def dispatch(self, publish: Callable[[Mapping[str, Any]], None]) -> int:
        """Publish pending entries; returns how many were dispatched this call."""
        sent = 0
        for entry in self.pending():
            # Revalidate a snapshot: pending entries may have changed since append.
            envelope = validate_shared_event(entry.event)
            publish(envelope)
            with self._lock:
                if entry.dispatched_at is None:
                    entry.dispatched_at = datetime.now(timezone.utc).isoformat()
                    sent += 1
        return sent

    def keys(self) -> set[str]:
        with self._lock:
            return {dedupe_key(entry.event) for entry in self._entries.values()}

    def __len__(self) -> int:
        with self._lock:
            return len(self._entries)
