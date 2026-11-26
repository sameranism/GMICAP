# Build status — ETEMAD

**Updated:** 2026-11-23 (phase 0 complete, phase 1 code-complete, Gate-01 review pending)
**Snapshot base:** `main @ 8e51c9c` (the only code available in this environment)

Every line below is backed by a command that was actually run. Anything not run says
`NOT_RUN` together with the reason.

## Verified green

| Check | Command | Result |
|---|---|---|
| Contract layer | `python tools/validate_contracts.py` | `schemas: 30  examples: 30` then `CONTRACT-CHECK: PASS` |
| Backend tests | `python -m pytest -q backend/tests` | **106 passed** |
| Migration round trip | `python3 -m alembic upgrade head` / `downgrade base` on PostgreSQL 18.6 | central: 8 tables (control/identity/audit/processing) at `002_processing`, downgrade to `001_baseline` removes `processing`; domestic: 2 tables at `001_ingest`, downgrade removes them, re-upgrade restores |
| Package boundaries | `python tools/check_boundaries.py` | `BOUNDARIES: PASS` |
| Boundary self-test | `python tools/check_boundaries.py --self-test` | `SELF-TEST: PASS (2 violations detected in fixtures)` |
| Preflight (task known) | `python tools/preflight.py S02-001 --pack <pack>` | `PASS ... attachments=8` |
| Preflight (no pack) | `python tools/preflight.py S02-001` | `BLOCKED` (exit 2) |
| Frontend build | `npm run build` (frontend/) | `built in ~4s`, exit 0 |

## Phase 0 — done (62/62 tasks)

- 30 JSON Schema v1.0 + 30 examples in `source/contracts/`.
- `AGENTS.md`, six `.cursor/rules/*.mdc`, six ADRs (`docs/decisions/`).
- `docs/architecture/SYSTEM_MAP.md` (29 projects, 44 edges, no invented edge).
- `docs/architecture/CONTRACT_OWNERSHIP.md` (30 contracts mapped; open items listed).
- `docs/architecture/DATABASE_REVIEW.md` (41 proposed tables reviewed; no DDL executed).
- `docs/contract-audits/*.md` (30 audits, task `S00-022`..`S00-051`).
- `tools/validate_contracts.py`, `tools/preflight.py`, `tools/check_boundaries.py`,
  `.github/workflows/contract-check.yml`.
- Hygiene: `.gitignore`, `.editorconfig`, `.github/CODEOWNERS` (placeholder teams), `README.md`.
- Frontend config: `components.json`, `eslint.config.js`, `playwright.config.ts`, `@` path alias
  (tsconfig + vite).

Contract audits are **draft until the applicable Gate-00 semantic and security checks pass**; they were generated from
the frozen schemas, not hand-waved.

## Phase 1 — code complete (30/30 targets present)

`backend/core/`: `contracts`, `settings_service` (+`get_latest`), `output_switches`, `sources_service`,
`auth`, `permissions` (+`InMemoryGrantStore`), `audit`, `secrets`, `archive`, `events`, `jobs`, `outbox`,
`orchestrator`, `ai_gateway`, `db`, `object_store`, `errors`, `health`, `observability`.

`backend/app/`: `main` (single error-handler installation), `dependencies`, `api_router` (`/v1`),
`demo_news` (local-only, behind two env flags).

`backend/migrations/`: `alembic.ini`, `env.py`, `central/001_baseline.py`.
`backend/tests/`: `conftest`, `test_contracts`, `test_security`, `test_orchestration`, `test_ai_gateway`,
`test_api` (66 tests).

### Behavioural evidence from tests

- `output_controls` revision is accepted through `SettingsService` (the previously broken path).
- Default output switches are **all off**; publishing is held while off and allowed when on.
- Private reports are denied for `owner` and `staff`; `editor_in_chief` needs an explicit grant.
- 401 / 403 / 409 / 413 semantics are exercised; one error envelope with a correlation id.
- Archive keys and object-store keys reject traversal; audit redacts secrets; AI gateway is off by
  default and blocks on budget.

