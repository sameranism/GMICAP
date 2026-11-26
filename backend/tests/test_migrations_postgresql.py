"""Round-trip active Alembic chains against disposable loopback PostgreSQL."""

import os
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError, IntegrityError

from backend.core.db import DatabaseRegistry
from backend.modules.processing.classifier import classify
from backend.modules.processing.deduplicator import Clusterer
from backend.modules.processing.normalizer import normalize
from backend.modules.processing.repository import PostgresProcessingRepository

ADMIN_URL = os.environ.get("ETEMAD_TEST_PG_ADMIN_URL")
BACKEND = Path(__file__).resolve().parents[1]

TABLES_SQL = """
    SELECT table_schema, table_name FROM information_schema.tables
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema', 'public')
    AND table_type = 'BASE TABLE'
"""


@pytest.mark.skipif(not ADMIN_URL, reason="ETEMAD_TEST_PG_ADMIN_URL is unset")
def test_migration_round_trip_and_database_separation(monkeypatch):
    from alembic import command
    from alembic.config import Config

    assert ADMIN_URL is not None
    admin = make_url(ADMIN_URL)
    assert admin.host == "127.0.0.1" and admin.database == "postgres"
    assert admin.username == "fixture_admin" and not admin.query

    suffix = uuid4().hex[:12]
    databases = {role: f"etemad_test_{role}_{suffix}" for role in ("central", "domestic", "foreign")}

    def conninfo(database):
        url = admin.set(drivername="postgresql", database=database)
        return url.render_as_string(hide_password=False)

    def tables(role):
        with psycopg.connect(conninfo(databases[role])) as conn:
            return set(conn.execute(TABLES_SQL).fetchall())

    monkeypatch.chdir(BACKEND)
    created = []
    with psycopg.connect(conninfo("postgres"), autocommit=True) as control:
        try:
            for role, database in databases.items():
                control.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
                created.append(database)
                test_url = admin.set(drivername="postgresql+psycopg", database=database)
                monkeypatch.setenv(
                    f"ETEMAD_DB_{role.upper()}_URL", test_url.render_as_string(hide_password=False),
                )

            central = Config("alembic.ini")
            command.upgrade(central, "head")
            central_tables = tables("central")
            assert len(central_tables) == 9
            assert ("processing", "artifact_history") in central_tables
            assert {schema for schema, _ in central_tables} == {
                "audit", "control", "identity", "processing",
            }
            assert tables("domestic") == tables("foreign") == set()
            command.downgrade(central, "001_baseline")
            assert tables("central") == {row for row in central_tables if row[0] != "processing"}
            command.downgrade(central, "base")
            assert tables("central") == set()
            command.upgrade(central, "head")
            assert tables("central") == central_tables

            domestic = Config("alembic_domestic.ini")
            command.upgrade(domestic, "head")
            domestic_tables = tables("domestic")
            assert len(domestic_tables) == 2
            assert not domestic_tables & central_tables
            command.downgrade(domestic, "base")
            assert tables("domestic") == set()
            command.upgrade(domestic, "head")
            assert tables("domestic") == domestic_tables
            assert tables("central") == central_tables
            assert tables("foreign") == set()
            _exercise_processing_history(central)
            assert tables("domestic") == domestic_tables
            assert tables("foreign") == set()
        finally:
            for database in reversed(created):
                control.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(database)))


