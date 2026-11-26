# GATE-06 — بازبینی مستقل مرحله 6

**مدل:** Codex (در محیط جدا از نویسندگان؛ اجرا با PR read-only، مگر تسک اصلاح مستقل تصویب شود).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## پرامپت آماده

Act as an independent ETEMAD architecture, security and contract reviewer for phase 6 — رسان. Review ONLY the diff for tasks listed below. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Do not edit code in review run. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S06-001` → `backend/modules/publishing/scheduler.py` — صف انتشار
- `S06-002` → `backend/modules/publishing/destinations.py` — دفتر مقصدها
- `S06-003` → `backend/modules/publishing/formatter.py` — قالب‌بندی مقصد
- `S06-004` → `backend/modules/publishing/dispatcher.py` — ارسال چندکاناله
- `S06-005` → `backend/adapters/base.py` — قرارداد آداپتور انتشار
- `S06-006` → `backend/adapters/telegram.py` — آداپتور تلگرام
- `S06-007` → `backend/adapters/bale.py` — آداپتور بله
- `S06-008` → `backend/adapters/eitaa.py` — آداپتور ایتا
- `S06-009` → `backend/adapters/rubika.py` — آداپتور روبیکا
- `S06-010` → `backend/adapters/whatsapp.py` — آداپتور واتساپ بیزینس
- `S06-011` → `backend/adapters/cms.py` — آداپتور CMS نامشخص
- `S06-012` → `backend/adapters/registry.py` — ثبت آداپتورها
- `S06-013` → `backend/modules/publishing/repository.py` — داده نشر
- `S06-014` → `backend/migrations/central/005_publishing.py` — جداول انتشار
- `S06-015` → `backend/tests/test_publishing.py` — آزمون رسان

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- بدون ادغام/استقرار خودکار.
