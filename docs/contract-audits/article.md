# Contract audit - `article`

- **Task:** `S00-027` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/article.schema.json`
- **Example:** `source/contracts/examples/article.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/article.schema.json`
- **Producer:** P13 | **Consumers:** P11, P18, P21, P24 | **Owning package:** B05

## Required root fields

- `schema_version`
- `article_id`
- `news_id`
- `stream`
- `desk`
- `title`
- `lead`
- `body`
- `short_summary`
- `source_refs`
- `framework_version`
- `editorial_rules_version`
- `status`
- `created_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `article_id`: string
- `news_id`: string
- `stream`: enum ['domestic', 'foreign', 'mixed', 'manual']
- `desk`: string
- `title`: string
- `lead`: string
- `body`: string
- `short_summary`: string
- `source_refs`: array
- `framework_version`: string
- `editorial_rules_version`: string
- `status`: enum ['draft', 'ready_for_policy', 'held']
- `created_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `stream` = ['domestic', 'foreign', 'mixed', 'manual']
- `status` = ['draft', 'ready_for_policy', 'held']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (14): `article_id`, `body`, `created_at`, `desk`, `editorial_rules_version`, `framework_version`, `lead`, `news_id`, `schema_version`, `short_summary`, `source_refs`, `status`, `stream`, `title`
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
