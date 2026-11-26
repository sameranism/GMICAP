"""P07/P08/P09 repository for processed records.

One record per news id, holding the normalised form, its cluster result and its
classification. Writes are idempotent so a retried poll cannot fork history.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Mapping

from sqlalchemy import text
from sqlalchemy.engine import Connection, Engine

from backend.core.contracts import validate_payload
from backend.core.db import DatabaseRegistry

_CONTRACTS = {
    "news": "normalized_news",
    "cluster": "cluster_result",
    "classification": "classified_news",
}


@dataclass
class ProcessingItem:
    news: dict[str, Any]
    cluster: dict[str, Any]
    classification: dict[str, Any]
    extraction: dict[str, Any] = field(default_factory=dict)
    routing: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "news": dict(self.news),
            "cluster": dict(self.cluster),
            "classification": dict(self.classification),
            "extraction": dict(self.extraction),
            "routing": dict(self.routing),
        }


@dataclass
class ProcessingRepository:
    """Fixture store; production writes the three contract tables in central."""

    _items: dict[str, ProcessingItem] = field(default_factory=dict, repr=False)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def save(
        self,
        *,
        news: Mapping[str, Any],
        cluster: Mapping[str, Any],
        classification: Mapping[str, Any],
        extraction: Mapping[str, Any] | None = None,
        routing: Mapping[str, Any] | None = None,
    ) -> ProcessingItem:
        validate_payload(_CONTRACTS["news"], news)
        validate_payload(_CONTRACTS["cluster"], cluster)
        validate_payload(_CONTRACTS["classification"], classification)
        item = ProcessingItem(
            news=dict(news),
            cluster=dict(cluster),
            classification=dict(classification),
            extraction=dict(extraction or {}),
            routing=dict(routing or {}),
        )
        with self._lock:
            self._items[str(news["news_id"])] = item
        return item

    def get(self, news_id: str) -> ProcessingItem | None:
        with self._lock:
            return self._items.get(news_id)

    def contains(self, news_id: str) -> bool:
        with self._lock:
            return news_id in self._items

    def by_event(self, event_id: str) -> list[ProcessingItem]:
        with self._lock:
            return [item for item in self._items.values() if item.cluster.get("event_id") == event_id]

    def by_desk(self, desk: str) -> list[ProcessingItem]:
        with self._lock:
            return [item for item in self._items.values() if desk in item.classification.get("desks", [])]

    def list(self, *, limit: int = 50) -> list[ProcessingItem]:
        with self._lock:
            values = list(self._items.values())
        values.sort(key=lambda item: str(item.news["collected_at"]), reverse=True)
        return values[:limit]

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)



class PostgresProcessingRepository:
    """Central PostgreSQL store; fixture wiring remains unchanged until integration."""

    def __init__(self, registry: DatabaseRegistry) -> None:
        self._registry = registry

    def _engine(self) -> Engine:
        engine = self._registry.engine("central")
        if engine.dialect.name != "postgresql":
            raise ValueError("processing storage requires PostgreSQL")
        return engine

    def save(
        self,
        *,
        news: Mapping[str, Any],
        cluster: Mapping[str, Any],
        classification: Mapping[str, Any],
        extraction: Mapping[str, Any] | None = None,
        routing: Mapping[str, Any] | None = None,
    ) -> ProcessingItem:
        item = _checked_snapshot(news, cluster, classification, extraction, routing)
        digest = _artifact_hash(item)
        news_id = item["news"]["news_id"]
        params = {"news_id": news_id, "snapshot": _json(item)}
        with self._engine().begin() as conn:
            inserted = conn.execute(text(_INSERT_NEWS), params).scalar_one_or_none()
            identity = conn.execute(text("""
                SELECT source_id, original_url, stream FROM processing.normalized_news
                WHERE news_id = :news_id FOR UPDATE
            """), params).mappings().one()
            if any(identity[k] != item["news"][k] for k in ("source_id", "original_url", "stream")):
                raise ValueError("news identity conflict")
            revision = int(conn.execute(text("""
                SELECT COALESCE(MAX(revision_no), 0) FROM processing.artifact_history
                WHERE news_id = :news_id
            """), params).scalar_one())
            if inserted is None and revision == 0:
                # Revision 002 may contain existing records. Preserve a complete
                # legacy projection before changing anything. Partial rows fail closed.
                legacy = conn.execute(text(_READ_CURRENT + " WHERE n.news_id = :news_id"),
                                      params).scalar_one_or_none()
                if legacy is None:
                    raise ValueError("incomplete legacy processing record")
                legacy = _checked_snapshot(legacy["news"], legacy["cluster"],
                                           legacy["classification"], None, None)
                _append_history(conn, news_id, 1, legacy, _artifact_hash(legacy))
                revision = 1
            if revision:
                replay = conn.execute(text("""
                    SELECT 1 FROM processing.artifact_history
                    WHERE news_id = :news_id AND artifact_hash = :digest
                """), {"news_id": news_id, "digest": digest}).scalar_one_or_none()
                if replay is not None:
                    current = conn.execute(text("""
                        SELECT snapshot FROM processing.artifact_history WHERE news_id = :news_id
                        ORDER BY revision_no DESC LIMIT 1
                    """), params).scalar_one()
                    return ProcessingItem(**current)
            conn.execute(text(_UPDATE_NEWS), params)
            conn.execute(text(_UPSERT_CLUSTER), params)
            conn.execute(text(_UPSERT_CLASSIFICATION), params)
            _append_history(conn, news_id, revision + 1, item, digest)
        return ProcessingItem(**item)

    def _read(self, suffix: str, params: Mapping[str, Any]) -> list[ProcessingItem]:
        with self._engine().connect() as conn:
            return [ProcessingItem(**record) for record in
                    conn.execute(text(_READ_CURRENT + suffix), params).scalars()]

    def get(self, news_id: str) -> ProcessingItem | None:
        rows = self._read(" WHERE n.news_id = :news_id", {"news_id": news_id})
        return rows[0] if rows else None

    def contains(self, news_id: str) -> bool:
        return self.get(news_id) is not None

    def by_event(self, event_id: str) -> list[ProcessingItem]:
        return self._read(" WHERE c.event_id = :event_id ORDER BY n.news_id", {"event_id": event_id})

    def by_desk(self, desk: str) -> list[ProcessingItem]:
        return self._read(" WHERE CAST(d.desks AS jsonb) @> CAST(:desk AS jsonb) ORDER BY n.news_id",
                          {"desk": _json([desk])})

    def list(self, *, limit: int = 50) -> list[ProcessingItem]:
        if limit < 0:
            raise ValueError("limit must be nonnegative")
        return self._read(" ORDER BY n.collected_at DESC, n.news_id LIMIT :limit", {"limit": limit})

    def __len__(self) -> int:
        with self._engine().connect() as conn:
            return int(conn.execute(text("""
                SELECT COUNT(*) FROM processing.normalized_news n
                JOIN processing.cluster_result c USING (news_id)
                JOIN processing.classified_news d USING (news_id)
            """)).scalar_one())


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _checked_snapshot(
    news: Mapping[str, Any], cluster: Mapping[str, Any], classification: Mapping[str, Any],
    extraction: Mapping[str, Any] | None, routing: Mapping[str, Any] | None,
) -> dict[str, Any]:
    item = json.loads(_json(ProcessingItem(dict(news), dict(cluster), dict(classification),
                                         dict(extraction or {}), dict(routing or {})).as_dict()))
    for key, contract in _CONTRACTS.items():
        validate_payload(contract, item[key])
    if item["news"]["news_id"] != item["cluster"]["news_id"] or (
        item["news"]["news_id"] != item["classification"]["news_id"]
    ) or item["cluster"]["event_id"] != item["classification"]["event_id"]:
        raise ValueError("processing artifact identity mismatch")
    if item["news"]["stream"] != item["classification"]["stream"]:
        raise ValueError("processing stream mismatch")
    if item["cluster"]["duplicate_of"] == item["news"]["news_id"]:
        raise ValueError("self duplicate")
    if set(item["extraction"]) - {"word_count", "quotes", "truncated", "method"} or (
        set(item["routing"]) - {"news_id", "target_project", "queue", "analysis_queue",
                                "reasons", "rules_version"}
    ):
        raise ValueError("unknown processing metadata")
    if item["routing"].get("news_id", item["news"]["news_id"]) != item["news"]["news_id"]:
        raise ValueError("routing identity mismatch")
    return item


def _artifact_hash(snapshot: Mapping[str, Any]) -> str:
    stable = json.loads(_json(snapshot))
    stable["cluster"].pop("created_at", None)
    stable["classification"].pop("classified_at", None)
    return hashlib.sha256(_json(stable).encode("utf-8")).hexdigest()


def _append_history(conn: Connection, news_id: str, revision: int,
                    snapshot: Mapping[str, Any], digest: str) -> None:
    conn.execute(text("""
        INSERT INTO processing.artifact_history (news_id, revision_no, artifact_hash, snapshot)
        VALUES (:news_id, :revision, :digest, CAST(:snapshot AS jsonb))
    """), {"news_id": news_id, "revision": revision, "digest": digest, "snapshot": _json(snapshot)})


# All SQL uses fixed table/column identifiers and bound values. Only this package's
# owned central schema is touched. The row lock serializes revisions per news id.
_INSERT_NEWS = """
INSERT INTO processing.normalized_news
    (news_id, stream, source_id, original_url, language, content_scope, reuse_permission,
     fingerprint, normalization_version, normalized_text, collected_at, document)
