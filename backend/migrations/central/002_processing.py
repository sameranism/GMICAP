"""central 002 processing tables (S03-007).

Stores the processed contract records owned by P07/P08/P09: normalised news,
cluster results and classifications. Raw payloads stay in domestic/foreign
databases and object storage; only references cross the boundary.

Status: verified by ``alembic upgrade head`` / ``downgrade`` on PostgreSQL 18.

Revision ID: 002_processing
Revises: 001_baseline
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "002_processing"
down_revision = "001_baseline"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS processing")

    op.create_table(
        "normalized_news",
        sa.Column("news_id", sa.String(64), primary_key=True),
        sa.Column("stream", sa.String(16), nullable=False),
        sa.Column("source_id", sa.String(64), nullable=False),
        sa.Column("original_url", sa.Text(), nullable=False),
        sa.Column("language", sa.String(16), nullable=False),
        sa.Column("content_scope", sa.String(16), nullable=False),
        sa.Column("reuse_permission", sa.String(16), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("normalization_version", sa.String(16), nullable=False),
        sa.Column("normalized_text", sa.Text(), nullable=True),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("document", sa.JSON(), nullable=False),
        sa.CheckConstraint(
            "content_scope IN ('metadata','summary','full_text')", name="ck_norm_scope"
        ),
        sa.CheckConstraint(
            "reuse_permission IN ('unverified','licensed','link_only','blocked')",
            name="ck_norm_reuse",
        ),
        sa.UniqueConstraint("source_id", "original_url", name="uq_norm_source_url"),
        schema="processing",
    )
    op.execute(
        "CREATE INDEX ix_norm_fingerprint ON processing.normalized_news (fingerprint)"
    )
    op.execute(
        "CREATE INDEX ix_norm_collected ON processing.normalized_news (collected_at DESC)"
    )

    op.create_table(
        "cluster_result",
        sa.Column("news_id", sa.String(64), primary_key=True),
        sa.Column("event_id", sa.String(32), nullable=False),
        sa.Column("duplicate_of", sa.String(64), nullable=True),
        sa.Column("related_news_ids", sa.JSON(), nullable=False),
        sa.Column("similarity_method", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("news_id <> duplicate_of", name="ck_cluster_no_self_duplicate"),
        schema="processing",
    )
    op.execute("CREATE INDEX ix_cluster_event ON processing.cluster_result (event_id)")

    op.create_table(
        "classified_news",
        sa.Column("news_id", sa.String(64), primary_key=True),
        sa.Column("stream", sa.String(16), nullable=False),
        sa.Column("desks", sa.JSON(), nullable=False),
        sa.Column("topics", sa.JSON(), nullable=False),
        sa.Column("subject_countries", sa.JSON(), nullable=False),
        sa.Column("event_id", sa.String(32), nullable=False),
        sa.Column("operational_priority", sa.String(16), nullable=False),
        sa.Column("rules_version", sa.String(32), nullable=False),
        sa.Column("classified_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "operational_priority IN ('urgent','normal','low')", name="ck_classified_priority"
        ),
        schema="processing",
    )
    op.execute(
        "CREATE INDEX ix_classified_event ON processing.classified_news (event_id)"
    )


def downgrade() -> None:
    op.drop_table("classified_news", schema="processing")
    op.drop_table("cluster_result", schema="processing")
    op.drop_table("normalized_news", schema="processing")
    op.execute("DROP SCHEMA IF EXISTS processing")
