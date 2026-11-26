"""domestic 001 ingest baseline (S02-006).

Creates the domestic schema owned by P05: raw news as received, plus poll state.
This database is separate from central (ADR-003); no foreign key crosses it.

Status: verified by ``alembic upgrade head`` / ``downgrade base`` on PostgreSQL 18.

Revision ID: 001_ingest
Revises:
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "001_ingest"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS domestic")

    op.create_table(
        "raw_news",
        sa.Column("news_id", sa.String(64), primary_key=True),
        sa.Column("source_id", sa.String(64), nullable=False),
        sa.Column("stream", sa.String(16), nullable=False, server_default="domestic"),
        sa.Column("original_url", sa.Text(), nullable=False),
        sa.Column("original_title", sa.Text(), nullable=False),
        sa.Column("original_text", sa.Text(), nullable=True),
        sa.Column("language", sa.String(16), nullable=False),
        sa.Column("source_country", sa.String(2), nullable=True),
        sa.Column("subject_countries", sa.JSON(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("content_scope", sa.String(16), nullable=False),
        sa.Column("reuse_permission", sa.String(16), nullable=False),
        sa.Column("source_payload_ref", sa.Text(), nullable=True),
        sa.Column("schema_version", sa.String(8), nullable=False, server_default="1.0"),
        sa.CheckConstraint("stream = 'domestic'", name="ck_raw_news_stream_domestic"),
        sa.CheckConstraint(
            "content_scope IN ('metadata','summary','full_text')", name="ck_raw_news_scope"
        ),
        sa.CheckConstraint(
            "reuse_permission IN ('unverified','licensed','link_only','blocked')",
            name="ck_raw_news_reuse",
        ),
        schema="domestic",
    )
    op.execute(
        "CREATE INDEX ix_raw_news_source_time ON domestic.raw_news (source_id, collected_at DESC)"
    )
    op.execute(
        "CREATE UNIQUE INDEX uq_raw_news_url ON domestic.raw_news (source_id, original_url)"
    )

    op.create_table(
        "poll_state",
        sa.Column("source_id", sa.String(64), primary_key=True),
        sa.Column("etag", sa.String(256), nullable=True),
        sa.Column("last_modified", sa.String(128), nullable=True),
        sa.Column("last_success_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.String(200), nullable=True),
        sa.Column("consecutive_failures", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("next_poll_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("consecutive_failures >= 0", name="ck_poll_state_failures"),
        schema="domestic",
    )


def downgrade() -> None:
    op.drop_table("poll_state", schema="domestic")
    op.drop_table("raw_news", schema="domestic")
    op.execute("DROP SCHEMA IF EXISTS domestic")
