# ADR-001 — Architecture, package boundaries and identifiers

- **Status:** Accepted (phase 0 baseline)
- **Date:** 2026-11-23
- **Task:** S00-008
- **Supersedes:** none
- **Source:** `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/technical/project_package_map.csv`, `source/technical/dependency_edges.csv`

## Context

ETEMAD is an intelligent newsroom for a Persian daily: domestic and foreign monitoring, news processing,
editorial work, political analysis, audio/video studio, multi-channel publishing, and a role-based dashboard.
The client requires a non-destructive, incrementally verifiable build: no big-bang integration, no real
publication, and no external API use before official authorization.

## Decision

1. **Six conceptual layers**, kept in code as import boundaries:
   `contracts -> core -> ingest -> processing -> editorial/intelligence -> publish/ui`.
2. **Nine development packages** B01..B09 and **29 project IDs** P01..P29 are stable identifiers.
   They may not be renamed, merged, or renumbered without a new ADR.
3. **Modular monolith for the central core** (B01): one deployable API, internally separated modules.
   Domestic ingest (B02) and foreign ingest (B03) are *separate deployments* with separate PostgreSQL
   databases and Redis queues; the foreign-to-central bridge is authenticated HTTPS, not shared DB access.
4. **All cross-package traffic** uses versioned JSON contracts (API or events). Direct cross-package
   database reads/writes, ORM sharing, and imports of another package's internals are forbidden.
5. **PostgreSQL is authoritative**, Redis is transient queue/cache, S3-compatible storage holds
   large media with scoped ACL. Original source payloads are preserved and never mutated.
6. **Time is UTC** in storage and transport; `source_country` and `subject_countries` are distinct fields;
   every record carries provenance and, where applicable, `correlation_id`.

## Consequences

- A task may touch only its declared `TARGET`; a boundary change needs a separate ADR and task.
- Package isolation is enforced by `tools/check_boundaries.py` and review, not by convention alone.
- Local development can run the core alone with fixture adapters; ingest runs with mocks.

## Impacted contracts

`event_envelope`, `workflow_status`, `raw_news`, `normalized_news`, `cluster_result`, `classified_news`,
`archive_record`, `source_registry`.

## Open external dependencies

- VPS topology and network policy for the three databases (owner decision).
- Whether foreign ingest runs on the same host or a separate one (sanctions/proxy constraints).

## Unchanged

`source/contracts/**` and `source/technical/*.sql` remain read-only evidence in this phase.
