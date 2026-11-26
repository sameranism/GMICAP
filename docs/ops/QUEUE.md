# QUEUE — صف کار ETEMAD (به ترتیب وابستگی)

> قاعده: از بالا به پایین. اولین موردی که وضعیتش `پذیرفته‌شده` نیست، تسک جاری است.
> **هرگز از صف بیرون نرو** مگر صف خالی باشد؛ آن‌وقت اولین تسک وابسته‌برآورده از ماتریس ۲۲۳ تسکی را اضافه کن.
> کار هر تسک = «بررسی وجود فایل با `git ls-files` → اگر موجود بود ولی به DB/API/آزمون وصل نیست، کار = سیم‌کشی، نه بازنویسی».

| # | کد | نوع | مسیر هدف | پیش‌نیاز | معیار پذیرش (یک خط) | وضعیت |
|---|---|---|---|---|---|---|
| 1 | OPS-001 | ops | `docs/decisions/ADR-010-*.md` + `docs/gates/GATE-00.md` | — | ADR با وضعیت `accepted-with-risk` و جدول ۶۲ تسک؛ Gate-00 «باز با پذیرش مشروط» | تست موفق |
| 2 | OPS-002 | ops | `docs/decisions/ADR-011-*.md` + `.github/workflows/merge-guardian.yml` | — | علت 403 اثبات‌شده + ورک‌فلو روی main اجرا و ممیزی review را نشان می‌دهد | باز |
| 3 | S09-023 | matrix | `.github/workflows/backend-ci.yml` | — | CI بک‌اند: lint+type+pytest با خروجی خام؛ روی PR اجرا می‌شود | باز |
| 4 | S03-006 | matrix | `backend/modules/processing/repository.py` | S03-002/003 | ذخیره روی Postgres با unique روی `canonical_url` و `content_hash`؛ تست idempotent | باز |
| 5 | S03-007 | matrix | `backend/migrations/central/002_processing.py` | S03-006 | مهاجرت برگشت‌پذیر و idempotent؛ `upgrade`/`downgrade` در تست | باز |
| 6 | S02-004 | matrix | `backend/modules/domestic/repository.py` | S02-002 | ذخیرهٔ خبر خام + وضعیت دریافت؛ تست تکراری‌نشدن | باز |
| 7 | S02-006 | matrix | `backend/migrations/domestic/001_ingest.py` | S02-004 | مهاجرت برگشت‌پذیر؛ ایندکس زمان دریافت | باز |
| 8 | S02-005 | matrix | `backend/modules/domestic/api.py` | S02-004 | endpoint فهرست/جزئیات با pagination و کد خطای typed | باز |
| 9 | S09-012 | matrix | `backend/tests/test_end_to_end.py` | 4–8 | یک item با `synthetic: true` سه‌بار ارسال → یک رکورد در DB → ۲۰۰ از API؛ + تست منفی feed down | باز |
| 10 | S08-009 | matrix | `frontend/src/features/newsroom/NewsDesk.tsx` | 8 | میز خبر دادهٔ واقعی API را نشان می‌دهد (RTL)؛ با `S08-023` آزمون | باز |
| 11 | S08-023 | matrix | `frontend/tests/newsroom.spec.ts` | 10 | آزمون UI میز خبر: بارگذاری، خالی، خطا | باز |
| 12 | S03-004 | matrix | `backend/modules/processing/classifier.py` | 4 | طبقه‌بندی با قرارداد JSON؛ تست مثبت/منفی | باز |

## قواعد صف
- **WIP = 1**: یک تسک جاری، یک شاخه، یک PR. تسک بعدی شروع نمی‌شود تا PR قبلی سبز و ثبت‌شده باشد.
- تسک‌هایی که به تصمیم کارفرما وابسته‌اند (CMS، برند رسمی، API رسمی، حقوقی نشر) از صف حذف نمی‌شوند؛ با `Mock` و `flag خاموش` پیش می‌روند و در STATE به‌عنوان `blocked-external` ثبت می‌شوند.
- هیچ تسکی از S04/S05/S06 قبل از سبز شدن #9 شروع نمی‌شود.
- وضعیت هر ردیف فقط یکی از این چهار: `باز` / `در حال توسعه` / `تست موفق` / `پذیرفته‌شده`.
