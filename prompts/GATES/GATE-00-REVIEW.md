# GATE-00 — پذیرش خودکار مرحله 0

**سیاست:** پذیرش خودکار بر پایهٔ [ADR-012](../../docs/decisions/ADR-012-automated-acceptance.md).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## روش ثبت پذیرش

Run ETEMAD architecture, security and contract acceptance checks for phase 0 — مرحله صفر: قفل قرارداد و قوانین. Use the listed tasks and their applicable test and security criteria. Match every check to the current PR head or exact accepted integration revision. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Record commands, exit codes, workflow links and the exact SHA. For missing evidence mark the affected item BLOCKED and run or implement its check in the appropriate scope. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## کنترل پایه تکرارپذیر
- `python tools/check_gate00.py` موجودی ۶۲ تسک و پیوست‌ها، اثر انگشت ۳۰ قرارداد و آزمون‌های ساختاری مثبت و منفی را بررسی می‌کند. در مسیر CI قرارداد اجرا می‌شود.
- `python tools/check_boundaries.py --self-test` و `python tools/check_boundaries.py` مرز معماری را بررسی می‌کنند.
- وضعیت نهایی از [دفتر شواهد](../../docs/gates/GATE-00.md) خوانده می‌شود. در نتیجهٔ نهایی شواهد ممیزی معنایی، کنترل محرمانگی و مجوز و اجرای واقعی CI باید برای همان نسخه درج شوند.

