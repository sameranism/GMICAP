# GATE-03 — پذیرش خودکار مرحله 3

**سیاست:** پذیرش خودکار بر پایهٔ [ADR-012](../../docs/decisions/ADR-012-automated-acceptance.md).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## روش ثبت پذیرش

Run ETEMAD architecture, security and contract acceptance checks for phase 3 — خبرپرداز. Use the listed tasks and their applicable test and security criteria. Match every check to the current PR head or exact accepted integration revision. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Record commands, exit codes, workflow links and the exact SHA. For missing evidence mark the affected item BLOCKED and run or implement its check in the appropriate scope. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S03-001` → `backend/modules/processing/extractor.py` — استخراج مجاز متن
- `S03-002` → `backend/modules/processing/normalizer.py` — استانداردسازی
- `S03-003` → `backend/modules/processing/deduplicator.py` — حذف تکرار منطقی
- `S03-004` → `backend/modules/processing/classifier.py` — طبقه‌بندی سرویس
- `S03-005` → `backend/modules/processing/router.py` — مسیریابی خبر
- `S03-006` → `backend/modules/processing/repository.py` — ذخیره نتایج پردازش
- `S03-007` → `backend/migrations/central/002_processing.py` — مهاجرت داده پردازش
- `S03-008` → `backend/tests/test_processing.py` — آزمون پردازش

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- ادغام فقط از مسیر PR حفاظت‌شده پس از موفقیت کنترل‌های الزامی و احراز پیش‌نیازها. اجرای عملیاتی نیازمند مجوز جداگانه است.
