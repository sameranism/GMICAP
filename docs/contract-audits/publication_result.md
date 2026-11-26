# Contract audit - `publication_result`

- **Task:** `S00-044` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/publication_result.schema.json`
- **Example:** `source/contracts/examples/publication_result.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/publication_result.schema.json`
- **Producer:** P25 | **Consumers:** P27, P26 | **Owning package:** B08

## Required root fields

- `schema_version`
- `job_id`
- `object_id`
- `deliveries`
- `completed_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `job_id`: string
- `object_id`: string
- `deliveries`: array
- `completed_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `deliveries[].status` = ['success', 'failed', 'unknown', 'skipped']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 2/2
- Example top-level keys (5): `completed_at`, `deliveries`, `job_id`, `object_id`, `schema_version`
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
