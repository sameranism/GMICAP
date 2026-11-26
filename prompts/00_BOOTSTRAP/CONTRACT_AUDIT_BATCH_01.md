# ممیزی گروهی قراردادها — دسته 1 از ۶

**هدف:** کاهش سربار اجرای ۳۰ تسک ممیزی بدون حذف پرامپت اختصاصی هر فایل.

**پیشنهاد اجرا:** Grok در Cursor Cloud، فقط تحلیل قراردادها؛ سپس Codex در نقش بازبین مستقل.

## قراردادهای این دسته
- `S00-022`: `docs/contract-audits/access_decision.md`؛ بخوان: `source/contracts/schemas/access_decision.schema.json` و example متناظر
- `S00-023`: `docs/contract-audits/ai_models_config.md`؛ بخوان: `source/contracts/schemas/ai_models_config.schema.json` و example متناظر
- `S00-024`: `docs/contract-audits/analysis_chat_response.md`؛ بخوان: `source/contracts/schemas/analysis_chat_response.schema.json` و example متناظر
- `S00-025`: `docs/contract-audits/analysis_result.md`؛ بخوان: `source/contracts/schemas/analysis_result.schema.json` و example متناظر
- `S00-026`: `docs/contract-audits/archive_record.md`؛ بخوان: `source/contracts/schemas/archive_record.schema.json` و example متناظر


## پرامپت آماده

As a contract documentation agent for ETEMAD, read `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/technical/project_package_map.csv`, and the source JSON Schema plus example for each contract listed above. First read the **full individual task prompts** for all five IDs listed, then perform only those five audits. You may create/edit EXACTLY these output files: docs/contract-audits/access_decision.md, docs/contract-audits/ai_models_config.md, docs/contract-audits/analysis_chat_response.md, docs/contract-audits/analysis_result.md, docs/contract-audits/archive_record.md. Do not edit source/contracts, application code, migrations or other docs. Each audit must identify schema version, required fields, producer/consumer, enum semantics, sample validation status (only if actually run), unresolved contradictions, and whether a separate ADR is necessary. Never silently reconcile mismatched contracts. Provide results per ID and a consolidated blocker list. No code implementation, no network, no live publication. If tools cannot validate, mark NOT_RUN.

Reviewer: Codex independently checks five audit files against original schemas and examples, not the model's claims.
