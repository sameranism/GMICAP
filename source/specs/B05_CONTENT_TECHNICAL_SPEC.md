# B05_CONTENT_TECHNICAL_SPEC


> Extracted without semantic modification from `B05_CONTENT_TECHNICAL_SPEC.docx`. If ambiguous, consult the original DOCX.


## بسته B05 — نگار

Editorial AI | راهنمای اجرایی مستقل تیم توسعه

نسخه 1.1  |  ۳۰ آبان ۱۴۰۵ / ۲۱ نوامبر ۲۰۲۶  |  وضعیت: مشخصات طراحی، نه سامانه عملیاتی

## ۱. مأموریت بسته و مرز مسئولیت

اجرای قواعد واژگان و قوانین محتوا، ترجمه، بازنویسی و تصویرسازی مناسب خبر.

| مشخصه | مقدار |

| --- | --- |

| شناسه بسته | B05 |

| مسئولیت استقرار | پردازش مشترک هسته |

| پروژه‌های تحت مالکیت | P10، P11، P12، P13، P14 |

| فناوری پایه | Python/FastAPI + PostgreSQL + Redis / برای B09: React/TypeScript/Mantine |

| مبنای قرارداد | ۳۰ JSON Schema مصوب v1.0؛ تغییر ناسازگار ممنوع |

| وابستگی پایه | B01 / احراز هویت، تنظیمات، آرشیو و رویدادها |

## ۲. پروژه‌های داخلی، ورودی و خروجی

## P10 — چارچوب/واژه‌نامه

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| قواعد و سبک | editorial_rules نسخه‌دار | ۱۲ و ۱۳ |

وظیفه و منطق: قواعد جایگزینی نسخه‌دار و نمایش diff پیش از تأیید

روش انجام: auto_replace فقط موارد بی‌ابهام؛ title سیاسی suggest_review

خطا و مرز حساس: نقل قول و اصل منبع never_replace

قراردادهای موجود: editorial_rules.schema.json, news_framework.schema.json

عدم مسئولیت: تغییر متن منبع یا نقل‌قول مستقیم

## P11 — کنترل محتوا و انتشار

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| article/public_report/حقوق | validation_decision | ۲۲ |

وظیفه و منطق: کنترل قوانین محتوای رسانه و rights + تشخیص نیازمند بررسی

روش انجام: auto_allowed/human_review/blocked با reason و rule_id

خطا و مرز حساس: خبر بدون مجوز یا ادعای مبهم به صف بازبینی

قراردادهای موجود: validation_decision.schema.json

عدم مسئولیت: فرض‌کردن مجوز انتشار در شرایط عدم قطعیت

## P12 — مترجم هوشمند

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| خبر خارجی/واژه‌نامه | translation | ۱۳ و ۲۶ |

وظیفه و منطق: translation model adapter قابل تعویض و حفظ اصل و تعداد

روش انجام: خروجی چندزبانه با qa و origin span

خطا و مرز حساس: نام‌ها/اعداد ناسازگار نیازمند human_review

قراردادهای موجود: translation.schema.json

عدم مسئولیت: تغییر نام‌ها و اعداد بدون هشدار

## P13 — ویراستار

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| خبر/ترجمه/چارچوب | article | ۱۴ و ۱۱ |

وظیفه و منطق: تیتر، لید، خبر کامل، خلاصه و variant هر کانال

روش انجام: revision immutable همراه با model_version و prompts_ref

خطا و مرز حساس: نقل‌قول اختراعی و ادعای بدون evidence ممنوع

قراردادهای موجود: article.schema.json

## عدم مسئولیت: انتشار مستقیم بدون P11/P22

## P14 — آماده‌سازی تصویر

| ورودی‌های مستقیم | خروجی قراردادی | مصرف‌کننده |

| --- | --- | --- |

| تصویر/لوگو/قالب | image_manifest | ۱۱ و ۲۴ |

وظیفه و منطق: رندر برای ابعاد مقصد و ثبت مجوز تصویر

روش انجام: تصاویر + manifest + synthetic_label

خطا و مرز حساس: تصویر بدون rights_ref برای انتشار مردود

قراردادهای موجود: image_manifest.schema.json

عدم مسئولیت: نمایش تصویر مصنوعی به‌عنوان عکس مستند

## ۳. معماری فرآیند و اتصال به سایر بسته‌ها

| تولیدکننده | مصرف‌کننده | داده عبوری |

| --- | --- | --- |

| P09 | P12 | foreign classified |

| P09 | P13 | domestic classified |

| P10 | P12 | واژه‌نامه |

| P10 | P13 | چارچوب |

| P12 | P13 | translation |

| P12 | P26 | نگهداری |

| P13 | P14 | article |

| P13 | P11 | article |

| P14 | P11 | image_manifest |

