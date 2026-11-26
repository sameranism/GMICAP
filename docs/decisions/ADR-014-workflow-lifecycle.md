# ADR-014 — P29 fixture workflow identity, lifecycle and bounded execution

Status: owner-authorized correction; proposed until this protected PR passes.
Baseline: signed main 95feb0692dbd667fedf0c0b38475fa91f5c9c3ba, [PR #63](https://github.com/sameranism/ETEMAD-pre/pull/63).
Related: [S00-051 audit](../contract-audits/workflow_status.md), S01-012, S01-021, [ADR-004](ADR-004-publishing-gates.md), [ADR-012](ADR-012-automated-acceptance.md).
This decision does not close Gate-00 or accept downstream tasks.

## Context

The frozen workflow_status v1.0 has six states; the queue is an in-memory
fixture. Current ingestion returns completed with a queued job, assigns a fresh
correlation ID on replay, has no bounded public retry or cancel operation, and
allows held resume with only a caller callback. Master/B01/database dictionary
require bounded retry, deadline, stable identity and guarded output resumption.
ADR-004 additionally requires current rights and policy and prohibits uncontrolled
backfill. Production authority and persistence are not present.

## Decision

1. P29 owns the status of the tracked fixture job/handoff, not a claim of
   completion across all downstream packages. Project queued -> new, running ->
   running, held -> held, done -> completed, failed -> failed, cancelled ->
   cancelled. A completion status requires an actual legal running-to-done
   transition, never enqueue/archive/event emission alone. Use the same
   workflow_id and correlation_id on replay of the same job identity; retain
   correlation in the queue and use the stable job identifier for workflow
   identity and event idempotency. A changed input fingerprint is a distinct
   job; no claim of global durable deduplication. Preserve wire fields, enums,
   schema and example; no new wire versions.
2. Keep fixture lifecycle small. Provide explicit retry and cancellation;
   cancellation allowed for queued, held and failed only, not an in-flight
   worker (real cancellation requires worker coordination). Done and cancelled
   are terminal. Retry only failed, before deadline and while attempts remain;
   increment attempts only on start. Use finite fixture defaults of three total
   attempts and 24 hours from enqueue, injectable clock and explicit positive
   per-job attempt/deadline overrides; reject naive timestamps and invalid
   bounds. Recheck deadline/attempt budget at retry, resume and start. Expiry
   or exhausted budget denies new execution without incrementing attempt or
   silently dropping records. Running jobs may be finalized after deadline
   because this fixture does not interrupt in-flight work. Use controlled
   error codes, never raw exception/credential text in workflow output.
3. Do not resume a held job merely because output turns on. Preserve explicit
   revalidation for non-publishing fixture jobs. Publishing-kind jobs must
   fail closed on generic resume, retry and start unless an authoritative
   revalidation/dispatch path exists; the current fixture has none. Do not
   implement a caller boolean or fabricated rights/policy check as an
   authorization substitute. The existing request_publish switch check is
   only a switch decision, not permission to deliver or execute. A later
   authenticated publishing adapter must check current switch revision,
   authorization, rights, policy, expiry and destination immediately before
   dispatch, with no automatic backlog drain and no private fallback.
4. Queue state and identity must not be externally mutable through returned
   objects. Return immutable snapshots or detached copies, keep transitions
   under the queue lock, and do not run untrusted callbacks while holding
   that lock; recheck unchanged state/version and deadline after validation.
   No changes to DB ownership, Redis, APIs, permissions, output switches,
   external services, event classification policy or real publishing.

## Implementation and evidence

After this ADR passes protected exact-head CI, one narrowly scoped Gate-00
fixture maintenance PR may change only backend/core/jobs.py,
backend/core/orchestrator.py, backend/tests/test_orchestration.py and associated
audit/evidence files if required. Existing erroneous completed-on-enqueue
assertion and bare publish-resume success assertion must be replaced with
stronger contract/security assertions, never removed without replacement.
Other existing tests and controls retained. Before edit read the S01-012 and
S01-021 prompts and all ten attachments each; record the S00-051 preflight and
applicable CI. Scope is not downstream S01 acceptance.

Test new/running/completed mapping and stable replay/event correlation,
distinct fingerprints, invalid and terminal transitions, cancelled jobs,
deadline and retry limits, attempt accounting, error redaction, snapshot
isolation, failed/exception/stale revalidation, and fail-closed held
publishing despite an enabled switch or a true callback. Test no external
calls, no change in schema or ordinary fixture delivery and no regression in
restricted denial. Require backend PostgreSQL CI, contract/boundary checks,
bootstrap, Guardian and CodeQL on exact head. Document unavailable local
execution and skipped checks. Separate durable DB/Redis job/lease/recovery,
authoritative access and publishing revalidation, full P29 workflow semantics,
stream isolation and cancellation of in-flight workers remain future gated
work; do not claim those are fixed by fixture tests.

Rollback only through a protected revert PR; no production credentials,
deployment, real publishing or external calls.
