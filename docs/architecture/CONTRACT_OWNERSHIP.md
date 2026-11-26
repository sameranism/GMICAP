# CONTRACT_OWNERSHIP - who owns each of the 30 contracts

- **Task:** `S00-015`  
- **Status:** draft - producer/consumer mapping needs client confirmation where noted

| # | Contract | Producer | Consumers | Owning package | Required root fields |
|---:|---|---|---|---|---:|
| 1 | `access_decision` | P28 | P11, P19, P27 | B01 | 10 |
| 2 | `ai_models_config` | P02 | P12, P13, P15, P16, P18, P19, P20, P21 | B01 | 4 |
| 3 | `analysis_chat_response` | P16 | P27 | B06 | 8 |
| 4 | `analysis_result` | P15 | P18, P19, P27 | B06 | 8 |
| 5 | `archive_record` | P26 | P08, P17, P19 | B01 | 10 |
| 6 | `article` | P13 | P11, P18, P21, P24 | B05 | 14 |
| 7 | `audio_manifest` | P20 | P21, P24, P26 | B07 | 10 |
| 8 | `classified_news` | P09 | P12, P13, P15, P19 | B04 | 10 |
| 9 | `cluster_result` | P08 | P09, P26 | B04 | 7 |
| 10 | `country_source_pack` | P04 | P06, P27 | B03 | 6 |
| 11 | `destination_config` | P23 | P22, P25 | B08 | 11 |
| 12 | `destination_payload` | P24 | P25 | B08 | 9 |
| 13 | `editorial_rules` | P10 | P12, P13 | B05 | 8 |
| 14 | `event_envelope` | P29 | all packages | B01 | 10 |
| 15 | `image_manifest` | P14 | P21, P24, P26 | B05 | 4 |
| 16 | `metrics_snapshot` | P17 | P18, P19, P27 | B06 | 12 |
| 17 | `news_framework` | P10 | P12, P13 | B05 | 9 |
| 18 | `normalized_news` | P07 | P08, P09, P12, P13, P26 | B04 | 14 |
| 19 | `output_controls` | P02 | P06, P18, P20, P21, P25 | B01 | 7 |
| 20 | `private_report` | P19 | P27 (editor_in_chief only) | B06 | 13 |
| 21 | `public_report` | P18 | P22, P25, P27 | B06 | 11 |
| 22 | `publication_job` | P22 | P25 | B08 | 12 |
| 23 | `publication_result` | P25 | P27, P26 | B08 | 5 |
| 24 | `raw_news` | P05, P06 | P07 | B02, B03 | 12 |
| 25 | `schedule_config` | P22 | P25 | B08 | 10 |
| 26 | `source_registry` | P03 | P05, P06, P07 | B01 | 4 |
| 27 | `translation` | P12 | P13, P15 | B05 | 11 |
| 28 | `validation_decision` | P11 | P22, P27 | B05 | 10 |
| 29 | `video_manifest` | P21 | P24, P26 | B07 | 9 |
| 30 | `workflow_status` | P29 | P27, all packages | B01 | 8 |

## Ownership rules

1. Only the producing project may write a record of that contract type.
2. Consumers receive the record through a versioned API or event; no shared tables.
3. A schema change is proposed by the producer and approved by consumers; silence is not approval.
4. `raw_news` has two producers (domestic and foreign ingest) in separate databases; the shared
   shape is owned by `P01` and published in `source/contracts`.

## Unresolved mappings (client input required)

- Which physical table backs `ai_models_config` (proposed: `control` schema in central).
- Whether `schedule_config` is owned by scheduling (P22) or destination setup (P23).
- Final CMS identity for `destination_config`/`destination_payload`.
