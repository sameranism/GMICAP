# Contract audit - `country_source_pack`

- **Task:** `S00-031` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/country_source_pack.schema.json`
- **Example:** `source/contracts/examples/country_source_pack.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/country_source_pack.schema.json`
- **Producer:** P04 | **Consumers:** P06, P27 | **Owning package:** B03

## Required root fields

- `schema_version`
- `pack_id`
- `country`
- `generated_at`
- `sources`
- `verified_feed_count`

## Field inventory

- `schema_version`: enum ['1.0']
- `pack_id`: string
- `country`: string
- `generated_at`: string (date-time)
- `sources`: array
- `verified_feed_count`: integer

## Enumerations

- `schema_version` = ['1.0']
- `sources[].stream` = ['domestic', 'foreign']
- `sources[].license_scope` = ['metadata', 'summary', 'full_text', 'unknown']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 2/2
- Example top-level keys (6): `country`, `generated_at`, `pack_id`, `schema_version`, `sources`, `verified_feed_count`
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