| P11 | P22 | auto_allowed |

| P11 | P20 | محتوای تأییدشده |

| P18 | P11 | public_report به کنترل |

| P14 | P24 | image_manifest |

هیچ سرویس نباید به پایگاه داده بسته دیگر مستقیماً متصل شود. انتقال‌های بین‌بسته‌ای با API نسخه‌دار یا پیام event_envelope صورت می‌گیرد. Data reference باید شناسه artifact و دسترسی مجاز داشته باشد.

## ۴. طرح دیتابیس و مالکیت داده

## editorial.rulesets

## مالک: P10 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: ruleset_id, revision, locale, desk, terms_ref, policy_ref, approved_at

کلید / ایندکس / قید: نقل‌قول‌ها هرگز auto_replace نشوند

## editorial.policy_decisions

## مالک: P11 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: decision_id, object_id, decision, reasons_json, policy_revision, decided_at

کلید / ایندکس / قید: UNIQUE(object_id,policy_revision,content_hash)

## editorial.translations

## مالک: P12 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: translation_id, news_id, input_hash, lang_pair, model_ref, text_ref, qa_json

کلید / ایندکس / قید: نگهداری متن اصلی و ارجاع ترجمه

## editorial.articles

## مالک: P13 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: article_id, news_id, desk_id, version, content_ref, summary_ref, state

کلید / ایندکس / قید: UNIQUE(article_id,version)؛ revisionهای غیرقابل ویرایش

## editorial.image_assets

## مالک: P14 | محل فیزیکی: هسته مرکزی

ستون‌های پیشنهادی: image_id, article_id, media_ref, rights_ref, rendition_json, approval

## کلید / ایندکس / قید: حفظ حقوق تصویر و منشأ AI

تمام جدول‌ها دارای کلید UUID، created_at، updated_at در صورت تغییرپذیری، ثبت event/outbox و migrations نسخه‌دار باشند. SQL ابتدایی بسته صرفاً طرح مفهومی است؛ DDL typed باید به‌صورت migration اختصاصی همین تیم نوشته و آزمایش شود.

## ۵. APIهای موردنیاز (پیشنهادی برای OpenAPI)

| روش | مسیر | ورودی | خروجی | مالک |

| --- | --- | --- | --- | --- |

| POST | /v1/editorial/rules/preview | ruleset + sample text | diff/ warnings | P10 |

| POST | /v1/editorial/validate | article/report | validation_decision | P11 |

| POST | /v1/translate | news + target language | translation | P12 |

| POST | /v1/articles/draft | classified news + framework | article | P13 |

| POST | /v1/images/renditions | original image + template | image_manifest | P14 |

قاعده مشترک: headerهای Authorization/Service Identity، X-Correlation-ID و Idempotency-Key برای عملیات تغییر؛ پاسخ خطا {code,message,correlation_id,details}؛ pagination و rate limit بر اساس سیاست بسته.

## ۶. تنظیمات و اسرار

•  تنظیمات از P02 با scope مشخص: stream, desk, project, destination دریافت می‌شود؛ snapshot و revision در job ثبت شود.

•  API key یا رمز در فایل پیکربندی، سند تحویل، event، log یا جدول عمومی ذخیره نشود؛ فقط credential_ref از Secret Store.

•  بازۀ زمانی در DB UTC و در UI با timezone تهران نمایش داده شود؛ فاصله اجرا و زمان‌بندی قابل تغییر توسط نقش مجاز.

•  امنیت service-to-service از توکن خدمت/کلید موقت و حداقل مجوز پیروی کند؛ عملیات حساس audit شود.

## ۷. معیارهای خروجی و مرز صحت

اصل خبر، ارجاع منابع، نسخه مدل و provenance همراه خروجی بمانند. تصمیم نهایی مجوز انتشار متعلق به P11 و برنامه انتشار متعلق به P22 است؛ این بسته نباید مستقیماً پیام به شبکه اجتماعی ارسال کند.

## ۸. آزمون‌های پذیرش اختصاصی

•  مترجم مستقل با فایل تست کار کند و متن اصلی را تغییر ندهد.

•  جایگزینی عنوان حساس سیاسی/مذهبی بدون بازبینی خودکار اعمال نشود.

•  خبر فاقد حقوق بازنشر مجاز به انتشار متن کامل نشود.

•  تصویر AI با synthetic label و rights provenance مشخص شود.

•  هنگام عدم دسترسی provider هوش مصنوعی، مدل جایگزین مطابق سیاست انتخاب شود.

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

•  ارائه‌دهنده AI اصلی تعیین نشده؛ model router و quota قابل تغییر باشد.

•  حقوق بازنشر منابع و تصویر باید در P03 ثبت شود؛ متن بدون حق بازنشر حذف یا لینک‌محور شود.
