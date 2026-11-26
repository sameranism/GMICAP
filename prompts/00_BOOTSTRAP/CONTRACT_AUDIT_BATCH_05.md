# ممیزی گروهی قراردادها — دسته 5 از ۶

**هدف:** کاهش سربار اجرای ۳۰ تسک ممیزی بدون حذف پرامپت اختصاصی هر فایل.

**پیشنهاد اجرا:** Grok در Cursor Cloud، تحلیل قراردادها و اجرای کنترل‌های خودکار سازگاری.

## قراردادهای این دسته
- `S00-042`: `docs/contract-audits/public_report.md`؛ بخوان: `source/contracts/schemas/public_report.schema.json` و example متناظر
- `S00-043`: `docs/contract-audits/publication_job.md`؛ بخوان: `source/contracts/schemas/publication_job.schema.json` و example متناظر
- `S00-044`: `docs/contract-audits/publication_result.md`؛ بخوان: `source/contracts/schemas/publication_result.schema.json` و example متناظر
- `S00-045`: `docs/contract-audits/raw_news.md`؛ بخوان: `source/contracts/schemas/raw_news.schema.json` و example متناظر
- `S00-046`: `docs/contract-audits/schedule_config.md`؛ بخوان: `source/contracts/schemas/schedule_config.schema.json` و example متناظر


## پرامپت آماده

As a contract documentation agent for ETEMAD, read `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/technical/project_package_map.csv`, and the source JSON Schema plus example for each contract listed above. First read the **full individual task prompts** for all five IDs listed, then perform only those five audits. You may create/edit EXACTLY these output files: docs/contract-audits/public_report.md, docs/contract-audits/publication_job.md, docs/contract-audits/publication_result.md, docs/contract-audits/raw_news.md, docs/contract-audits/schedule_config.md. Do not edit source/contracts, application code, migrations or other docs. Each audit must identify schema version, required fields, producer/consumer, enum semantics, sample validation status (only if actually run), unresolved contradictions, and whether a separate ADR is necessary. Never silently reconcile mismatched contracts. Provide results per ID and a consolidated blocker list. No code implementation, no network, no live publication. If tools cannot validate, mark NOT_RUN.

Reviewer: Codex independently checks five audit files against original schemas and examples, not the model's claims.
