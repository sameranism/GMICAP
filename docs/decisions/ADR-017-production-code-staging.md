# ADR-017 — Develop actual product code before dependent integration

Date: 2026-11-26 (Asia/Tehran).
Status: owner-directed scheduling change; effective on protected merge.
Baseline: c305fcf2e454f424b53207c9e9798ccc02cb20a7.
References: ADR-012, ADR-015, AGENTS.md, manifests/coding_path.csv, manifests/tasks.csv.

## Context

The owner explicitly requests development of other ETEMAD packages alongside Gate-00 evidence, and rejects prototype/ZIP-only deliverables. Current planning conflates opening a product implementation task with integrating it. Keep the existing acceptance and security conditions; change only the order of authoring actual product code.

## Decision

- After this ADR merges, allow production-intended implementation in the original repository's scoped task branches before a dependent Gate passes, only if the frozen contracts, authoritative references, existing interfaces and task-owned paths are sufficient. Use the real implementation target, not a parallel mock implementation or ZIP. Tests may use synthetic inputs and temporary local PostgreSQL and mock external dependencies; this is a test environment for actual product code, not a substitute product. Preserve existing functionality.
- The existing matrix Gate and task dependencies remain mandatory for acceptance, opening an integration-ready PR, merging product changes into main and enabling features. If a required Gate is open, record the branch/head and evidence as IMPLEMENTATION_IN_PROGRESS or TESTED_AWAITING_DEPENDENCIES, never PASS/accepted. An unresolved interface or source contradiction stops that affected change; no schema change, fabricated API, dependency bypass or integration claim.
- Work in one active task at a time; a completed authoring branch may be parked without an open PR to allow Gate evidence work. Do not let parked branches block the evidence lane. Record branch name, exact baseline and head SHA, changed paths, executed tests, pending dependencies and next step in the evidence record. Refresh against protected main, retest and open a scoped PR only after all relevant gates/dependencies are actually satisfied. Never force-push or push directly to main.
- First implementation candidate is S03-006: real central PostgreSQL repository for normalized, clustered and classified news, using owned tables and existing frozen contracts. Read S03-002/003, S03-006, S03-007, current database interfaces, schema and migration ownership before coding. Use a separate migration task in the same owning package when needed; do not invent columns or merge across unresolved contract/DB boundaries. Preserve uniqueness, provenance, original records, history, transactional behavior and permission isolation. If an interface conflict blocks the candidate, report it and select another authorable production module with stable inputs.
- Continue Gate-00 evidence independently, then Gate-01 and integration in dependency order. Existing ADR-015 advanced security ownership and studio deferral remain unchanged. No real credentials, live external APIs, publishing, paid calls, public deployment or operational release are authorized. No change to contract versions, security thresholds, required CI, branch protection, or Gate acceptance procedures.

This ADR supersedes ADR-012/015 and queue wording only insofar as they prohibit *authoring* a downstream implementation on an isolated branch before integration prerequisites pass. It does not waive any integration or acceptance criterion. Rollback: protected revert PR; parked branches remain unmerged until compliant.
