"""S01-026: the versioned API surface, auth and the single error envelope."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app.dependencies import build_services
from backend.app.main import create_app
from backend.core.auth import Principal, issue_session
from backend.core.errors import _STATUS, ErrorCode
from backend.core.permissions import Grant

KEY = b"api-test-session-key"


@pytest.fixture()
def services():
    built = build_services(environ={"ETEMAD_SESSION_KEY": KEY.decode("ascii")})
    built.grants.grant(Grant("eic-1", "editor_in_chief", "source_registry", "default", "read"))
    built.grants.grant(Grant("eic-1", "editor_in_chief", "source_registry", "SRC-IR-01", "write"))
    built.grants.grant(
        Grant("eic-1", "editor_in_chief", "config", "output_controls:global:controls-main", "read")
    )
    built.sources.register(
        {
            "source_id": "SRC-IR-01",
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
    )
    return built


@pytest.fixture()
def client(services):
    app = create_app(services=services)
    with TestClient(app) as test_client:
        yield test_client


def _token(services, principal: Principal | None = None) -> str:
    return issue_session(principal or Principal("eic-1", "editor_in_chief"), services.session_key)


def test_liveness_and_versioned_health(client) -> None:
    assert client.get("/health").json() == {"status": "ok"}
    body = client.get("/v1/health").json()
    assert body["status"] == "ok"
    assert "db.central" in body["checks"]
    assert "ETEMAD_DB" not in json.dumps(body)


def test_sources_require_authentication(client) -> None:
    response = client.get("/v1/sources")
    assert response.status_code == 401
    assert response.json()["code"] == "unauthorized"


def test_tampered_token_is_unauthorized(client) -> None:
    response = client.get("/v1/sources", headers={"Authorization": "Bearer v1.abc.def"})
    assert response.status_code == 401


def test_authorized_list_returns_sources_and_audits(client, services) -> None:
    headers = {"Authorization": f"Bearer {_token(services)}"}
    response = client.get("/v1/sources", headers=headers)
    assert response.status_code == 200
    assert response.json()["sources"][0]["source_id"] == "SRC-IR-01"
    assert services.audit_sink.entries()[-1].action == "source_registry.read"


def test_missing_grant_is_forbidden(client, services) -> None:
    token = issue_session(Principal("staff-1", "staff"), services.session_key)
    response = client.get("/v1/sources", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert response.json()["code"] == "forbidden"


def test_register_source_validates_contract(client, services) -> None:
    headers = {"Authorization": f"Bearer {_token(services)}"}
    payload = {
        "source_id": "SRC-IR-01",
        "site_url": "https://example.org",
        "country": "IR",
        "language": "fa",
        "stream": "domestic",
        "license_scope": "summary",
        "enabled": True,
    }
    response = client.post("/v1/sources", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["source"]["site_url"] == "https://example.org"

    bad = dict(payload, country="")
    assert client.post("/v1/sources", json=bad, headers=headers).status_code == 400


def test_unknown_config_contract_is_a_contract_error(client, services) -> None:
    services.grants.grant(
        Grant("eic-1", "editor_in_chief", "config", "not_a_contract:global:x", "read")
    )
    headers = {"Authorization": f"Bearer {_token(services)}"}
    response = client.get("/v1/config/not_a_contract/x", headers=headers)
    assert response.status_code == 400
    assert response.json()["code"] == "contract_invalid"


def test_config_update_requires_revision_and_role_grant(client, services) -> None:
    headers = {"Authorization": f"Bearer {_token(services)}"}
    example = json.loads(
        (Path(__file__).resolve().parents[2] / "source/contracts/examples/output_controls.example.json")
        .read_text(encoding="utf-8")
    )
    example["revision"] = 1
    example["updated_by"] = "eic-1"

    services.grants.grant(
        Grant("eic-1", "editor_in_chief", "config", "output_controls:global:controls-main", "update")
    )
    response = client.put(
        "/v1/config/output_controls/controls-main",
        json={"value": example, "scope": "global", "expected_revision": 0},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["revision"] == 1

    stale = client.put(
        "/v1/config/output_controls/controls-main",
        json={"value": example, "scope": "global", "expected_revision": 0},
        headers=headers,
    )
    assert stale.status_code in {400, 409}


def test_error_envelope_is_single_and_correlated(client) -> None:
    response = client.get("/v1/sources", headers={"X-Correlation-ID": "corr-42"})
    body = response.json()
    assert set(body) == {"code", "message", "correlation_id", "details"}
    assert body["correlation_id"] == "corr-42"
    assert response.headers["X-Correlation-ID"] == "corr-42"


def test_payload_too_large_maps_to_413() -> None:
    assert _STATUS[ErrorCode.PAYLOAD_TOO_LARGE] == 413


def test_demo_router_is_off_by_default(client) -> None:
    assert client.get("/v1/demo/news").status_code == 404
