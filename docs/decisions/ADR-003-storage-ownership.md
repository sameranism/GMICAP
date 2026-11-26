# ADR-003 — Storage ownership: three PostgreSQL databases, separate queues, scoped object storage

- **Status:** Accepted (proposal-level; not production DDL)
- **Date:** 2026-11-23
- **Task:** S00-010
- **Source:** `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/technical/database_dictionary.csv`,
  `source/technical/postgres_central_schema_PROPOSAL.sql`, `postgres_domestic_schema_PROPOSAL.sql`,
  `postgres_foreign_schema_PROPOSAL.sql`

## Context

The architecture separates central processing from domestic and foreign ingestion. The three
`*.sql` files in `source/technical/` are **proposals** (41 tables total), never executed in production.
Without an ownership decision, packages start reading each other's tables — the failure mode this ADR
exists to prevent.

## Decision

1. **Three logical PostgreSQL databases:** `etemad_central`, `etemad_domestic`, `etemad_foreign`.
   Phase 1 may run all three as separate databases on one server; physical separation is a deployment
   detail, not a schema permission.
2. **Schema ownership is exclusive.** A table has exactly one owning package; other packages read it only
   through a versioned API or an event. No cross-database foreign keys and no cross-database transactions.
3. **Redis is transient only:** per-stream queues and cache, never the system of record.
   Queue payloads reference contract records by id.
4. **Object storage** (S3-compatible) holds raw payloads and media with scoped ACL; the database keeps the
   reference (`source_payload_ref`, archive record), never the bytes.
5. **Migrations:** Alembic revisions per database, append-only, reviewed; `001_baseline` is written from the
   reviewed proposal, not by executing the proposal SQL. Every migration must be reversible and tested on a
   throwaway database.
6. **Unapproved SQL must not run** against any environment. The proposal files stay as evidence and are
   never edited to "make things work".

## Consequences

- Ingest writes to its own database and emits events; the bridge to central is authenticated.
- Archive (P26) stores identifiers and checksums, not copies of other packages' payloads.
- Migration tests for new tables must verify the ownership mapping and database boundary.

## Impacted contracts

`raw_news`, `normalized_news`, `cluster_result`, `classified_news`, `archive_record`, `source_registry`,
`event_envelope`, `workflow_status`.

## Open external dependencies

- Host/VPS and backup policy for three databases.
- Storage provider and sizing for media (audio/video/image).
- Retention policy and deletion semantics for archived material.
