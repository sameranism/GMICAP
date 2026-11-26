# ممیزی گروهی قراردادها — دسته 2 از ۶

**هدف:** کاهش سربار اجرای ۳۰ تسک ممیزی بدون حذف پرامپت اختصاصی هر فایل.

**پیشنهاد اجرا:** Grok در Cursor Cloud، تحلیل قراردادها و اجرای کنترل‌های خودکار سازگاری.

## قراردادهای این دسته
- `S00-027`: `docs/contract-audits/article.md`؛ بخوان: `source/contracts/schemas/article.schema.json` و example متناظر
- `S00-028`: `docs/contract-audits/audio_manifest.md`؛ بخوان: `source/contracts/schemas/audio_manifest.schema.json` و example متناظر
- `S00-029`: `docs/contract-audits/classified_news.md`؛ بخوان: `source/contracts/schemas/classified_news.schema.json` و example متناظر
- `S00-030`: `docs/contract-audits/cluster_result.md`؛ بخوان: `source/contracts/schemas/cluster_result.schema.json` و example متناظر
- `S00-031`: `docs/contract-audits/country_source_pack.md`؛ بخوان: `source/contracts/schemas/country_source_pack.schema.json` و example متناظر


## پرامپت آماده

As a contract documentation agent for ETEMAD, read `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/technical/project_package_map.csv`, and the source JSON Schema plus example for each contract listed above. First read the **full individual task prompts** for all five IDs listed, then perform only those five audits. You may create/edit EXACTLY these output files: docs/contract-audits/article.md, docs/contract-audits/audio_manifest.md, docs/contract-audits/classified_news.md, docs/contract-audits/cluster_result.md, docs/contract-audits/country_source_pack.md. Do not edit source/contracts, application code, migrations or other docs. Each audit must identify schema version, required fields, producer/consumer, enum semantics, sample validation status (only if actually run), unresolved contradictions, and whether a separate ADR is necessary. Never silently reconcile mismatched contracts. Provide results per ID and a consolidated blocker list. No code implementation, no network, no live publication. If tools cannot validate, mark NOT_RUN.

Reviewer: Codex independently checks five audit files against original schemas and examples, not the model's claims.
