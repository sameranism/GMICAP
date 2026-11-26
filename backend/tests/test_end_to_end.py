"""S09-012 domestic ingestion-to-newsroom slice, on disposable loopback PostgreSQL."""

from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg import sql
from sqlalchemy.engine import make_url

from backend.app.dependencies import build_services
from backend.app.main import create_app
from backend.core.auth import Principal, issue_session
from backend.core.permissions import Grant
from backend.modules.domestic.feed_client import FeedResponse, FixtureFeedTransport

ADMIN_URL = os.environ.get("ETEMAD_TEST_PG_ADMIN_URL")
BACKEND = Path(__file__).resolve().parents[1]
SOURCE_ID = "SRC-DB-TEST"
FEED_URL = "https://example.invalid/rss"
RSS = b"""<rss version="2.0"><channel><title>fixture</title>
<item><title>One source record</title><link>https://example.invalid/news/1</link>
<description>Synthetic test content</description></item></channel></rss>"""


@pytest.mark.skipif(not ADMIN_URL, reason="ETEMAD_TEST_PG_ADMIN_URL is unset")
def test_postgres_news_api_persists_across_app_restart(monkeypatch, tmp_path):
    from alembic import command
    from alembic.config import Config

    assert ADMIN_URL is not None
    admin = make_url(ADMIN_URL)
    assert admin.host == "127.0.0.1" and admin.database == "postgres"
    assert admin.username == "fixture_admin" and not admin.query
    suffix = uuid4().hex[:12]
    names = {role: f"etemad_test_{role}_{suffix}" for role in ("central", "domestic")}
    environ = {
        "ETEMAD_SESSION_KEY": "test-only-session-key",
        "ETEMAD_NEWS_STORAGE": "postgres",
        "ETEMAD_FEED_MODE": "fixture",
        "ETEMAD_OBJECT_ROOT": str(tmp_path / "objects"),
    }
    monkeypatch.chdir(BACKEND)
    created = []
    services = []
    with psycopg.connect(ADMIN_URL, autocommit=True) as control:
        try:
            for role, name in names.items():
                control.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name)))
                created.append(name)
                url = admin.set(drivername="postgresql+psycopg", database=name)
                key = f"ETEMAD_DB_{role.upper()}_URL"
                environ[key] = url.render_as_string(hide_password=False)
                monkeypatch.setenv(key, environ[key])
            command.upgrade(Config("alembic.ini"), "head")
            command.upgrade(Config("alembic_domestic.ini"), "head")

            first = build_services(environ=environ)
            services.append(first)
            first.sources.register({
                "source_id": SOURCE_ID, "site_url": "https://example.invalid",
                "feed_url": FEED_URL, "api_base_url": None, "country": "IR",
                "language": "en", "stream": "domestic", "auth_ref": None,
                "license_scope": "summary", "enabled": True,
            })
            assert isinstance(first.transport, FixtureFeedTransport)
            first.transport.responses = {
                FEED_URL: FeedResponse(url=FEED_URL, status_code=200, body=RSS)
            }
            first.grants.grant(Grant("eic-test", "editor_in_chief", "source_registry", SOURCE_ID, "poll"))
            first.grants.grant(Grant("eic-test", "editor_in_chief", "newsroom", "feed", "read"))
            token = issue_session(Principal("eic-test", "editor_in_chief"), first.session_key)
            headers = {"Authorization": f"Bearer {token}", "X-Correlation-ID": "CORR-PG-TEST"}
            unauthorized = issue_session(Principal("staff-test", "staff"), first.session_key)
            with TestClient(create_app(services=first)) as client:
                assert client.get("/v1/news").status_code == 401
                assert client.get("/v1/news", headers={
                    "Authorization": f"Bearer {unauthorized}"
                }).status_code == 403
                for expected in (1, 0, 0):
                    response = client.post(f"/v1/ingest/{SOURCE_ID}/poll", headers=headers)
                    assert response.status_code == 200
                    assert response.json()["collected"] == expected
                feed = client.get("/v1/news", headers=headers)
                assert feed.status_code == 200
                assert feed.json()["count"] == 1
                item = feed.json()["items"][0]
                assert item["title"] == "One source record"
                assert item["original_url"] == "https://example.invalid/news/1"
                news_id = item["news_id"]
                first.grants.grant(Grant("eic-test", "editor_in_chief", "newsroom", news_id, "read"))
                assert client.get(f"/v1/news/{news_id}", headers=headers).json()["news"]["news_id"] == news_id
            assert len(first.pipeline.repository) == len(first.pipeline.processed) == 1
            first.registry.dispose()

            # The app composition is recreated; both news stores must survive it.
            second = build_services(environ=environ)
            services.append(second)
            second.grants.grant(Grant("eic-test", "editor_in_chief", "newsroom", "feed", "read"))
            with TestClient(create_app(services=second)) as client:
                again = client.get("/v1/news", headers=headers)
                assert again.status_code == 200
                assert again.json()["items"] == [item]
            assert len(second.pipeline.repository) == len(second.pipeline.processed) == 1
        finally:
            for service in services:
                service.registry.dispose()
            for name in reversed(created):
                control.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(name)))


def test_news_storage_configuration_fails_closed():
    with pytest.raises(ValueError, match="invalid ETEMAD_NEWS_STORAGE"):
        build_services({"ETEMAD_NEWS_STORAGE": "unknown"})
    with pytest.raises(ValueError, match="separate"):
        build_services({"ETEMAD_NEWS_STORAGE": "postgres"})
    same = "postgresql+psycopg://fixture_admin@127.0.0.1/fixture"
    with pytest.raises(ValueError, match="separate"):
        build_services({
            "ETEMAD_NEWS_STORAGE": "postgres", "ETEMAD_SESSION_KEY": "test-only",
            "ETEMAD_DB_CENTRAL_URL": same, "ETEMAD_DB_DOMESTIC_URL": same,
        })