def _exercise_processing_history(central):
    from alembic import command

    registry = DatabaseRegistry()
    repo = PostgresProcessingRepository(registry)
    stamp = "2026-11-23T07:00:00Z"
    raw = {
        "schema_version": "1.0",
        "news_id": "NEWS-TEST-1",
        "stream": "domestic",
        "source_id": "SRC-TEST-1",
        "original_url": "https://example.invalid/one",
        "original_title": "Fixture title",
        "original_text": "Synthetic original",
        "language": "en",
        "subject_countries": [],
        "collected_at": stamp,
        "content_scope": "summary",
        "reuse_permission": "unverified",
    }
    news = normalize(raw)
    cluster = Clusterer().cluster(news, created_at=stamp)
    classified = classify(news, event_id=cluster["event_id"], classified_at=stamp)
    first = {"news": news, "cluster": cluster, "classification": classified}
    try:
        assert repo.save(**first).news == news
        assert repo.save(**first).news == news
        assert len(repo) == 1
        assert repo.get("NEWS-TEST-1").news == news
        assert repo.by_event(cluster["event_id"])[0].news == news
        assert repo.by_desk(classified["desks"][0])[0].news == news
        assert repo.list(limit=0) == []
        assert repo.list(limit=1)[0].news == news

        retry = deepcopy(first)
        retry["cluster"]["created_at"] = "2026-11-23T08:00:00Z"
        retry["classification"]["classified_at"] = "2026-11-23T08:00:00Z"
        with ThreadPoolExecutor(max_workers=4) as workers:
            results = list(workers.map(lambda _: repo.save(**retry), range(8)))
        assert all(item.news == news for item in results)

        revised = deepcopy(first)
        revised["news"] = normalize({**raw, "original_text": "Corrected synthetic original"})
        repo.save(**revised)
        assert repo.get("NEWS-TEST-1").news == revised["news"]
        assert repo.save(**first).news == revised["news"]

        conflicting = deepcopy(first)
        conflicting["cluster"]["news_id"] = "NEWS-OTHER"
        with pytest.raises(ValueError, match="identity mismatch"):
            repo.save(**conflicting)
        conflicting = deepcopy(first)
        conflicting["news"]["source_id"] = "SRC-OTHER"
        with pytest.raises(ValueError, match="identity conflict"):
            repo.save(**conflicting)

        # Identical content from another source remains an independent record.
        other = deepcopy(first)
        other["news"] = normalize({**raw, "news_id": "NEWS-TEST-2",
                                   "source_id": "SRC-TEST-2",
                                   "original_url": "https://example.invalid/two"})
        other["cluster"]["news_id"] = "NEWS-TEST-2"
        other["cluster"]["duplicate_of"] = "NEWS-TEST-1"
        other["classification"]["news_id"] = "NEWS-TEST-2"
        repo.save(**other)
        assert len(repo) == 2

        # A failed child write must roll back the parent insert.
        bad = deepcopy(other)
        bad["news"]["news_id"] = "NEWS-TEST-3"
        bad["news"]["original_url"] = "https://example.invalid/three"
        bad["cluster"]["news_id"] = "NEWS-TEST-3"
        bad["classification"]["news_id"] = "NEWS-TEST-3"
        bad["cluster"]["event_id"] = "x" * 33
        bad["classification"]["event_id"] = "x" * 33
        with pytest.raises(DBAPIError):
            repo.save(**bad)

        engine = registry.engine("central")
        with engine.connect() as conn:
            assert conn.execute(text(
                "SELECT count(*) FROM processing.normalized_news"
            )).scalar_one() == 2
            rows = conn.execute(text(
                "SELECT revision_no, snapshot FROM processing.artifact_history "
                "WHERE news_id = 'NEWS-TEST-1' ORDER BY revision_no"
            )).all()
            assert [row.revision_no for row in rows] == [1, 2]
            assert rows[0].snapshot["news"]["original_text"] == "Synthetic original"
            assert rows[1].snapshot["news"]["original_text"] == "Corrected synthetic original"
        with pytest.raises(IntegrityError):
            with engine.begin() as conn:
                conn.execute(text(
                    "INSERT INTO processing.cluster_result "
                    "(news_id, event_id, related_news_ids, similarity_method, created_at) "
                    "VALUES ('orphan', 'EVENT-X', '[]', 'test', now())"
                ))
        with pytest.raises(DBAPIError, match="processing history is not empty"):
            command.downgrade(central, "002_processing")
        assert repo.get("NEWS-TEST-1").news == revised["news"]
    finally:
        registry.dispose()
