# Contract audit - `ai_models_config`

- **Task:** `S00-023` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/ai_models_config.schema.json`
- **Example:** `source/contracts/examples/ai_models_config.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/ai_models_config.schema.json`
- **Producer:** P02 | **Consumers:** P12, P13, P15, P16, P18, P19, P20, P21 | **Owning package:** B01

## Required root fields

- `schema_version`
- `configuration_id`
- `tasks`
- `updated_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `configuration_id`: string
- `tasks`: array
- `updated_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 2/2
- Example top-level keys (4): `configuration_id`, `schema_version`, `tasks`, `updated_at`
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
