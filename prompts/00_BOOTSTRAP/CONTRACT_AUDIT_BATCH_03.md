# ممیزی گروهی قراردادها — دسته 3 از ۶

**هدف:** کاهش سربار اجرای ۳۰ تسک ممیزی بدون حذف پرامپت اختصاصی هر فایل.

**پیشنهاد اجرا:** Grok در Cursor Cloud، فقط تحلیل قراردادها؛ سپس Codex در نقش بازبین مستقل.

## قراردادهای این دسته
- `S00-032`: `docs/contract-audits/destination_config.md`؛ بخوان: `source/contracts/schemas/destination_config.schema.json` و example متناظر
- `S00-033`: `docs/contract-audits/destination_payload.md`؛ بخوان: `source/contracts/schemas/destination_payload.schema.json` و example متناظر
- `S00-034`: `docs/contract-audits/editorial_rules.md`؛ بخوان: `source/contracts/schemas/editorial_rules.schema.json` و example متناظر
- `S00-035`: `docs/contract-audits/event_envelope.md`؛ بخوان: `source/contracts/schemas/event_envelope.schema.json` و example متناظر
- `S00-036`: `docs/contract-audits/image_manifest.md`؛ بخوان: `source/contracts/schemas/image_manifest.schema.json` و example متناظر


## پرامپت آماده

As a contract documentation agent for ETEMAD, read `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/technical/project_package_map.csv`, and the source JSON Schema plus example for each contract listed above. First read the **full individual task prompts** for all five IDs listed, then perform only those five audits. You may create/edit EXACTLY these output files: docs/contract-audits/destination_config.md, docs/contract-audits/destination_payload.md, docs/contract-audits/editorial_rules.md, docs/contract-audits/event_envelope.md, docs/contract-audits/image_manifest.md. Do not edit source/contracts, application code, migrations or other docs. Each audit must identify schema version, required fields, producer/consumer, enum semantics, sample validation status (only if actually run), unresolved contradictions, and whether a separate ADR is necessary. Never silently reconcile mismatched contracts. Provide results per ID and a consolidated blocker list. No code implementation, no network, no live publication. If tools cannot validate, mark NOT_RUN.

Reviewer: Codex independently checks five audit files against original schemas and examples, not the model's claims.
