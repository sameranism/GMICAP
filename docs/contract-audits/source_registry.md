# Contract audit - `source_registry`

- **Task:** `S00-047` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/source_registry.schema.json`
- **Example:** `source/contracts/examples/source_registry.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/source_registry.schema.json`
- **Producer:** P03 | **Consumers:** P05, P06, P07 | **Owning package:** B01

## Required root fields

- `schema_version`
- `registry_id`
- `updated_at`
- `sources`

## Field inventory

- `schema_version`: enum ['1.0']
- `registry_id`: string
- `updated_at`: string (date-time)
- `sources`: array

## Enumerations

- `schema_version` = ['1.0']
- `sources[].stream` = ['domestic', 'foreign']
- `sources[].license_scope` = ['metadata', 'summary', 'full_text', 'unknown']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 2/2
- Example top-level keys (4): `registry_id`, `schema_version`, `sources`, `updated_at`
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
