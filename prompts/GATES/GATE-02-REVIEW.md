# GATE-02 — پذیرش خودکار مرحله 2

**سیاست:** پذیرش خودکار بر پایهٔ [ADR-012](../../docs/decisions/ADR-012-automated-acceptance.md).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## روش ثبت پذیرش

Run ETEMAD architecture, security and contract acceptance checks for phase 2 — رصد داخلی و خارجی + پایه طراحی. Use the listed tasks and their applicable test and security criteria. Match every check to the current PR head or exact accepted integration revision. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Record commands, exit codes, workflow links and the exact SHA. For missing evidence mark the affected item BLOCKED and run or implement its check in the appropriate scope. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S02-001` → `backend/modules/domestic/feed_client.py` — کلاینت خوراک داخلی
- `S02-002` → `backend/modules/domestic/collector.py` — استخراج اولیه داخلی
- `S02-003` → `backend/modules/domestic/scheduler.py` — زمان‌بندی داخلی
- `S02-004` → `backend/modules/domestic/repository.py` — DB داخلی
- `S02-005` → `backend/modules/domestic/api.py` — API داخلی
- `S02-006` → `backend/migrations/domestic/001_ingest.py` — مهاجرت DB داخلی
- `S02-007` → `backend/tests/test_domestic.py` — آزمون ایران‌بان
- `S02-008` → `backend/modules/foreign/country_discovery.py` — کشف رسانه کشور
- `S02-009` → `backend/modules/foreign/feed_client.py` — کلاینت خوراک خارجی
- `S02-010` → `backend/modules/foreign/collector.py` — خبر خام خارجی
- `S02-011` → `backend/modules/foreign/bridge.py` — پل امن خارجی به مرکز
- `S02-012` → `backend/modules/foreign/repository.py` — DB خارجی
- `S02-013` → `backend/modules/foreign/api.py` — API جهان‌بان
- `S02-014` → `backend/migrations/foreign/001_ingest.py` — مهاجرت DB خارجی
- `S02-015` → `backend/tests/test_foreign.py` — آزمون جهان‌بان
- `S02-016` → `frontend/src/design-system/tokens.json` — توکن‌های DTCG
- `S02-017` → `frontend/src/design-system/theme.css` — تم روشن و تاریک
- `S02-018` → `frontend/src/styles/globals.css` — استایل جهانی
- `S02-019` → `frontend/src/design-system/README.md` — راهنمای سیستم طراحی
- `S02-020` → `frontend/src/assets/BRAND_ASSETS_REQUIRED.md` — لیست دارایی‌های رسمی برند

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- ادغام فقط از مسیر PR حفاظت‌شده پس از موفقیت کنترل‌های الزامی و احراز پیش‌نیازها. اجرای عملیاتی نیازمند مجوز جداگانه است.
