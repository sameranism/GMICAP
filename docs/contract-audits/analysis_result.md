# Contract audit - `analysis_result`

- **Task:** `S00-025` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/analysis_result.schema.json`
- **Example:** `source/contracts/examples/analysis_result.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/analysis_result.schema.json`
- **Producer:** P15 | **Consumers:** P18, P19, P27 | **Owning package:** B06

## Required root fields

- `schema_version`
- `analysis_id`
- `topic`
- `time_range`
- `source_refs`
- `claims`
- `uncertainties`
- `created_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `analysis_id`: string
- `topic`: string
- `time_range`: object
- `source_refs`: array
- `claims`: array
- `uncertainties`: array
- `created_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `claims[].classification` = ['documented', 'attributed', 'interpretation', 'uncertain']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 3/3
- Example top-level keys (8): `analysis_id`, `claims`, `created_at`, `schema_version`, `source_refs`, `time_range`, `topic`, `uncertainties`
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
