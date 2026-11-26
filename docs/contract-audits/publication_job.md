# Contract audit - `publication_job`

- **Task:** `S00-043` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/publication_job.schema.json`
- **Example:** `source/contracts/examples/publication_job.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/publication_job.schema.json`
- **Producer:** P22 | **Consumers:** P25 | **Owning package:** B08

## Required root fields

- `schema_version`
- `job_id`
- `object_type`
- `object_id`
- `stream`
- `destination_ids`
- `scheduled_at`
- `expires_at`
- `policy_decision_id`
- `idempotency_key`
- `state`
- `created_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `job_id`: string
- `object_type`: enum ['article', 'public_report']
- `object_id`: string
- `stream`: enum ['domestic', 'foreign', 'mixed', 'manual']
- `destination_ids`: array
- `scheduled_at`: string (date-time)
- `expires_at`: 
- `policy_decision_id`: string
- `idempotency_key`: string
- `state`: enum ['scheduled', 'held', 'in_progress', 'completed', 'cancelled']
- `created_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `object_type` = ['article', 'public_report']
- `stream` = ['domestic', 'foreign', 'mixed', 'manual']
- `state` = ['scheduled', 'held', 'in_progress', 'completed', 'cancelled']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (12): `created_at`, `destination_ids`, `expires_at`, `idempotency_key`, `job_id`, `object_id`, `object_type`, `policy_decision_id`, `scheduled_at`, `schema_version`, `state`, `stream`
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
