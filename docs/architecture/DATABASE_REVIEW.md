# ETEMAD database proposal review — S00-016

**Status: REVIEWED AS PROPOSALS / BLOCKED FOR REAL MIGRATIONS.** This is an architecture review, not migration approval or a live PostgreSQL test.

## Inputs

- `source/technical/database_dictionary.csv` — **41** proposed table ownership records
- `source/technical/postgres_central_schema_PROPOSAL.sql` — **35** proposed central tables
- `source/technical/postgres_domestic_schema_PROPOSAL.sql` — **3** proposed domestic tables
- `source/technical/postgres_foreign_schema_PROPOSAL.sql` — **3** proposed foreign tables
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, the package/project map, dependency edges, `AGENTS.md` and frozen contracts.

## Verified structural observations from the SQL proposals

1. Three environments are represented by separate SQL draft files, matching the 35 + 3 + 3 = **41** proposed tables. **They were not executed on PostgreSQL.**
2. Central draft contains explicit `TODO SECURITY` for `executive.private_reports` RLS, separate database role and object bucket. There are **no implemented `CREATE POLICY` / `ENABLE ROW LEVEL SECURITY` statements** in the inspected central draft. Thus private report segregation is not enforceable by applying this draft.
3. Central draft similarly leaves role-specific `GRANT` and package isolation in `TODO MIGRATION`; no implemented owner-specific grant policy is present.
4. The draft calls out the 10-user active-human limit, initial-password reset and Argon2id hashing as TODOs, not enforced database behavior.
5. Many business columns are nullable in the draft (for instance `control.output_switches.enabled` and `identity.users.is_active`), whereas the desired workflows require explicit state and authorization rules. Constraints must be reviewed per table rather than relying on model/API-level validation only.
6. Several uniqueness constraints are present as optional hardening indexes, but the design comments refer to additional uniqueness and immutability rules. Verify every documented business key, nullable-key behavior and repeat-event idempotency before accepting a migration.
7. **Ownership collision to resolve:** `control.editorial_rules` is documented under `P02/P10`, even though a table has a single write owner. Define one owner/authorized API and a separate `editorial.rulesets` responsibility without silent cross-package writes.
8. The sample drafts include `CREATE EXTENSION IF NOT EXISTS pgcrypto` and object creation. They are **never** suitable as an automatic production apply script without privilege, dependency, migration, rollback and recovery review.

## Required migration plan (proposal, not executed)

1. Inventory table contracts and field types with owners P01–P29. Resolve the `P02/P10` ownership overlap and document all cross-package APIs.
2. Create reversible per-environment, per-owner migrations, with explicit grants, revokes, unique/not-null/check/FK constraints, indexing, immutability and per-table retention policy. Separate migrations for domestic, foreign and central.
3. Establish private-report isolation via approved dedicated DB role or isolated database, RLS/GRANT policy, separate object store scope and denied public retrieval/queue routes, with negative tests. Do not rely on hidden UI controls.
4. Implement output switches with an explicit deny-safe default and checks immediately before every external side effect. Use transactional idempotency for outbox/jobs and cap active users under concurrent requests.
5. Run migrations only in an isolated disposable PostgreSQL test environment, then test rollback, duplicate data, cross-role denials, crash-restart, backups/restoration and reconciliation.
6. Require independent security, database and editorial signoff for production migration. No VPS use during S00.

## Gate decision for this task

**PARTIAL.** Inventory and concrete risk findings are recorded. Production-migration readiness is **BLOCKED** by absent RLS/grants, insufficient reviewed constraints, ownership ambiguity, and unrun database tests. S00-016 is not authorization to apply DDL. Gate-00 requires independent review.

## Rollback

Close the document-only PR; no source DDL, schema, production data or application files were changed.
