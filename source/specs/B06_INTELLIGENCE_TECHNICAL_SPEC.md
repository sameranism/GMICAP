# B06_INTELLIGENCE_TECHNICAL_SPEC


> Extracted without semantic modification from `B06_INTELLIGENCE_TECHNICAL_SPEC.docx`. If ambiguous, consult the original DOCX.


## بسته B06 — ژرفان

Intelligence & Reports | راهنمای اجرایی مستقل تیم توسعه

نسخه 1.1  |  ۳۰ آبان ۱۴۰۵ / ۲۱ نوامبر ۲۰۲۶  |  وضعیت: مشخصات طراحی، نه سامانه عملیاتی

## ۱. مأموریت بسته و مرز مسئولیت

تحلیل مستند و بی‌طرفانه، چت‌بات فقط در بخش تحلیل، شاخص‌ها و هفت گزارش روزانه.

| مشخصه | مقدار |

| --- | --- |

| شناسه بسته | B06 |

| مسئولیت استقرار | تحلیل مشترک؛ حریم خصوصی جدا |

| پروژه‌های تحت مالکیت | P15، P16، P17، P18، P19 |

| فناوری پایه | Python/FastAPI + PostgreSQL + Redis / برای B09: React/TypeScript/Mantine |

| مبنای قرارداد | ۳۰ JSON Schema مصوب v1.0؛ تغییر ناسازگار ممنوع |

| وابستگی پایه | B01 / احراز هویت، تنظیمات، آرشیو و رویدادها |

## ۲. پروژه‌های داخلی، ورودی و خروجی

## P15 — تحلیل سیاسی

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| خبر/آرشیو/بازه | analysis_result | ۱۶ و ۱۸ و ۱۹ |

وظیفه و منطق: تحلیل روایی مبتنی بر منابع و timeline، ادعا/فکت جدا

روش انجام: حجم پوشش، اختلاف ادعاها و اسناد پشتیبان

خطا و مرز حساس: به افراد امتیاز سیاسی یا پیش‌بینی انتخاباتی داده نشود

قراردادهای موجود: analysis_result.schema.json

عدم مسئولیت: ارزیابی محبوبیت/صلاحیت سیاسی بدون داده معتبر

## P16 — چت‌بات تحلیل

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| سؤال/اسناد مجاز | analysis_chat_response | رابط تحلیل |

وظیفه و منطق: Retrieval مجاز مبتنی بر سطح دسترسی پیش از فراخوانی AI

روش انجام: پاسخ با evidence_ref و uncertainty

خطا و مرز حساس: prompt injection منبع و تلاش برای افشای private

قراردادهای موجود: analysis_chat_response.schema.json

عدم مسئولیت: بازیابی گزارش خصوصی بدون مجوز

## P17 — شاخص‌ها

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| آرشیو/انتشار/بازه | metrics_snapshot | ۱۸ و ۱۹ و ۲۷ |

وظیفه و منطق: محاسبه شاخص آماری با timestamp دقیق و sample denominator

روش انجام: metrics snapshot منبع‌دار

خطا و مرز حساس: نسبت/نرخ بدون مخرج یا نمونه قابل اتکا ممنوع

قراردادهای موجود: metrics_snapshot.schema.json

عدم مسئولیت: قضاوت کیفی درباره شخصیت‌های سیاسی

## P18 — چهار گزارش عمومی

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| آرشیو/شاخص/زمان | public_report | ۱۱ سپس ۲۲ |

وظیفه و منطق: چهار slot عمومی، زمان‌بندی مستقل و کنترل output switch

روش انجام: public_report با evidence و flag publishable پس از P11

خطا و مرز حساس: public_analysis=false => هیچ تولید تازه

قراردادهای موجود: public_report.schema.json

عدم مسئولیت: دورزدن کنترل کیفیت/کلید خاموشی

## P19 — سه گزارش اختصاصی

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| تحلیل/آرشیو/مجوز | private_report | فقط ۲۷ و ۱۶ با مجوز |

وظیفه و منطق: سه slot ۵..۷، رمزنگاری، نگهداری در private storage

روش انجام: private_report با visibility اجرایی؛ بدون publish job

