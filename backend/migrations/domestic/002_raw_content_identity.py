"""Preserve domestic source URLs while recording unique source/content identities.

Revision ID: 002_raw_content_identity
Revises: 001_ingest
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "002_raw_content_identity"
down_revision = "001_ingest"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "raw_content_identity",
        sa.Column("source_id", sa.String(64), nullable=False),
        sa.Column("source_hash", sa.String(64), nullable=False),
        sa.PrimaryKeyConstraint("source_id", "source_hash", name="pk_raw_content_identity"),
        sa.CheckConstraint("source_hash ~ '^[0-9a-f]{64}$'", name="ck_raw_content_hash"),
        schema="domestic",
    )
    op.add_column(
        "raw_news", sa.Column("source_hash", sa.String(64), nullable=True), schema="domestic"
    )
    op.execute("""
        UPDATE domestic.raw_news
        SET source_hash = encode(sha256(convert_to(
            jsonb_build_array(language, original_title, original_text)::text, 'UTF8'
        )), 'hex')
    """)
    op.execute("""
        INSERT INTO domestic.raw_content_identity (source_id, source_hash)
        SELECT DISTINCT source_id, source_hash FROM domestic.raw_news
    """)
    op.alter_column("raw_news", "source_hash", nullable=False, schema="domestic")
    op.create_foreign_key(
        "fk_raw_news_content_identity", "raw_news", "raw_content_identity",
        ["source_id", "source_hash"], ["source_id", "source_hash"],
        source_schema="domestic", referent_schema="domestic", ondelete="RESTRICT",
    )
    op.create_check_constraint(
        "ck_raw_news_source_hash", "raw_news",
        "source_hash = encode(sha256(convert_to("
        "jsonb_build_array(language, original_title, original_text)::text, 'UTF8')), 'hex')",
        schema="domestic",
    )
    op.create_index("ix_raw_news_content_identity", "raw_news",
                    ["source_id", "source_hash"], schema="domestic")


def downgrade() -> None:
    # Only derived identity data is removed; immutable raw records are untouched.
    op.drop_index("ix_raw_news_content_identity", table_name="raw_news", schema="domestic")
    op.drop_constraint("ck_raw_news_source_hash", "raw_news", schema="domestic",
                       type_="check")
    op.drop_constraint("fk_raw_news_content_identity", "raw_news", schema="domestic",
                       type_="foreignkey")
    op.drop_column("raw_news", "source_hash", schema="domestic")
    op.drop_table("raw_content_identity", schema="domestic")
