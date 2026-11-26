# ETEMAD system map — S00-014

**Status:** Baseline inventory / review pending. This register is generated from the authoritative CSVs; it does not authorize new edges or runtime implementation.

## Source of truth

- `source/technical/project_package_map.csv` (project/package owner and interface summary)
- `source/technical/dependency_edges.csv` (documented project-to-project edges)
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md` (six layers and deployment boundaries)
- `source/technical/database_dictionary.csv` (table ownership, reviewed in S00-016)

## Projects and packages (29)

| Project | Name | Package | Inputs | Outputs | Consumers |
|---|---|---|---|---|---|
| P01 | استاندارد داده | B01 | نیاز سایر بخش‌ها | schemas/*.schema.json | همه بخش‌ها |
| P02 | تنظیمات مدیریتی | B01 | درخواست مدیر/قواعد | output_controls و تنظیمات نسخه‌دار | همه با مجوز |
| P03 | مدیریت منابع | B01 | URL/RSS/API/کشور | source_registry | ۵ و ۶ |
| P04 | کشف رسانه کشورها | B03 | نام کشور/قید زبان | country_source_pack | ۳ |
| P05 | دریافت داخلی | B02 | فهرست منابع داخلی | raw_news:domestic | ۷ |
| P06 | دریافت خارجی | B03 | فهرست منابع خارجی | raw_news:foreign | ۷ |
| P07 | استانداردسازی | B04 | raw_news | normalized_news | ۸ و ۲۶ |
| P08 | تشخیص تکرار | B04 | normalized_news/آرشیو | cluster_result | ۹ |
| P09 | دسته‌بندی سرویس‌ها | B04 | خبر و خوشه | classified_news | ۱۲ و ۱۳ و ۱۵ |
| P10 | چارچوب/واژه‌نامه | B05 | قواعد و سبک | editorial_rules نسخه‌دار | ۱۲ و ۱۳ |
| P11 | کنترل محتوا و انتشار | B05 | article/public_report/حقوق | validation_decision | ۲۲ |
| P12 | مترجم هوشمند | B05 | خبر خارجی/واژه‌نامه | translation | ۱۳ و ۲۶ |
| P13 | ویراستار | B05 | خبر/ترجمه/چارچوب | article | ۱۴ و ۱۱ |
| P14 | آماده‌سازی تصویر | B05 | تصویر/لوگو/قالب | image_manifest | ۱۱ و ۲۴ |
| P15 | تحلیل سیاسی | B06 | خبر/آرشیو/بازه | analysis_result | ۱۶ و ۱۸ و ۱۹ |
| P16 | چت‌بات تحلیل | B06 | سؤال/اسناد مجاز | analysis_chat_response | رابط تحلیل |
| P17 | شاخص‌ها | B06 | آرشیو/انتشار/بازه | metrics_snapshot | ۱۸ و ۱۹ و ۲۷ |
| P18 | چهار گزارش عمومی | B06 | آرشیو/شاخص/زمان | public_report | ۱۱ سپس ۲۲ |
| P19 | سه گزارش اختصاصی | B06 | تحلیل/آرشیو/مجوز | private_report | فقط ۲۷ و ۱۶ با مجوز |
| P20 | گوینده هوشمند | B07 | article/public_report | audio_manifest | ۲۱ یا ۲۴ |
| P21 | مجری مجازی استودیو | B07 | صوت/زیرنویس/قالب | video_manifest | ۲۴ |
| P22 | زمان‌بندی | B08 | validation_decision/زمان | publication_job | ۲۴ و ۲۵ |
| P23 | مقاصد انتشار | B08 | پلتفرم/credential_ref | destination_config | ۲۴ و ۲۵ |
| P24 | قالب‌بندی مقصد | B08 | خبر/تصویر/مقصد | destination_payloads | ۲۵ |
| P25 | ارسال چندکاناله | B08 | publication_job/payload | publication_result | ۲۶ و ۱۷ |
| P26 | آرشیو | B01 | خبر/گزارش/نتیجه | API و شناسه شیء | ۸ و ۱۵ و ۱۷ و ۲۷ |
| P27 | داشبوردها | B09 | شاخص/وضعیت/مجوز | رابط واحد | کاربر نهایی |
| P28 | کنترل دسترسی | B01 | هویت/نقش/منبع | access_decision | همه پروژه‌ها |
| P29 | هماهنگ‌کننده | B01 | رویداد/وضعیت | event_envelope/Workflow | همه پروژه‌ها |

## Explicit directed edges (44)

| From | To | Contract / purpose | Kind |
|---|---|---|---|
| P04 | P03 | بسته منابع کشور | data_flow |
| P03 | P05 | منابع داخلی | data_flow |
| P03 | P06 | منابع خارجی | data_flow |
| P05 | P07 | raw_news | data_flow |
| P06 | P07 | raw_news | data_flow |
| P07 | P08 | normalized_news | data_flow |
| P07 | P26 | آرشیو | data_flow |
| P08 | P09 | cluster_result | data_flow |
| P26 | P08 | سابقه تکرار | data_flow |
| P09 | P12 | foreign classified | data_flow |
| P09 | P13 | domestic classified | data_flow |
| P09 | P15 | موضوعات | data_flow |
| P10 | P12 | واژه‌نامه | data_flow |
| P10 | P13 | چارچوب | data_flow |
| P12 | P13 | translation | data_flow |
| P12 | P26 | نگهداری | data_flow |
| P13 | P14 | article | data_flow |
| P13 | P11 | article | data_flow |
| P14 | P11 | image_manifest | data_flow |
| P11 | P22 | auto_allowed | data_flow |
| P11 | P20 | محتوای تأییدشده | data_flow |
| P26 | P15 | منابع و آرشیو | data_flow |
| P26 | P17 | داده محاسبه | data_flow |
| P26 | P27 | جست‌وجو | data_flow |
| P15 | P16 | analysis_result | data_flow |
| P15 | P18 | analysis_result | data_flow |
| P15 | P19 | analysis_result | data_flow |
| P17 | P18 | metrics | data_flow |
| P17 | P19 | metrics | data_flow |
| P17 | P27 | metrics | data_flow |
| P18 | P11 | public_report به کنترل | data_flow |
| P19 | P16 | مجاز؛ خصوصی | data_flow |
| P19 | P27 | مجاز؛ خصوصی | data_flow |
| P20 | P21 | audio_manifest | data_flow |
| P20 | P24 | audio_manifest | data_flow |
| P21 | P24 | video_manifest | data_flow |
| P22 | P24 | publication_job | data_flow |
| P22 | P25 | publication_job | data_flow |
| P23 | P24 | destination_config | data_flow |
| P23 | P25 | destination_config | data_flow |
| P14 | P24 | image_manifest | data_flow |
| P24 | P25 | destination_payload | data_flow |
| P25 | P26 | publication_result | data_flow |
| P25 | P17 | publication_result | data_flow |

## Architecture invariants

- Six conceptual layers; B01–B09 are delivery boundaries, not necessarily individual servers.
- Domestic ingest, foreign ingest and central core have independent PostgreSQL/queue environments and a vetted authenticated bridge.
- Cross-package transfers use authorized versioned APIs/events and baseline JSON Schema v1.0; never access another package's private ORM/tables directly.
- Three editor-in-chief reports are `executive_private` and cannot be sent to public search/Studio/Publishing. Output controls remain independent and server-enforced.
- Do not treat the CSV `consumers` human shorthand as extra graph edges. Only listed `dependency_edges.csv` rows are the directed edge register.

## Verification pending

Dependency cycles, direction correctness, API signatures, permissions and actual implementations require independent review and S00 testing. Existing CSV values are preserved verbatim; no new project or edge was invented.

## Rollback

Close the draft PR. Neither source CSV was changed.
