-- ETEMAD architecture v1.1: typed PostgreSQL DDL proposal (development reference)
-- NOT a finalized production migration. Security policies, row access rules, relationships,
-- retention and official editorial policy must be reviewed by DB/security/legal teams.
-- Contract-level IDs are TEXT because v1.0 examples use readable string identifiers.
-- Application secrets and password plaintext must never be written to these tables.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS "foreign";
-- P04 | بازبینی ادمین پیش از افزودن به P03
CREATE TABLE IF NOT EXISTS "foreign".source_candidates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "candidate_id" TEXT,
  "country_code" TEXT,
  "title" TEXT,
  "site_url" TEXT,
  "feed_url" TEXT,
  "verified" BOOLEAN,
  "evidence_uri" TEXT
);
CREATE SCHEMA IF NOT EXISTS "foreign";
-- P06 | UNIQUE(source_id)؛ استقلال صف خارجی
CREATE TABLE IF NOT EXISTS "foreign".poll_state (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "source_id" TEXT,
  "etag" TEXT,
  "last_modified" TEXT,
  "last_success_at" TIMESTAMPTZ,
  "next_poll_at" TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS ix_foreign_poll_state_source_id ON "foreign".poll_state ("source_id");
CREATE SCHEMA IF NOT EXISTS "foreign";
-- P06 | UNIQUE(source_id,source_hash)؛ ارسال فقط از Bridge
CREATE TABLE IF NOT EXISTS "foreign".raw_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "raw_id" TEXT,
  "source_id" TEXT,
  "country_code" TEXT,
  "source_url" TEXT,
  "fetched_at" TIMESTAMPTZ,
  "content_ref" TEXT,
  "source_hash" TEXT
);
CREATE INDEX IF NOT EXISTS ix_foreign_raw_items_source_id ON "foreign".raw_items ("source_id");
