# B01_FOUNDATION_TECHNICAL_SPEC


> Extracted without semantic modification from `B01_FOUNDATION_TECHNICAL_SPEC.docx`. If ambiguous, consult the original DOCX.


## بسته B01 — بنیان

Etemad Core | راهنمای اجرایی مستقل تیم توسعه

نسخه 1.1  |  ۳۰ آبان ۱۴۰۵ / ۲۱ نوامبر ۲۰۲۶  |  وضعیت: مشخصات طراحی، نه سامانه عملیاتی

## ۱. مأموریت بسته و مرز مسئولیت

قرارداد داده، منبع، تنظیمات، هویت، آرشیو و هماهنگی را به‌صورت سرویس‌های مستقل و قابل آزمون فراهم می‌کند.

| مشخصه | مقدار |

| --- | --- |

| شناسه بسته | B01 |

| مسئولیت استقرار | مشترک / هسته مرکزی |

| پروژه‌های تحت مالکیت | P01، P02، P03، P26، P28، P29 |

| فناوری پایه | Python/FastAPI + PostgreSQL + Redis / برای B09: React/TypeScript/Mantine |

| مبنای قرارداد | ۳۰ JSON Schema مصوب v1.0؛ تغییر ناسازگار ممنوع |

| وابستگی پایه | B01 / احراز هویت، تنظیمات، آرشیو و رویدادها |

## ۲. پروژه‌های داخلی، ورودی و خروجی

