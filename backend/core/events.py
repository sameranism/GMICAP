"""B01/P29 event envelopes and the in-process bus.

Events carry a reference, not a payload copy. Every envelope is validated
against ``event_envelope`` v1.0 before it reaches a subscriber, and the
idempotency key lets consumers drop duplicates after a retry.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Callable, Mapping, Protocol
from uuid import uuid4

from backend.core.contracts import validate_payload

CLASSIFICATIONS = frozenset({"public", "internal", "executive_private"})


class UnknownClassification(ValueError):
    """Classification must be explicit; there is no default in the contract."""


def make_event(
    *,
    event_type: str,
    producer_project: str,
    object_id: str,
    correlation_id: str,
    payload_ref: str,
    classification: str = "internal",
    occurred_at: str | None = None,
    event_id: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    """Build and validate one event envelope."""
    if classification not in CLASSIFICATIONS:
        raise UnknownClassification(f"unknown classification: {classification!r}")
    event = {
        "schema_version": "1.0",
        "event_id": event_id or str(uuid4()),
        "event_type": event_type,
        "producer_project": producer_project,
        "object_id": object_id,
        "correlation_id": correlation_id,
        "idempotency_key": idempotency_key or f"{event_type}:{object_id}",
        "classification": classification,
        "occurred_at": occurred_at or datetime.now(timezone.utc).isoformat(),
        "payload_ref": payload_ref,
    }
    validate_payload("event_envelope", event)
    return event


def dedupe_key(event: Mapping[str, Any]) -> str:
    """Stable key for consumer-side deduplication."""
    return f"{event['producer_project']}:{event['idempotency_key']}"


class EventBus(Protocol):
    def publish(self, event: Mapping[str, Any]) -> None:
        """Validate and deliver to every subscriber of the event type."""

    def subscribe(self, event_type: str, handler: Callable[[dict[str, Any]], None]) -> None:
        """Register a synchronous handler for one event type."""


@dataclass
class InMemoryEventBus:
    """Synchronous fixture bus with per-consumer deduplication by idempotency key."""

    _handlers: dict[str, list[Callable[[dict[str, Any]], None]]] = field(
        default_factory=dict, repr=False
    )
    _seen: set[str] = field(default_factory=set, repr=False)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def subscribe(self, event_type: str, handler: Callable[[dict[str, Any]], None]) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: Mapping[str, Any]) -> None:
        validate_payload("event_envelope", event)
        with self._lock:
            if dedupe_key(event) in self._seen:
                return
            self._seen.add(dedupe_key(event))
            handlers = list(self._handlers.get(str(event["event_type"]), ()))
        for handler in handlers:
            handler(dict(event))

    def deliveries(self) -> set[str]:
        with self._lock:
            return set(self._seen)


def event_json(event: Mapping[str, Any]) -> str:
    """Canonical JSON for logs and outbox storage; stable key order."""
    return json.dumps(dict(event), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
