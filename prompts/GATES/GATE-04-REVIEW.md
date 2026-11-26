# GATE-04 — بازبینی مستقل مرحله 4

**مدل:** Codex (در محیط جدا از نویسندگان؛ اجرا با PR read-only، مگر تسک اصلاح مستقل تصویب شود).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## پرامپت آماده

Act as an independent ETEMAD architecture, security and contract reviewer for phase 4 — نگار. Review ONLY the diff for tasks listed below. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Do not edit code in review run. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S04-001` → `backend/modules/editorial/glossary.py` — واژه‌نامه
- `S04-002` → `backend/modules/editorial/policy.py` — دروازه قانون و مجوز نشر
- `S04-003` → `backend/modules/editorial/quality.py` — کنترل کیفیت محتوا
- `S04-004` → `backend/modules/editorial/translator.py` — مترجم مستقل
- `S04-005` → `backend/modules/editorial/editor.py` — ویراستار هوشمند
- `S04-006` → `backend/modules/editorial/image_processor.py` — پردازش تصویر
- `S04-007` → `backend/modules/editorial/repository.py` — حافظه خروجی نگار
- `S04-008` → `backend/migrations/central/003_editorial.py` — جداول نگار
- `S04-009` → `backend/tests/test_editorial.py` — آزمون نگار

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- بدون ادغام/استقرار خودکار.
