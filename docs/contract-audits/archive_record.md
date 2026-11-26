# Contract audit - `archive_record`

- **Task:** `S00-026` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/archive_record.schema.json`
- **Example:** `source/contracts/examples/archive_record.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/archive_record.schema.json`
- **Producer:** P26 | **Consumers:** P08, P17, P19 | **Owning package:** B01

## Required root fields

- `schema_version`
- `archive_id`
- `object_type`
- `object_id`
- `stream`
- `classification`
- `payload_ref`
- `source_refs`
- `retention_policy_id`
- `stored_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `archive_id`: string
- `object_type`: string
- `object_id`: string
- `stream`: enum ['domestic', 'foreign', 'mixed', 'manual']
- `classification`: enum ['public', 'internal', 'restricted', 'executive_private']
- `payload_ref`: string
- `source_refs`: array
- `retention_policy_id`: string
- `stored_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `stream` = ['domestic', 'foreign', 'mixed', 'manual']
- `classification` = ['public', 'internal', 'restricted', 'executive_private']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (10): `archive_id`, `classification`, `object_id`, `object_type`, `payload_ref`, `retention_policy_id`, `schema_version`, `source_refs`, `stored_at`, `stream`
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
