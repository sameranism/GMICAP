# SYSTEM_MAP - authoritative project and dependency register

- **Task:** `S00-014`  
- **Status:** draft - normalised from `project_package_map.csv` and `dependency_edges.csv`; no edge invented
- **Projects:** 29 | **Edges:** 44

## Projects

| Project | Name | Package | Outputs | Consumers |
|---|---|---|---|---|
| P01 | استاندارد داده | B01 | schemas/*.schema.json | همه بخش‌ها |
| P02 | تنظیمات مدیریتی | B01 | output_controls و تنظیمات نسخه‌دار | همه با مجوز |
| P03 | مدیریت منابع | B01 | source_registry | ۵ و ۶ |
| P04 | کشف رسانه کشورها | B03 | country_source_pack | ۳ |
| P05 | دریافت داخلی | B02 | raw_news:domestic | ۷ |
| P06 | دریافت خارجی | B03 | raw_news:foreign | ۷ |
| P07 | استانداردسازی | B04 | normalized_news | ۸ و ۲۶ |
| P08 | تشخیص تکرار | B04 | cluster_result | ۹ |
| P09 | دسته‌بندی سرویس‌ها | B04 | classified_news | ۱۲ و ۱۳ و ۱۵ |
| P10 | چارچوب/واژه‌نامه | B05 | editorial_rules نسخه‌دار | ۱۲ و ۱۳ |
| P11 | کنترل محتوا و انتشار | B05 | validation_decision | ۲۲ |
| P12 | مترجم هوشمند | B05 | translation | ۱۳ و ۲۶ |
| P13 | ویراستار | B05 | article | ۱۴ و ۱۱ |
| P14 | آماده‌سازی تصویر | B05 | image_manifest | ۱۱ و ۲۴ |
| P15 | تحلیل سیاسی | B06 | analysis_result | ۱۶ و ۱۸ و ۱۹ |
| P16 | چت‌بات تحلیل | B06 | analysis_chat_response | رابط تحلیل |
| P17 | شاخص‌ها | B06 | metrics_snapshot | ۱۸ و ۱۹ و ۲۷ |
| P18 | چهار گزارش عمومی | B06 | public_report | ۱۱ سپس ۲۲ |
| P19 | سه گزارش اختصاصی | B06 | private_report | فقط ۲۷ و ۱۶ با مجوز |
| P20 | گوینده هوشمند | B07 | audio_manifest | ۲۱ یا ۲۴ |
| P21 | مجری مجازی استودیو | B07 | video_manifest | ۲۴ |
| P22 | زمان‌بندی | B08 | publication_job | ۲۴ و ۲۵ |
| P23 | مقاصد انتشار | B08 | destination_config | ۲۴ و ۲۵ |
| P24 | قالب‌بندی مقصد | B08 | destination_payloads | ۲۵ |
| P25 | ارسال چندکاناله | B08 | publication_result | ۲۶ و ۱۷ |
| P26 | آرشیو | B01 | API و شناسه شیء | ۸ و ۱۵ و ۱۷ و ۲۷ |
| P27 | داشبوردها | B09 | رابط واحد | کاربر نهایی |
| P28 | کنترل دسترسی | B01 | access_decision | همه پروژه‌ها |
| P29 | هماهنگ‌کننده | B01 | event_envelope/Workflow | همه پروژه‌ها |

## Dependency edges (data flow)

| From | To | Contract | Kind |
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

## Reading rules

- An edge means the target consumes the named contract from the source; it never means shared tables.
- `P01` is the contract standard consumed by every project; it has no runtime component.
- `P27` (dashboards) and `P29` (coordinator) only read versioned APIs/events, never package internals.
