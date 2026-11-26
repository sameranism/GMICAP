"""S01-021: orchestration, jobs, outbox, archive, storage and source rights."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from backend.core.archive import (
    InMemoryArchiveStore,
    InvalidArchiveKey,
    build_archive_record,
    object_key,
)
from backend.core.events import InMemoryEventBus, dedupe_key, make_event
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
    assert first.workflow["state"] == "completed"
    assert first.job is not None and first.job.state is JobState.QUEUED
    assert len(deliveries) == 1

    second = orchestrator.ingest_domestic(record)
    assert second.job is not None and first.job is not None
    assert second.job.job_id == first.job.job_id, "idempotency key must deduplicate"
    assert len(deliveries) == 1, "dedupe key must suppress the second delivery"


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
    job = queue.enqueue(kind="publish", idempotency_key="k2")
    queue.hold(job.job_id, "publishing disabled")
    with pytest.raises(InvalidTransition):
        queue.resume(job.job_id, lambda _job: False)
    resumed = queue.resume(job.job_id, lambda _job: True)
    assert resumed.state is JobState.QUEUED
    assert resumed.hold_reason is None


def test_job_attempts_increment_on_start() -> None:
    queue = JobQueue()
    job = queue.enqueue(kind="ingest", idempotency_key="k3")
    assert queue.start(job.job_id).attempt == 1


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
