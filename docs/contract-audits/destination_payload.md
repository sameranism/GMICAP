# Contract audit - `destination_payload`

- **Task:** `S00-033` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/destination_payload.schema.json`
- **Example:** `source/contracts/examples/destination_payload.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/destination_payload.schema.json`
- **Producer:** P24 | **Consumers:** P25 | **Owning package:** B08

## Required root fields

- `schema_version`
- `payload_id`
- `job_id`
- `destination_id`
- `content_type`
- `text`
- `asset_uris`
- `source_refs`
- `prepared_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `payload_id`: string
- `job_id`: string
- `destination_id`: string
- `content_type`: enum ['text', 'image', 'audio', 'video']
- `text`: 
- `asset_uris`: array
- `source_refs`: array
- `prepared_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `content_type` = ['text', 'image', 'audio', 'video']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (9): `asset_uris`, `content_type`, `destination_id`, `job_id`, `payload_id`, `prepared_at`, `schema_version`, `source_refs`, `text`
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
