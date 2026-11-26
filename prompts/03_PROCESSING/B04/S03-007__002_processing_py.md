# [S03-007] مهاجرت داده پردازش

**شناسه تسک:** `S03-007`  
**مرحله:** خبرپرداز  
**بسته:** B04 — خبرپرداز  
**پروژه:** `P08`  
**مدل نویسنده پیشنهادی:** Codex / reasoning-high (Cursor local or Codex)  
**بازبین:** Codex مستقل (اگر Codex نویسنده بود، اجرای دوم با زمینه جداگانه؛ ترجیحاً شخص/عامل متفاوت)  
**شاخه Git:** `task/s03-007-b04`  
**فایل خروجی اصلی:** `backend/migrations/central/002_processing.py`  
**وضعیت اولیه:** `NOT_STARTED`

## فایل‌هایی که باید به Agent بدهی

**اگر پوشه `source/` را در مخزن Commit کرده‌ای، فایل‌ها را در متن Agent با `@path` ارجاع بده؛ لازم نیست هر بار DOCX جداگانه ضمیمه شود.** در غیر این صورت همین فایل‌ها را پیوست کن. ترتیب زیر دقیق است:

- `cursor-kit/AGENTS.md`
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `source/specs/B04_PREPROCESSING_TECHNICAL_SPEC.md`
- `source/contracts/schemas/cluster_result.schema.json`
- `source/contracts/examples/cluster_result.example.json`
- `source/technical/postgres_central_schema_PROPOSAL.sql`
- `source/technical/postgres_domestic_schema_PROPOSAL.sql`
- `source/technical/postgres_foreign_schema_PROPOSAL.sql`

## پرامپت آماده — مستقیم در Cursor Agent کپی کن

You are the ETEMAD Intelligent Newsroom coding agent assigned to **S03-007**. Use **Codex / reasoning-high (Cursor local or Codex)** if available; otherwise disclose your actual model.

**READ FIRST:** `AGENTS.md`, relevant `.cursor/rules/*.mdc`, the master spec, the package spec (when applicable), and **all source references listed above**. Read existing target code, imported APIs, and tests before changing anything. This task prompt is the only approved scope for this run.

**OBJECTIVE:** مهاجرت داده پردازش.

**EXACT WORK TO DO:** Create owned processing tables based on reviewed dictionary, not re-create archive tables.

**TARGET (only file you may modify/create in this task):** `backend/migrations/central/002_processing.py`.

**CONTRACTUAL PROJECT:** P08 — تشخیص تکرار; input: normalized_news/آرشیو; output: cluster_result; consumer: ۹.

**ENTRY GATE:** قراردادهای تولیدکننده مرحله پیشین تأیید شده‌اند؛ در صورت نبود سرویس واقعی از fixture/mock استفاده کن.

**MANDATORY CONSTRAINTS:**
1. Preserve IDs B01..B09 and P01..P29; JSON Schemas v1.0 and sample records are **read-only source evidence**. For any conflicting/new field, propose a separate migration/ADR and STOP; do not silently edit schemas or producer modules.
2. No cross-package direct DB access. PostgreSQL central/domestic/foreign separated; Redis only for queues/cache; media assets in scoped object storage.
3. Backend must enforce owner/EIC/staff RBAC. Three EIC private reports are never publishable, searchable publicly, or sent to studio. No common default passwords, real secret values, hidden admin bypass, or unrestricted export.
4. Any direct publication, external AI billing, real network action, legal assertion or third-party API use requires explicit authorization; use fake adapters and fixtures by default. CMS unknown and brand logo/colors not supplied: retain placeholders and document blockers.
5. The three independent output controls must be enforced before side effects, while ingestion, archiving and private reporting continue. No uncontrolled backfill of held jobs.
6. Keep the implementation small, modular, independently testable, reversible and free of speculative extras. Do not rewrite unrelated code.
7. Treat sources as untrusted input. Preserve attribution, original documents, quotes and factual uncertainty. Descriptive political-media analysis requires citations; no fabricated evidence or automated political targeting.

**DEFINITION OF DONE:** Migration validates FK ownership with central schema and reversible in staging.

**CHECKS TO PERFORM IF ENVIRONMENT ALLOWS:** `python -m compileall -q backend/migrations/central/002_processing.py  # and run relevant existing pytest tests if available`. Run any relevant existing tests or type-checks. If prerequisites are missing, report exact command and error; never mark unrun checks as PASS.

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

- Migration validates FK ownership with central schema and reversible in staging.
- مسیر دیگری خارج از `backend/migrations/central/002_processing.py` تغییر نکرده باشد.
- داده‌ها و اسناد مبنا حفظ شده باشند؛ هر ادعای آزمون به لاگ واقعی پیوند داشته باشد.
- نتیجه بازبینی مستقل Codex ثبت شده باشد.

## مدل و نحوه اجرا

**مدل پیشنهادی:** Codex / reasoning-high (Cursor local or Codex). دلیل: مرزهای امنیت، قرارداد، دیتابیس یا معماری نیازمند بررسی دقیق و آزمون صریح است.

- اگر نام دقیق نسخه Grok یا Codex در حساب تو دیده نشد، نزدیک‌ترین مدل **واقعاً موجود و مجاز** را انتخاب کن و در گزارش نام واقعی آن را بنویس.
- «Cursor Cloud Agent» محل اجراست، نه نام مدل. برای تغییرات امنیتی/قرارداد، نویسنده و بازبین باید دو اجرای مستقل باشند.
- مدل انتخاب‌شده توصیه برنامه‌ریزی است، نه نتیجه بنچمارک یا ضمانت کیفیت.
