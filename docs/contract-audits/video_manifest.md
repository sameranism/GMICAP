# Contract audit - `video_manifest`

- **Task:** `S00-050` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/video_manifest.schema.json`
- **Example:** `source/contracts/examples/video_manifest.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/video_manifest.schema.json`
- **Producer:** P21 | **Consumers:** P24, P26 | **Owning package:** B07

## Required root fields

- `schema_version`
- `video_id`
- `audio_id`
- `video_uri`
- `presenter_id`
- `studio_template_id`
- `synthetic_presenter`
- `disclosure_label`
- `created_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `video_id`: string
- `audio_id`: string
- `video_uri`: string
- `presenter_id`: string
- `studio_template_id`: string
- `synthetic_presenter`: boolean
- `disclosure_label`: string
- `created_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (9): `audio_id`, `created_at`, `disclosure_label`, `presenter_id`, `schema_version`, `studio_template_id`, `synthetic_presenter`, `video_id`, `video_uri`
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
