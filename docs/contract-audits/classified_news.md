# Contract audit - `classified_news`

- **Task:** `S00-029` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/classified_news.schema.json`
- **Example:** `source/contracts/examples/classified_news.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/classified_news.schema.json`
- **Producer:** P09 | **Consumers:** P12, P13, P15, P19 | **Owning package:** B04

## Required root fields

- `schema_version`
- `news_id`
- `stream`
- `desks`
- `topics`
- `subject_countries`
- `event_id`
- `operational_priority`
- `rules_version`
- `classified_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `news_id`: string
- `stream`: enum ['domestic', 'foreign', 'mixed', 'manual']
- `desks`: array
- `topics`: array
- `subject_countries`: array
- `event_id`: string
- `operational_priority`: enum ['urgent', 'normal', 'low']
- `rules_version`: string
- `classified_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `stream` = ['domestic', 'foreign', 'mixed', 'manual']
- `operational_priority` = ['urgent', 'normal', 'low']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (10): `classified_at`, `desks`, `event_id`, `news_id`, `operational_priority`, `rules_version`, `schema_version`, `stream`, `subject_countries`, `topics`
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
