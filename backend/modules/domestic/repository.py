"""P05/S02-004 raw-news repository with idempotent upsert.

Identity is the ``news_id`` derived from source and canonical URL, so re-polling
the same feed cannot create duplicates.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Mapping, Sequence

from sqlalchemy import text
from sqlalchemy.engine import Connection, Engine

from backend.core.contracts import validate_payload
from backend.core.db import DatabaseRegistry


@dataclass
class RawNewsRepository:
    """Fixture repository; production writes ``domestic.raw_news`` in PostgreSQL."""

    _by_id: dict[str, dict[str, Any]] = field(default_factory=dict, repr=False)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def upsert(self, record: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
        """Store a validated record; returns (record, created)."""
        validate_payload("raw_news", record)
        news_id = str(record["news_id"])
        with self._lock:
            existing = self._by_id.get(news_id)
            if existing is not None:
                return dict(existing), False
            stored = dict(record)
            self._by_id[news_id] = stored
            return dict(stored), True

    def upsert_many(self, records: Sequence[Mapping[str, Any]]) -> tuple[int, int]:
        """Returns (created, skipped) after validating every record first."""
        created = skipped = 0
        for record in records:
            _, was_created = self.upsert(record)
            if was_created:
                created += 1
            else:
                skipped += 1
        return created, skipped

    def get(self, news_id: str) -> dict[str, Any] | None:
        with self._lock:
            record = self._by_id.get(news_id)
            return dict(record) if record is not None else None

    def list(self, *, stream: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            values = [dict(record) for record in self._by_id.values()]
        values.sort(key=lambda item: str(item["collected_at"]), reverse=True)
        if stream is not None:
            values = [value for value in values if value["stream"] == stream]
        return values[:limit]

    def __len__(self) -> int:
        with self._lock:
            return len(self._by_id)


class PostgresRawNewsRepository:
    """Immutable domestic raw records with transactional source/hash identity."""

    def __init__(self, registry: DatabaseRegistry) -> None:
        self._registry = registry

    def _engine(self) -> Engine:
        engine = self._registry.engine("domestic")
        if engine.dialect.name != "postgresql":
            raise ValueError("domestic storage requires PostgreSQL")
        return engine

    @staticmethod
    def _prepare(record: Mapping[str, Any]) -> dict[str, Any]:
        stored = json.loads(json.dumps(dict(record), ensure_ascii=False, allow_nan=False))
        validate_payload("raw_news", stored)
        if stored["stream"] != "domestic":
            raise ValueError("only domestic records may enter domestic storage")
        return stored

    def _upsert(self, conn: Connection, record: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
        params = {"payload": json.dumps(record, ensure_ascii=False, allow_nan=False),
                  "news_id": record["news_id"], "source_id": record["source_id"],
                  "original_url": record["original_url"]}
        # Both constraints are enforced by PostgreSQL, even across worker processes.
        digest = conn.execute(text(_HASH_SQL), params).scalar_one()
        params["digest"] = digest
        conn.execute(text("""
            INSERT INTO domestic.raw_content_identity (source_id, source_hash)
            VALUES (:source_id, :digest) ON CONFLICT DO NOTHING
        """), params)
        created = conn.execute(text(_INSERT_RAW), params).scalar_one_or_none() is not None
        row = conn.execute(text("""
            SELECT to_jsonb(n) - 'source_hash' AS payload, n.source_hash
            FROM domestic.raw_news n WHERE news_id = :news_id
        """), params).mappings().one_or_none()
        if row is None:
            raise ValueError("source URL already belongs to another news identity")
        stored = dict(row["payload"])
        if (stored["source_id"], stored["original_url"]) != (
            record["source_id"], record["original_url"]
        ):
            raise ValueError("raw news identity conflict")
        if row["source_hash"] != digest:
            # Never overwrite the first collected original. A revised source
            # article requires its own explicit raw revision contract/strategy.
            raise ValueError("raw news content changed for an immutable identity")
        validate_payload("raw_news", stored)
        return stored, created

    def upsert(self, record: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
        prepared = self._prepare(record)
        with self._engine().begin() as conn:
            return self._upsert(conn, prepared)

    def upsert_many(self, records: Sequence[Mapping[str, Any]]) -> tuple[int, int]:
        prepared = [self._prepare(record) for record in records]
        created = 0
        with self._engine().begin() as conn:
            # Consistent lock order reduces deadlocks on overlapping batches.
            for record in sorted(prepared, key=lambda r: (r["source_id"], r["news_id"])):
                _, was_created = self._upsert(conn, record)
                created += int(was_created)
        return created, len(prepared) - created

    def get(self, news_id: str) -> dict[str, Any] | None:
        with self._engine().connect() as conn:
            record = conn.execute(text("""
                SELECT to_jsonb(n) - 'source_hash' FROM domestic.raw_news n
                WHERE news_id = :news_id
            """), {"news_id": news_id}).scalar_one_or_none()
            if record is None:
                return None
            validate_payload("raw_news", record)
            return dict(record)

    def list(self, *, stream: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        if limit < 0:
            raise ValueError("limit must be nonnegative")
        if stream not in (None, "domestic"):
            return []
        with self._engine().connect() as conn:
            records = [dict(row) for row in conn.execute(text("""
                SELECT to_jsonb(n) - 'source_hash' FROM domestic.raw_news n
                ORDER BY collected_at DESC, news_id LIMIT :limit
            """), {"limit": limit}).scalars()]
            for record in records:
                validate_payload("raw_news", record)
            return records

    def __len__(self) -> int:
        with self._engine().connect() as conn:
            return int(conn.execute(text("SELECT count(*) FROM domestic.raw_news")).scalar_one())


_HASH_SQL = """
SELECT encode(sha256(convert_to(
    jsonb_build_array(p->>'language', p->>'original_title', p->>'original_text')::text,
    'UTF8')), 'hex')
FROM (SELECT CAST(:payload AS jsonb) AS p) AS data
"""

_INSERT_RAW = """
INSERT INTO domestic.raw_news (
    news_id, source_id, stream, original_url, original_title, original_text,
    language, source_country, subject_countries, published_at, collected_at,
    content_scope, reuse_permission, source_payload_ref, schema_version, source_hash
)
SELECT :news_id, :source_id, p->>'stream', :original_url, p->>'original_title',
       p->>'original_text', p->>'language', p->>'source_country',
       CAST(p->'subject_countries' AS json), CAST(p->>'published_at' AS timestamptz),
       CAST(p->>'collected_at' AS timestamptz), p->>'content_scope',
       p->>'reuse_permission', p->>'source_payload_ref', p->>'schema_version', :digest
FROM (SELECT CAST(:payload AS jsonb) AS p) AS data
ON CONFLICT DO NOTHING RETURNING news_id
"""