SELECT :news_id, j->>'stream', j->>'source_id', j->>'original_url', j->>'language',
       j->>'content_scope', j->>'reuse_permission', j->>'fingerprint',
       j->>'normalization_version', j->>'normalized_text', CAST(j->>'collected_at' AS timestamptz), j
FROM (SELECT CAST(:snapshot AS jsonb)->'news' AS j) AS p
ON CONFLICT (news_id) DO NOTHING RETURNING news_id
"""
_UPDATE_NEWS = """
UPDATE processing.normalized_news AS n SET language=j->>'language',
    content_scope=j->>'content_scope', reuse_permission=j->>'reuse_permission',
    fingerprint=j->>'fingerprint', normalization_version=j->>'normalization_version',
    normalized_text=j->>'normalized_text', collected_at=CAST(j->>'collected_at' AS timestamptz),
    document=j
FROM (SELECT CAST(:snapshot AS jsonb)->'news' AS j) AS p WHERE n.news_id=:news_id
"""
_UPSERT_CLUSTER = """
INSERT INTO processing.cluster_result
    (news_id, event_id, duplicate_of, related_news_ids, similarity_method, created_at)
SELECT :news_id, j->>'event_id', j->>'duplicate_of', j->'related_news_ids',
       j->>'similarity_method', CAST(j->>'created_at' AS timestamptz)
