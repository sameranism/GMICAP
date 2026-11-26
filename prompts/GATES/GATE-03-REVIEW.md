# GATE-03 — بازبینی مستقل مرحله 3

**مدل:** Codex (در محیط جدا از نویسندگان؛ اجرا با PR read-only، مگر تسک اصلاح مستقل تصویب شود).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## پرامپت آماده

Act as an independent ETEMAD architecture, security and contract reviewer for phase 3 — خبرپرداز. Review ONLY the diff for tasks listed below. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Do not edit code in review run. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

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
- بدون ادغام/استقرار خودکار.
