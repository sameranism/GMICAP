# Contract audit - `event_envelope`

- **Task:** `S00-035` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
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
