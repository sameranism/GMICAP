# Contract audit - `access_decision`

- **Task:** `S00-022` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/access_decision.schema.json`
- **Example:** `source/contracts/examples/access_decision.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/access_decision.schema.json`
- **Producer:** P28 | **Consumers:** P11, P19, P27 | **Owning package:** B01

## Required root fields

- `schema_version`
- `request_id`
- `principal_id`
- `role`
- `resource_type`
- `resource_id`
- `action`
- `allowed`
- `reason_code`
- `decided_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `request_id`: string
- `principal_id`: string
- `role`: string
- `resource_type`: string
- `resource_id`: string
- `action`: string
- `allowed`: boolean
- `reason_code`: string
- `decided_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (10): `action`, `allowed`, `decided_at`, `principal_id`, `reason_code`, `request_id`, `resource_id`, `resource_type`, `role`, `schema_version`
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
