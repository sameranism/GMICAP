"""Append processing artifact history without rewriting revision 002.

Revision ID: 003_processing_history
Revises: 002_processing
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "003_processing_history"
down_revision = "002_processing"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_cluster_normalized_news", "cluster_result", "normalized_news",
        ["news_id"], ["news_id"], source_schema="processing", referent_schema="processing",
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_classified_normalized_news", "classified_news", "normalized_news",
        ["news_id"], ["news_id"], source_schema="processing", referent_schema="processing",
        ondelete="RESTRICT",
    )
    op.create_table(
        "artifact_history",
        sa.Column("news_id", sa.String(64), nullable=False),
        sa.Column("revision_no", sa.Integer(), nullable=False),
        sa.Column("artifact_hash", sa.String(64), nullable=False),
        sa.Column("snapshot", postgresql.JSONB(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("news_id", "revision_no", name="pk_processing_history"),
        sa.UniqueConstraint("news_id", "artifact_hash", name="uq_processing_history_hash"),
        sa.ForeignKeyConstraint(
            ["news_id"], ["processing.normalized_news.news_id"],
            name="fk_history_normalized_news", ondelete="RESTRICT",
        ),
        sa.CheckConstraint("revision_no > 0", name="ck_processing_history_revision"),
        sa.CheckConstraint("artifact_hash ~ '^[0-9a-f]{64}$'", name="ck_processing_history_hash"),
        sa.CheckConstraint(
            "jsonb_typeof(snapshot) = 'object' AND "
            "(snapshot ? 'news') AND (snapshot ? 'cluster') AND "
            "(snapshot ? 'classification') AND "
            "(snapshot->'news'->>'news_id') IS NOT DISTINCT FROM news_id AND "
            "(snapshot->'cluster'->>'news_id') IS NOT DISTINCT FROM news_id AND "
            "(snapshot->'classification'->>'news_id') IS NOT DISTINCT FROM news_id",
            name="ck_processing_history_identity",
        ),
        schema="processing",
    )


def downgrade() -> None:
    # Never silently discard recorded provenance during a rollback.
    op.execute("""
        DO $$ BEGIN
            LOCK TABLE processing.artifact_history IN ACCESS EXCLUSIVE MODE;
            IF EXISTS (SELECT 1 FROM processing.artifact_history) THEN
                RAISE EXCEPTION 'processing history is not empty; preserve it before downgrade';
            END IF;
        END $$;
    """)
    op.drop_table("artifact_history", schema="processing")
    op.drop_constraint("fk_classified_normalized_news", "classified_news",
                       schema="processing", type_="foreignkey")
    op.drop_constraint("fk_cluster_normalized_news", "cluster_result",
                       schema="processing", type_="foreignkey")
