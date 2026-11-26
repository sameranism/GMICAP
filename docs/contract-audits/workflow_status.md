# Contract audit - `workflow_status`

- **Task:** `S00-051` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/workflow_status.schema.json`
- **Example:** `source/contracts/examples/workflow_status.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/workflow_status.schema.json`
- **Producer:** P29 | **Consumers:** P27, all packages | **Owning package:** B01

## Required root fields

- `schema_version`
- `workflow_id`
- `correlation_id`
- `current_project`
- `state`
- `attempt_count`
- `last_error_code`
- `updated_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `workflow_id`: string
- `correlation_id`: string
- `current_project`: string
- `state`: enum ['new', 'running', 'held', 'completed', 'failed', 'cancelled']
- `attempt_count`: integer
- `last_error_code`: 
- `updated_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `state` = ['new', 'running', 'held', 'completed', 'failed', 'cancelled']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (8): `attempt_count`, `correlation_id`, `current_project`, `last_error_code`, `schema_version`, `state`, `updated_at`, `workflow_id`
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
