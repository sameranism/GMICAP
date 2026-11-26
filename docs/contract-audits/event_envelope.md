# Contract audit - `event_envelope`

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