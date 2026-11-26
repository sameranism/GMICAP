# Contract audit - `validation_decision`

- **Task:** `S00-049` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/validation_decision.schema.json`
- **Example:** `source/contracts/examples/validation_decision.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/validation_decision.schema.json`
- **Producer:** P11 | **Consumers:** P22, P27 | **Owning package:** B05

## Required root fields

- `schema_version`
- `decision_id`
- `object_id`
- `object_type`
- `decision`
- `reason_codes`
- `evidence_refs`
- `policy_version`
- `decided_at`
- `expires_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `decision_id`: string
- `object_id`: string
- `object_type`: enum ['article', 'public_report']
- `decision`: enum ['auto_allowed', 'human_review', 'blocked']
- `reason_codes`: array
- `evidence_refs`: array
- `policy_version`: string
- `decided_at`: string (date-time)
- `expires_at`: 

## Enumerations

- `schema_version` = ['1.0']
- `object_type` = ['article', 'public_report']
- `decision` = ['auto_allowed', 'human_review', 'blocked']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (10): `decided_at`, `decision`, `decision_id`, `evidence_refs`, `expires_at`, `object_id`, `object_type`, `policy_version`, `reason_codes`, `schema_version`
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
