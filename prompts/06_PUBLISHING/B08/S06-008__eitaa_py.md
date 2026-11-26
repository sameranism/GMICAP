# [S06-008] آداپتور ایتا

**شناسه تسک:** `S06-008`  
**مرحله:** رسان  
**بسته:** B08 — رسان  
**پروژه:** `P25`  
**مدل نویسنده پیشنهادی:** Grok available in Cursor Cloud Agent  
**پذیرش توسعه:** کنترل‌های خودکار و شواهد ثبت‌شده طبق ADR-012.\
**شاخه Git:** `task/s06-008-b08`  
**فایل خروجی اصلی:** `backend/adapters/eitaa.py`  
**وضعیت اولیه:** `NOT_STARTED`

## فایل‌هایی که باید به Agent بدهی

**اگر پوشه `source/` را در مخزن Commit کرده‌ای، فایل‌ها را در متن Agent با `@path` ارجاع بده؛ لازم نیست هر بار DOCX جداگانه ضمیمه شود.** در غیر این صورت همین فایل‌ها را پیوست کن. ترتیب زیر دقیق است:

- `cursor-kit/AGENTS.md`
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `source/specs/B08_PUBLISHING_TECHNICAL_SPEC.md`
- `source/contracts/schemas/publication_result.schema.json`
- `source/contracts/examples/publication_result.example.json`
- `source/contracts/schemas/publication_job.schema.json`
- `source/contracts/schemas/validation_decision.schema.json`
- `source/contracts/schemas/private_report.schema.json`
- `source/contracts/schemas/output_controls.schema.json`

## پرامپت آماده — مستقیم در Cursor Agent کپی کن

You are the ETEMAD Intelligent Newsroom coding agent assigned to **S06-008**. Use **Grok available in Cursor Cloud Agent** if available; otherwise disclose your actual model.

**READ FIRST:** `AGENTS.md`, relevant `.cursor/rules/*.mdc`, the master spec, the package spec (when applicable), and **all source references listed above**. Read existing target code, imported APIs, and tests before changing anything. This task prompt is the only approved scope for this run.

**OBJECTIVE:** آداپتور ایتا.

**EXACT WORK TO DO:** Check supported authorized APIs and scope before write; if not verified, keep mock-only implementation.

**TARGET (only file you may modify/create in this task):** `backend/adapters/eitaa.py`.

**CONTRACTUAL PROJECT:** P25 — ارسال چندکاناله; input: publication_job/payload; output: publication_result; consumer: ۲۶ و ۱۷.

**ENTRY GATE:** قراردادهای تولیدکننده مرحله پیشین تأیید شده‌اند؛ در صورت نبود سرویس واقعی از fixture/mock استفاده کن.

**MANDATORY CONSTRAINTS:**
1. Preserve IDs B01..B09 and P01..P29; JSON Schemas v1.0 and sample records are **read-only source evidence**. For any conflicting/new field, propose a separate migration/ADR and STOP; do not silently edit schemas or producer modules.
2. No cross-package direct DB access. PostgreSQL central/domestic/foreign separated; Redis only for queues/cache; media assets in scoped object storage.
3. Backend must enforce owner/EIC/staff RBAC. Three EIC private reports are never publishable, searchable publicly, or sent to studio. No common default passwords, real secret values, hidden admin bypass, or unrestricted export.
4. Any direct publication, external AI billing, real network action, legal assertion or third-party API use requires explicit authorization; use fake adapters and fixtures by default. CMS unknown and brand logo/colors not supplied: retain placeholders and document blockers.
5. The three independent output controls must be enforced before side effects, while ingestion, archiving and private reporting continue. No uncontrolled backfill of held jobs.
6. Keep the implementation small, modular, independently testable, reversible and free of speculative extras. Do not rewrite unrelated code.
7. Treat sources as untrusted input. Preserve attribution, original documents, quotes and factual uncertainty. Descriptive political-media analysis requires citations; no fabricated evidence or automated political targeting.

**DEFINITION OF DONE:** No unofficial workaround or fabricated production-ready claim.

**CHECKS TO PERFORM IF ENVIRONMENT ALLOWS:** `python -m compileall -q backend/adapters/eitaa.py  # and run relevant existing pytest tests if available`. Run any relevant existing tests or type-checks. If prerequisites are missing, report exact command and error; never mark unrun checks as PASS.

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

- No unofficial workaround or fabricated production-ready claim.
- مسیر دیگری خارج از `backend/adapters/eitaa.py` تغییر نکرده باشد.
- داده‌ها و اسناد مبنا حفظ شده باشند؛ هر ادعای آزمون به لاگ واقعی پیوند داشته باشد.
- نتیجهٔ کنترل‌های الزامی روی SHA همین PR طبق ADR-012 ثبت شده باشد.

## مدل و نحوه اجرا

**مدل پیشنهادی:** Grok available in Cursor Cloud Agent. دلیل: ماژول قابل جداسازی و مناسب توسعه در شاخه Cloud پس از تثبیت قراردادها.

- اگر نام دقیق نسخه Grok یا Codex در حساب تو دیده نشد، نزدیک‌ترین مدل **واقعاً موجود و مجاز** را انتخاب کن و در گزارش نام واقعی آن را بنویس.
- «Cursor Cloud Agent» محل اجراست. تغییرات امنیتی یا قراردادی به آزمون‌های سازگاری و مسیرهای منفی متناسب نیاز دارند.
- مدل انتخاب‌شده توصیه برنامه‌ریزی است، نه نتیجه بنچمارک یا ضمانت کیفیت.
