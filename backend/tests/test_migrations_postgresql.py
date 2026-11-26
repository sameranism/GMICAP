"""Round-trip active Alembic chains against disposable loopback PostgreSQL."""

import os
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from sqlalchemy.engine import make_url

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
            assert len(central_tables) == 8
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
        finally:
            for database in reversed(created):
                control.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(database)))
