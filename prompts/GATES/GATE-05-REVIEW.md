# GATE-05 — پذیرش خودکار مرحله 5

**سیاست:** پذیرش خودکار بر پایهٔ [ADR-012](../../docs/decisions/ADR-012-automated-acceptance.md).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## روش ثبت پذیرش

Run ETEMAD architecture, security and contract acceptance checks for phase 5 — ژرفان. Use the listed tasks and their applicable test and security criteria. Match every check to the current PR head or exact accepted integration revision. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Record commands, exit codes, workflow links and the exact SHA. For missing evidence mark the affected item BLOCKED and run or implement its check in the appropriate scope. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S05-001` → `backend/modules/intelligence/analysis.py` — تحلیل رسانه و سیاست
- `S05-002` → `backend/modules/intelligence/evidence.py` — بسته اسناد تحلیل
- `S05-003` → `backend/modules/intelligence/retrieval.py` — بازیابی ایمن
- `S05-004` → `backend/modules/intelligence/chat.py` — چت‌بات تحلیل
- `S05-005` → `backend/modules/intelligence/metrics.py` — محاسبه شاخص‌ها
- `S05-006` → `backend/modules/intelligence/public_reports.py` — چهار گزارش عمومی
- `S05-007` → `backend/modules/intelligence/private_reports.py` — سه گزارش محرمانه
- `S05-008` → `backend/modules/intelligence/repository.py` — جداول ژرفان
- `S05-009` → `backend/migrations/central/004_intelligence.py` — جداول تحلیل
- `S05-010` → `backend/tests/test_intelligence.py` — آزمون ژرفان

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- ادغام فقط از مسیر PR حفاظت‌شده پس از موفقیت کنترل‌های الزامی و احراز پیش‌نیازها. اجرای عملیاتی نیازمند مجوز جداگانه است.
