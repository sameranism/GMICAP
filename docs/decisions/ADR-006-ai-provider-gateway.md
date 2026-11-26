# ADR-006 — AI provider gateway: interchangeable models, budgets, provenance

- **Status:** Accepted
- **Date:** 2026-11-23
- **Task:** S00-013
- **Source:** `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/contracts/schemas/ai_models_config.schema.json`

## Context

Translation, summarization, political analysis, reporting and studio narration all use language models.
Providers change, prices change, and free text must never leak personal data or secrets into a third-party
log. Hard-coding one provider would make the product dependent on a single vendor and a single price list.

## Decision

1. **One gateway** (`backend/core/ai_gateway.py`) exposes task-oriented calls
   (`translate`, `summarize`, `classify`, `analyze`, `draft`, `narrate`). Feature code never imports a
   provider SDK directly.
2. **Configuration comes from the `ai_models_config` contract**: per-task provider, model, timeout,
   retry policy, budget and `credential_ref`. Secrets live only in the vault; `credential_ref` is a pointer.
3. **Fallback is explicit and bounded:** primary, optional fallback, no silent provider switching on
   content-moderation or billing errors; every fallback is recorded.
4. **Budgets:** a per-run and per-month ceiling is enforced before the call; exceeding it returns
   `dependency_unavailable` and leaves the job `held`, never retries unbounded.
5. **Provenance:** every AI output stored with the product record records provider, model, prompt template
   version, timestamp and request id — enough to reproduce a disputed result.
6. **Logging:** prompts and completions are logged only as redacted summaries with hashes; no personal
   data, no secrets, no full source documents in logs.
7. **Default state is off.** No external model call occurs without an explicit switch and a configured,
   authorized key. Development uses deterministic fixtures.

## Consequences

- A new provider is an adapter plus config change, not a code change in feature modules.
- Tests can run fully offline with a recording adapter.
- Cost anomalies are visible per task and per month before they become an invoice.

## Impacted contracts

`ai_models_config`, `translation`, `analysis_result`, `analysis_chat_response`, `metrics_snapshot`,
`public_report`, `private_report`, `audio_manifest`, `video_manifest`.

## Open external dependencies

- Which providers are permitted and billable for the newspaper (client decision).
- Monthly budget ceiling and approval path for overages.
- Data-residency and confidentiality terms for foreign providers.
