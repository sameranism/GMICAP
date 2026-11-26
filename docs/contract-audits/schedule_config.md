# Contract audit - `schedule_config`

- **Task:** `S00-046` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/schedule_config.schema.json`
- **Example:** `source/contracts/examples/schedule_config.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/schedule_config.schema.json`
- **Producer:** P22 | **Consumers:** P25 | **Owning package:** B08

## Required root fields

- `schema_version`
- `config_id`
- `stream`
- `desk`
- `timezone`
- `mode`
- `fixed_times_local`
- `interval_minutes`
- `enabled`
- `updated_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `config_id`: string
- `stream`: enum ['domestic', 'foreign', 'mixed']
- `desk`: string
- `timezone`: string
- `mode`: enum ['immediate', 'fixed_times', 'interval']
- `fixed_times_local`: array
- `interval_minutes`: 
- `enabled`: boolean
- `updated_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `stream` = ['domestic', 'foreign', 'mixed']
- `mode` = ['immediate', 'fixed_times', 'interval']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (10): `config_id`, `desk`, `enabled`, `fixed_times_local`, `interval_minutes`, `mode`, `schema_version`, `stream`, `timezone`, `updated_at`
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