FROM (SELECT CAST(:snapshot AS jsonb)->'cluster' AS j) AS p
ON CONFLICT (news_id) DO UPDATE SET event_id=EXCLUDED.event_id,
    duplicate_of=EXCLUDED.duplicate_of, related_news_ids=EXCLUDED.related_news_ids,
    similarity_method=EXCLUDED.similarity_method, created_at=EXCLUDED.created_at
"""
_UPSERT_CLASSIFICATION = """
INSERT INTO processing.classified_news
    (news_id, stream, desks, topics, subject_countries, event_id, operational_priority,
     rules_version, classified_at)
SELECT :news_id, j->>'stream', j->'desks', j->'topics', j->'subject_countries', j->>'event_id',
       j->>'operational_priority', j->>'rules_version', CAST(j->>'classified_at' AS timestamptz)
FROM (SELECT CAST(:snapshot AS jsonb)->'classification' AS j) AS p
ON CONFLICT (news_id) DO UPDATE SET stream=EXCLUDED.stream, desks=EXCLUDED.desks,
    topics=EXCLUDED.topics, subject_countries=EXCLUDED.subject_countries,
    event_id=EXCLUDED.event_id, operational_priority=EXCLUDED.operational_priority,
    rules_version=EXCLUDED.rules_version, classified_at=EXCLUDED.classified_at
"""
_READ_CURRENT = """
SELECT COALESCE(h.snapshot, jsonb_build_object(
    'news', n.document,
    'cluster', to_jsonb(c) || jsonb_build_object('schema_version', '1.0'),
    'classification', to_jsonb(d) || jsonb_build_object('schema_version', '1.0'),
    'extraction', '{}'::jsonb, 'routing', '{}'::jsonb))
FROM processing.normalized_news n
JOIN processing.cluster_result c USING (news_id)
JOIN processing.classified_news d USING (news_id)
LEFT JOIN LATERAL (SELECT snapshot FROM processing.artifact_history WHERE news_id = n.news_id
                   ORDER BY revision_no DESC LIMIT 1) h ON TRUE
"""
