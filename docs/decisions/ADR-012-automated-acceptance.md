# ADR-012 — Automated development acceptance

Status: Owner-authorized policy, effective when merged into the protected default branch.
Date: 2026-11-26 (Asia/Tehran).

## Decision

An ETEMAD development task, including a change to security, data handling, contracts,
CI, or governance, advances after the applicable automated acceptance checks and
dependency Gates pass. Human, owner, independent-agent and Codex reviews are optional
development feedback. A review that was never performed is recorded as NOT_REQUIRED
for current acceptance. Earlier review and audit results retain their original status.

Use the first dependency-eligible task in the queue. Read its prompt, references and
preconditions, run preflight, and keep the change within its declared scope. A
separate, narrowly scoped ADR and PR is required for a contract or boundary change;
breaking wire changes use a new contract version and compatibility tests. Add
the positive, negative and failure-path checks applicable to the scope. Preserve
existing checks, provenance, private-data isolation, safe defaults and the studio deferral.

## Pull requests and branch protection

Use an up-to-date PR and squash merge the exact checked head through protected main.
Keep deletion and force-push protection, linear history, signed commits, strict
status checks and native CodeQL scanning at the existing alert thresholds.
Set GitHub's approval count to zero and disable mandatory code-owner, last-push,
unattributed-change and other per-person approval conditions. Prefer GitHub Actions
as the expected source for existing Actions checks when configuring rules.
Verify effective protection before merging, and record any remaining configuration drift.

Merge Guardian validates main's native security constraints and PR provenance using
the trusted base on pull_request_target, with no checkout or execution of the PR head
under its status-write token. Its main-push audit verifies that each introduced
main commit came from a merged PR and that the latest applicable exact-head
GitHub workflow runs and their required jobs passed. Missing, failed, stale,
skipped or unexpected evidence fails the applicable check. The native Ruleset
continues to enforce required CI and scanning during merge. GitHub Actions'
commit status alone is not a separate App identity or proof of CI provenance.

## Gates and checkpoints

Use the relevant procedure in [prompts/GATES](../../prompts/GATES). Require passing
checks for every active dependency, with the actual test command, exit code, run
URL, task ID, allowed paths, exact SHA and applicability. Record missing required
results as BLOCKED, failures as FAIL, and executed successful checks as PASS.
Record an out-of-scope optional result as NOT_REQUIRED with its reason. Passing
a structure check never closes the semantic, security or integration requirements.
Resume from the last recorded passing dependency. If a result is missing,
work on the evidenced predecessor or a scoped maintenance correction.

Development acceptance is separate from legal and editorial authorization for
live publishing. Public release, operational deployment, real credentials,
external API/model calls and spending require the owner's specific authorization.

Rollback uses a protected revert PR and retains native protections. Preserve all
historical failed runs, including direct/unassociated commits and results under
the superseded independent-review policy.