خطا و مرز حساس: عدم دسترسی دیگر نقش‌ها، حتی مالک سیستم بدون grant

قراردادهای موجود: private_report.schema.json

عدم مسئولیت: تولید هر نوع publication_job

## ۳. معماری فرآیند و اتصال به سایر بسته‌ها

| تولیدکننده | مصرف‌کننده | داده عبوری |

| --- | --- | --- |

| P09 | P15 | موضوعات |

| P26 | P15 | منابع و آرشیو |

| P26 | P17 | داده محاسبه |

| P15 | P16 | analysis_result |

| P15 | P18 | analysis_result |

| P15 | P19 | analysis_result |

| P17 | P18 | metrics |

| P17 | P19 | metrics |

| P17 | P27 | metrics |

| P18 | P11 | public_report به کنترل |

| P19 | P16 | مجاز؛ خصوصی |

| P19 | P27 | مجاز؛ خصوصی |

| P25 | P17 | publication_result |

هیچ سرویس نباید به پایگاه داده بسته دیگر مستقیماً متصل شود. انتقال‌های بین‌بسته‌ای با API نسخه‌دار یا پیام event_envelope صورت می‌گیرد. Data reference باید شناسه artifact و دسترسی مجاز داشته باشد.

## ۴. طرح دیتابیس و مالکیت داده

## insights.analyses

## مالک: P15 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: analysis_id, topic, period_start, period_end, evidence_ref, confidence_note

کلید / ایندکس / قید: اسناد/نقل‌قول‌ها و فرضیه جدا

## insights.chat_sessions

## مالک: P16 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: chat_id, user_id, scope, started_at, state

کلید / ایندکس / قید: RLS/RBAC قبل از retrieval

## insights.chat_messages

## مالک: P16 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: message_id, chat_id, actor, text_ref, evidence_ref, created_at

کلید / ایندکس / قید: داده محرمانه بدون دسترسی در prompt نیست

## insights.metric_snapshots

## مالک: P17 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: snapshot_id, stream, desk, metric_date, value_json, data_cutoff

کلید / ایندکس / قید: UNIQUE(stream,desk,metric_date,snapshot_type)

## insights.public_reports

## مالک: P18 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: report_id, report_slot, report_day, revision, content_ref, validation_state

کلید / ایندکس / قید: UNIQUE(report_day,report_slot,revision)؛ slot 1..4

## executive.private_reports

## مالک: P19 | محل فیزیکی: مخزن محرمانه مجزا

ستون‌های پیشنهادی: report_id, report_slot, report_day, content_ref, owner_id, restricted_at

کلید / ایندکس / قید: slot 5..7؛ DB role و bucket خصوصی؛ publishable=false

تمام جدول‌ها دارای کلید UUID، created_at، updated_at در صورت تغییرپذیری، ثبت event/outbox و migrations نسخه‌دار باشند. SQL ابتدایی بسته صرفاً طرح مفهومی است؛ DDL typed باید به‌صورت migration اختصاصی همین تیم نوشته و آزمایش شود.

## ۵. APIهای موردنیاز (پیشنهادی برای OpenAPI)

| روش | مسیر | ورودی | خروجی | مالک |

| --- | --- | --- | --- | --- |

| POST | /v1/analysis/run | topic/time/evidence | analysis_result | P15 |

| POST | /v1/analysis/chat | question + authorized scope | analysis_chat_response | P16 |

| GET | /v1/metrics | period/stream/desk | metrics_snapshot | P17 |

| POST | /v1/reports/public/build | slot 1..4 | public_report | P18 |

| POST | /v1/reports/private/build | slot 5..7 | private_report | P19 |

قاعده مشترک: headerهای Authorization/Service Identity، X-Correlation-ID و Idempotency-Key برای عملیات تغییر؛ پاسخ خطا {code,message,correlation_id,details}؛ pagination و rate limit بر اساس سیاست بسته.

## ۶. تنظیمات و اسرار

•  تنظیمات از P02 با scope مشخص: stream, desk, project, destination دریافت می‌شود؛ snapshot و revision در job ثبت شود.

