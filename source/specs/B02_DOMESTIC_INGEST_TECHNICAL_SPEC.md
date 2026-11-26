# B02_DOMESTIC_INGEST_TECHNICAL_SPEC


> Extracted without semantic modification from `B02_DOMESTIC_INGEST_TECHNICAL_SPEC.docx`. If ambiguous, consult the original DOCX.


## بسته B02 — ایران‌بان

Iran Monitor | راهنمای اجرایی مستقل تیم توسعه

نسخه 1.1  |  ۳۰ آبان ۱۴۰۵ / ۲۱ نوامبر ۲۰۲۶  |  وضعیت: مشخصات طراحی، نه سامانه عملیاتی

## ۱. مأموریت بسته و مرز مسئولیت

دریافت و پایش منابع داخلی با صف، زمان‌بندی و پایگاه داده جدا از رصد خارجی.

| مشخصه | مقدار |

| --- | --- |

| شناسه بسته | B02 |

| مسئولیت استقرار | محیط داخلی مستقل |

| پروژه‌های تحت مالکیت | P05 |

| فناوری پایه | Python/FastAPI + PostgreSQL + Redis / برای B09: React/TypeScript/Mantine |

| مبنای قرارداد | ۳۰ JSON Schema مصوب v1.0؛ تغییر ناسازگار ممنوع |

| وابستگی پایه | B01 / احراز هویت، تنظیمات، آرشیو و رویدادها |

## ۲. پروژه‌های داخلی، ورودی و خروجی

## P05 — دریافت داخلی

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| فهرست منابع داخلی | raw_news:domestic | ۷ |

وظیفه و منطق: پایش مستقل منابع ایرانی با conditional GET و poll schedule

روش انجام: Raw item immutable به همراه fingerprint و source_ref

خطا و مرز حساس: 429/timeout؛ عدم ورود به DB خارجی

قراردادهای موجود: raw_news.schema.json

عدم مسئولیت: ترجمه، تحلیل یا تصمیم انتشار

## ۳. معماری فرآیند و اتصال به سایر بسته‌ها

| تولیدکننده | مصرف‌کننده | داده عبوری |

| --- | --- | --- |

| P03 | P05 | منابع داخلی |

| P05 | P07 | raw_news |

هیچ سرویس نباید به پایگاه داده بسته دیگر مستقیماً متصل شود. انتقال‌های بین‌بسته‌ای با API نسخه‌دار یا پیام event_envelope صورت می‌گیرد. Data reference باید شناسه artifact و دسترسی مجاز داشته باشد.

## ۴. طرح دیتابیس و مالکیت داده

## domestic.sources_snapshot

## مالک: P05 | محل فیزیکی: سرور داخلی

ستون‌های پیشنهادی: source_id, version, url, mode, poll_interval_s, enabled

کلید / ایندکس / قید: نسخه local snapshot از P03

## domestic.poll_state

## مالک: P05 | محل فیزیکی: سرور داخلی

ستون‌های پیشنهادی: source_id, etag, last_modified, last_success_at, next_poll_at

کلید / ایندکس / قید: UNIQUE(source_id)؛ conditional HTTP GET

## domestic.raw_items

## مالک: P05 | محل فیزیکی: سرور داخلی

ستون‌های پیشنهادی: raw_id, source_id, source_url, fetched_at, content_ref, source_hash, state

کلید / ایندکس / قید: UNIQUE(source_id,source_hash)؛ متن مجاز در ذخیره‌ساز محلی

تمام جدول‌ها دارای کلید UUID، created_at، updated_at در صورت تغییرپذیری، ثبت event/outbox و migrations نسخه‌دار باشند. SQL ابتدایی بسته صرفاً طرح مفهومی است؛ DDL typed باید به‌صورت migration اختصاصی همین تیم نوشته و آزمایش شود.

## ۵. APIهای موردنیاز (پیشنهادی برای OpenAPI)

| روش | مسیر | ورودی | خروجی | مالک |

| --- | --- | --- | --- | --- |

| POST | /v1/domestic/poll | source_id یا batch | job_id | P05 |

| GET | /v1/domestic/health | - | آمار freshness و خطا | P05 |

قاعده مشترک: headerهای Authorization/Service Identity، X-Correlation-ID و Idempotency-Key برای عملیات تغییر؛ پاسخ خطا {code,message,correlation_id,details}؛ pagination و rate limit بر اساس سیاست بسته.

## ۶. تنظیمات و اسرار

•  تنظیمات از P02 با scope مشخص: stream, desk, project, destination دریافت می‌شود؛ snapshot و revision در job ثبت شود.

•  API key یا رمز در فایل پیکربندی، سند تحویل، event، log یا جدول عمومی ذخیره نشود؛ فقط credential_ref از Secret Store.

•  بازۀ زمانی در DB UTC و در UI با timezone تهران نمایش داده شود؛ فاصله اجرا و زمان‌بندی قابل تغییر توسط نقش مجاز.

•  امنیت service-to-service از توکن خدمت/کلید موقت و حداقل مجوز پیروی کند؛ عملیات حساس audit شود.

## ۷. مرز شبکه و پایگاه داده

هر جریان PostgreSQL و Redis مستقل خود را دارد. سرور خارجی فقط به درگاه انتقال امن مجاز وصل می‌شود و هیچ مجوز SQL به هسته مرکزی ندارد. تکرار رویداد از طریق fingerprint و idempotency مدیریت می‌شود، نه زیرساخت مستقل و پیچیده مدیریت اختلال اینترنت.

## ۸. آزمون‌های پذیرش اختصاصی

•  RSS/Atom یا API آزمایشی تبدیل به raw_news دارای source_id و checksum شود.

•  درخواست با ETag/Last-Modified تنها آیتم جدید ایجاد می‌کند.

•  خروجی داخلی با stream=domestic و DB مستقل ذخیره می‌شود.

•  در صورت عدم دسترسی به مرکز، داده محلی محفوظ و ارسال تکراری کنترل شود.

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
