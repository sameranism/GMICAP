"""central 001 baseline - reviewed subset of the proposal (S01-018).

Scope: control (settings revisions, output switches), identity (users, grants),
audit. Media payloads live in object storage; other packages own their tables.

Status: NOT_RUN against PostgreSQL in this environment. Run forward and back on
a throwaway database, record the log, and only then promote.

Revision ID: 001_baseline
Revises:
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS control")
    op.execute("CREATE SCHEMA IF NOT EXISTS identity")
    op.execute("CREATE SCHEMA IF NOT EXISTS audit")

    op.create_table(
        "config_revisions",
        sa.Column("config_id", sa.String(64), primary_key=True),
        sa.Column("version_no", sa.Integer(), primary_key=True),
        sa.Column("scope", sa.String(32), primary_key=True),
        sa.Column("contract_name", sa.String(64), nullable=False),
        sa.Column("value_json", sa.JSON(), nullable=False),
        sa.Column("changed_by", sa.String(64), nullable=False),
        sa.Column("effective_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("config_id", "version_no", "scope", name="uq_config_revision"),
        schema="control",
    )
    op.execute(
        "CREATE INDEX ix_config_revisions_contract ON control.config_revisions (contract_name, scope)"
    )

    op.create_table(
        "output_switches",
        sa.Column("switch_key", sa.String(32), primary_key=True),
        sa.Column("scope", sa.String(32), primary_key=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("updated_by", sa.String(64), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        schema="control",
    )

    op.create_table(
        "users",
        sa.Column("user_id", sa.String(64), primary_key=True),
        sa.Column("username", sa.String(64), nullable=False, unique=True),
        sa.Column("role_id", sa.String(32), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("must_reset", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "role_id IN ('owner', 'editor_in_chief', 'staff')", name="ck_users_role"
        ),
        schema="identity",
    )

    op.create_table(
        "grants",
        sa.Column("grant_id", sa.String(64), primary_key=True),
        sa.Column("principal_id", sa.String(64), nullable=False),
        sa.Column("role", sa.String(32), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", sa.String(128), nullable=False),
        sa.Column("action", sa.String(32), nullable=False),
        sa.Column("granted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint(
            "principal_id", "role", "resource_type", "resource_id", "action",
            name="uq_grant_scope",
        ),
        schema="identity",
    )

    op.create_table(
        "audit_entries",
        sa.Column("audit_id", sa.String(64), primary_key=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor_id", sa.String(64), nullable=False),
        sa.Column("actor_role", sa.String(32), nullable=False),
        sa.Column("action", sa.String(64), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", sa.String(128), nullable=False),
        sa.Column("decision", sa.String(32), nullable=False),
        sa.Column("correlation_id", sa.String(128), nullable=False),
        sa.Column("details_json", sa.JSON(), nullable=False),
        schema="audit",
    )
    op.execute(
        "CREATE INDEX ix_audit_actor_time ON audit.audit_entries (actor_id, occurred_at)"
    )


def downgrade() -> None:
    op.drop_table("audit_entries", schema="audit")
    op.drop_table("grants", schema="identity")
    op.drop_table("users", schema="identity")
    op.drop_table("output_switches", schema="control")
    op.drop_table("config_revisions", schema="control")
    op.execute("DROP SCHEMA IF EXISTS audit")
    op.execute("DROP SCHEMA IF EXISTS identity")
    op.execute("DROP SCHEMA IF EXISTS control")
