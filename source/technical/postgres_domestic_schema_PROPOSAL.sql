-- ETEMAD architecture v1.1: typed PostgreSQL DDL proposal (development reference)
-- NOT a finalized production migration. Security policies, row access rules, relationships,
-- retention and official editorial policy must be reviewed by DB/security/legal teams.
-- Contract-level IDs are TEXT because v1.0 examples use readable string identifiers.
-- Application secrets and password plaintext must never be written to these tables.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS domestic;
-- P05 | نسخه local snapshot از P03
CREATE TABLE IF NOT EXISTS domestic.sources_snapshot (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "source_id" TEXT,
  "version" INTEGER,
  "url" TEXT,
  "mode" TEXT,
  "poll_interval_s" INTEGER,
  "enabled" BOOLEAN
);
CREATE INDEX IF NOT EXISTS ix_domestic_sources_snapshot_source_id ON domestic.sources_snapshot ("source_id");
CREATE SCHEMA IF NOT EXISTS domestic;
-- P05 | UNIQUE(source_id)؛ conditional HTTP GET
CREATE TABLE IF NOT EXISTS domestic.poll_state (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "source_id" TEXT,
  "etag" TEXT,
  "last_modified" TEXT,
  "last_success_at" TIMESTAMPTZ,
  "next_poll_at" TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS ix_domestic_poll_state_source_id ON domestic.poll_state ("source_id");
CREATE SCHEMA IF NOT EXISTS domestic;
-- P05 | UNIQUE(source_id,source_hash)؛ متن مجاز در ذخیره‌ساز محلی
CREATE TABLE IF NOT EXISTS domestic.raw_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "raw_id" TEXT,
  "source_id" TEXT,
  "source_url" TEXT,
  "fetched_at" TIMESTAMPTZ,
  "content_ref" TEXT,
  "source_hash" TEXT,
  "state" TEXT
);
CREATE INDEX IF NOT EXISTS ix_domestic_raw_items_source_id ON domestic.raw_items ("source_id");
