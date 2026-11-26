# GATE-07 — بازبینی مستقل مرحله 7

**مدل:** Codex (در محیط جدا از نویسندگان؛ اجرا با PR read-only، مگر تسک اصلاح مستقل تصویب شود).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## پرامپت آماده

Act as an independent ETEMAD architecture, security and contract reviewer for phase 7 — آوانما. Review ONLY the diff for tasks listed below. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Do not edit code in review run. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S07-001` → `backend/modules/studio/tts.py` — ساخت صوت
- `S07-002` → `backend/modules/studio/subtitles.py` — زیرنویس
- `S07-003` → `backend/modules/studio/renderer.py` — رندر ویدیو
- `S07-004` → `backend/modules/studio/repository.py` — داده استودیو
- `S07-005` → `backend/migrations/central/006_studio.py` — جداول استودیو
- `S07-006` → `backend/tests/test_studio.py` — آزمون آوانما

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- بدون ادغام/استقرار خودکار.
