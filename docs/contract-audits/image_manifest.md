# Contract audit - `image_manifest`

- **Task:** `S00-036` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/image_manifest.schema.json`
- **Example:** `source/contracts/examples/image_manifest.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/image_manifest.schema.json`
- **Producer:** P14 | **Consumers:** P21, P24, P26 | **Owning package:** B05

## Required root fields

- `schema_version`
- `article_id`
- `assets`
- `created_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `article_id`: string
- `assets`: array
- `created_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `assets[].format` = ['jpg', 'png', 'webp']
- `assets[].license_status` = ['verified', 'unknown', 'restricted']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 2/2
- Example top-level keys (4): `article_id`, `assets`, `created_at`, `schema_version`
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
