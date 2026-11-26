# Contract audit - `analysis_chat_response`

- **Task:** `S00-024` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/analysis_chat_response.schema.json`
- **Example:** `source/contracts/examples/analysis_chat_response.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/analysis_chat_response.schema.json`
- **Producer:** P16 | **Consumers:** P27 | **Owning package:** B06

## Required root fields

- `schema_version`
- `response_id`
- `question_id`
- `answer`
- `citations`
- `uncertainty_notes`
- `classification`
- `created_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `response_id`: string
- `question_id`: string
- `answer`: string
- `citations`: array
- `uncertainty_notes`: array
- `classification`: enum ['public', 'internal', 'restricted', 'executive_private']
- `created_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `classification` = ['public', 'internal', 'restricted', 'executive_private']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 2/2
- Example top-level keys (8): `answer`, `citations`, `classification`, `created_at`, `question_id`, `response_id`, `schema_version`, `uncertainty_notes`
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
