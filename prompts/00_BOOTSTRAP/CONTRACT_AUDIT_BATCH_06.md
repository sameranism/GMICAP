# ممیزی گروهی قراردادها — دسته 6 از ۶

**هدف:** کاهش سربار اجرای ۳۰ تسک ممیزی بدون حذف پرامپت اختصاصی هر فایل.

**پیشنهاد اجرا:** Grok در Cursor Cloud، فقط تحلیل قراردادها؛ سپس Codex در نقش بازبین مستقل.

## قراردادهای این دسته
- `S00-047`: `docs/contract-audits/source_registry.md`؛ بخوان: `source/contracts/schemas/source_registry.schema.json` و example متناظر
- `S00-048`: `docs/contract-audits/translation.md`؛ بخوان: `source/contracts/schemas/translation.schema.json` و example متناظر
- `S00-049`: `docs/contract-audits/validation_decision.md`؛ بخوان: `source/contracts/schemas/validation_decision.schema.json` و example متناظر
- `S00-050`: `docs/contract-audits/video_manifest.md`؛ بخوان: `source/contracts/schemas/video_manifest.schema.json` و example متناظر
- `S00-051`: `docs/contract-audits/workflow_status.md`؛ بخوان: `source/contracts/schemas/workflow_status.schema.json` و example متناظر


## پرامپت آماده

As a contract documentation agent for ETEMAD, read `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/technical/project_package_map.csv`, and the source JSON Schema plus example for each contract listed above. First read the **full individual task prompts** for all five IDs listed, then perform only those five audits. You may create/edit EXACTLY these output files: docs/contract-audits/source_registry.md, docs/contract-audits/translation.md, docs/contract-audits/validation_decision.md, docs/contract-audits/video_manifest.md, docs/contract-audits/workflow_status.md. Do not edit source/contracts, application code, migrations or other docs. Each audit must identify schema version, required fields, producer/consumer, enum semantics, sample validation status (only if actually run), unresolved contradictions, and whether a separate ADR is necessary. Never silently reconcile mismatched contracts. Provide results per ID and a consolidated blocker list. No code implementation, no network, no live publication. If tools cannot validate, mark NOT_RUN.

Reviewer: Codex independently checks five audit files against original schemas and examples, not the model's claims.
