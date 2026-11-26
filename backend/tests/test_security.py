"""S01-020: authentication, authorization, audit and configuration safety."""

from __future__ import annotations

import time

import pytest

from backend.core.audit import Auditor, REDACTED, InMemoryAuditSink, sanitize
from backend.core.auth import (
    AuthenticationError,
    MIN_PASSWORD_LENGTH,
    Principal,
    SessionInvalid,
    bearer_token,
    generate_first_use_credential,
    hash_password,
    issue_session,
    verify_password,
    verify_session,
)
from backend.core.db import DatabaseNotConfigured, DatabaseRegistry, configured_roles, redact_url
from backend.core.permissions import Grant, InMemoryGrantStore, decide_access, require_access
from backend.core.secrets import (
    EnvSecretStore,
    InMemorySecretStore,
    InvalidSecretReference,
    SecretUnavailable,
    require_secret,
)

KEY = b"test-session-key-not-a-real-secret"


# --- passwords and credentials -------------------------------------------------


def test_password_hash_roundtrip() -> None:
    encoded = hash_password("correct horse battery staple")
    assert encoded.startswith("scrypt$")
    assert "correct horse" not in encoded
    assert verify_password("correct horse battery staple", encoded)
    assert not verify_password("wrong password entirely", encoded)


def test_short_password_is_rejected() -> None:
    with pytest.raises(ValueError):
        hash_password("x" * (MIN_PASSWORD_LENGTH - 1))


def test_same_password_has_different_hashes() -> None:
    first = hash_password("correct horse battery staple")
    second = hash_password("correct horse battery staple")
    assert first != second


def test_first_use_credential_is_long_and_unique() -> None:
    values = {generate_first_use_credential() for _ in range(20)}
    assert len(values) == 20
    assert all(len(value) >= 30 for value in values)


# --- sessions ------------------------------------------------------------------


def test_session_roundtrip_preserves_principal() -> None:
    principal = Principal("user-001", "editor_in_chief", must_reset_password=True)
    token = issue_session(principal, KEY, ttl_seconds=60)
    restored = verify_session(token, KEY)
    assert restored == principal


def test_tampered_token_is_rejected() -> None:
    token = issue_session(Principal("user-001", "staff"), KEY)
    head, body, signature = token.split(".")
    forged = f"{head}.{body[:-2]}AA.{signature}"
    with pytest.raises(SessionInvalid):
        verify_session(forged, KEY)


def test_expired_token_is_rejected() -> None:
    token = issue_session(Principal("user-001", "staff"), KEY, ttl_seconds=1)
    with pytest.raises(SessionInvalid):
        verify_session(token, KEY, now=int(time.time()) + 10)


def test_unknown_role_cannot_be_a_principal() -> None:
    with pytest.raises(ValueError):
        Principal("user-001", "superuser")


def test_bearer_extraction() -> None:
    assert bearer_token("Bearer abc.def") == "abc.def"
    assert bearer_token("Basic abc") is None
    assert bearer_token(None) is None


# --- authorization -------------------------------------------------------------


def test_default_is_deny() -> None:
    decision = decide_access("user-001", "staff", "article", "a-1", "read", lambda *args: False)
    assert decision["allowed"] is False
    assert decision["reason_code"] == "DENY_DEFAULT"


def test_grant_allows_the_named_action_only() -> None:
    store = InMemoryGrantStore([Grant("user-001", "staff", "article", "a-1", "read")])
    allowed = decide_access("user-001", "staff", "article", "a-1", "read", store)
    denied = decide_access("user-001", "staff", "article", "a-1", "publish", store)
    assert allowed["allowed"] is True
    assert denied["allowed"] is False


def test_private_report_requires_explicit_editor_in_chief_grant() -> None:
    store = InMemoryGrantStore()
    without_grant = decide_access(
        "eic-1", "editor_in_chief", "private_report", "r-9", "read", store
    )
    assert without_grant["allowed"] is False
    assert without_grant["reason_code"] == "GRANT_REQUIRED"

    store.grant(Grant("eic-1", "editor_in_chief", "private_report", "r-9", "read"))
    with_grant = decide_access("eic-1", "editor_in_chief", "private_report", "r-9", "read", store)
    assert with_grant["allowed"] is True


