"""S02/S03 integration: poll a fixture feed and read the real newsroom feed."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app.dependencies import build_services
from backend.app.main import create_app
from backend.core.auth import Principal, issue_session
from backend.core.permissions import Grant
from backend.modules.domestic.feed_client import FeedResponse

KEY = b"news-api-session-key"
FEED_URL = "https://example.com/rss"
RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>fixture</title>
<item><title>جلسه شورای شهر تهران</title>
<link>https://example.com/news/1</link>
<description>شهرداری درباره بودجه جلسه داشت.</description>
<pubDate>Mon, 23 Nov 2026 06:00:00 GMT</pubDate></item>
<item><title>رشد شاخص بورس</title>
<link>https://example.com/news/2</link>
<description>بورس تهران امروز رشد کرد و تورم کاهش یافت.</description>
<pubDate>Mon, 23 Nov 2026 07:30:00 GMT</pubDate></item>
</channel></rss>""".encode("utf-8")


@pytest.fixture()
def services():
    built = build_services(environ={"ETEMAD_SESSION_KEY": KEY.decode("ascii")})
    built.sources.register(
        {
            "source_id": "SRC-IR-01",
            "site_url": "https://example.com",
            "feed_url": FEED_URL,
            "api_base_url": None,
            "country": "IR",
            "language": "fa",
            "stream": "domestic",
            "auth_ref": None,
            "license_scope": "summary",
            "enabled": True,
        }
    )
    built.transport.responses = {
        FEED_URL: FeedResponse(url=FEED_URL, status_code=200, body=RSS, etag='W/"1"')
    }
    built.grants.grant(Grant("eic-1", "editor_in_chief", "source_registry", "SRC-IR-01", "poll"))
    built.grants.grant(Grant("eic-1", "editor_in_chief", "source_registry", "SRC-IR-01", "read"))
    built.grants.grant(Grant("eic-1", "editor_in_chief", "newsroom", "feed", "read"))
    return built


@pytest.fixture()
def client(services):
    with TestClient(create_app(services=services)) as test_client:
        yield test_client


def _headers(services) -> dict[str, str]:
    token = issue_session(Principal("eic-1", "editor_in_chief"), services.session_key)
    return {"Authorization": f"Bearer {token}"}


def test_poll_collects_fixture_articles(client, services) -> None:
    response = client.post("/v1/ingest/SRC-IR-01/poll", headers=_headers(services))
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["collected"] == 2
    assert body["state"]["last_success_at"]


def test_second_poll_is_idempotent(client, services) -> None:
    headers = _headers(services)
    client.post("/v1/ingest/SRC-IR-01/poll", headers=headers)
    second = client.post("/v1/ingest/SRC-IR-01/poll", headers=headers).json()
    assert second["status"] in {"ok", "not_modified"}
    assert second["collected"] == 0


def test_news_feed_returns_real_contract_items(client, services) -> None:
    headers = _headers(services)
    client.post("/v1/ingest/SRC-IR-01/poll", headers=headers)
    body = client.get("/v1/news", headers=headers).json()
    assert body["count"] == 2
    items = body["items"]
    assert {item["stream"] for item in items} == {"domestic"}
    assert all(item["event_id"].startswith("EVENT-") for item in items)
    assert any("economy" in item["desks"] for item in items)
    assert all(item["reuse_permission"] == "unverified" for item in items)
    assert all(item["source_id"] == "SRC-IR-01" for item in items)


def test_single_news_item_and_missing_id(client, services) -> None:
    headers = _headers(services)
    client.post("/v1/ingest/SRC-IR-01/poll", headers=headers)
    news_id = client.get("/v1/news", headers=headers).json()["items"][0]["news_id"]
    services.grants.grant(Grant("eic-1", "editor_in_chief", "newsroom", news_id, "read"))
    detail = client.get(f"/v1/news/{news_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["news"]["news_id"] == news_id
    assert client.get("/v1/news/NEWS-UNKNOWN", headers=headers).status_code == 403


def test_poll_requires_its_own_grant(client, services) -> None:
    token = issue_session(Principal("staff-1", "staff"), services.session_key)
    response = client.post(
        "/v1/ingest/SRC-IR-01/poll", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_poll_reports_blocked_for_unknown_source(client, services) -> None:
    services.grants.grant(Grant("eic-1", "editor_in_chief", "source_registry", "SRC-XX-9", "poll"))
    body = client.post("/v1/ingest/SRC-XX-9/poll", headers=_headers(services)).json()
    assert body["status"] == "blocked"
    assert body["collected"] == 0


def test_poll_state_endpoint_reports_last_run(client, services) -> None:
    headers = _headers(services)
    client.post("/v1/ingest/SRC-IR-01/poll", headers=headers)
    response = client.get("/v1/ingest/SRC-IR-01/poll-state", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["known"] is True
    assert body["state"]["source_id"] == "SRC-IR-01"
    assert body["state"]["last_success_at"]


def test_poll_state_for_unknown_source_is_marked_unknown(client, services) -> None:
    services.grants.grant(Grant("eic-1", "editor_in_chief", "source_registry", "SRC-XX-9", "read"))
    body = client.get("/v1/ingest/SRC-XX-9/poll-state", headers=_headers(services)).json()
    assert body["known"] is False


def test_feed_failure_is_a_failed_poll_not_a_crash(client, services) -> None:
    services.transport.failures = {FEED_URL: "timeout"}
    body = client.post("/v1/ingest/SRC-IR-01/poll", headers=_headers(services)).json()
    assert body["status"] == "failed"
    assert "timeout" in body["error"]
    services.transport.failures = {}
