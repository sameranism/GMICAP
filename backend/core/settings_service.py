"""B01/P02 versioned settings, with an explicit mock revision store.

The persistence boundary must atomically append both a revision and its audit
record. ``InMemoryRevisionStore`` is for local fixtures only; it is not durable.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Callable, Mapping, Protocol

from fastapi import HTTPException

from backend.core.contracts import ContractError, validate_payload
from backend.core.permissions import GrantLookup, decide_access, require_access

_SUPPORTED = frozenset(
    {"output_controls", "schedule_config", "ai_models_config", "news_framework"}
)


@dataclass(frozen=True)
class ConfigRevision:
    contract_name: str
    config_id: str
    scope: str
    revision: int
    value: dict[str, Any]
    updated_by: str


@dataclass(frozen=True)
class ConfigAudit:
    contract_name: str
    config_id: str
    scope: str
    revision: int
    actor_id: str
    occurred_at: str
    action: str = "config.update"


class RevisionConflict(Exception):
    """Expected revision did not match authoritative storage."""


class RevisionStore(Protocol):
    def get(self, contract_name: str, config_id: str, scope: str) -> ConfigRevision | None:
        """Return the latest revision without exposing internal mutable state."""

    def compare_and_append(
        self,
        *,
        contract_name: str,
        config_id: str,
        scope: str,
        expected_revision: int,
        value: Mapping[str, Any],
        actor_id: str,
    ) -> ConfigRevision:
        """Atomically compare, append an immutable revision, and append audit."""


class InMemoryRevisionStore:
    """Thread-safe fixture store; never use as production persistence."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._revisions: dict[tuple[str, str, str], list[ConfigRevision]] = {}
        self._audit: list[ConfigAudit] = []

    def get(self, contract_name: str, config_id: str, scope: str) -> ConfigRevision | None:
        key = (contract_name, config_id, scope)
        with self._lock:
            records = self._revisions.get(key, [])
            return deepcopy(records[-1]) if records else None

    def compare_and_append(
        self,
        *,
        contract_name: str,
        config_id: str,
        scope: str,
        expected_revision: int,
        value: Mapping[str, Any],
        actor_id: str,
    ) -> ConfigRevision:
        key = (contract_name, config_id, scope)
        with self._lock:
            records = self._revisions.setdefault(key, [])
            current = records[-1].revision if records else 0
            if current != expected_revision:
                raise RevisionConflict
            revision = current + 1
            record = ConfigRevision(
                contract_name, config_id, scope, revision, deepcopy(dict(value)), actor_id
            )
            audit = ConfigAudit(
                contract_name,
                config_id,
                scope,
                revision,
                actor_id,
                datetime.now(timezone.utc).isoformat(),
            )
            records.append(record)
            self._audit.append(audit)
            return deepcopy(record)

    def audit_entries(self) -> tuple[ConfigAudit, ...]:
        with self._lock:
            return tuple(self._audit)


CredentialRefCheck = Callable[[str], bool]


class SettingsService:
    """Authorize and validate a scoped revision before committing it."""

    def __init__(
        self,
        store: RevisionStore,
        grant_lookup: GrantLookup,
        *,
        credential_ref_check: CredentialRefCheck | None = None,
    ) -> None:
        self._store = store
        self._grant_lookup = grant_lookup
        self._credential_ref_check = credential_ref_check

    def update(
        self,
        *,
        contract_name: str,
        config_id: str,
        scope: str,
        value: Mapping[str, Any],
        expected_revision: int,
        actor_id: str,
        actor_role: str,
    ) -> ConfigRevision:
        if (
            not all((contract_name, config_id, scope, actor_id))
            or type(expected_revision) is not int
            or expected_revision < 0
        ):
            raise HTTPException(status_code=400, detail="Invalid config key or revision")
        decision = decide_access(
            actor_id,
            actor_role,
            "config",
            f"{contract_name}:{scope}:{config_id}",
            "update",
            self._grant_lookup,
        )
        require_access(decision)
        if contract_name not in _SUPPORTED:
            raise HTTPException(status_code=400, detail="Unknown config contract")
        try:
            validate_payload(contract_name, value)
        except ContractError as exc:
            raise HTTPException(status_code=400, detail="Invalid config contract") from exc
        if contract_name == "output_controls":
            if value["revision"] != expected_revision + 1 or value["updated_by"] != actor_id:
                raise HTTPException(status_code=400, detail="Invalid output control revision")
        elif contract_name == "schedule_config" and value["config_id"] != config_id:
            raise HTTPException(status_code=400, detail="Config ID mismatch")
        elif contract_name == "ai_models_config":
            if value["configuration_id"] != config_id:
                raise HTTPException(status_code=400, detail="Config ID mismatch")
            refs = [task["credential_ref"] for task in value["tasks"]]
            if refs and (
                self._credential_ref_check is None
                or not all(self._credential_ref_check(ref) for ref in refs)
            ):
                raise HTTPException(status_code=400, detail="Invalid credential reference")
        elif contract_name == "news_framework" and value["framework_id"] != config_id:
            raise HTTPException(status_code=400, detail="Config ID mismatch")
        try:
            return self._store.compare_and_append(
                contract_name=contract_name,
                config_id=config_id,
                scope=scope,
                expected_revision=expected_revision,
                value=value,
                actor_id=actor_id,
            )
        except RevisionConflict as exc:
            raise HTTPException(status_code=409, detail="Revision conflict") from exc