•  API key یا رمز در فایل پیکربندی، سند تحویل، event، log یا جدول عمومی ذخیره نشود؛ فقط credential_ref از Secret Store.

•  بازۀ زمانی در DB UTC و در UI با timezone تهران نمایش داده شود؛ فاصله اجرا و زمان‌بندی قابل تغییر توسط نقش مجاز.

•  امنیت service-to-service از توکن خدمت/کلید موقت و حداقل مجوز پیروی کند؛ عملیات حساس audit شود.

## ۷. سیاست خروجی هفت گزارش و چت‌بات

P18 چهار گزارش با slotهای ۱ تا ۴ و P19 سه گزارش اختصاصی با slotهای ۵ تا ۷ تولید می‌کند. خروجی P19 فقط به نقش editor_in_chief از private bucket و API خصوصی می‌رود. Chatbot P16 فقط در بخش تحلیل، با فیلتر دسترسی قبل از retrieval اجرا می‌شود.

تحلیل‌ها حق ندارند محبوبیت، شایستگی یا پیش‌بینی انتخاباتی شخصیت‌ها را خودسرانه امتیازدهی کنند. آمار پوشش، مواضع علنی و تفاوت متن منابع با زمان و شواهد گزارش می‌شود.

## ۸. آزمون‌های پذیرش اختصاصی

•  چهار گزارش عمومی فقط پس از validate قابلیت publish پیدا کنند.

•  سه گزارش اختصاصی حتی با جعل object_type به صف عمومی وارد نشوند.

•  چت‌بات فقط اسناد مجاز نقش جاری را بازیابی کند.

•  امتیاز محبوبیت سیاسی یا پیش‌بینی انتخاباتی توسط مدل تولید نشود.

•  خاموش‌کردن public_analysis تولید ۴ گزارش را متوقف کند، ولی گزارش‌های private ادامه یابند.

## ۹. تحویل‌های تیم و تعریف پایان کار

•  README اجرایی برای توسعه‌دهنده مستقل، دیاگرام درون‌بسته، فایل OpenAPI و قراردادهای JSON Schema لازم.

•  Migrationهای تایپ‌شده PostgreSQL، راهنمای داده تست، بدون اطلاعات واقعی یا credential.

•  نمونه ورودی معتبر، نمونه نامعتبر، سناریوی تکرار event و تست اجازه/عدم اجازه.

•  آزمون API قراردادی با پروژه‌های مصرف‌کننده و گزارش trace از correlation_id.

•  متریک سلامت، log ساخت‌یافته، شناسایی نسخه و روش rollback تغییر ناسازگار.

•  هیچ الزام غیرمصوب درون کد hardcode نشود؛ feature flag و تنظیمات نسخه‌دار.

## الزامات غیرقابل مذاکره بین بسته‌ها

•  قراردادهای موجود v1.0 حفظ می‌شوند؛ فیلد اختیاری جدید تنها با نسخه‌گذاری و آزمون سازگاری مجاز است.

•  هویت کاربر و سطح دسترسی باید در API/DB اعمال شود؛ UI به‌تنهایی کنترل امنیتی نیست.

•  محتوای اصلی منبع و نقل‌قول‌های دقیق نباید با قواعد بازنویسی تحریف شوند.

•  هیچ داده executive_private از طریق P22/P24/P25 یا UI عمومی صادر نمی‌شود.

•  کلیدهای خاموش/روشن report عمومی، استودیو و انتشار سمت سرور و پیش از اقدام اثرگذار بررسی شوند.

•  فایل‌های حجیم در Object Store؛ PostgreSQL برای metadata و مالکیت حقیقت؛ Redis صف/cache موقت.

•  سرور خارجی هیچ اتصال DB مستقیم با هسته مرکزی ندارد؛ فقط Bridge احراز هویت‌شده.

## ۱۰. تصمیم‌های باز که توسعه این بسته را متوقف نمی‌کند

•  نسخه نهایی سرویس‌ها و سخت‌افزار در DevOps/ADR بعدی قفل می‌شود.

•  نام جدول‌ها و مسیر API تا تصویب OpenAPI و migration اختصاصی این بسته به عنوان پیش‌نویس تلقی شوند.
