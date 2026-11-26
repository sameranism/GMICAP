# Contract audit - `event_envelope`

## ADR-016 baseline containment correction — 2026-11-26

[ADR-016](../decisions/ADR-016-private-event-containment.md) merged in [PR #68](https://github.com/sameranism/ETEMAD-pre/pull/68) at signed main `1fc80f48ab46500ee8fbb2647223f7e119ea737e`. Its exact-head [backend](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720153275), [contract](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720153339), [CodeQL](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720153351), [bootstrap](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720153317) and [Guardian](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720153084) passed. The correction adds typed executive_private rejection to the existing shared guard, used by both bus and outbox at append and dispatch. The five new test cases cover constructor and raw envelopes, shared dedupe preservation, no persistence or callback, and mutated pending entries. Existing restricted and public/internal behavior and all previous tests remain intact. No frozen contract, grant, storage, queue infrastructure or external service changes. Exact-head CI is required for these new tests; their success is not yet asserted in this entry. No local execution claimed. Dedicated private storage and authenticated transport remain deferred per ADR-015. This correction is not full semantic or privacy acceptance; Gate-00 remains BLOCKED.

## Current automated acceptance evidence — 2026-11-26

Status: PARTIAL / BLOCKED for full semantics. Historical independent-review wording below describes the earlier process; under [ADR-012](../decisions/ADR-012-automated-acceptance.md) an independent or human review is NOT_REQUIRED. Gate-00 evidence is still required.

Baseline: signed protected main [`cd4a109715d591bd021ee8224debb51b007ac0ca`](https://github.com/sameranism/ETEMAD-pre/commit/cd4a109715d591bd021ee8224debb51b007ac0ca). [ADR-013](../decisions/ADR-013-restricted-event-routing.md) was merged in [PR #60](https://github.com/sameranism/ETEMAD-pre/pull/60); the scoped implementation was merged in [PR #61](https://github.com/sameranism/ETEMAD-pre/pull/61) after exact-head `755d5c61cc11981319caa7cdf86c28e8c09cb480` checks passed.

| Check | Result and evidence |
| --- | --- |
| Constructor compatibility and shared route denial | PASS in fixture tests: all four v1.0 classifications; unknown enum/version; raw restricted envelope; no shared delivery, dedupe-key consumption or outbox persistence; mutated pending entry denied before callback; ordinary delivery and deduplication retained. [Backend job](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715867304/job/139561626605) reports 153 passed, 15 warnings, Ruff PASS, Mypy PASS (35 files), PostgreSQL 18.7. |
| Contract validation and preflight | PASS, 62 task preflights (S00-035 target and four attachments), 336 negative contract cases, boundaries PASS, two deliberate boundary violations detected. [PR job](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715867411/job/139561627613); [exact main job](https://github.com/sameranism/ETEMAD-pre/actions/runs/45716200967/job/139562766766). |
| Separate unit job | 152 passed, 1 skipped, 1 warning; PostgreSQL-covered backend job passed. [PR job](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715867411/job/139561627696). |
| Provenance and scanning | [PR Guardian](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715867503), [PR CodeQL](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715867263), [bootstrap](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715867229) and [main provenance](https://github.com/sameranism/ETEMAD-pre/actions/runs/45716200902) passed. Other main-push checks were not yet complete at the evidence capture. |

The schema remains frozen, with Git blob `6cb35988557e365dab5f3f5f299d3a25228a7fb9`; example blob `a6941845157bc6241eafae75490255e285240468`. Neither was changed by PR #61. Pre-edit S00-035 preflight evidence comes from the exact-main contract job above, not a fresh local execution.

### Remaining semantic boundaries

- P29 owns the envelope contract. The fixture P07 handoff in [orchestrator.py](../../backend/core/orchestrator.py) emits internal `news.ingested`; the shared [bus](../../backend/core/events.py) and [outbox](../../backend/core/outbox.py) now deny restricted. This is not authorization for artifact reads, durable delivery or production use.
- The master specification requires private queues and separate service identities. The fixture shared router still lacks classification-aware executive-private authorization. Do not deploy it for executive-private events. A separate owner-authorized correction must establish the approved private boundary and test denied direct/shared delivery and artifact access; ADR-013 specifically did not authorize this policy change.
- The wire/prose mismatch remains: propose a separate ADR treating `event_type` and `occurred_at` as authoritative v1.0 names and retaining stream as trusted internal routing metadata, never an extra wire field. Before deciding, trace source of stream from trusted authoritative records and every cross-stream consumer; do not invent a mapping or alter the frozen schema. If a wire stream field is actually needed, require separately versioned contract and migration approval.
- A fixture in-memory dedupe set is not durable global uniqueness or exactly-once delivery. Handler failure after dedupe reservation, crash recovery, transactional outbox, UTC normalization and consumer artifact-level authorization need separate evidence. No passing security claim is made for these paths.

The restricted constructor/shared-routing discrepancy is resolved within the approved scope; S00-035 full semantic acceptance and Gate-00 remain BLOCKED. No new production, permission, schema, or runtime change is included in this audit. Only this audit document is modified; rollback through a protected revert PR.

- **Task:** `S00-035` (phase 0)
- **Status:** draft — schema/example validation PASS; semantic audit BLOCKED pending architecture ADR and independent signoff (Gate-00)
- **Schema:** `source/contracts/schemas/event_envelope.schema.json`
- **Example:** `source/contracts/examples/event_envelope.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/event_envelope.schema.json`
- **Producer:** P29 | **Consumers:** all packages | **Owning package:** B01

## Required root fields

- `schema_version`
- `event_id`
- `event_type`
- `producer_project`
- `object_id`
- `correlation_id`
- `idempotency_key`
- `classification`
- `occurred_at`
- `payload_ref`

## Field inventory

- `schema_version`: enum ['1.0']
- `event_id`: string
- `event_type`: string
- `producer_project`: string
- `object_id`: string
- `correlation_id`: string
- `idempotency_key`: string
- `classification`: enum ['public', 'internal', 'restricted', 'executive_private']
- `occurred_at`: string (date-time)
- `payload_ref`: string

## Enumerations

- `schema_version` = ['1.0']
- `classification` = ['public', 'internal', 'restricted', 'executive_private']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (10): `classification`, `correlation_id`, `event_id`, `event_type`, `idempotency_key`, `object_id`, `occurred_at`, `payload_ref`, `producer_project`, `schema_version`
- `schema_version` in example: `1.0`

## Semantic checks the schema does NOT enforce

- Uniqueness of ids across records (enforced by storage keys, not JSON Schema).
- Cross-contract joins (for example `normalized_news` -> `cluster_result`) are referential, not validated here.
- Provenance/rights truthfulness: the schema records a value, it cannot prove it is correct.
- Time correctness beyond `format: date-time` (UTC normalisation is producer responsibility).

## Compatibility rules

- v1.0 is frozen: no silent field rename or enum narrowing.
- A required-field or enum change needs a new version, an ADR and producer/consumer tests.
- Consumers must reject unknown `schema_version` and warn with the record id.

## Independent review status (non-normative)

**Status:** BLOCKED on semantic audit / separate ADR decision; schema and example validation are PASS. This is an audit finding, **not** a proposal to silently edit v1.0 wire messages.

- **Authoritative architecture prose:** `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, event/orchestration section, states `event_id, correlation_id, idempotency_key, timestamp UTC, object_id, type, stream, classification, payload_ref`.
- **Frozen wire source:** `source/contracts/schemas/event_envelope.schema.json` requires `event_type` and `occurred_at`, and requires `schema_version`, `producer_project`; it does **not** allow `type`, `timestamp`, or `stream` because `additionalProperties: false`.
- **Consequence:** a producer implementing the prose literally fails Schema v1.0; a consumer expecting prose fields may fail or produce uncorrelated events. `stream` has no wire equivalent and its operational meaning must be clarified separately.
- **Decision required:** approve an ADR clarifying that v1.0 wire format is authoritative (`type` → `event_type`, `timestamp` → `occurred_at`, with UTC normalization by the producer), and explicitly choose whether `stream` is only an internal routing concept or merits a separately versioned new contract. Do not modify the v1.0 schema or producers in this audit task.
- **Owner:** B01/P29. All package consumers require compatibility review. Create an independent ADR/change-request task before changing implementation if any semantic difference is approved.

### Verification evidence (2026-11-23)

- Staging snapshot `/srv/etemad/staging` (no code changes): `python -B tools/validate_contracts.py` → exit 0, 30 schema/example pairs PASS.
- `python -B tools/preflight.py S00-035 --pack .` → exit 0 (target and 4 attachments found). File availability is not semantic acceptance.
- Independent isolated negative tests against disposable copies of `event_envelope.example.json`: remove required `event_type` → validator exit 1; insert invalid classification `DO_NOT_ACCEPT` → exit 1; restore example → exit 0. Source baseline unchanged.
- Tests cannot prove UTC clock truth, global idempotency uniqueness, authorization of `payload_ref`, or absence of private data in referenced objects. These must receive separate producer/consumer and access tests.
- No PostgreSQL/Redis integration, EIC isolation end-to-end, source traffic, production publishing, or production deploy verified in this audit.

**Gate-00 disposition:** S00-035 is NOT PASS while the ADR decision, semantic review, and independent signoff remain open. Safe rollback: close this one-file draft PR; the frozen v1.0 schema and existing runtime remain unchanged.