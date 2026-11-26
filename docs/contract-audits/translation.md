# Contract audit - `translation`

- **Task:** `S00-048` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/translation.schema.json`
- **Example:** `source/contracts/examples/translation.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/translation.schema.json`
- **Producer:** P12 | **Consumers:** P13, P15 | **Owning package:** B05

## Required root fields

- `schema_version`
- `translation_id`
- `news_id`
- `source_language`
- `target_language`
- `translated_text`
- `source_text_ref`
- `glossary_version`
- `model_id`
- `warnings`
- `created_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `translation_id`: string
- `news_id`: string
- `source_language`: string
- `target_language`: string
- `translated_text`: string
- `source_text_ref`: string
- `glossary_version`: string
- `model_id`: string
- `warnings`: array
- `created_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (11): `created_at`, `glossary_version`, `model_id`, `news_id`, `schema_version`, `source_language`, `source_text_ref`, `target_language`, `translated_text`, `translation_id`, `warnings`
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
