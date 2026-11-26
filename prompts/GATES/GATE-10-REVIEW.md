# GATE-10 — بازبینی مستقل مرحله 10

**مدل:** Codex (در محیط جدا از نویسندگان؛ اجرا با PR read-only، مگر تسک اصلاح مستقل تصویب شود).

## ورودی‌های لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `manifests/tasks.csv`
- لاگ واقعی CI، گزارش PR و تغییرات Git برای همین مرحله.

## پرامپت آماده

Act as an independent ETEMAD architecture, security and contract reviewer for phase 10 — تحویل، استقرار و بازبینی نهایی. Review ONLY the diff for tasks listed below. Read referenced master/package specs and source JSON Schemas. Check that edits obey allowed-file boundaries, cross-package API isolation, data provenance, 3-DB separation, EIC private isolation, output switches, model/branding placeholders, verified adapter status, and actual test evidence. Never accept statements of success without logs. Do not edit code in review run. Return a table: task ID, changed files, test evidence, security/contract findings, PASS/FAIL/BLOCKED, required patch task; finish with a gate decision. If test tools unavailable, mark UNKNOWN not PASS. Reject any unauthorized public/private publication path or real API use.

## تسک‌های این مرحله
- `S10-001` → `docs/release/RELEASE_CHECKLIST.md` — معیار نسخه آزمایشی و عملیاتی
- `S10-002` → `docs/release/CHANGELOG.md` — ثبت تغییرات
- `S10-003` → `docs/release/HANDOFF_TO_TEAMS.md` — راهنمای تحویل تیم‌ها
- `S10-004` → `docs/release/FINAL_ACCEPTANCE.md` — پذیرش کارفرما
- `S10-005` → `docs/release/PROMPT_CHANGE_LOG.md` — تغییرات پرامپت‌ها
- `S10-006` → `docs/release/AS_BUILT_ARCHITECTURE.md` — معماری آنچه واقعاً ساخته شده

## خروجی
- گزارش تصمیم Gate با شواهد، خطاها، فایل‌های مغایر و تسک‌های اصلاح.
- بدون ادغام/استقرار خودکار.
