# Contract audit - `raw_news`

- **Task:** `S00-045` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/raw_news.schema.json`
- **Example:** `source/contracts/examples/raw_news.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/raw_news.schema.json`
- **Producer:** P05, P06 | **Consumers:** P07 | **Owning package:** B02, B03

## Required root fields

- `schema_version`
- `news_id`
- `stream`
- `source_id`
- `original_url`
- `original_title`
- `original_text`
- `language`
- `subject_countries`
- `collected_at`
- `content_scope`
- `reuse_permission`

## Field inventory

- `schema_version`: enum ['1.0']
- `news_id`: string
- `stream`: enum ['domestic', 'foreign', 'manual']
- `source_id`: string
- `original_url`: string
- `original_title`: string
- `original_text`: 
- `language`: string
- `source_country`: 
- `subject_countries`: array
- `published_at`: 
- `collected_at`: string (date-time)
- `content_scope`: enum ['metadata', 'summary', 'full_text']
- `reuse_permission`: enum ['unverified', 'licensed', 'link_only', 'blocked']
- `source_payload_ref`: 

## Enumerations

- `schema_version` = ['1.0']
- `stream` = ['domestic', 'foreign', 'manual']
- `content_scope` = ['metadata', 'summary', 'full_text']
- `reuse_permission` = ['unverified', 'licensed', 'link_only', 'blocked']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (15): `collected_at`, `content_scope`, `language`, `news_id`, `original_text`, `original_title`, `original_url`, `published_at`, `reuse_permission`, `schema_version`, `source_country`, `source_id`, `source_payload_ref`, `stream`, `subject_countries`
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
