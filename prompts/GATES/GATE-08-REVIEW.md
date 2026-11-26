# GATE-08 — پذیرش خودکار مرحله 8

**سیاست:** پذیرش خودکار بر پایهٔ [ADR-012](../../docs/decisions/ADR-012-automated-acceptance.md).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## روش ثبت پذیرش

Run ETEMAD architecture, security and contract acceptance checks for phase 8 — دیدبان و رابط‌های کامل. Use the listed tasks and their applicable test and security criteria. Match every check to the current PR head or exact accepted integration revision. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Record commands, exit codes, workflow links and the exact SHA. For missing evidence mark the affected item BLOCKED and run or implement its check in the appropriate scope. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S08-001` → `frontend/src/app/App.tsx` — پوسته اصلی اپ
- `S08-002` → `frontend/src/app/router.tsx` — مسیریابی نقش‌ها
- `S08-003` → `frontend/src/lib/api.ts` — کلاینت API
- `S08-004` → `frontend/src/lib/contracts.ts` — انواع رابط مشترک
- `S08-005` → `frontend/src/components/AppShell.tsx` — قاب برنامه
- `S08-006` → `frontend/src/components/NewsTable.tsx` — جدول اخبار
- `S08-007` → `frontend/src/components/StatusBadge.tsx` — نشان وضعیت
- `S08-008` → `frontend/src/components/SourceCitation.tsx` — ارجاع منبع
- `S08-009` → `frontend/src/features/newsroom/NewsDesk.tsx` — میز خبر
- `S08-010` → `frontend/src/features/editor/ArticleEditor.tsx` — ویرایشگر حرفه‌ای
- `S08-011` → `frontend/src/features/translation/TranslatorWorkspace.tsx` — فضای مترجم مستقل
- `S08-012` → `frontend/src/features/analysis/PoliticalAnalysis.tsx` — رابط تحلیل سیاسی
- `S08-013` → `frontend/src/features/executive/ExecutiveDashboard.tsx` — داشبورد مدیرمسئول
- `S08-014` → `frontend/src/features/owner/OwnerDashboard.tsx` — داشبورد مالک
- `S08-015` → `frontend/src/features/staff/StaffDashboard.tsx` — داشبورد کارکنان
- `S08-016` → `frontend/src/features/sources/SourcesManager.tsx` — پنل منابع
- `S08-017` → `frontend/src/features/publishing/PublishingCenter.tsx` — مرکز انتشار
- `S08-018` → `frontend/src/features/studio/StudioWorkspace.tsx` — پنل استودیو
- `S08-019` → `frontend/src/features/settings/Settings.tsx` — مرکز تنظیمات
- `S08-020` → `frontend/src/features/auth/Login.tsx` — صفحه ورود
- `S08-021` → `frontend/src/i18n/fa.ts` — متن‌های فارسی
- `S08-022` → `frontend/tests/access.spec.ts` — آزمون دسترسی UI
- `S08-023` → `frontend/tests/newsroom.spec.ts` — آزمون میز خبر
- `S08-024` → `frontend/tests/design-system.spec.ts` — آزمون طراحی
- `S08-025` → `frontend/src/lib/auth.ts` — سشن و احراز هویت UI
- `S08-026` → `frontend/src/lib/query.ts` — مدیریت درخواست‌ها
- `S08-027` → `frontend/src/components/PrivateReportGuard.tsx` — حفاظت بصری گزارش ویژه
- `S08-028` → `frontend/src/components/ConfirmAction.tsx` — تأیید عملیات حساس

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- ادغام فقط از مسیر PR حفاظت‌شده پس از موفقیت کنترل‌های الزامی و احراز پیش‌نیازها. اجرای عملیاتی نیازمند مجوز جداگانه است.
