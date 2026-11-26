# Contract audit - `output_controls`

- **Task:** `S00-040` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/output_controls.schema.json`
- **Example:** `source/contracts/examples/output_controls.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/output_controls.schema.json`
- **Producer:** P02 | **Consumers:** P06, P18, P20, P21, P25 | **Owning package:** B01

## Required root fields

- `schema_version`
- `revision`
- `updated_at`
- `updated_by`
- `public_analysis`
- `studio`
- `publishing`

## Field inventory

- `schema_version`: enum ['1.0']
- `revision`: integer
- `updated_at`: string (date-time)
- `updated_by`: string
- `public_analysis`: object
- `studio`: object
- `publishing`: object

## Enumerations

- `schema_version` = ['1.0']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 4/4
- Example top-level keys (7): `public_analysis`, `publishing`, `revision`, `schema_version`, `studio`, `updated_at`, `updated_by`
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
