"""S01-021: orchestration, jobs, outbox, archive, storage and source rights."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from backend.core.archive import (
    InMemoryArchiveStore,
    InvalidArchiveKey,
    build_archive_record,
    object_key,
)
from backend.core.contracts import ContractError, validate_payload
from backend.core.events import (
    ExecutivePrivateEventRoutingError,
    InMemoryEventBus,
    RestrictedEventRoutingError,
    UnknownClassification,
    dedupe_key,
    make_event,
)
from backend.core.health import health_report
from backend.core.jobs import InvalidTransition, JobQueue, JobState
from backend.core.object_store import InvalidObjectKey, LocalObjectStore
from backend.core.orchestrator import Orchestrator
from backend.core.outbox import Outbox
from backend.core.output_switches import OutputDisabled, OutputSwitches, default_off_switches
from backend.core.sources_service import SourceNotAllowed, SourceNotFound, SourceService


def _normalized(example_dir: Path) -> dict:
    return json.loads((example_dir / "normalized_news.example.json").read_text(encoding="utf-8"))


def _switches(example_dir: Path, *, publishing: bool) -> OutputSwitches:
    record = json.loads((example_dir / "output_controls.example.json").read_text(encoding="utf-8"))
    record["revision"] = 2
    record["updated_by"] = "user-001"
    record["publishing"]["enabled"] = publishing
    record["publishing"]["domestic_enabled"] = publishing
    record["publishing"]["foreign_enabled"] = publishing
    record["publishing"]["public_reports_enabled"] = publishing
    return OutputSwitches.from_record(record)


def _orchestrator(example_dir: Path, switches):
    return Orchestrator(
        jobs=JobQueue(),
        bus=InMemoryEventBus(),
        archive=InMemoryArchiveStore(),
        switches=lambda: switches,
    )


# --- output switches -----------------------------------------------------------


def test_default_switches_are_all_off(example_dir: Path) -> None:
    switches = default_off_switches()
    assert not switches.enabled("public_analysis")
    assert not switches.enabled("studio")
    assert not switches.enabled("publishing")
    assert not switches.publishing_stream_enabled("domestic")
    with pytest.raises(OutputDisabled):
        switches.require("publishing")


def test_switches_are_independent(example_dir: Path) -> None:
    record = json.loads((example_dir / "output_controls.example.json").read_text(encoding="utf-8"))
    record["public_analysis"]["enabled"] = True
    switches = OutputSwitches.from_record(record)
    assert switches.enabled("public_analysis")
    assert not switches.enabled("studio")
    assert switches.studio_channel_enabled("audio") is False


# --- orchestration -------------------------------------------------------------


def test_ingest_archives_and_emits_once(example_dir: Path) -> None:
    record = _normalized(example_dir)
    orchestrator = _orchestrator(example_dir, default_off_switches())
    deliveries: list[dict] = []
    orchestrator._bus.subscribe("news.ingested", deliveries.append)  # noqa: SLF001 - test wiring

    first = orchestrator.ingest_domestic(record)
    assert first.archived is True
    assert first.workflow["state"] == "new"
    assert first.job is not None and first.job.state is JobState.QUEUED
    assert len(deliveries) == 1

    second = orchestrator.ingest_domestic(record)
    assert second.job is not None and first.job is not None
    assert second.job.job_id == first.job.job_id, "idempotency key must deduplicate"
    assert len(deliveries) == 1, "dedupe key must suppress the second delivery"
    assert second.workflow == first.workflow
    assert deliveries[0]["correlation_id"] == first.workflow["correlation_id"]
    assert len(orchestrator._archive) == 1


def test_publish_is_held_while_the_switch_is_off(example_dir: Path) -> None:
    orchestrator = _orchestrator(example_dir, default_off_switches())
    job = orchestrator._jobs.enqueue(kind="publish", idempotency_key="publish:a-1")  # noqa: SLF001
    decision = orchestrator.request_publish(stream="domestic", job=job)
    assert decision["allowed"] is False
    assert orchestrator._jobs.get(job.job_id).state is JobState.HELD  # noqa: SLF001


def test_publish_is_allowed_when_the_switch_is_on(example_dir: Path) -> None:
    orchestrator = _orchestrator(example_dir, _switches(example_dir, publishing=True))
    decision = orchestrator.request_publish(stream="domestic")
    assert decision["allowed"] is True


# --- event envelope and restricted routing (ADR-013) ----------------------------


def _event(classification: str = "internal") -> dict:
    return make_event(
        event_type="news.ingested",
        producer_project="P07",
        object_id="n-1",
        correlation_id="corr-1",
        payload_ref="archive/n-1.json",
        classification=classification,
    )


@pytest.mark.parametrize("classification", ["public", "internal", "restricted", "executive_private"])
def test_event_constructor_matches_frozen_classification_enum(classification: str) -> None:
    event = _event(classification)
    assert event["classification"] == classification
    assert event["schema_version"] == "1.0"
    assert event["payload_ref"] == "archive/n-1.json"
    validate_payload("event_envelope", event)


def test_event_constructor_rejects_unknown_classification() -> None:
    with pytest.raises(UnknownClassification):
        _event("unknown")


def test_restricted_event_cannot_consume_shared_bus_idempotency_key() -> None:
    bus = InMemoryEventBus()
    delivered: list[dict] = []
    bus.subscribe("news.ingested", delivered.append)
    event = _event()
    # Simulate a valid envelope received directly, not via the constructor.
    restricted = dict(event, classification="restricted")
    validate_payload("event_envelope", restricted)
    with pytest.raises(RestrictedEventRoutingError) as rejected:
        bus.publish(restricted)
    assert restricted["payload_ref"] not in str(rejected.value)
    assert delivered == []
    assert bus.deliveries() == set()
    bus.publish(event)
    bus.publish(event)
    assert delivered == [event]
    assert bus.deliveries() == {dedupe_key(event)}


def test_restricted_event_cannot_enter_generic_outbox() -> None:
    outbox = Outbox()
    restricted = dict(_event(), classification="restricted")
    validate_payload("event_envelope", restricted)
    with pytest.raises(RestrictedEventRoutingError) as rejected:
        outbox.append(restricted)
    assert restricted["payload_ref"] not in str(rejected.value)
    assert len(outbox) == 0
    assert outbox.pending() == []
    assert outbox.keys() == set()


def test_outbox_rechecks_classification_before_dispatch() -> None:
    outbox = Outbox()
    entry = outbox.append(_event())
    entry.event["classification"] = "restricted"
    delivered: list = []
    with pytest.raises(RestrictedEventRoutingError):
        outbox.dispatch(delivered.append)
    assert delivered == []
    assert entry.dispatched_at is None
    assert outbox.pending() == [entry]


@pytest.mark.parametrize("raw", [False, True])
def test_private_event_cannot_consume_shared_bus_idempotency_key(raw: bool) -> None:
    bus = InMemoryEventBus()
    delivered: list[dict] = []
    bus.subscribe("news.ingested", delivered.append)
    ordinary = _event()
    private = (
        dict(ordinary, classification="executive_private")
        if raw
        else _event("executive_private")
    )
    validate_payload("event_envelope", private)
    with pytest.raises(ExecutivePrivateEventRoutingError) as rejected:
        bus.publish(private)
    assert private["payload_ref"] not in str(rejected.value)
    assert private["object_id"] not in str(rejected.value)
    assert delivered == []
    assert bus.deliveries() == set()
    bus.publish(ordinary)
    bus.publish(ordinary)
    assert delivered == [ordinary]
    assert bus.deliveries() == {dedupe_key(ordinary)}


@pytest.mark.parametrize("raw", [False, True])
def test_private_event_cannot_enter_generic_outbox(raw: bool) -> None:
    outbox = Outbox()
    private = (
        dict(_event(), classification="executive_private")
        if raw
        else _event("executive_private")
    )
    validate_payload("event_envelope", private)
    with pytest.raises(ExecutivePrivateEventRoutingError) as rejected:
        outbox.append(private)
    assert private["payload_ref"] not in str(rejected.value)
    assert len(outbox) == 0
    assert outbox.pending() == []
    assert outbox.keys() == set()


def test_outbox_rechecks_private_classification_before_dispatch() -> None:
    outbox = Outbox()
    entry = outbox.append(_event())
    entry.event["classification"] = "executive_private"
    delivered: list = []
    with pytest.raises(ExecutivePrivateEventRoutingError) as rejected:
        outbox.dispatch(delivered.append)
    assert entry.event["payload_ref"] not in str(rejected.value)
    assert delivered == []
    assert entry.dispatched_at is None
    assert outbox.pending() == [entry]


@pytest.mark.parametrize("classification", ["public", "internal"])
def test_ordinary_events_keep_shared_delivery_and_deduplication(classification: str) -> None:
    event = _event(classification)
    bus = InMemoryEventBus()
    delivered: list[dict] = []
    bus.subscribe("news.ingested", delivered.append)
    outbox = Outbox()
    outbox.append(event)
    assert outbox.dispatch(bus.publish) == 1
    assert outbox.dispatch(bus.publish) == 0
    bus.publish(event)
    assert delivered == [event]


def test_shared_routes_reject_unknown_wire_version_without_side_effects() -> None:
    event = dict(_event(), schema_version="2.0")
    bus = InMemoryEventBus()
    delivered: list[dict] = []
    bus.subscribe("news.ingested", delivered.append)
    outbox = Outbox()
    with pytest.raises(ContractError):
        bus.publish(event)
    with pytest.raises(ContractError):
        outbox.append(event)
    assert delivered == []
    assert bus.deliveries() == set()
    assert len(outbox) == 0


# --- jobs ----------------------------------------------------------------------


def test_job_lifecycle_and_transitions() -> None:
    queue = JobQueue()
    job = queue.enqueue(kind="ingest", idempotency_key="k1")
    queue.start(job.job_id)
    queue.complete(job.job_id)
    assert queue.get(job.job_id).state is JobState.DONE
    with pytest.raises(InvalidTransition):
        queue.start(job.job_id)


def test_held_job_requires_revalidation() -> None:
    queue = JobQueue()
    job = queue.enqueue(kind="ingest", idempotency_key="k2")
    queue.hold(job.job_id, "fixture validation required")
    with pytest.raises(InvalidTransition):
        queue.resume(job.job_id, lambda _job: False)
    resumed = queue.resume(job.job_id, lambda _job: True)
    assert resumed.state is JobState.QUEUED
    assert resumed.hold_reason is None


def test_job_attempts_increment_on_start() -> None:
    queue = JobQueue()
    job = queue.enqueue(kind="ingest", idempotency_key="k3")
    assert queue.start(job.job_id).attempt == 1


def test_workflow_tracks_job_lifecycle_and_replay(example_dir: Path) -> None:
    record = _normalized(example_dir)
    orchestrator = _orchestrator(example_dir, default_off_switches())
    first = orchestrator.ingest_domestic(record)
    job = first.job
    assert job is not None
    with pytest.raises(InvalidTransition):
        orchestrator._jobs.complete(job.job_id)
    orchestrator._jobs.start(job.job_id)
    running = orchestrator.ingest_domestic(record)
    assert running.workflow["state"] == "running"
    assert running.workflow["attempt_count"] == 1
    orchestrator._jobs.complete(job.job_id)
    done = orchestrator.ingest_domestic(record)
    assert done.workflow["state"] == "completed"
    assert done.workflow["workflow_id"] == first.workflow["workflow_id"]
    assert done.workflow["correlation_id"] == first.workflow["correlation_id"]
    validate_payload("workflow_status", done.workflow)
    with pytest.raises(InvalidTransition):
        orchestrator._jobs.cancel(job.job_id)


def test_distinct_fingerprint_creates_distinct_workflow_and_event(example_dir: Path) -> None:
    orchestrator = _orchestrator(example_dir, default_off_switches())
    delivered: list[dict] = []
    orchestrator._bus.subscribe("news.ingested", delivered.append)
    record = _normalized(example_dir)
    first = orchestrator.ingest_domestic(record)
    second = orchestrator.ingest_domestic(dict(record, fingerprint="sha256:changed"))
    assert first.workflow["workflow_id"] != second.workflow["workflow_id"]
    assert first.workflow["correlation_id"] != second.workflow["correlation_id"]
    assert len(delivered) == 2
    assert dedupe_key(delivered[0]) != dedupe_key(delivered[1])


def test_retry_limit_and_controlled_failure_code() -> None:
    queue = JobQueue()
    job = queue.enqueue(kind="ingest", idempotency_key="bounded", max_attempts=2)
    for attempt in (1, 2):
        assert queue.start(job.job_id).attempt == attempt
        failed = queue.fail(job.job_id, "sensitive fixture exception")
        assert failed.last_error == "job_failed"
        if attempt == 1:
            assert queue.retry(job.job_id).attempt == attempt
    with pytest.raises(InvalidTransition, match="attempt limit"):
        queue.retry(job.job_id)
    assert queue.get(job.job_id) == failed


@pytest.mark.parametrize("operation", ["start", "retry", "resume"])
def test_expired_job_cannot_execute(operation: str) -> None:
    now = datetime(2026, 11, 26, tzinfo=timezone.utc)
    queue = JobQueue(clock=lambda: now)
    job = queue.enqueue(kind="ingest", idempotency_key="expiry", deadline_at=now + timedelta(seconds=1))
    if operation == "retry":
        queue.start(job.job_id)
        queue.fail(job.job_id, "fixture")
    elif operation == "resume":
        queue.hold(job.job_id, "fixture")
    before = queue.get(job.job_id)
    now += timedelta(seconds=1)
    with pytest.raises(InvalidTransition, match="deadline"):
        if operation == "resume":
            queue.resume(job.job_id, lambda _job: True)
        elif operation == "retry":
            queue.retry(job.job_id)
        else:
            queue.start(job.job_id)
    assert queue.get(job.job_id) == before


def test_invalid_job_bounds_and_immutable_snapshot() -> None:
    queue = JobQueue()
    with pytest.raises(ValueError):
        queue.enqueue(kind="ingest", idempotency_key="bad", max_attempts=0)
    with pytest.raises(ValueError):
        queue.enqueue(kind="ingest", idempotency_key="bad", deadline_at=datetime(2026, 11, 26))
    job = queue.enqueue(kind="ingest", idempotency_key="valid")
    with pytest.raises(FrozenInstanceError):
        setattr(job, "state", JobState.DONE)
    assert queue.get(job.job_id) == job
    assert queue.enqueue(kind="ingest", idempotency_key="valid") == job


@pytest.mark.parametrize("state", ["queued", "held", "failed"])
def test_cancel_is_terminal(state: str) -> None:
    queue = JobQueue()
    job = queue.enqueue(kind="ingest", idempotency_key="cancel")
    if state == "held":
        queue.hold(job.job_id, "fixture")
    elif state == "failed":
        queue.fail(job.job_id, "fixture")
    cancelled = queue.cancel(job.job_id)
    assert cancelled.state is JobState.CANCELLED
    for operation in (queue.start, queue.retry, queue.cancel, queue.complete):
        with pytest.raises(InvalidTransition):
            operation(job.job_id)
    assert queue.get(job.job_id) == cancelled


def test_running_job_cannot_be_cancelled() -> None:
    queue = JobQueue()
    job = queue.enqueue(kind="ingest", idempotency_key="running")
    queue.start(job.job_id)
    with pytest.raises(InvalidTransition):
        queue.cancel(job.job_id)


def test_held_revalidation_rejects_exception_and_stale_result() -> None:
    queue = JobQueue()
    job = queue.enqueue(kind="ingest", idempotency_key="held")
    held = queue.hold(job.job_id, "fixture")

    def unavailable(_job):
        raise RuntimeError("fixture validation unavailable")

    with pytest.raises(RuntimeError):
        queue.resume(job.job_id, unavailable)
    assert queue.get(job.job_id) == held

    def changed(_job):
        queue.cancel(job.job_id)
        return True

    with pytest.raises(InvalidTransition, match="changed"):
        queue.resume(job.job_id, changed)
    assert queue.get(job.job_id).state is JobState.CANCELLED


def test_resume_rechecks_deadline_after_validation() -> None:
    now = datetime(2026, 11, 26, tzinfo=timezone.utc)
    queue = JobQueue(clock=lambda: now)
    job = queue.enqueue(kind="ingest", idempotency_key="late", deadline_at=now + timedelta(seconds=1))
    held = queue.hold(job.job_id, "fixture")

    def late(_job):
        nonlocal now
        now += timedelta(seconds=1)
        return True

    with pytest.raises(InvalidTransition, match="deadline"):
        queue.resume(job.job_id, late)
    assert queue.get(job.job_id) == held


def test_publishing_cannot_start_retry_or_resume_on_generic_queue(example_dir: Path) -> None:
    orchestrator = _orchestrator(example_dir, _switches(example_dir, publishing=True))
    queue = orchestrator._jobs
    job = queue.enqueue(kind="publish", idempotency_key="publish:held")
    with pytest.raises(InvalidTransition, match="authorized"):
        queue.start(job.job_id)
    queue.hold(job.job_id, "fixture")
    assert orchestrator.request_publish(stream="domestic")["allowed"] is True
    with pytest.raises(InvalidTransition, match="authorized"):
        queue.resume(job.job_id, lambda _job: True)
    assert queue.get(job.job_id).state is JobState.HELD
    queue.fail(job.job_id, "fixture")
    with pytest.raises(InvalidTransition, match="authorized"):
        queue.retry(job.job_id)


# --- outbox --------------------------------------------------------------------


def test_outbox_dispatches_pending_once() -> None:
    outbox = Outbox()
    event = make_event(
        event_type="news.ingested",
        producer_project="P07",
        object_id="n-1",
        correlation_id="corr-1",
        payload_ref="archive/n-1.json",
    )
    outbox.append(event)
    delivered: list = []
    assert outbox.dispatch(delivered.append) == 1
    assert outbox.dispatch(delivered.append) == 0
    assert len(delivered) == 1
    assert dedupe_key(event) in outbox.keys()


# --- archive and storage -------------------------------------------------------


def test_archive_key_rejects_traversal() -> None:
    assert object_key("n-1") == "archive/n-1.json"
    with pytest.raises(InvalidArchiveKey):
        object_key("../escape")


def test_archive_record_validates_and_roundtrips() -> None:
    store = InMemoryArchiveStore()
    record = build_archive_record(
        object_type="normalized_news",
        object_id="n-1",
        stream="domestic",
        classification="internal",
        payload_ref="archive/n-1.json",
    )
    store.put(record)
    assert store.get(record["archive_id"]) == record


def test_local_object_store_roundtrip_and_escaping(tmp_path: Path) -> None:
    store = LocalObjectStore(tmp_path / "objects")
    key = store.put("archive/n-1.json", b'{"a":1}')
    assert store.exists(key)
    assert store.get(key) == b'{"a":1}'
    with pytest.raises(InvalidObjectKey):
        store.put("../escape.json", b"x")
    with pytest.raises(InvalidObjectKey):
        store.get("/etc/passwd")


# --- sources -------------------------------------------------------------------


def _source(source_id: str = "SRC-IR-01", **overrides):
    base = {
        "source_id": source_id,
        "site_url": "https://example.com",
        "feed_url": "https://example.com/rss",
        "api_base_url": None,
        "country": "IR",
        "language": "fa",
        "stream": "domestic",
        "auth_ref": None,
        "license_scope": "summary",
        "enabled": True,
    }
    base.update(overrides)
    return base


def test_source_registry_document_is_valid() -> None:
    service = SourceService()
    service.register(_source())
    document = service.document()
    assert document["sources"][0]["source_id"] == "SRC-IR-01"


def test_disabled_or_blocked_source_is_not_usable() -> None:
    service = SourceService()
    service.register(_source())
    service.set_enabled("SRC-IR-01", False)
    with pytest.raises(SourceNotAllowed):
        service.require_usable("SRC-IR-01")

    service.register(_source("SRC-IR-02", license_scope="unknown"))
    with pytest.raises(SourceNotAllowed):
        service.require_usable("SRC-IR-02")

    with pytest.raises(SourceNotFound):
        service.require_usable("SRC-XX-99")


def test_source_stream_must_match() -> None:
    service = SourceService()
    service.register(_source())
    with pytest.raises(SourceNotAllowed):
        service.require_usable("SRC-IR-01", stream="foreign")


# --- health --------------------------------------------------------------------


def test_health_report_is_ok_without_dependencies() -> None:
    report = health_report()
    assert report["status"] == "ok"
    assert report["degraded"] == []


def test_health_report_marks_failing_probe_degraded() -> None:
    def boom() -> bool:
        raise RuntimeError("probe failed")

    report = health_report(probes={"redis": boom})
    assert report["status"] == "degraded"
    assert report["checks"]["redis"]["state"] == "unavailable"
