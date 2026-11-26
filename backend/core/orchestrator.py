"""B01/P29 workflow orchestration for one news record.

The orchestrator is intentionally small and synchronous: it validates the
incoming contract, archives the reference, records workflow status, and gates
every external side effect behind the three output switches (ADR-004).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Mapping
from uuid import uuid4

from backend.core.archive import ArchiveStore, build_archive_record, object_key
from backend.core.contracts import validate_payload
from backend.core.events import EventBus, make_event
from backend.core.jobs import Job, JobQueue
from backend.core.output_switches import OutputSwitches


@dataclass(frozen=True)
class WorkflowResult:
    workflow: dict[str, Any]
    job: Job | None
    archived: bool


class Orchestrator:
    """Coordinates B01 hand-offs; never performs an external side effect itself."""

    def __init__(
        self,
        *,
        jobs: JobQueue,
        bus: EventBus,
        archive: ArchiveStore,
        switches: Callable[[], OutputSwitches],
    ) -> None:
        self._jobs = jobs
        self._bus = bus
        self._archive = archive
        self._switches = switches

    def _status(self, *, workflow_id: str, correlation_id: str, state: str, attempt: int, error: str | None) -> dict[str, Any]:
        status = {
            "schema_version": "1.0",
            "workflow_id": workflow_id,
            "correlation_id": correlation_id,
            "current_project": "P07",
            "state": state,
            "attempt_count": attempt,
            "last_error_code": error,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        validate_payload("workflow_status", status)
        return status

    def ingest_domestic(self, record: Mapping[str, Any]) -> WorkflowResult:
        """Accept one ``normalized_news`` record, archive its reference, emit an event."""
        validate_payload("normalized_news", record)
        correlation_id = str(uuid4())
        workflow_id = f"wf-{record['news_id']}"

        job = self._jobs.enqueue(
            kind="ingest",
            idempotency_key=f"ingest:{record['news_id']}:{record['fingerprint']}",
            payload_ref=object_key(str(record["news_id"]), "json"),
        )

        archive_record = build_archive_record(
            object_type="normalized_news",
            object_id=str(record["news_id"]),
            stream=str(record["stream"]),
            classification="internal",
            payload_ref=object_key(str(record["news_id"]), "json"),
            source_refs=[str(record.get("original_url", ""))],
        )
        self._archive.put(archive_record)

        event = make_event(
            event_type="news.ingested",
            producer_project="P07",
            object_id=str(record["news_id"]),
            correlation_id=correlation_id,
            payload_ref=archive_record["payload_ref"],
            classification="internal",
        )
        self._bus.publish(event)

        status = self._status(
            workflow_id=workflow_id,
            correlation_id=correlation_id,
            state="completed",
            attempt=job.attempt,
            error=None,
        )
        return WorkflowResult(workflow=status, job=job, archived=True)

    def request_publish(self, *, stream: str, job: Job | None = None) -> dict[str, Any]:
        """Gate a publishing side effect; hold the job when the switch is off."""
        switches = self._switches()
        if not switches.publishing_stream_enabled(stream):
            reason = f"publishing:{stream} disabled at revision {switches.revision}"
            if job is not None:
                self._jobs.hold(job.job_id, reason)
            return {"allowed": False, "reason": reason, "switch_revision": switches.revision}
        return {"allowed": True, "reason": "enabled", "switch_revision": switches.revision}
