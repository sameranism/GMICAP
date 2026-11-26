# ADR-015 — Stage advanced security implementation at its owning phase

Date: 2026-11-26 (Asia/Tehran).
Status: owner-authorized scheduling decision, effective upon protected merge.
Baseline: signed main 190649ad3b75969b7345beb3da71f1f21bc070a7; [PR #66](https://github.com/sameranism/ETEMAD-pre/pull/66).
References: ADR-004, ADR-005, ADR-012, ADR-013, ADR-014; S00-041 private_report audit; manifests/tasks.csv and manifests/coding_path.csv.

## Decision

Do not pull production infrastructure and full-system integration forward into
phase zero. The owner requested that the dedicated private repository, durable
queues, advanced access control and integrated security testing be completed
in their designated phases, not waived. Continue dependency-eligible isolated
development with synthetic data and mock adapters. No real private data,
external publication, credentials, deployment or paid model calls are authorized.
Keep studio deferral, frozen contracts, task ownership, existing tests, CodeQL
and all native branch protections.

| Deferred implementation | Owning work (existing task IDs) | Required completion boundary |
| --- | --- | --- |
| Durable queue, transactional outbox, leases/recovery | S01-012, S01-013, S01-021 | Gate-01 and before reliance on restart-safe execution |
| Authoritative grants, audit, secret-reference handling, scoped archive/object-store access | S01-007–010, S01-017, S01-020, S01-029 | Gate-01 and before any protected resource is enabled |
| Dedicated P19 private repository/bucket, private retrieval and report isolation | S05-003, S05-004, S05-007–010; P27 S08-013/026/027 | Applicable Gate-05/Gate-08 and before private data access; P16/P27 only with authorization |
| Integrated privacy and threat evidence, full security CI | S06-015, S09-010, S09-014, S09-025 | Applicable publishing/integration Gates and before operational release |

These are existing prerequisites, not new tasks or blanket waivers. A task
whose official entry Gate is open remains BLOCKED. Do not mark deferred
implementation PASS or NOT_REQUIRED. Use the existing isolated-fixture and
evidence-work allowance in AGENTS.md / ADR-012; no product integration may
bypass a required Gate. Where the queue ordering conflicts with a manifest,
record the conflict and resolve it in a separate scoped planning decision
before starting the dependent task.

## Non-deferred Gate-00 baseline

Gate-00 remains OPEN/BLOCKED until its own contract, architecture, basic
security and per-task evidence is complete. In particular, fail closed for
executive_private on the shared fixture event bus/outbox, including raw
envelopes and dispatch rechecks, while retaining constructor schema
compatibility and existing restricted denial. This is a prerequisite
containment correction, not the deferred private queue implementation.
No classification downgrade, authorization widening, or fabricated rights
check. A narrowly scoped ADR and tested PR must establish this behavior.
Generic archive/object paths must not be used for real private data; prove
applicable baseline isolation/denial before dependent access, leaving
dedicated storage and integration to their owners. Preserve S00-041 findings.
Resolve remaining contract semantics and applicable secret/permission checks
at Gate-00; GitHub alert evidence was inaccessible, not clean. Full-system
tests requiring unimplemented modules stay assigned to their documented gates,
but missing required Gate-00 evidence remains BLOCKED. No Gate procedure,
matrix dependency, CI rule or security threshold is removed by this decision.

Next eligible activity: finish phase-zero baseline evidence and the scoped
shared-route denial correction; then first dependency-eligible task in QUEUE.
S03-006 still needs Gate-00, Gate-01, source-list evidence and its own task
dependencies. Do not report advancement to phase 3 until those pass.

Rollback: protected revert PR. All historical audit and CI results retained.