def test_owner_and_staff_never_reach_private_reports() -> None:
    store = InMemoryGrantStore()
    for role, actor in (("owner", "owner-1"), ("staff", "staff-1")):
        decision = decide_access(actor, role, "private_report", "r-9", "read", store)
        assert decision["allowed"] is False
        assert decision["reason_code"] == "EXECUTIVE_PRIVATE"


def test_require_access_hides_private_objects() -> None:
    denied_private = decide_access("s", "staff", "private_report", "r-9", "read", lambda *a: False)
    denied_public = decide_access("s", "staff", "article", "a-1", "read", lambda *a: False)
    with pytest.raises(Exception) as private:
        require_access(denied_private)
    with pytest.raises(Exception) as public:
        require_access(denied_public)
    assert getattr(private.value, "status_code", None) == 404
    assert getattr(public.value, "status_code", None) == 403


# --- audit ---------------------------------------------------------------------


def test_audit_sanitizes_secrets_and_bounds_values() -> None:
    sink = InMemoryAuditSink()
    auditor = Auditor(sink)
    entry = auditor.record(
        action="config.update",
        actor_id="user-001",
        actor_role="editor_in_chief",
        resource_type="output_controls",
        resource_id="controls-main",
        decision="allow",
        correlation_id="req-1",
        details={
            "password": "hunter2",
            "credential_ref": "dest/a",
            "note": "x" * 500,
        },
    )
    assert entry.details["password"] == REDACTED
    assert entry.details["credential_ref"] == REDACTED
    assert entry.details["note"].endswith("...")
    assert len(entry.details["note"]) <= 203
    assert sink.entries() == (entry,)


def test_audit_requires_complete_identity() -> None:
    with pytest.raises(ValueError):
        Auditor(InMemoryAuditSink()).record(
            action="x",
            actor_id="",
            actor_role="staff",
            resource_type="article",
            resource_id="a-1",
            decision="deny",
            correlation_id="req-1",
        )


def test_sanitize_keeps_ids_and_neutralizes_objects() -> None:
    clean = sanitize({"resource_id": "a-1", "payload": {"a": 1}})
    assert clean["resource_id"] == "a-1"
    assert clean["payload"] == "<dict>"


# --- database configuration ----------------------------------------------------


def test_database_roles_are_optional_and_redacted() -> None:
    registry = DatabaseRegistry(environ={})
    with pytest.raises(DatabaseNotConfigured):
        registry.engine("central")
    assert registry.describe()["central"] == "not_configured"
    assert configured_roles({}) == []


def test_database_url_password_is_redacted() -> None:
    url = "postgresql+psycopg://etemad:s3cr3t@db:5432/etemad_central"
    redacted = redact_url(url)
    assert "s3cr3t" not in redacted
    assert redacted.endswith("/etemad_central")


def test_engine_is_created_lazily_for_a_configured_role(tmp_path) -> None:
    registry = DatabaseRegistry(environ={"ETEMAD_DB_CENTRAL_URL": "sqlite://"})
    engine = registry.engine("central")
    assert engine.dialect.name == "sqlite"
    registry.dispose()


def test_unknown_database_role_is_rejected() -> None:
    with pytest.raises(KeyError):
        DatabaseRegistry(environ={}).url_for("staging")


# --- secrets -------------------------------------------------------------------


def test_env_secret_store_maps_reference_to_variable() -> None:
    store = EnvSecretStore(environ={"ETEMAD_SECRET_DEST_TELEGRAM": "abc"})
    assert require_secret(store, "dest/telegram") == "abc"
    with pytest.raises(SecretUnavailable):
        require_secret(store, "dest/missing")


def test_secret_reference_format_is_enforced() -> None:
    with pytest.raises(InvalidSecretReference):
        InMemorySecretStore({"Bad Ref!": "x"})


def test_authentication_error_is_the_common_base() -> None:
    assert issubclass(SessionInvalid, AuthenticationError)
