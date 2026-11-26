"""P05/S02-003..007 polling state, backoff and failure accounting.

The scheduler never retries in a tight loop: consecutive failures double the
interval up to one hour, and a successful poll resets it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Mapping

BASE_INTERVAL_SECONDS = 300
MAX_INTERVAL_SECONDS = 3600


def _now() -> datetime:
    return datetime.now(timezone.utc)


def next_interval_seconds(consecutive_failures: int) -> int:
    """Exponential backoff, capped; zero failures means the base interval."""
    if consecutive_failures <= 0:
        return BASE_INTERVAL_SECONDS
    return min(BASE_INTERVAL_SECONDS * (2 ** min(consecutive_failures, 5)), MAX_INTERVAL_SECONDS)


@dataclass
class PollState:
    source_id: str
    etag: str | None = None
    last_modified: str | None = None
    last_success_at: str | None = None
    last_error: str | None = None
    consecutive_failures: int = 0
    next_poll_at: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "etag": self.etag,
            "last_modified": self.last_modified,
            "last_success_at": self.last_success_at,
            "last_error": self.last_error,
            "consecutive_failures": self.consecutive_failures,
            "next_poll_at": self.next_poll_at,
        }


class PollStateStore:
    """Fixture store; production keeps ``domestic.poll_state`` in PostgreSQL."""

    def __init__(self) -> None:
        self._states: dict[str, PollState] = {}
        self._lock = Lock()

    def get_or_create(self, source_id: str) -> PollState:
        with self._lock:
            state = self._states.get(source_id)
            if state is None:
                # A new source is immediately eligible; the first completed poll
                # establishes its next scheduled time.
                state = PollState(source_id=source_id)
                self._states[source_id] = state
            return state

    def save(self, state: PollState) -> PollState:
        with self._lock:
            self._states[state.source_id] = state
            return state

    def all(self) -> list[dict[str, object]]:
        with self._lock:
            return [state.as_dict() for state in self._states.values()]


def should_poll(state: PollState, now: datetime | None = None) -> bool:
    """True when the next poll time has arrived (never raises on bad timestamps)."""
    if not state.next_poll_at:
        return True
    try:
        due = datetime.fromisoformat(state.next_poll_at)
    except ValueError:
        return True
    current = now or _now()
    if due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)
    return current >= due


def record_success(
    state: PollState,
    *,
    etag: str | None,
    last_modified: str | None,
    now: datetime | None = None,
) -> PollState:
    moment = now or _now()
    state.etag = etag or state.etag
    state.last_modified = last_modified or state.last_modified
    state.last_success_at = moment.isoformat()
    state.last_error = None
    state.consecutive_failures = 0
    state.next_poll_at = (moment + timedelta(seconds=BASE_INTERVAL_SECONDS)).isoformat()
    return state


def record_failure(
    state: PollState,
    *,
    error: str,
    now: datetime | None = None,
) -> PollState:
    moment = now or _now()
    state.last_error = error[:200]
    state.consecutive_failures += 1
    interval = next_interval_seconds(state.consecutive_failures)
    state.next_poll_at = (moment + timedelta(seconds=interval)).isoformat()
    return state


@dataclass
class PollResult:
    source_id: str
    status: str
    collected: int = 0
    error: str | None = None
    state: Mapping[str, object] = field(default_factory=dict)
