# Contract audit - `private_report`

- **Task:** `S00-041` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/private_report.schema.json`
- **Example:** `source/contracts/examples/private_report.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/private_report.schema.json`
- **Producer:** P19 | **Consumers:** P27 (editor_in_chief only) | **Owning package:** B06

## Required root fields

- `schema_version`
- `report_id`
- `title`
- `sections`
- `source_refs`
- `generated_at`
- `time_range`
- `generation_status`
- `created_by_project`
- `visibility`
- `report_type`
- `owner_role`
- `publishable`

## Field inventory

- `schema_version`: enum ['1.0']
- `report_id`: string
- `title`: string
- `sections`: array
- `source_refs`: array
- `generated_at`: string (date-time)
- `time_range`: object
- `generation_status`: enum ['draft', 'ready_for_policy', 'completed']
- `created_by_project`: string
- `visibility`: enum ['executive_private']
- `report_type`: enum ['media_narratives', 'political_public_affairs', 'editorial_decision_support']
- `owner_role`: enum ['editor_in_chief']
- `publishable`: boolean

## Enumerations

- `schema_version` = ['1.0']
- `generation_status` = ['draft', 'ready_for_policy', 'completed']
- `visibility` = ['executive_private']
- `report_type` = ['media_narratives', 'political_public_affairs', 'editorial_decision_support']
- `owner_role` = ['editor_in_chief']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 3/3
- Example top-level keys (13): `created_by_project`, `generated_at`, `generation_status`, `owner_role`, `publishable`, `report_id`, `report_type`, `schema_version`, `sections`, `source_refs`, `time_range`, `title`, `visibility`
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
