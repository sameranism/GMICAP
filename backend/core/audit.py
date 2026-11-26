"""B01/P01 append-only audit trail.

Every privileged action writes one entry. Entries carry no secret values and no
raw request bodies: details are filtered and truncated before they leave the
process.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Callable, Mapping, Protocol
from uuid import uuid4

_SENSITIVE_KEY = re.compile(
    r"(password|passwd|secret|token|credential|authorization|api[_-]?key|cookie)",
    re.IGNORECASE,
)
_MAX_VALUE = 200
REDACTED = "[redacted]"


def sanitize(details: Mapping[str, Any] | None) -> dict[str, Any]:
    """Drop sensitive keys and truncate long values; keep ids and decisions."""
    if not details:
        return {}
    clean: dict[str, Any] = {}
    for key, value in details.items():
        if _SENSITIVE_KEY.search(str(key)):
            clean[str(key)] = REDACTED
            continue
        if isinstance(value, str) and len(value) > _MAX_VALUE:
            clean[str(key)] = value[:_MAX_VALUE] + "..."
        elif isinstance(value, (str, int, float, bool)) or value is None:
            clean[str(key)] = value
        else:
            clean[str(key)] = f"<{type(value).__name__}>"
    return clean


@dataclass(frozen=True)
class AuditEntry:
    action: str
    actor_id: str
    actor_role: str
    resource_type: str
    resource_id: str
    decision: str
    correlation_id: str
    occurred_at: str
    audit_id: str = field(default_factory=lambda: str(uuid4()))
    details: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "occurred_at": self.occurred_at,
            "actor_id": self.actor_id,
            "actor_role": self.actor_role,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "decision": self.decision,
            "correlation_id": self.correlation_id,
            "details": dict(self.details),
        }


class AuditSink(Protocol):
    def write(self, entry: AuditEntry) -> None:
        """Persist one entry; implementations must not mutate it."""


class InMemoryAuditSink:
    """Fixture sink: keeps entries for tests, never durable."""

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []
        self._lock = Lock()

    def write(self, entry: AuditEntry) -> None:
        with self._lock:
            self._entries.append(entry)

    def entries(self) -> tuple[AuditEntry, ...]:
        with self._lock:
            return tuple(self._entries)


class Auditor:
    """Builds validated entries and forwards them to the configured sink."""

    def __init__(
        self,
        sink: AuditSink,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._sink = sink
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def record(
        self,
        *,
        action: str,
        actor_id: str,
        actor_role: str,
        resource_type: str,
        resource_id: str,
        decision: str,
        correlation_id: str,
        details: Mapping[str, Any] | None = None,
    ) -> AuditEntry:
        if not all((action, actor_id, resource_type, resource_id, decision, correlation_id)):
            raise ValueError("audit entry requires action, actor, resource, decision and correlation id")
        entry = AuditEntry(
            action=action,
            actor_id=actor_id,
            actor_role=actor_role,
            resource_type=resource_type,
            resource_id=resource_id,
            decision=decision,
            correlation_id=correlation_id,
            occurred_at=self._clock().isoformat(),
            details=sanitize(details),
        )
        self._sink.write(entry)
        return entry
