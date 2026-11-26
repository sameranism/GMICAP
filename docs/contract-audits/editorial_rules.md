# Contract audit - `editorial_rules`

- **Task:** `S00-034` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/editorial_rules.schema.json`
- **Example:** `source/contracts/examples/editorial_rules.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/editorial_rules.schema.json`
- **Producer:** P10 | **Consumers:** P12, P13 | **Owning package:** B05

## Required root fields

- `schema_version`
- `ruleset_id`
- `revision`
- `stream`
- `desk`
- `replacement_rules`
- `prohibited_content_categories`
- `updated_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `ruleset_id`: string
- `revision`: integer
- `stream`: enum ['domestic', 'foreign', 'mixed', 'manual']
- `desk`: string
- `replacement_rules`: array
- `prohibited_content_categories`: array
- `updated_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `stream` = ['domestic', 'foreign', 'mixed', 'manual']
- `replacement_rules[].mode` = ['auto_replace', 'suggest_review', 'never_replace']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 2/2
- Example top-level keys (8): `desk`, `prohibited_content_categories`, `replacement_rules`, `revision`, `ruleset_id`, `schema_version`, `stream`, `updated_at`
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
