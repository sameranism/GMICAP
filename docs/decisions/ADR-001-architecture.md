# ADR-001 — Architecture and ownership boundaries

- **Status:** Proposed for independent S00 review (not yet accepted)
- **Scope:** ETEMAD S00-008 / P01
- **Baseline:** `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/technical/project_package_map.csv`, `source/technical/dependency_edges.csv`, `source/technical/database_dictionary.csv`, baseline contract schemas and examples
- **Decision authority:** Owner-approved master v1.1; this ADR documents and operationalizes those constraints without changing them.

## Context

ETEMAD uses six conceptual layers and nine delivery packages across 29 stable projects. The layers are domestic monitoring, foreign monitoring, content processing, intelligence and reporting, studio and publishing, and central platform. A package is a delivery/ownership boundary, not necessarily a separate server. Implementing one server or service for every package would introduce operational complexity not required by the baseline.

## Proposed decision

1. Keep identifiers **B01–B09** and **P01–P29** stable, with responsibilities and dependencies defined in the baseline project map. B01 owns core data contracts/configuration/source registry/identity/archive/orchestration; B02 domestic ingest; B03 foreign discovery and ingest; B04 normalization/dedup/routing; B05 editorial policy/translation/article/media; B06 analysis/chat/metrics/reports; B07 audio/video; B08 destination scheduling/formatting/sending; B09 Persian RTL interface.
2. Maintain three **separate environments**, databases and queues: domestic ingest (`etemad_domestic`), foreign ingest (`etemad_foreign`), and central core (`etemad_core`). The central PostgreSQL uses package-owned schemas, not shared ORM writes. Foreign-to-central transfer uses an authenticated, auditable bridge. No direct inter-package database reads or writes; use explicit versioned APIs and events.
3. Use PostgreSQL as authoritative state, Redis for queues/cache and scoped S3-compatible object storage for large artifacts. Events carry references rather than confidential payloads; follow frozen JSON Schema Draft 2020-12 v1.0 including correlation and idempotency.
4. Keep the central application modular rather than introducing gratuitous microservices or Kubernetes. Independent workers/adapters may be deployed behind explicit service boundaries as specified. The baseline does **not** authorize collapsing domestic and foreign databases into the core.
5. Preserve backend-enforced RBAC, the ten-active-human-user limit, separately protected `executive_private` reports for editor-in-chief only, independent `public_analysis`, `studio` and `publishing` output controls, one canonical AI output and destination-local formatting.
6. Until implementation gates pass, develop with mocks and synthetic fixtures. No production publication, real CMS integration, unverified third-party API or VPS deployment.

## Consequences

- Positive: ownership and trust boundaries are explicit; modular core minimizes deployment complexity while preserving isolation.
- Cost: three data/queue environments and authenticated transfer require operational testing; queue and private-report ACLs are nontrivial.
- Open items: exact infrastructure sizing and high availability, secret manager, private report isolation design, CMS API, official publishing APIs, legal review and recovery targets must be resolved in their owning tasks. This ADR does not approve those integrations.

## Verification and change control

Validate repository layout against the P/B mapping, dependencies and each contract; verify forbidden cross-database access, private-report leakage and switch behavior before integration. Any changed ownership, edge or wire schema needs a separate scoped ADR/contract migration and consumer tests. Independent Gate-00 review determines acceptance. **This is documentation, not proof of implemented services.**

## Rollback

Reject or revert this ADR before merge; preserve the original master specification and schemas unchanged.
