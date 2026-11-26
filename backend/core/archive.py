"""B01/P26 archive records: identifiers, checksums and storage references.

The archive never copies another package's payload into its own tables; it keeps
a reference plus a checksum so integrity can be re-verified later.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Protocol
from uuid import uuid4

from backend.core.contracts import validate_payload

_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class InvalidArchiveKey(ValueError):
    """An object key or identifier would escape its scope."""


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def object_key(archive_id: str, extension: str = "json") -> str:
    """Content-scoped key, no path traversal, no user-controlled slashes."""
    if not _SAFE_ID.fullmatch(archive_id):
        raise InvalidArchiveKey("archive_id must match [A-Za-z0-9][A-Za-z0-9._-]{0,127}")
    if not re.fullmatch(r"[A-Za-z0-9]{1,8}", extension):
        raise InvalidArchiveKey("extension must be alphanumeric")
    return f"archive/{archive_id}.{extension}"


def build_archive_record(
    *,
    object_type: str,
    object_id: str,
    stream: str,
    classification: str,
    payload_ref: str,
    source_refs: list[str] | None = None,
    retention_policy_id: str = "standard-24m",
    stored_at: str | None = None,
    archive_id: str | None = None,
) -> dict[str, Any]:
    """Create and validate one ``archive_record`` v1.0."""
    record = {
        "schema_version": "1.0",
        "archive_id": archive_id or str(uuid4()),
        "object_type": object_type,
        "object_id": object_id,
        "stream": stream,
        "classification": classification,
        "payload_ref": payload_ref,
        "source_refs": list(source_refs or []),
        "retention_policy_id": retention_policy_id,
        "stored_at": stored_at or datetime.now(timezone.utc).isoformat(),
    }
    validate_payload("archive_record", record)
    return record


class ArchiveStore(Protocol):
    def put(self, record: Mapping[str, Any]) -> None:
        """Persist an already validated archive record."""

    def get(self, archive_id: str) -> dict[str, Any] | None:
        """Return a copy of the record or None."""


@dataclass
class InMemoryArchiveStore:
    """Fixture store; never durable."""

    _records: dict[str, dict[str, Any]] = field(default_factory=dict, repr=False)

    def put(self, record: Mapping[str, Any]) -> None:
        validate_payload("archive_record", record)
        self._records[str(record["archive_id"])] = dict(record)

    def get(self, archive_id: str) -> dict[str, Any] | None:
        record = self._records.get(archive_id)
        return dict(record) if record is not None else None

    def __len__(self) -> int:
        return len(self._records)