## P01 — استاندارد داده

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| نیاز سایر بخش‌ها | schemas/*.schema.json | همه بخش‌ها |

وظیفه و منطق: انتشار مجموعه قراردادها با semver و JSON Schema Draft 2020-12

روش انجام: دریافت schema_id؛ اعتبارسنجی و برگرداندن خطاهای دقیق

خطا و مرز حساس: نمونه معتبر/نامعتبر برای هر قرارداد و ماتریس سازگاری

قراردادهای موجود: event_envelope.schema.json, workflow_status.schema.json

عدم مسئولیت: پیاده‌سازی دریافت یا ارسال خبر

## P02 — تنظیمات مدیریتی

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| درخواست مدیر/قواعد | output_controls و تنظیمات نسخه‌دار | همه با مجوز |

وظیفه و منطق: ثبت تنظیمات scoped و نسخه‌دار با audit؛ تعارض revision=409

روش انجام: POST تغییر با expected_revision و actor permission

خطا و مرز حساس: تغییر بدون مجوز 403؛ ارسال هنگام publishing off مسدود

قراردادهای موجود: output_controls.schema.json, schedule_config.schema.json, ai_models_config.schema.json, news_framework.schema.json

عدم مسئولیت: ذخیره متن آشکار API key در JSON و رابط

## P03 — مدیریت منابع

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| URL/RSS/API/کشور | source_registry | ۵ و ۶ |

وظیفه و منطق: ثبت منابع و بررسی حقوق انتشار و سلامت با credential_ref

روش انجام: Feed validation؛ snapshot پیکربندی domestic/foreign

خطا و مرز حساس: URL ناسالم، محدودیت rate و منبع فاقد rights

قراردادهای موجود: source_registry.schema.json

عدم مسئولیت: افزودن خودکار منبع بدون مجوز و آزمون

## P26 — آرشیو

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| خبر/گزارش/نتیجه | API و شناسه شیء | ۸ و ۱۵ و ۱۷ و ۲۷ |

وظیفه و منطق: آرشیو immutable اصل خبر و manifestهای مرحله‌ای

روش انجام: جست‌وجوی متمرکز فقط با مجوز؛ artifact refs

خطا و مرز حساس: retention و right-to-reuse inherited

قراردادهای موجود: archive_record.schema.json

عدم مسئولیت: افشای محتوای محرمانه در جست‌وجو

## P28 — کنترل دسترسی

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| هویت/نقش/منبع | access_decision | همه پروژه‌ها |

وظیفه و منطق: شناسه یکتا و MFA برای owner/editor، reset امن

روش انجام: signed permission decision کوتاه‌عمر، RLS

خطا و مرز حساس: حساب یازدهم و رمز مشترک رد شوند

قراردادهای موجود: access_decision.schema.json

عدم مسئولیت: اعطای دسترسی پیش‌فرض بدون مجوز صریح

## P29 — هماهنگ‌کننده

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| رویداد/وضعیت | event_envelope/Workflow | همه پروژه‌ها |

وظیفه و منطق: پیوند رویدادها با inbox/outbox و idempotency

روش انجام: job status و dead-letter با correlation_id

خطا و مرز حساس: duplicate, schema mismatch, expired job

قراردادهای موجود: event_envelope.schema.json, workflow_status.schema.json

عدم مسئولیت: پیاده‌سازی منطق مترجم، ویراستار یا ناشر

## ۳. معماری فرآیند و اتصال به سایر بسته‌ها

| تولیدکننده | مصرف‌کننده | داده عبوری |

| --- | --- | --- |

| P04 | P03 | بسته منابع کشور |

| P03 | P05 | منابع داخلی |

| P03 | P06 | منابع خارجی |

| P07 | P26 | آرشیو |

| P26 | P08 | سابقه تکرار |

| P12 | P26 | نگهداری |

| P26 | P15 | منابع و آرشیو |

| P26 | P17 | داده محاسبه |

| P26 | P27 | جست‌وجو |

| P25 | P26 | publication_result |

هیچ سرویس نباید به پایگاه داده بسته دیگر مستقیماً متصل شود. انتقال‌های بین‌بسته‌ای با API نسخه‌دار یا پیام event_envelope صورت می‌گیرد. Data reference باید شناسه artifact و دسترسی مجاز داشته باشد.

## ۴. طرح دیتابیس و مالکیت داده

## control.config_revisions

## مالک: P02 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: config_id, version_no, scope, value_json, changed_by, effective_at

کلید / ایندکس / قید: UNIQUE(config_id,version_no)؛ تغییرات immutable

## control.output_switches

## مالک: P02 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: switch_key, scope, enabled, revision, updated_by, updated_at

کلید / ایندکس / قید: UNIQUE(switch_key,scope)؛ پیش از side effect خوانده شود

## control.editorial_rules

## مالک: P02/P10 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: rule_id, revision, desk, kind, rule_json, approved_by

کلید / ایندکس / قید: نسخه‌بندی و ارجاع به قواعد، بدون تغییر متن منبع

## sources.source_registry

## مالک: P03 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: source_id, country, stream, url, mode, language, rights_scope, state

کلید / ایندکس / قید: UNIQUE(stream,url_normalized)؛ API keys فقط credential_ref

## identity.users

## مالک: P28 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: user_id, username, role_id, password_hash, must_reset, is_active, created_at

کلید / ایندکس / قید: سقف ۱۰ حساب انسانی فعال؛ گذرواژه هش‌شده؛ مجوز مدیریت کاربران

## identity.roles_permissions

## مالک: P28 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: role_id, permission_key, resource_scope, condition_json

کلید / ایندکس / قید: کلید(role_id,permission_key,resource_scope)

## identity.auth_sessions

## مالک: P28 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: session_id, user_id, expires_at, revoked_at, client_fingerprint

کلید / ایندکس / قید: جلسه کوتاه‌عمر + MFA نقش ممتاز؛ audit

## archive.news_records

## مالک: P26 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: news_id, stream, source_id, title, source_ref, published_at, received_at, classification

کلید / ایندکس / قید: UNIQUE(news_id)؛ شاخص(stream,published_at)؛ متن منبع immutable

## archive.artifact_index

## مالک: P26 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: artifact_id, object_type, owner_project, object_uri, sha256, visibility, created_at

کلید / ایندکس / قید: صرفاً URI امن؛ فایل بزرگ در Object Store

## orchestration.jobs

## مالک: P29 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: job_id, type, project_id, state, idempotency_key, attempts, deadline_at

کلید / ایندکس / قید: UNIQUE(project_id,idempotency_key)؛ retry bounded

## orchestration.outbox

## مالک: P29 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: event_id, topic, aggregate_id, payload_ref, published_at, created_at

کلید / ایندکس / قید: Transactional Outbox و نگهداری محدود

## security.audit_log

## مالک: P28 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: audit_id, actor_id, action, object_type, object_id, time, reason

کلید / ایندکس / قید: append-only؛ پاک‌کردن توسط نقش عملیاتی ممنوع

تمام جدول‌ها دارای کلید UUID، created_at، updated_at در صورت تغییرپذیری، ثبت event/outbox و migrations نسخه‌دار باشند. SQL ابتدایی بسته صرفاً طرح مفهومی است؛ DDL typed باید به‌صورت migration اختصاصی همین تیم نوشته و آزمایش شود.

## ۵. APIهای موردنیاز (پیشنهادی برای OpenAPI)

| روش | مسیر | ورودی | خروجی | مالک |

| --- | --- | --- | --- | --- |

| POST | /v1/auth/login | نام کاربری و گذرواژه | cookie/session کوتاه‌عمر | P28 |

| POST | /v1/auth/first-login/reset | رمز موقت و رمز جدید | جلسه تازه | P28 |

| GET | /v1/config/effective | scope/stream | پیکربندی نسخه‌دار | P02 |

| POST | /v1/output-controls | key,scope,enabled,revision | audit + وضعیت | P02 |

| POST | /v1/sources | source registry | source_id | P03 |

| GET | /v1/artifacts/{id} | شناسه + هویت | URI امن یا داده مجاز | P26 |

| POST | /v1/events | event_envelope | event_id | P29 |

قاعده مشترک: headerهای Authorization/Service Identity، X-Correlation-ID و Idempotency-Key برای عملیات تغییر؛ پاسخ خطا {code,message,correlation_id,details}؛ pagination و rate limit بر اساس سیاست بسته.

## ۶. تنظیمات و اسرار

•  تنظیمات از P02 با scope مشخص: stream, desk, project, destination دریافت می‌شود؛ snapshot و revision در job ثبت شود.

•  API key یا رمز در فایل پیکربندی، سند تحویل، event، log یا جدول عمومی ذخیره نشود؛ فقط credential_ref از Secret Store.

•  بازۀ زمانی در DB UTC و در UI با timezone تهران نمایش داده شود؛ فاصله اجرا و زمان‌بندی قابل تغییر توسط نقش مجاز.

•  امنیت service-to-service از توکن خدمت/کلید موقت و حداقل مجوز پیروی کند؛ عملیات حساس audit شود.

## ۷. سیاست کاربران ۱۰نفره و کنترل محرمانگی

| نقش | تعداد پیش‌فرض | حق دسترسی و محدودیت |

| --- | --- | --- |

| owner | ۱ | داشبورد مالک، تنظیمات و حساب‌ها؛ عدم دسترسی private بدون grant ویژه |

| editor_in_chief | ۱ | داشبورد مدیرمسئول، گزارش‌های ۵ تا ۷، مجوز تصمیم تحریریه |

| staff | تا ۸ | حساب یکتا، دسترسی حداقلی سرویس، بدون سه گزارش محرمانه |

رمز اولیه برای کارکنان باید توسط سامانه از CSPRNG تولید و یک‌بار به‌صورت محرمانه تحویل شود؛ رمز در این سند ساخته نشده و هیچ رمز مشترکی مجاز نیست. Argon2id برای ذخیره hash، MFA برای owner/editor و reset اجباری اولین ورود.

## ۸. آزمون‌های پذیرش اختصاصی

•  با ۱۰ حساب فعال، ایجاد حساب یازدهم با خطای صریح رد می‌شود.

## •  رمزهای آزمایشی در هیچ سند، لاگ یا پاسخ API چاپ نمی‌شوند.

•  کاربر فاقد مجوز با لینک مستقیم، private_report را نمی‌بیند.

## •  خاموش‌کردن انتشار پیش از ارسال خارجی، مسیر P25 را مسدود می‌کند.

•  رویداد تکراری با idempotency_key خروجی دوباره تولید نمی‌کند.

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
