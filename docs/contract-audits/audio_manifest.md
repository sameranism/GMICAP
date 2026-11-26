# Contract audit - `audio_manifest`

- **Task:** `S00-028` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/audio_manifest.schema.json`
- **Example:** `source/contracts/examples/audio_manifest.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/audio_manifest.schema.json`
- **Producer:** P20 | **Consumers:** P21, P24, P26 | **Owning package:** B07

## Required root fields

- `schema_version`
- `audio_id`
- `source_object_type`
- `source_object_id`
- `audio_uri`
- `subtitle_uri`
- `voice_id`
- `language`
- `ai_generated`
- `created_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `audio_id`: string
- `source_object_type`: enum ['article', 'public_report']
- `source_object_id`: string
- `audio_uri`: string
- `subtitle_uri`: 
- `voice_id`: string
- `language`: string
- `ai_generated`: boolean
- `created_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `source_object_type` = ['article', 'public_report']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (10): `ai_generated`, `audio_id`, `audio_uri`, `created_at`, `language`, `schema_version`, `source_object_id`, `source_object_type`, `subtitle_uri`, `voice_id`
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
