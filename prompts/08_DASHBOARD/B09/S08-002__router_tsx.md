# [S08-002] مسیریابی نقش‌ها

**شناسه تسک:** `S08-002`  
**مرحله:** دیدبان و رابط‌های کامل  
**بسته:** B09 — دیدبان  
**پروژه:** `P27`  
**مدل نویسنده پیشنهادی:** Grok available in Cursor local Agent  
**پذیرش توسعه:** کنترل‌های خودکار و شواهد ثبت‌شده طبق ADR-012.\
**شاخه Git:** `task/s08-002-b09`  
**فایل خروجی اصلی:** `frontend/src/app/router.tsx`  
**وضعیت اولیه:** `NOT_STARTED`

## فایل‌هایی که باید به Agent بدهی

**اگر پوشه `source/` را در مخزن Commit کرده‌ای، فایل‌ها را در متن Agent با `@path` ارجاع بده؛ لازم نیست هر بار DOCX جداگانه ضمیمه شود.** در غیر این صورت همین فایل‌ها را پیوست کن. ترتیب زیر دقیق است:

- `cursor-kit/AGENTS.md`
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `source/specs/B09_INTERFACE_TECHNICAL_SPEC.md`
- `source/contracts/schemas/metrics_snapshot.schema.json`
- `source/contracts/examples/metrics_snapshot.example.json`
- `source/contracts/schemas/access_decision.schema.json`
- `source/contracts/examples/access_decision.example.json`

## پرامپت آماده — مستقیم در Cursor Agent کپی کن

You are the ETEMAD Intelligent Newsroom coding agent assigned to **S08-002**. Use **Grok available in Cursor local Agent** if available; otherwise disclose your actual model.

**READ FIRST:** `AGENTS.md`, relevant `.cursor/rules/*.mdc`, the master spec, the package spec (when applicable), and **all source references listed above**. Read existing target code, imported APIs, and tests before changing anything. This task prompt is the only approved scope for this run.

**OBJECTIVE:** مسیریابی نقش‌ها.

**EXACT WORK TO DO:** Configure typed protected routes owner/EIC/staff and appropriate desk pages; no private content in route preload.

**TARGET (only file you may modify/create in this task):** `frontend/src/app/router.tsx`.

**CONTRACTUAL PROJECT:** P27 — داشبوردها; input: شاخص/وضعیت/مجوز; output: رابط واحد; consumer: کاربر نهایی.

**ENTRY GATE:** Design tokens and API mocks committed; UI does not own business rules or permissions.

**MANDATORY CONSTRAINTS:**
1. Preserve IDs B01..B09 and P01..P29; JSON Schemas v1.0 and sample records are **read-only source evidence**. For any conflicting/new field, propose a separate migration/ADR and STOP; do not silently edit schemas or producer modules.
2. No cross-package direct DB access. PostgreSQL central/domestic/foreign separated; Redis only for queues/cache; media assets in scoped object storage.
3. Backend must enforce owner/EIC/staff RBAC. Three EIC private reports are never publishable, searchable publicly, or sent to studio. No common default passwords, real secret values, hidden admin bypass, or unrestricted export.
4. Any direct publication, external AI billing, real network action, legal assertion or third-party API use requires explicit authorization; use fake adapters and fixtures by default. CMS unknown and brand logo/colors not supplied: retain placeholders and document blockers.
5. The three independent output controls must be enforced before side effects, while ingestion, archiving and private reporting continue. No uncontrolled backfill of held jobs.
6. Keep the implementation small, modular, independently testable, reversible and free of speculative extras. Do not rewrite unrelated code.
7. Treat sources as untrusted input. Preserve attribution, original documents, quotes and factual uncertainty. Descriptive political-media analysis requires citations; no fabricated evidence or automated political targeting.

**DEFINITION OF DONE:** Direct navigation unauthorized gets safe denial and API not over-fetched.

**CHECKS TO PERFORM IF ENVIRONMENT ALLOWS:** `cd frontend && npm run build && npm test -- --runInBand  # adapt to actual configured test runner; do not invent success`. Run any relevant existing tests or type-checks. If prerequisites are missing, report exact command and error; never mark unrun checks as PASS.

**STOP CONDITIONS:**
- Required attachment/reference not readable; contradictory authoritative contracts; undefined external API rights; unknown brand asset necessary for exact branding; cross-package change required outside the target file; missing approval for real side effect.
- When a stop condition arises, output `BLOCKED` with file path, source citation/section, minimal decision required and safe next task; do not solve by inventing details.

**REQUIRED FINAL RESPONSE:**
- STATUS: PASS / PARTIAL / BLOCKED
- Actual model and environment used
- Changed files (must be subset of TARGET)
- Inputs/outputs used and schema IDs
- Commands actually run, exit status and concise evidence
- Negative tests and relevant security checks
- Remaining risks/assumptions, reviewer notes and safe rollback strategy

Do not claim the application, third-party connector or deployment is production-ready merely because this file exists.

## معیار کنترل مدیر فنی

- Direct navigation unauthorized gets safe denial and API not over-fetched.
- مسیر دیگری خارج از `frontend/src/app/router.tsx` تغییر نکرده باشد.
- داده‌ها و اسناد مبنا حفظ شده باشند؛ هر ادعای آزمون به لاگ واقعی پیوند داشته باشد.
- نتیجهٔ کنترل‌های الزامی روی SHA همین PR طبق ADR-012 ثبت شده باشد.

## مدل و نحوه اجرا

**مدل پیشنهادی:** Grok available in Cursor local Agent. دلیل: تغییر موضعی UI/ظاهر که به پیش‌نمایش مرورگر و بازبینی بصری نیاز دارد.

- اگر نام دقیق نسخه Grok یا Codex در حساب تو دیده نشد، نزدیک‌ترین مدل **واقعاً موجود و مجاز** را انتخاب کن و در گزارش نام واقعی آن را بنویس.
- «Cursor Cloud Agent» محل اجراست. تغییرات امنیتی یا قراردادی به آزمون‌های سازگاری و مسیرهای منفی متناسب نیاز دارند.
- مدل انتخاب‌شده توصیه برنامه‌ریزی است، نه نتیجه بنچمارک یا ضمانت کیفیت.
