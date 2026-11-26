# ADR-006 — Provider-neutral AI model gateway

**Status:** Proposed for S00 independent review. **Task:** S00-013.

## Baseline
`source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, B01 and B05/B06 specifications, `guides/CLIENT_DECISIONS.md`, the P01 contract set and `AGENTS.md`.

## Proposed decision
- Route authorized model calls via a **replaceable provider adapter interface** with versioned input/output contracts. No model/provider hard-coding in core news-processing, translation, analysis, chat or report generation logic.
- Support a configurable task/model mapping, token and monetary budgets, concurrency limits, deadlines, bounded retries, circuit-breaker behavior and auditable fallbacks. Fallback must be permitted by the task's confidentiality, output rights and cost policy; never silently downgrade privacy or change semantics.
- Store model ID, provider ID, prompt/config revision, bounded latency and usage/cost provenance in restricted audit metadata without secrets, sensitive news content or private report text. Use scoped `credential_ref` backed by the approved vault; no tokens in repository or developer chat.
- Treat news and retrieved materials as untrusted. Validate outputs to relevant frozen JSON Schema Draft 2020-12 v1.0 contracts; distinguish unsupported claims from supported, attributable evidence. Preserve original text, quotations and provenance.
- Keep generated content private until applicable human editorial/legal and backend policy decisions. Respect `executive_private` scope at retrieval and provider-routing boundaries. Do not send restricted payloads to unapproved external models or logs.
- **External AI traffic and billing are disabled by default**. Build and test mock provider adapters first; turn on a real provider only after independently verified API terms, permissions, budgets, security and explicit authorization.

## Trade-offs / follow-up
Provider neutrality adds minimal adapter and observability overhead but avoids proprietary lock-in. Exact models, commercial limits, provider fallback order, key management and data residency are unresolved decisions for owning tasks. Do not infer that an API key has been supplied or that calls have been tested.

## Acceptance and rollback
Test adapter contract validation, timeout/retry, rate-limit/budget, privacy-denied routing, failure and fallback using deterministic mocks. Reviewer signoff and real logs are required for Gate-00. Rollback: close the draft PR; no live provider access to revoke from this task.
