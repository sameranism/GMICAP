# ETEMAD contract ownership inventory — S00-015

**Status: PROPOSED / requires independent per-contract audit.** This is a reconciliation register, not a change to the frozen wire contracts or an approval to create tables.

## Authoritative references

- `source/contracts/schemas/*.schema.json` and `source/contracts/examples/*.example.json` — frozen Draft 2020-12 v1.0
- `source/technical/project_package_map.csv`, `source/technical/dependency_edges.csv` and `source/technical/database_dictionary.csv`
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md` and its package specifications

## 30 contract records

Producer/project and table below are **audit candidates**, derived from project responsibilities and proposed table names; the schema definitions do not intrinsically certify a producer or storage table. Consumer mappings must be confirmed through the explicit dependency edges and individual contract audits S00-022–S00-051; do not infer a dependency simply because a project is a potential consumer.

| Contract schema (same basename) | Baseline example | Proposed producer | Proposed table / store | Review status |
|---|---|---|---|---|
| `access_decision` | `source/contracts/examples/access_decision.example.json` | P28 | identity.roles_permissions | PROPOSED — verify exact producer/consumer |
| `ai_models_config` | `source/contracts/examples/ai_models_config.example.json` | P02 | control.config_revisions | PROPOSED — verify exact producer/consumer |
| `analysis_chat_response` | `source/contracts/examples/analysis_chat_response.example.json` | P16 | insights.chat_messages | PROPOSED — verify exact producer/consumer |
| `analysis_result` | `source/contracts/examples/analysis_result.example.json` | P15 | insights.analyses | PROPOSED — verify exact producer/consumer |
| `archive_record` | `source/contracts/examples/archive_record.example.json` | P26 | archive.news_records | PROPOSED — verify exact producer/consumer |
| `article` | `source/contracts/examples/article.example.json` | P13 | editorial.articles | PROPOSED — verify exact producer/consumer |
| `audio_manifest` | `source/contracts/examples/audio_manifest.example.json` | P20 | studio.audio_jobs | PROPOSED — verify exact producer/consumer |
| `classified_news` | `source/contracts/examples/classified_news.example.json` | P09 | processing.news_desks | PROPOSED — verify exact producer/consumer |
| `cluster_result` | `source/contracts/examples/cluster_result.example.json` | P08 | processing.clusters | PROPOSED — verify exact producer/consumer |
| `country_source_pack` | `source/contracts/examples/country_source_pack.example.json` | P04 | foreign.source_candidates | PROPOSED — verify exact producer/consumer |
| `destination_config` | `source/contracts/examples/destination_config.example.json` | P23 | publish.destinations | PROPOSED — verify exact producer/consumer |
| `destination_payload` | `source/contracts/examples/destination_payload.example.json` | P24 | publish.payloads | PROPOSED — verify exact producer/consumer |
| `editorial_rules` | `source/contracts/examples/editorial_rules.example.json` | P10 | editorial.rulesets | PROPOSED — verify exact producer/consumer |
| `event_envelope` | `source/contracts/examples/event_envelope.example.json` | P29 | orchestration.outbox | PROPOSED — verify exact producer/consumer |
| `image_manifest` | `source/contracts/examples/image_manifest.example.json` | P14 | editorial.image_assets | PROPOSED — verify exact producer/consumer |
| `metrics_snapshot` | `source/contracts/examples/metrics_snapshot.example.json` | P17 | insights.metric_snapshots | PROPOSED — verify exact producer/consumer |
| `news_framework` | `source/contracts/examples/news_framework.example.json` | UNRESOLVED | UNRESOLVED | UNRESOLVED |
| `normalized_news` | `source/contracts/examples/normalized_news.example.json` | P07 | processing.normalized_items | PROPOSED — verify exact producer/consumer |
| `output_controls` | `source/contracts/examples/output_controls.example.json` | P02 | control.output_switches | PROPOSED — verify exact producer/consumer |
| `private_report` | `source/contracts/examples/private_report.example.json` | P19 | executive.private_reports | PROPOSED — verify exact producer/consumer |
| `public_report` | `source/contracts/examples/public_report.example.json` | P18 | insights.public_reports | PROPOSED — verify exact producer/consumer |
| `publication_job` | `source/contracts/examples/publication_job.example.json` | P22 | publish.jobs | PROPOSED — verify exact producer/consumer |
| `publication_result` | `source/contracts/examples/publication_result.example.json` | P25 | publish.attempts | PROPOSED — verify exact producer/consumer |
| `raw_news` | `source/contracts/examples/raw_news.example.json` | P05 / P06 | domestic.raw_items / foreign.raw_items | PROPOSED — verify exact producer/consumer |
| `schedule_config` | `source/contracts/examples/schedule_config.example.json` | UNRESOLVED | UNRESOLVED | UNRESOLVED |
| `source_registry` | `source/contracts/examples/source_registry.example.json` | P03 | sources.source_registry | PROPOSED — verify exact producer/consumer |
| `translation` | `source/contracts/examples/translation.example.json` | P12 | editorial.translations | PROPOSED — verify exact producer/consumer |
| `validation_decision` | `source/contracts/examples/validation_decision.example.json` | P11 | editorial.policy_decisions | PROPOSED — verify exact producer/consumer |
| `video_manifest` | `source/contracts/examples/video_manifest.example.json` | P21 | studio.video_jobs | PROPOSED — verify exact producer/consumer |
| `workflow_status` | `source/contracts/examples/workflow_status.example.json` | P29 | orchestration.jobs | PROPOSED — verify exact producer/consumer |

## Consumer and producer verification method

1. For each contract, compare the project map's `outputs` and the dependency edge's `contract` value with the actual JSON Schema `$id`, properties, example and authoritative package specification.
2. Record only **verified** producer → consumer edges in the contract-specific audit. A package or project name in this table is not sufficient evidence of an API call or a field-level contract.
3. For `raw_news`, preserve separate domestic P05 and foreign P06 producer boundaries. The central B04 pipeline consumes through authenticated authorized transfer, not direct remote DB reads.
4. For `event_envelope`, P29 is a proposed orchestration owner, but the actual `producer_project` field names the emitting project. Do not rewrite event producers as P29 or create a dependency edge without evidence.
5. Private report visibility restrictions apply independently of mapping. `private_report` must never become a public report, Studio or publishing input.

## Open mapping questions

- `news_framework`: project and table owner not unambiguously proven by this register; resolve with the source technical specifications and contract audit.
- `schedule_config`: scheduling and central config responsibilities overlap; resolve before assigning write ownership.
- For all other rows, the candidate producer/table requires a traceable confirmation in the contract-specific audit and schema-to-API mapping. Consumer lists are intentionally not asserted as verified.

## Verification and rollback

- Checked tracked tree: exactly 30 schema files; each has matching example pathname in the tracked tree: true.
- Gate-00 independent review: PENDING. No application logic, database or source schema changed.
- Rollback: close this document-only draft PR.
