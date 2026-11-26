# ADR-003 — Storage ownership and environment isolation

**Status:** Proposed; requires independent S00 acceptance. **Task:** S00-010.

## Sources
`source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/technical/database_dictionary.csv`, `source/technical/project_package_map.csv`, `source/technical/dependency_edges.csv`, `AGENTS.md`, and the frozen v1.0 contracts.

## Decision
- Preserve three independent PostgreSQL deployment boundaries: `etemad_domestic` for B02 ingestion, `etemad_foreign` for B03 discovery/ingestion, and `etemad_core` for all central package-owned schemas. Keep ingestion queues independently isolated; Redis is transient cache/queue infrastructure and **never authoritative news storage**.
- At the center, use database schema/role ownership according to the baseline dictionary: B01 identity/control/sources/archive/orchestration/security, B04 processing, B05 editorial, B06 insights and restricted executive scope, B07 studio, B08 publish, B09 ui. Strictly prohibit cross-package write access and direct cross-package table reads. Use authenticated versioned APIs or events.
- An authenticated bridge sends foreign events into central processing; no foreign service gets central DB credentials. Preserve idempotency, correlation, source attribution, immutable original material, UTC time and access-scoped payload references.
- Large media and generated artifacts belong to S3-compatible object storage with scoped ACL and retention policy, not database blobs or publicly accessible buckets. `executive_private` reports require separate database roles and storage/queue/retrieval enforcement; evaluate physically separate private storage before production.
- Baseline table listings and SQL proposals are **design proposals, not approved DDL**. Never run source SQL directly against production. Migrations and RLS/GRANT policies must be reviewed in their owning tasks, including rollback, data migration and tests.

## Consequences and unresolved
The three environments add operational complexity but enforce trust and load isolation. Credentials, backup, secret store, RPO/RTO, HA, data retention and final private storage segregation remain open. No VPS deployment or external API is authorized by this ADR.

## Verification
Later tests must prove package-level grant denial, authenticated foreign bridge, idempotency, retention and leakage prevention. Independent Gate-00 review must check this ADR. **A proposed ADR is not an implemented database.**

## Rollback
Close the draft PR without merging; preserve baseline schema files unchanged.
