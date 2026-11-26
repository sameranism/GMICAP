"""B01/P29 job lifecycle with idempotency and the ``held`` state.

A job that is held because an output is off is never dispatched automatically
when the output comes back: it must be revalidated first (ADR-004).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from threading import Lock
from typing import Any, Callable, Mapping
from uuid import uuid4


class JobState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    HELD = "held"
    DONE = "done"
    FAILED = "failed"


class InvalidTransition(RuntimeError):
    """The requested state change is not allowed for the current state."""


_ALLOWED = {
    JobState.QUEUED: {JobState.RUNNING, JobState.HELD, JobState.FAILED},
    JobState.HELD: {JobState.QUEUED, JobState.FAILED},
    JobState.RUNNING: {JobState.DONE, JobState.FAILED, JobState.HELD},
    JobState.DONE: set(),
    JobState.FAILED: {JobState.QUEUED},
}


@dataclass
class Job:
    job_id: str
    kind: str
    idempotency_key: str
    state: JobState = JobState.QUEUED
    attempt: int = 0
    last_error: str | None = None
    hold_reason: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    payload_ref: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "kind": self.kind,
            "idempotency_key": self.idempotency_key,
            "state": self.state.value,
            "attempt": self.attempt,
            "last_error": self.last_error,
            "hold_reason": self.hold_reason,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "payload_ref": self.payload_ref,
        }


class JobQueue:
    """In-memory fixture queue; the production queue is Redis (ADR-003)."""

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._by_key: dict[str, str] = {}
        self._lock = Lock()

    def enqueue(self, *, kind: str, idempotency_key: str, payload_ref: str = "") -> Job:
        with self._lock:
            existing = self._by_key.get(idempotency_key)
            if existing is not None:
                return self._jobs[existing]
            job = Job(
                job_id=str(uuid4()),
                kind=kind,
                idempotency_key=idempotency_key,
                payload_ref=payload_ref,
            )
            self._jobs[job.job_id] = job
            self._by_key[idempotency_key] = job.job_id
            return job

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)

    def _transition(self, job: Job, target: JobState) -> Job:
        if target not in _ALLOWED[job.state]:
            raise InvalidTransition(f"{job.state.value} -> {target.value} is not allowed")
        job.state = target
        job.updated_at = datetime.now(timezone.utc).isoformat()
        return job

    def start(self, job_id: str) -> Job:
        with self._lock:
            job = self._require(job_id)
            self._transition(job, JobState.RUNNING)
            job.attempt += 1
            return job

    def complete(self, job_id: str) -> Job:
        with self._lock:
            return self._transition(self._require(job_id), JobState.DONE)

    def fail(self, job_id: str, error: str) -> Job:
        with self._lock:
            job = self._transition(self._require(job_id), JobState.FAILED)
            job.last_error = error[:200]
            return job

    def hold(self, job_id: str, reason: str) -> Job:
        with self._lock:
            job = self._transition(self._require(job_id), JobState.HELD)
            job.hold_reason = reason[:200]
            return job

    def resume(self, job_id: str, revalidate: Callable[[Job], bool]) -> Job:
        """Resume a held job only if the caller's revalidation returns True."""
        with self._lock:
            job = self._require(job_id)
            if job.state is not JobState.HELD:
                raise InvalidTransition("only a held job can be resumed")
            if not revalidate(job):
                raise InvalidTransition("revalidation refused the resume")
            job.hold_reason = None
            return self._transition(job, JobState.QUEUED)

    def _require(self, job_id: str) -> Job:
        job = self._jobs.get(job_id)
        if job is None:
            raise KeyError(f"unknown job: {job_id}")
        return job

    def counts(self) -> Mapping[str, int]:
        with self._lock:
            counts: dict[str, int] = {}
            for job in self._jobs.values():
                counts[job.state.value] = counts.get(job.state.value, 0) + 1
            return counts
