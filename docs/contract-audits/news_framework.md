# Contract audit - `news_framework`

- **Task:** `S00-038` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/news_framework.schema.json`
- **Example:** `source/contracts/examples/news_framework.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/news_framework.schema.json`
- **Producer:** P10 | **Consumers:** P12, P13 | **Owning package:** B05

## Required root fields

- `schema_version`
- `framework_id`
- `desk`
- `stream`
- `headline_max_chars`
- `summary_max_chars`
- `required_sections`
- `attribution_required`
- `updated_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `framework_id`: string
- `desk`: string
- `stream`: enum ['domestic', 'foreign', 'mixed', 'manual']
- `headline_max_chars`: integer
- `summary_max_chars`: integer
- `required_sections`: array
- `attribution_required`: boolean
- `updated_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `stream` = ['domestic', 'foreign', 'mixed', 'manual']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (9): `attribution_required`, `desk`, `framework_id`, `headline_max_chars`, `required_sections`, `schema_version`, `stream`, `summary_max_chars`, `updated_at`
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
