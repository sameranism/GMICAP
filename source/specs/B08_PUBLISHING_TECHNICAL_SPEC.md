# B08_PUBLISHING_TECHNICAL_SPEC


> Extracted without semantic modification from `B08_PUBLISHING_TECHNICAL_SPEC.docx`. If ambiguous, consult the original DOCX.


## بسته B08 — رسان

Publishing Engine | راهنمای اجرایی مستقل تیم توسعه

نسخه 1.1  |  ۳۰ آبان ۱۴۰۵ / ۲۱ نوامبر ۲۰۲۶  |  وضعیت: مشخصات طراحی، نه سامانه عملیاتی

## ۱. مأموریت بسته و مرز مسئولیت

ثبت مقصدها، صف و زمان‌بندی، قالب‌بندی اختصاصی و ارسال هم‌زمان.

| مشخصه | مقدار |

| --- | --- |

| شناسه بسته | B08 |

| مسئولیت استقرار | سرویس خروجی مستقل |

| پروژه‌های تحت مالکیت | P22، P23، P24، P25 |

| فناوری پایه | Python/FastAPI + PostgreSQL + Redis / برای B09: React/TypeScript/Mantine |

| مبنای قرارداد | ۳۰ JSON Schema مصوب v1.0؛ تغییر ناسازگار ممنوع |

| وابستگی پایه | B01 / احراز هویت، تنظیمات، آرشیو و رویدادها |

## ۲. پروژه‌های داخلی، ورودی و خروجی

## P22 — زمان‌بندی

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| validation_decision/زمان | publication_job | ۲۴ و ۲۵ |

وظیفه و منطق: scheduled_at مستقل per stream/desk؛ deadline و hold policy

روش انجام: publication_job فقط با validation_decision auto_allowed

خطا و مرز حساس: خاموش شدن انتشار و انقضای job

قراردادهای موجود: publication_job.schema.json

## عدم مسئولیت: ارسال درخواست به API مقصد

## P23 — مقاصد انتشار

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| پلتفرم/credential_ref | destination_config | ۲۴ و ۲۵ |

وظیفه و منطق: provider adapter registry، ثبت مقصد و تست مجوز

روش انجام: destination_config فعال فقط پس از verification

خطا و مرز حساس: API پشتیبانی‌نشده یا secret نامعتبر -> inactive

قراردادهای موجود: destination_config.schema.json

عدم مسئولیت: ذخیره کلید محرمانه در خروجی عمومی

## P24 — قالب‌بندی مقصد

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| خبر/تصویر/مقصد | destination_payloads | ۲۵ |

## وظیفه و منطق: ساخت متن/تصویر مناسب تلگرام، CMS و هر کانال

روش انجام: payload per destination + content hash

خطا و مرز حساس: داده private هرگز وارد payload نشود

قراردادهای موجود: destination_payload.schema.json

عدم مسئولیت: بازنویسی مستقل خبر یا تأیید انتشار

## P25 — ارسال چندکاناله

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| publication_job/payload | publication_result | ۲۶ و ۱۷ |

وظیفه و منطق: dispatch موازی با کنترل قبل از ارسال و وضعیت مقصد

روش انجام: publication_result با provider_msg_id یا unknown

خطا و مرز حساس: دوباره‌ارسال unknown بدون reconciliation ممنوع

قراردادهای موجود: publication_result.schema.json

عدم مسئولیت: ارسال در حالت خروجی خاموش یا retry کورکورانه

## ۳. معماری فرآیند و اتصال به سایر بسته‌ها

| تولیدکننده | مصرف‌کننده | داده عبوری |

| --- | --- | --- |

| P11 | P22 | auto_allowed |

| P20 | P24 | audio_manifest |

| P21 | P24 | video_manifest |

| P22 | P24 | publication_job |

| P22 | P25 | publication_job |

| P23 | P24 | destination_config |

| P23 | P25 | destination_config |

| P14 | P24 | image_manifest |

| P24 | P25 | destination_payload |

| P25 | P26 | publication_result |

| P25 | P17 | publication_result |

هیچ سرویس نباید به پایگاه داده بسته دیگر مستقیماً متصل شود. انتقال‌های بین‌بسته‌ای با API نسخه‌دار یا پیام event_envelope صورت می‌گیرد. Data reference باید شناسه artifact و دسترسی مجاز داشته باشد.