## تسک‌های این مرحله
- `S00-001` → `AGENTS.md` — قواعد پایه عامل‌ها
- `S00-002` → `.cursor/rules/architecture.mdc` — قواعد جداسازی بسته‌ها
- `S00-003` → `.cursor/rules/contracts.mdc` — قواعد قراردادها
- `S00-004` → `.cursor/rules/security.mdc` — قواعد امنیت و محرمانگی
- `S00-005` → `.cursor/rules/frontend.mdc` — قواعد سیستم طراحی اعتماد
- `S00-006` → `.cursor/rules/testing.mdc` — قواعد شواهد آزمون
- `S00-007` → `.cursor/rules/cloud-agent.mdc` — قواعد Cloud Agent
- `S00-008` → `docs/decisions/ADR-001-architecture.md` — معماری و مرزبندی
- `S00-009` → `docs/decisions/ADR-002-ui-design-system.md` — تغییر فناوری UI
- `S00-010` → `docs/decisions/ADR-003-storage-ownership.md` — مالکیت پایگاه داده
- `S00-011` → `docs/decisions/ADR-004-publishing-gates.md` — دروازه انتشار
- `S00-012` → `docs/decisions/ADR-005-auth-roles.md` — حساب‌ها و نقش‌ها
- `S00-013` → `docs/decisions/ADR-006-ai-provider-gateway.md` — درگاه مدل‌های قابل تعویض
- `S00-014` → `docs/architecture/SYSTEM_MAP.md` — فهرست ارتباطات و مرزها
- `S00-015` → `docs/architecture/CONTRACT_OWNERSHIP.md` — مالک هر قرارداد
- `S00-016` → `docs/architecture/DATABASE_REVIEW.md` — مرور طرح دیتابیس
- `S00-017` → `tools/validate_contracts.py` — ابزار اعتبارسنجی قراردادهای نسخه صفر
- `S00-018` → `.github/workflows/contract-check.yml` — آزمون قراردادی CI
- `S00-019` → `backend/pyproject.toml` — وابستگی‌های پایتون
- `S00-020` → `frontend/package.json` — وابستگی‌های رابط
- `S00-021` → `README.md` — راهنمای ریشه مخزن
- `S00-022` → `docs/contract-audits/access_decision.md` — ممیزی قرارداد access_decision
- `S00-023` → `docs/contract-audits/ai_models_config.md` — ممیزی قرارداد ai_models_config
- `S00-024` → `docs/contract-audits/analysis_chat_response.md` — ممیزی قرارداد analysis_chat_response
- `S00-025` → `docs/contract-audits/analysis_result.md` — ممیزی قرارداد analysis_result
- `S00-026` → `docs/contract-audits/archive_record.md` — ممیزی قرارداد archive_record
- `S00-027` → `docs/contract-audits/article.md` — ممیزی قرارداد article
- `S00-028` → `docs/contract-audits/audio_manifest.md` — ممیزی قرارداد audio_manifest
- `S00-029` → `docs/contract-audits/classified_news.md` — ممیزی قرارداد classified_news
- `S00-030` → `docs/contract-audits/cluster_result.md` — ممیزی قرارداد cluster_result
- `S00-031` → `docs/contract-audits/country_source_pack.md` — ممیزی قرارداد country_source_pack
- `S00-032` → `docs/contract-audits/destination_config.md` — ممیزی قرارداد destination_config
- `S00-033` → `docs/contract-audits/destination_payload.md` — ممیزی قرارداد destination_payload
- `S00-034` → `docs/contract-audits/editorial_rules.md` — ممیزی قرارداد editorial_rules
- `S00-035` → `docs/contract-audits/event_envelope.md` — ممیزی قرارداد event_envelope
- `S00-036` → `docs/contract-audits/image_manifest.md` — ممیزی قرارداد image_manifest
- `S00-037` → `docs/contract-audits/metrics_snapshot.md` — ممیزی قرارداد metrics_snapshot
- `S00-038` → `docs/contract-audits/news_framework.md` — ممیزی قرارداد news_framework
- `S00-039` → `docs/contract-audits/normalized_news.md` — ممیزی قرارداد normalized_news
- `S00-040` → `docs/contract-audits/output_controls.md` — ممیزی قرارداد output_controls
- `S00-041` → `docs/contract-audits/private_report.md` — ممیزی قرارداد private_report
- `S00-042` → `docs/contract-audits/public_report.md` — ممیزی قرارداد public_report
- `S00-043` → `docs/contract-audits/publication_job.md` — ممیزی قرارداد publication_job
- `S00-044` → `docs/contract-audits/publication_result.md` — ممیزی قرارداد publication_result
- `S00-045` → `docs/contract-audits/raw_news.md` — ممیزی قرارداد raw_news
- `S00-046` → `docs/contract-audits/schedule_config.md` — ممیزی قرارداد schedule_config
- `S00-047` → `docs/contract-audits/source_registry.md` — ممیزی قرارداد source_registry
- `S00-048` → `docs/contract-audits/translation.md` — ممیزی قرارداد translation
- `S00-049` → `docs/contract-audits/validation_decision.md` — ممیزی قرارداد validation_decision
- `S00-050` → `docs/contract-audits/video_manifest.md` — ممیزی قرارداد video_manifest
- `S00-051` → `docs/contract-audits/workflow_status.md` — ممیزی قرارداد workflow_status
- `S00-052` → `.gitignore` — گیت‌ایگنور محرمانگی
- `S00-053` → `.editorconfig` — تنظیمات یکسان ویرایش
- `S00-054` → `.github/CODEOWNERS` — مالکیت تغییرات
- `S00-055` → `tools/check_boundaries.py` — ممیزی وابستگی بین بسته‌ها
- `S00-056` → `frontend/tsconfig.json` — پیکربندی تایپ‌اسکریپت
- `S00-057` → `frontend/vite.config.ts` — پیکربندی Vite
- `S00-058` → `frontend/index.html` — سند ریشه وب
- `S00-059` → `frontend/src/main.tsx` — ورود React
- `S00-060` → `frontend/components.json` — پیکربندی shadcn/ui
- `S00-061` → `frontend/eslint.config.js` — بازبینی lint فرانت
- `S00-062` → `frontend/playwright.config.ts` — پیکربندی آزمون مرورگر

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- ادغام فقط از مسیر PR حفاظت‌شده پس از موفقیت کنترل‌های الزامی و احراز پیش‌نیازها. اجرای عملیاتی نیازمند مجوز جداگانه است.
