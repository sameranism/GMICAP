# GATE-09 — بازبینی مستقل مرحله 9

**مدل:** Codex (در محیط جدا از نویسندگان؛ اجرا با PR read-only، مگر تسک اصلاح مستقل تصویب شود).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## پرامپت آماده

Act as an independent ETEMAD architecture, security and contract reviewer for phase 9 — اتصال و آزمون یکپارچه. Review ONLY the diff for tasks listed below. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Do not edit code in review run. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S09-001` → `deploy/core/compose.yaml` — استقرار مرکزی
- `S09-002` → `deploy/domestic/compose.yaml` — استقرار داخلی
- `S09-003` → `deploy/foreign/compose.yaml` — استقرار خارجی
- `S09-004` → `deploy/core/Dockerfile` — تصویر هسته مرکزی
- `S09-005` → `deploy/domestic/Dockerfile` — تصویر رصد داخلی
- `S09-006` → `deploy/foreign/Dockerfile` — تصویر رصد خارجی
- `S09-007` → `deploy/frontend/Dockerfile` — تصویر رابط
- `S09-008` → `deploy/env.example` — نمونه متغیرهای محیط
- `S09-009` → `backend/tests/test_contract_integration.py` — آزمون زنجیره قرارداد
- `S09-010` → `backend/tests/test_private_isolation.py` — آزمون جدایی محرمانگی
- `S09-011` → `backend/tests/test_output_switches.py` — آزمون توقف خروجی
- `S09-012` → `backend/tests/test_end_to_end.py` — آزمون زنجیره خبر
- `S09-013` → `quality/load_test.py` — آزمون ظرفیت ۵۰۰ تا ۵۰۰۰ خبر/روز
- `S09-014` → `quality/security_review.md` — چک‌لیست تهدیدها
- `S09-015` → `quality/legal_editorial_review.md` — تأیید مقررات نشر
- `S09-016` → `quality/interface_review.md` — تحویل بصری
- `S09-017` → `quality/acceptance_matrix.md` — ماتریس پذیرش ۲۹ پروژه
- `S09-018` → `docs/runbooks/backup_restore.md` — بازیابی و پشتیبان
- `S09-019` → `docs/runbooks/operations.md` — راهنمای بهره‌برداری
- `S09-020` → `docs/runbooks/rollback.md` — طرح بازگشت
- `S09-021` → `docs/api/openapi-review.md` — ممیزی API و نسخه‌ها
- `S09-022` → `frontend/tests/e2e-critical.spec.ts` — آزمون مسیرهای حیاتی
- `S09-023` → `.github/workflows/backend-ci.yml` — CI بک‌اند
- `S09-024` → `.github/workflows/frontend-ci.yml` — CI فرانت
- `S09-025` → `.github/workflows/security-ci.yml` — CI امنیت
- `S09-026` → `frontend/tests/setup.ts` — تنظیم محیط آزمون UI
- `S09-027` → `deploy/frontend/nginx.conf` — تحویل فایل‌های وب
- `S09-028` → `deploy/README.md` — راهنمای سه محیط اجرا
- `S09-029` → `docs/api/openapi.yaml` — قرارداد API پیاده‌شده

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- بدون ادغام/استقرار خودکار.