## ۴. طرح دیتابیس و مالکیت داده

## publish.destinations

## مالک: P23 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: destination_id, provider, channel_ref, stream, desk, credential_ref, verified

کلید / ایندکس / قید: UNIQUE(provider,channel_ref)؛ credential امن و مجوز تست‌شده

## publish.jobs

## مالک: P22 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: job_id, article_id, report_id, stream, deadline_at, schedule_at, state, policy_decision_id

کلید / ایندکس / قید: UNIQUE(publication_intent_key)؛ تاریخ انقضا

## publish.payloads

## مالک: P24 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: payload_id, job_id, destination_id, message_ref, image_ref, payload_hash

کلید / ایندکس / قید: UNIQUE(job_id,destination_id)؛ rendition سازگار

## publish.attempts

## مالک: P25 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: attempt_id, job_id, destination_id, status, provider_msg_id, started_at, ended_at

کلید / ایندکس / قید: UNIQUE(job_id,destination_id,attempt_no)؛ وضعیت unknown مهار شود

تمام جدول‌ها دارای کلید UUID، created_at، updated_at در صورت تغییرپذیری، ثبت event/outbox و migrations نسخه‌دار باشند. SQL ابتدایی بسته صرفاً طرح مفهومی است؛ DDL typed باید به‌صورت migration اختصاصی همین تیم نوشته و آزمایش شود.

## ۵. APIهای موردنیاز (پیشنهادی برای OpenAPI)

| روش | مسیر | ورودی | خروجی | مالک |

| --- | --- | --- | --- | --- |

| POST | /v1/destinations | provider,channel,credential_ref | destination_config | P23 |

| POST | /v1/publishing/jobs | approved article/report | publication_job | P22 |

| POST | /v1/publishing/payloads | job + destination | destination_payload | P24 |

| POST | /v1/publishing/dispatch | job_id | publication_result | P25 |

قاعده مشترک: headerهای Authorization/Service Identity، X-Correlation-ID و Idempotency-Key برای عملیات تغییر؛ پاسخ خطا {code,message,correlation_id,details}؛ pagination و rate limit بر اساس سیاست بسته.

## ۶. تنظیمات و اسرار

•  تنظیمات از P02 با scope مشخص: stream, desk, project, destination دریافت می‌شود؛ snapshot و revision در job ثبت شود.

•  API key یا رمز در فایل پیکربندی، سند تحویل، event، log یا جدول عمومی ذخیره نشود؛ فقط credential_ref از Secret Store.

•  بازۀ زمانی در DB UTC و در UI با timezone تهران نمایش داده شود؛ فاصله اجرا و زمان‌بندی قابل تغییر توسط نقش مجاز.

•  امنیت service-to-service از توکن خدمت/کلید موقت و حداقل مجوز پیروی کند؛ عملیات حساس audit شود.

## ۷. مقصدها، CMS و کنترل توقف

CMS هنوز انتخاب نشده است. تعریف interface CMSAdapter و mock برای توسعه ضروری است. Telegram، Bale، Eitaa، Rubika، WhatsApp Business و سایر مقصدها هرکدام connector با حالت configured/verified/active دارند. فعال‌شدن پس از تست API، حق ارسال و credential معتبر مجاز است.

پیش از هر تلاش خارجی، publishing.enabled و کلید stream/report بررسی شود. پاسخ unknown موجب توقف تکرار خودکار تا مشخص‌شدن نتیجه می‌شود. افزودن انتشار خودکار خبر خصوصی مجاز نیست.

## ۸. آزمون‌های پذیرش اختصاصی

•  ثبت مقصد بدون توکن معتبر یا مجوز، آن را فعال تلقی نکند.

•  P25 قبل از هر side effect وضعیت publishing.enabled را بازخوانی کند.

•  ارسال به چند کانال خروجی مستقل با provider_msg_id بدهد.

•  در وضعیت unknown ارسال خودکار دوباره انجام نشود.

•  قطع خروجی foreign فقط انتشار خارجی را متوقف کند نه داخلی.

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

•  نام CMS، شناسه کانال‌های واقعی، credentials و مجوز ارسال هر پیام‌رسان پس از قرارداد مشخص شود.

•  تا آن زمان connectorها با mock و conformance test ارزیابی شوند.