## NOT_RUN (explicit reasons)

| Item | Status | Reason |
|---|---|---|
| Database-backed stores (settings, grants, queue, outbox, archive) | NOT_IMPLEMENTED | phase 1 ships fixture stores; the migration now runs, DB wiring is the next step |
| Frontend ESLint | NOT_RUN | devDependencies (`eslint`, `typescript-eslint`, `eslint-plugin-react-hooks`) not installed |
| Playwright E2E | NOT_RUN | `@playwright/test` and browsers not installed |
| Real source ingestion | NOT_RUN | no client-approved domestic source list yet; fixture transport is the default |
| Real publishing / CMS / AI calls | BLOCKED | no authorization, no CMS, no keys (by design) |
| Gate-00 / Gate-01 automated acceptance | PENDING | requires evidence for the applicable automated acceptance checks |

## Migration evidence (executed, not asserted)

PostgreSQL 18.6 was started in the local WSL distribution (`etemad_central`, role `etemad`), purely as a
throwaway verification target. The migration ran online through Alembic, not by pasting SQL:

```
upgrade head   -> 001_baseline (head); tables: audit.audit_entries, control.config_revisions,
                  control.output_switches, identity.grants, identity.users
downgrade base -> 0 tables and 0 schemas remain
upgrade head   -> 5 tables again, version 001_baseline
```

`alembic.ini` now pins `version_locations = %(here)s/migrations/central`; without that line Alembic
silently generated an empty migration (a real bug caught by the round trip).

## Phase 2 — backend vertical slice working (in progress)

Domestic ingest to newsroom feed now runs on real contract records, with a fixture feed and no network.
Module names now match the task pack exactly (no parallel naming):

- `backend/modules/domestic/`: `feed_client` (S02-001), `collector` (S02-002), `scheduler` (S02-003),
  `repository` (S02-004), `api` (S02-005). Migration `migrations/domestic/001_ingest.py` (S02-006) and
  tests `tests/test_domestic.py` (S02-007).
- `backend/modules/processing/`: `extractor` (S03-001), `normalizer` (S03-002), `deduplicator` (S03-003),
  `classifier` (S03-004), `router` (S03-005), `repository` (S03-006). Migration
  `migrations/central/002_processing.py` (S03-007) and tests `tests/test_processing.py` (S03-008).
- `backend/app/pipeline.py` wires P05 -> P07 -> P08 -> P09 without module-to-module imports.
- API: `GET /v1/news`, `GET /v1/news/{id}`, `POST /v1/ingest/{source_id}/poll`,
  `GET /v1/ingest/{source_id}/poll-state` (auth + per-resource grant).

`alembic.ini` selects the central chain; `alembic_domestic.ini` selects the domestic chain through the
`etemad_role` option, and `migrations/env.py` reads the matching `ETEMAD_DB_*_URL`.

Still open in phase 2: replace the demo frontend route with `/v1/news` once a login screen exists, and
add foreign ingest (S02-008..015) and the design-system tasks (S02-016..020).

## Known deviations from the pack snapshot

1. `S01-004` (`backend/core/output_switches.py`) was marked `present_in_main` in `docs/CODE_TARGETS.csv`
   but the file did not exist in the available code. It is now implemented.
2. `SettingsService` had no read method, so no route could read a revision. `get_latest()` was added
   (additive, no behaviour change to `update`).
3. `SettingsService.get_latest` is used by the API and by the output-switch provider; it fails closed
   to all-off when a stored `output_controls` record is invalid.

## Next (phase 2 — vertical slice)

`S02-001 .. S02-007` (domestic ingest with a fixture feed) and `S03-001 .. S03-008`
(normalisation, dedupe, classification), then replace `/v1/demo/news` with the real route and
generate the frontend type from `normalized_news.schema.json`.
