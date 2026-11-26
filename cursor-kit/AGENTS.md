# ETEMAD — Persistent instructions for all coding agents

## Scope and precedence
- Read `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, package spec, source contracts, and current task prompt before editing. Requirements in the source are baseline, with the **later approved UI stack** specified in `docs/decisions/ADR-002-ui-design-system.md` (when accepted): React+TypeScript+shadcn/ui+Tailwind v4 and Etemad Editorial Design System, not Mantine.
- Task prompt identifies the allowed files. Do not edit other files or contracts; if impossible, report the exact blocker and request a separate task/ADR.
- This repo uses 6 conceptual layers, 9 packages B01..B09, 29 projects P01..P29; IDs do not change.

## Routine development and Gate control
- Follow the repository root `AGENTS.md` and `docs/decisions/ADR-011-single-owner-development.md`. Routine fixture-only tasks use scoped PRs and actual successful checks without mandatory human approval; sensitive changes retain explicit authorization and independent review. Gate and release evidence requirements remain unchanged. Never push directly to main or force-push.

## Non-destructive modular development
- Prefer a small stable core and independently testable feature modules with minimal dependencies.
- Versioned JSON Schema Draft 2020-12 v1.0 is the data contract. Never silently change a required field/enum/semantics; preserve old examples.
- Cross-package traffic must be via explicit authorized API/events, not direct DB reads/writes, ORM sharing, or imports of private internals.
- Domestic ingest, foreign ingest, and central processing have independent deployment/DB/queues; foreign-to-central bridge is authenticated. PostgreSQL is authoritative, Redis is transient queue/cache, S3-compatible storage holds large media with scoped ACL.
- Preserve originals, provenance, UTC times, source_country vs subject_countries, idempotency and event correlation. Single AI output -> per-destination adapters. No reprocessing without clear need.

## Security and editorial gates
- Backend-enforced RBAC; no more than 10 active human users; distinct owner, editor-in-chief and staff; individual randomly generated first-use credentials with mandatory reset; no default/shared password. Privileged MFA and audit are required for staging/production.
- Three EIC reports are `executive_private` and cannot reach the public publishing queue/API/adapter/object storage; enforce at backend, DB/queue and retrieval levels. The owner's role is not assumed to have access without explicit authorization change.
- Output controls `public_analysis`, `studio` (audio/video), `publishing` (domestic/foreign/public_reports) must be checked in the backend before a side effect. Turning output off must not stop ingestion/archive/private EIC reports. Held jobs revalidated on resume; no massive backfill.
- No real publishing, credentials, external model calls, payments or deployments without explicit authorization. All provider/channel adapters dry-run/mock by default and only official, verified APIs. Unknown CMS remains an adapter contract only.
- Content must be evidence-based, credited, rights-aware, and neutral in descriptive analysis; human legal/editorial signoff required for Iranian publishing compliance. Never modify originals or quotations, invent quotes or claim legal compliance without review.
- A synthetic studio presenter must be disclosed as AI-generated, with cleared media/voice rights.
- Never commit secrets, private source materials, credentials, tokens or user passwords. Use credential_ref and vault interface.

## Verification and reporting
- Inspect existing files before editing, preserve working behavior, and avoid unrelated refactors.
- Run relevant tests when environment supports them. Never claim a test, build, API call, deploy, or review occurred unless it did.
- In every completion report include changed files, command + real exit status, relevant evidence, remaining gaps and rollback notes.
- If no official brand assets, current CMS, valid API, or legal rules are available, implement a safe placeholder and mark the integration BLOCKED; never fabricate.
