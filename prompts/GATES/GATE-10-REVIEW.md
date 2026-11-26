# GATE-10 — پذیرش خودکار مرحله 10

**سیاست:** پذیرش خودکار بر پایهٔ [ADR-012](../../docs/decisions/ADR-012-automated-acceptance.md).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## روش ثبت پذیرش

Run ETEMAD architecture, security and contract acceptance checks for phase 10 — تحویل، استقرار و بازبینی نهایی. Use the listed tasks and their applicable test and security criteria. Match every check to the current PR head or exact accepted integration revision. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Record commands, exit codes, workflow links and the exact SHA. For missing evidence mark the affected item BLOCKED and run or implement its check in the appropriate scope. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S10-001` → `docs/release/RELEASE_CHECKLIST.md` — معیار نسخه آزمایشی و عملیاتی
- `S10-002` → `docs/release/CHANGELOG.md` — ثبت تغییرات
- `S10-003` → `docs/release/HANDOFF_TO_TEAMS.md` — راهنمای تحویل تیم‌ها
- `S10-004` → `docs/release/FINAL_ACCEPTANCE.md` — پذیرش کارفرما
- `S10-005` → `docs/release/PROMPT_CHANGE_LOG.md` — تغییرات پرامپت‌ها
- `S10-006` → `docs/release/AS_BUILT_ARCHITECTURE.md` — معماری آنچه واقعاً ساخته شده

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- ادغام فقط از مسیر PR حفاظت‌شده پس از موفقیت کنترل‌های الزامی و احراز پیش‌نیازها. اجرای عملیاتی نیازمند مجوز جداگانه است.
