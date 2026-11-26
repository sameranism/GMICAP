# ممیزی گروهی قراردادها — دسته 4 از ۶

**هدف:** کاهش سربار اجرای ۳۰ تسک ممیزی بدون حذف پرامپت اختصاصی هر فایل.

**پیشنهاد اجرا:** Grok در Cursor Cloud، تحلیل قراردادها و اجرای کنترل‌های خودکار سازگاری.

## قراردادهای این دسته
- `S00-037`: `docs/contract-audits/metrics_snapshot.md`؛ بخوان: `source/contracts/schemas/metrics_snapshot.schema.json` و example متناظر
- `S00-038`: `docs/contract-audits/news_framework.md`؛ بخوان: `source/contracts/schemas/news_framework.schema.json` و example متناظر
- `S00-039`: `docs/contract-audits/normalized_news.md`؛ بخوان: `source/contracts/schemas/normalized_news.schema.json` و example متناظر
- `S00-040`: `docs/contract-audits/output_controls.md`؛ بخوان: `source/contracts/schemas/output_controls.schema.json` و example متناظر
- `S00-041`: `docs/contract-audits/private_report.md`؛ بخوان: `source/contracts/schemas/private_report.schema.json` و example متناظر


## پرامپت آماده

As a contract documentation agent for ETEMAD, read `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/technical/project_package_map.csv`, and the source JSON Schema plus example for each contract listed above. First read the **full individual task prompts** for all five IDs listed, then perform only those five audits. You may create/edit EXACTLY these output files: docs/contract-audits/metrics_snapshot.md, docs/contract-audits/news_framework.md, docs/contract-audits/normalized_news.md, docs/contract-audits/output_controls.md, docs/contract-audits/private_report.md. Do not edit source/contracts, application code, migrations or other docs. Each audit must identify schema version, required fields, producer/consumer, enum semantics, sample validation status (only if actually run), unresolved contradictions, and whether a separate ADR is necessary. Never silently reconcile mismatched contracts. Provide results per ID and a consolidated blocker list. No code implementation, no network, no live publication. If tools cannot validate, mark NOT_RUN.

Reviewer: Codex independently checks five audit files against original schemas and examples, not the model's claims.
