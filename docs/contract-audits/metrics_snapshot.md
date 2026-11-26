# Contract audit - `metrics_snapshot`

- **Task:** `S00-037` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/metrics_snapshot.schema.json`
- **Example:** `source/contracts/examples/metrics_snapshot.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/metrics_snapshot.schema.json`
- **Producer:** P17 | **Consumers:** P18, P19, P27 | **Owning package:** B06

## Required root fields

- `schema_version`
- `snapshot_id`
- `stream`
- `time_range`
- `collected_count`
- `unique_count`
- `published_count`
- `successful_deliveries`
- `failed_deliveries`
- `unknown_deliveries`
- `topic_coverage`
- `generated_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `snapshot_id`: string
- `stream`: enum ['domestic', 'foreign', 'mixed', 'manual']
- `time_range`: object
- `collected_count`: integer
- `unique_count`: integer
- `published_count`: integer
- `successful_deliveries`: integer
- `failed_deliveries`: integer
- `unknown_deliveries`: integer
- `topic_coverage`: array
- `generated_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `stream` = ['domestic', 'foreign', 'mixed', 'manual']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 3/3
- Example top-level keys (12): `collected_count`, `failed_deliveries`, `generated_at`, `published_count`, `schema_version`, `snapshot_id`, `stream`, `successful_deliveries`, `time_range`, `topic_coverage`, `unique_count`, `unknown_deliveries`
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
