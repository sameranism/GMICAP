"""B01/P01 application wiring: one Services object, injected via app.state.

News repositories support explicitly selected PostgreSQL storage. Other stores
retain their existing fixture wiring; selecting PostgreSQL never implies that
unrelated production prerequisites have passed.
"""

from __future__ import annotations

import logging
import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Mapping

from fastapi import Request
from sqlalchemy.engine import make_url

from backend.app.pipeline import IngestPipeline
from backend.core.archive import InMemoryArchiveStore
from backend.core.audit import Auditor, InMemoryAuditSink
from backend.core.db import DatabaseRegistry
from backend.core.events import InMemoryEventBus
from backend.core.jobs import JobQueue
from backend.core.object_store import LocalObjectStore
from backend.core.orchestrator import Orchestrator
from backend.core.outbox import Outbox
from backend.core.output_switches import OutputSwitches, default_off_switches
from backend.core.permissions import InMemoryGrantStore
from backend.core.settings_service import InMemoryRevisionStore, SettingsService
from backend.core.sources_service import SourceService
from backend.modules.domestic.feed_client import (
    FeedTransport,
    FixtureFeedTransport,
    HttpxFeedTransport,
)
from backend.modules.domestic.repository import PostgresRawNewsRepository, RawNewsRepository
from backend.modules.domestic.scheduler import PollStateStore
from backend.modules.processing.repository import PostgresProcessingRepository, ProcessingRepository

_LOG = logging.getLogger(__name__)


@dataclass
class Services:
    registry: DatabaseRegistry
    session_key: bytes
    grants: InMemoryGrantStore
    audit_sink: InMemoryAuditSink
    auditor: Auditor
    settings: SettingsService
    sources: SourceService
    jobs: JobQueue
    bus: InMemoryEventBus
    outbox: Outbox
    archive: InMemoryArchiveStore
    objects: LocalObjectStore
    switches: Callable[[], OutputSwitches]
    pipeline: IngestPipeline
    transport: FeedTransport
    orchestrator: Orchestrator = field(init=False)

    def __post_init__(self) -> None:
        self.orchestrator = Orchestrator(
            jobs=self.jobs,
            bus=self.bus,
            archive=self.archive,
            switches=self.switches,
        )


def build_services(environ: Mapping[str, str] | None = None) -> Services:
    environ = os.environ if environ is None else environ
    registry = DatabaseRegistry(environ=environ)
    storage = environ.get("ETEMAD_NEWS_STORAGE", "fixture")
    if storage not in {"fixture", "postgres"}:
        raise ValueError("invalid ETEMAD_NEWS_STORAGE")
    raw_repository: RawNewsRepository | PostgresRawNewsRepository
    processing_repository: ProcessingRepository | PostgresProcessingRepository
    if storage == "postgres":
        try:
            domestic_url = make_url(registry.url_for("domestic"))
            central_url = make_url(registry.url_for("central"))
        except (ValueError, RuntimeError):
            raise ValueError("separate domestic and central PostgreSQL URLs are required") from None
        urls = (domestic_url, central_url)
        if any(url.get_backend_name() != "postgresql" or not url.database for url in urls):
            raise ValueError("both news database roles require PostgreSQL database names")
        endpoints = {(url.host, url.port or 5432, url.database) for url in urls}
        if len(endpoints) != 2:
            raise ValueError("domestic and central databases must be separate")
        raw_repository = PostgresRawNewsRepository(registry)
        processing_repository = PostgresProcessingRepository(registry)
    else:
        raw_repository = RawNewsRepository()
        processing_repository = ProcessingRepository()

    session_key = environ.get("ETEMAD_SESSION_KEY", "").strip().encode("utf-8")
    if storage == "postgres" and not session_key:
        raise ValueError("ETEMAD_SESSION_KEY must be configured for persistent news storage")
    if not session_key:
        # Ephemeral per-process key: development only. Production must set the
        # variable; tokens do not survive a restart without it.
        session_key = secrets.token_bytes(32)
        _LOG.warning("ETEMAD_SESSION_KEY is not set; using an ephemeral session key")

    grant_store = InMemoryGrantStore()
    revision_store = InMemoryRevisionStore()
    audit_sink = InMemoryAuditSink()
    settings = SettingsService(revision_store, grant_store, credential_ref_check=lambda ref: bool(ref))
    sources = SourceService()
    jobs = JobQueue()
    bus = InMemoryEventBus()
    outbox = Outbox()
    archive = InMemoryArchiveStore()
    objects = LocalObjectStore(Path(environ.get("ETEMAD_OBJECT_ROOT", "backend/.local-objects")))

    def switches() -> OutputSwitches:
        stored = settings.get_latest("output_controls", "controls-main", "global")
        if stored is None:
            return default_off_switches()
        try:
            return OutputSwitches.from_record(stored.value)
        except Exception:  # noqa: BLE001 - a broken config must not enable outputs
            _LOG.error("stored output_controls is invalid; falling back to all-off")
            return default_off_switches()

    # Feed transport: fixture unless the operator explicitly asks for live polling.
    transport: FeedTransport
    if environ.get("ETEMAD_FEED_MODE", "fixture") == "live":
        transport = HttpxFeedTransport()
    else:
        transport = FixtureFeedTransport(responses={})

    pipeline = IngestPipeline(
        sources=sources,
        repository=raw_repository,
        processed=processing_repository,
        poll_states=PollStateStore(),
        transport=transport,
    )

    return Services(
        registry=registry,
        session_key=session_key,
        grants=grant_store,
        audit_sink=audit_sink,
        auditor=Auditor(audit_sink),
        settings=settings,
        sources=sources,
        jobs=jobs,
        bus=bus,
        outbox=outbox,
        archive=archive,
        objects=objects,
        switches=switches,
        pipeline=pipeline,
        transport=transport,
    )


def get_services(request: Request) -> Services:
    services = getattr(request.app.state, "services", None)
    if services is None:  # pragma: no cover - composition error, not a request path
        raise RuntimeError("application services are not initialised")
    return services
