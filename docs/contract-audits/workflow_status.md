# Contract audit - `workflow_status`

## ADR-014 fixture corrective change — 2026-11-26

The owner-authorized [ADR-014](../decisions/ADR-014-workflow-lifecycle.md) merged in [PR #64](https://github.com/sameranism/ETEMAD-pre/pull/64) at `eacb4910967887a011f7c99958d870fc157d869b`. This scoped correction projects actual fixture job state into v1.0, keeps job/workflow/event correlation stable on replay, bounds attempts and deadlines, supports cancellation of non-running jobs and refuses generic publishing execution/resume/retry. Non-publishing resume checks an immutable snapshot and rechecks state and deadline after the callback. The previously erroneous completed-on-enqueue and permissive publish resume assertions are replaced by stronger tests; no other existing test removed. The default three total attempts / 24-hour deadline is fixture policy, not production policy. Existing request_publish remains a switch check, not authorization. No schema, production, permissions or external integration changes.

Preceding [exact-head contract job](https://github.com/sameranism/ETEMAD-pre/actions/runs/45717101645/job/139565850733) reports S00-051 preflight PASS, 62 task preflights, 336 negative cases and boundary PASS. Local clone was previously unavailable (DNS); new tests require exact-head CI and are not asserted as passed here. Durable job leases, restart recovery, authenticated rights/policy/revision checks, in-flight cancellation and full cross-package workflow semantics remain unverified. Gate-00 remains OPEN/BLOCKED.

## Semantic audit — 2026-11-26

**Current disposition: PARTIAL / BLOCKED.** Independent or human development review is NOT_REQUIRED under [ADR-012](../decisions/ADR-012-automated-acceptance.md). This document records findings, not a wire or runtime change.

Baseline: signed protected [main `e4bc0a835b4ec5d6e6a3050f9bf338dda0af655d`](https://github.com/sameranism/ETEMAD-pre/commit/e4bc0a835b4ec5d6e6a3050f9bf338dda0af655d), merged [PR #62](https://github.com/sameranism/ETEMAD-pre/pull/62). Task S00-051, sole allowed target this document, entry S00-003 + frozen schema present. The four task attachments, master architecture, B01 specification, project mapping, ADR-004, AGENTS, rules and implementation/test references were inspected. The preceding exact-head [contract job](https://github.com/sameranism/ETEMAD-pre/actions/runs/45716323764/job/139563190456) reports S00-051 preflight PASS (target and four attachments), 62 task preflights, 336 negative contract cases and passing boundaries. No new local test execution is claimed; this PR requires its own exact-head CI.

### Field semantics and ownership

- P29/B01 owns the wire status, consumed by P27/B09 and other packages. `current_project` identifies the current processing project, not the owner of the status schema.
- `workflow_id` identifies a logical workflow; `correlation_id` links its events; both require stable authoritative identity semantics. `attempt_count` is an integer >= 0; retry bounds and attempt monotonicity are not expressed by JSON Schema. `last_error_code` accepts a nonempty string or null; it must be a controlled code, not exception text or a credential. `updated_at` is date-time; producers must maintain UTC and coherent ordering.
- Wire states are exactly new, running, held, completed, failed, cancelled. Internal queue states in [jobs.py](../../backend/core/jobs.py) are queued, running, held, done, failed. They are not interchangeable; queued/done cannot be serialized as wire states. Job and workflow lifecycle may be distinct; the audit does not assert a one-to-one mapping.
- [orchestrator.py](../../backend/core/orchestrator.py) builds a validated status with `current_project=P07` and returns completed after archive/event handoff. Its linked ingest job remains queued and attempt count zero; the existing `test_ingest_archives_and_emits_once` explicitly asserts this pair. Thus completed currently describes a fixture handoff, not demonstrated completion of all workflow processing. A new correlation ID is generated on each invocation even when the job and event are deduplicated. This is an observed semantic gap, not a failing CI assertion.
- The in-memory job transition table prevents direct queued-to-done, makes done terminal, and requires a revalidation callback for held-to-queued. However failed-to-queued is listed without a public retry method or bounded attempt/deadline enforcement. The frozen workflow cancelled state has no corresponding queue state. Mutable Job objects and non-durable fixture state cannot establish durable lifecycle invariants.
- [ADR-004](../decisions/ADR-004-publishing-gates.md) requires held jobs to be revalidated against expiry, rights, policy and current revision before resume. The fixture callback and tests for false/true callbacks are useful but do not establish authoritative revalidation or production safety. No public publishing is authorized.

### Separate proposed corrective decision (not adopted here)

A scoped ADR should first define the distinction between workflow completion and individual queue/handoff completion, authoritative P29 state ownership, stable workflow/correlation identity across idempotent replay, permissible transitions including cancelled, bounded retry/deadline semantics, terminal-state rules, and controlled error codes. Preserve the six existing wire states, all v1.0 fields and source examples. Do not silently translate arbitrary queue states, change output switches, or add a wire field. If a wire change is required, use a separately versioned contract and compatibility/migration approval.

Only after that decision, implement isolated fixture tests and then appropriately gated production adapters. Required positive and negative checks: new/running/completed transitions; illegal and terminal transitions; held job denied on missing or stale authorization/rights/expiry/revision; no automatic backfill; monotonic bounded attempts; cancellation and retry semantics; consistent correlation and identity on repeated input; no premature completion; unknown version/state rejection; durable persistence and recovery when available. Check actual producer and consumer compatibility, not just schema validation. Scope changes to P29 and its tests in a separate maintenance PR; do not alter the schema or extend publishing authorization.

### Evidence and next action

Existing tests cover basic queue transitions, held revalidation, attempt increment, ordinary event deduplication and the fixture handoff behavior; exact-head [backend CI](https://github.com/sameranism/ETEMAD-pre/actions/runs/45716323739) passed. They do not establish the full workflow invariants above. Full S00-051 semantic acceptance and Gate-00 remain BLOCKED. This audit is documentation-only and reversible by a protected revert PR.

- **Task:** `S00-051` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/workflow_status.schema.json`
- **Example:** `source/contracts/examples/workflow_status.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/workflow_status.schema.json`
- **Producer:** P29 | **Consumers:** P27, all packages | **Owning package:** B01

## Required root fields

- `schema_version`
- `workflow_id`
- `correlation_id`
- `current_project`
- `state`
- `attempt_count`
- `last_error_code`
- `updated_at`

## Field inventory

- `schema_version`: enum ['1.0']
- `workflow_id`: string
- `correlation_id`: string
- `current_project`: string
- `state`: enum ['new', 'running', 'held', 'completed', 'failed', 'cancelled']
- `attempt_count`: integer
- `last_error_code`: 
- `updated_at`: string (date-time)

## Enumerations

- `schema_version` = ['1.0']
- `state` = ['new', 'running', 'held', 'completed', 'failed', 'cancelled']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 1/1
- Example top-level keys (8): `attempt_count`, `correlation_id`, `current_project`, `last_error_code`, `schema_version`, `state`, `updated_at`, `workflow_id`
- `schema_version` in example: `1.0`

## Semantic checks the schema does NOT enforce

- Uniqueness of ids across records (enforced by storage keys, not JSON Schema).
- Cross-contract joins (for example `normalized_news` -> `cluster_result`) are referential, not validated here.
- Provenance/rights truthfulness: the schema records a value, it cannot prove it is correct.
- Time correctness beyond `format: date-time` (UTC normalisation is producer responsibility).

## Compatibility rules

- v1.0 is frozen: no silent field rename or enum narrowing.
- A required-field or enum change needs a new version, an ADR and producer/consumer tests.
- Consumers must reject unknown `schema_version` and warn with the record id.
