# GATE-01 — بازبینی مستقل مرحله 1

**مدل:** Codex (در محیط جدا از نویسندگان؛ اجرا با PR read-only، مگر تسک اصلاح مستقل تصویب شود).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## پرامپت آماده

Act as an independent ETEMAD architecture, security and contract reviewer for phase 1 — بنیان و زیرساخت مرکزی. Review ONLY the diff for tasks listed below. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Do not edit code in review run. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S01-001` → `backend/app/main.py` — ورود به API
- `S01-002` → `backend/core/contracts.py` — مصرف قراردادها
- `S01-003` → `backend/core/settings_service.py` — تنظیمات نسخه‌دار
- `S01-004` → `backend/core/output_switches.py` — سه کلید مستقل خروجی
- `S01-005` → `backend/core/sources_service.py` — دفتر منابع
- `S01-006` → `backend/core/auth.py` — احراز هویت
- `S01-007` → `backend/core/permissions.py` — کنترل دسترسی RBAC
- `S01-008` → `backend/core/audit.py` — لاگ ممیزی
- `S01-009` → `backend/core/secrets.py` — مرجع محرمانه
- `S01-010` → `backend/core/archive.py` — ثبت آرشیو و نسخه‌ها
- `S01-011` → `backend/core/events.py` — پوش رویدادها
- `S01-012` → `backend/core/jobs.py` — مدیریت کارها
- `S01-013` → `backend/core/outbox.py` — تراکنش و Outbox
- `S01-014` → `backend/core/orchestrator.py` — گردش کار
- `S01-015` → `backend/core/ai_gateway.py` — درگاه چندمدلی
- `S01-016` → `backend/core/db.py` — پایگاه مرکزی
- `S01-017` → `backend/core/object_store.py` — فایل‌ها در مخزن شیء
- `S01-018` → `backend/migrations/central/001_baseline.py` — مهاجرت پایه هسته
- `S01-019` → `backend/tests/test_contracts.py` — آزمون قراردادها
- `S01-020` → `backend/tests/test_security.py` — آزمون منفی امنیت
- `S01-021` → `backend/tests/test_orchestration.py` — آزمون هماهنگ‌کننده
- `S01-022` → `backend/tests/test_ai_gateway.py` — آزمون AI Gateway
- `S01-023` → `backend/alembic.ini` — پیکربندی Alembic
- `S01-024` → `backend/migrations/env.py` — محیط مهاجرت پایگاه‌ها
- `S01-025` → `backend/app/dependencies.py` — تزریق وابستگی مشترک
- `S01-026` → `backend/app/api_router.py` — روتر پایه نسخه‌دار
- `S01-027` → `backend/core/errors.py` — استاندارد خطا
- `S01-028` → `backend/core/health.py` — آمادگی و سلامت
- `S01-029` → `backend/core/observability.py` — رهگیری و ثبت لاگ
- `S01-030` → `backend/tests/conftest.py` — فیکسچرهای آزمون

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- بدون ادغام/استقرار خودکار.
