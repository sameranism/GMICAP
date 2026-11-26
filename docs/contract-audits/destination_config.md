# Contract audit - `destination_config`

- **Task:** `S00-032` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/destination_config.schema.json`
- **Example:** `source/contracts/examples/destination_config.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/destination_config.schema.json`
- **Producer:** P23 | **Consumers:** P22, P25 | **Owning package:** B08

## Required root fields

- `schema_version`
- `destination_id`
- `platform`
- `name`
- `address`
- `credential_ref`
- `desks`
- `allowed_streams`
- `enabled`
- `connection_state`
- `updated_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `destination_id`: string
- `platform`: enum ['website', 'telegram', 'bale', 'eitaa', 'rubika', 'other']
- `name`: string
- `address`: string
- `credential_ref`: 
- `desks`: array
- `allowed_streams`: array
- `enabled`: boolean
- `connection_state`: enum ['unverified', 'verified', 'disabled']
- `updated_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `platform` = ['website', 'telegram', 'bale', 'eitaa', 'rubika', 'other']
- `allowed_streams[]` = ['domestic', 'foreign']
- `connection_state` = ['unverified', 'verified', 'disabled']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (11): `address`, `allowed_streams`, `connection_state`, `credential_ref`, `desks`, `destination_id`, `enabled`, `name`, `platform`, `schema_version`, `updated_at`
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
