# Contract audit - `cluster_result`

- **Task:** `S00-030` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/cluster_result.schema.json`
- **Example:** `source/contracts/examples/cluster_result.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/cluster_result.schema.json`
- **Producer:** P08 | **Consumers:** P09, P26 | **Owning package:** B04

## Required root fields

- `schema_version`
- `news_id`
- `event_id`
- `duplicate_of`
- `related_news_ids`
- `similarity_method`
- `created_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `news_id`: string
- `event_id`: string
- `duplicate_of`: 
- `related_news_ids`: array
- `similarity_method`: string
- `created_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (7): `created_at`, `duplicate_of`, `event_id`, `news_id`, `related_news_ids`, `schema_version`, `similarity_method`
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
