# ETEMAD execution state

## Production implementation scheduling — 2026-11-26

The owner rejects prototype-only deliverables. [ADR-017](../decisions/ADR-017-production-code-staging.md) allows real task-owned implementation on parked branches, subject to authoritative interfaces. Integration/acceptance still requires all dependency Gates and exact-head checks. No new runtime implementation or gate acceptance is claimed by this decision. First candidate S03-006; continue Gate-00 evidence. Effective on protected merge.

## S00-001 continuation checkpoint — 2026-11-26

- [PR #73](https://github.com/sameranism/ETEMAD-pre/pull/73) merged evidence for
  S00-017, S00-018 and S00-055 at `0bb9240cd712011b042c279dffbbeb67c1f6daf1`.
- [PR #74](https://github.com/sameranism/ETEMAD-pre/pull/74) changed only `AGENTS.md`.
  Exact checked PR head `452ef7f43dbb6dd8f974a4576f96b6105a0180fc` merged at
  `765a193bd409eafb84bcabd6e5868f29639ac703`. Preflight, 10 focused tests,
  full foundation checks and exact-head CI passed. See the [evidence register](../gates/GATE-00.md).
- Four of 62 Gate-00 rows now have scoped PASS evidence (6.5%). The active
  target-path inventory remains 111 of 216 (51.4%); whole-project acceptance
  progress is unmeasured. Gate-00 and Gate-01 remain open.
- Continue OPS-001 with S00-002, the next open phase-zero row after S00-001.
  Inspect the current architecture rule and run its preflight and applicable
  tests before changing it. Preserve the remaining semantic and security
  requirements and keep S03-006 gated by its documented dependencies.

## Gate-00 task evidence — 2026-11-26

[PR #72](https://github.com/sameranism/ETEMAD-pre/pull/72) merged at signed main `1a09ebe7fc7a975c54017b419102fd2b7b17f72c`; all exact-head and main CI, CodeQL, Guardian passed. The Gate-00 register now records scoped PASS evidence for S00-017, S00-018 and S00-055 (effective after this documentation PR passes and merges). Local S00-055 fixture check verified the Git blob and rejected two violations with exit 1. Actions Secrets screenshot shows no configured repository/environment secrets, not a clean scan. Remaining semantic and applicable baseline security evidence stays BLOCKED. Continue first eligible task; no change to dependencies or deployment authorization.

## Verified containment and credential-file checkpoint — 2026-11-26

Signed protected main baseline: `64dc647cdbde2816a91df4a76807073b65107380`, [PR #70](https://github.com/sameranism/ETEMAD-pre/pull/70).
- [PR #67](https://github.com/sameranism/ETEMAD-pre/pull/67) merged ADR-015 and [PR #68](https://github.com/sameranism/ETEMAD-pre/pull/68) merged ADR-016. [PR #69](https://github.com/sameranism/ETEMAD-pre/pull/69) implemented executive_private shared fixture guard at signed main `c928a1d02334b0aa3f4a2169bdb9b30fbb3d0ac4`. Five new cases passed, with 172 backend tests, 15 warnings, 62 task preflights, 336 negative contract cases, boundary checks, Ruff and Mypy. [Backend](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720355075/job/139576842631), [contracts](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720355174/job/139576843599), [CodeQL](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720355117), [Guardian](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720355306), [bootstrap](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720355513). All four post-merge workflows at c928a1d also passed.
- S00-052: PR #70 changes only .gitignore. Exact-head [backend](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720637600), [contract](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720637546), [CodeQL](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720637601), [Guardian](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720637146), and [bootstrap](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720637466) all passed. Independently rechecked exact PR-head ignore rules in a temporary local Git repository: `git check-ignore -q --no-index PATH` returned expected exit 0 for 21 ignored paths and 1 for seven retained paths (including sample schemas/examples, .env.example and public SSH key). Harness exit 0, 28/28. This supersedes the earlier PR description's unverified 24-case count; no repository history/content scan was performed locally. No real credentials were accessed. Main post-merge CI for PR #70 was pending at capture.
- Owner-supplied GitHub Advanced Security screenshot shows Secret Protection enabled (Disable button), Push protection On, Security alert severity Any, standard alert severity Only errors. This is configuration evidence, not an alert count or scan outcome; screenshot is not committed to the public repository. The connector again rejected `/secret-scanning/alerts?state=open&per_page=100` with HTTP 400 (endpoint not allowed). Open alert count and complete scan coverage remain UNKNOWN. Do not claim a clean scan, disclose secrets, or disable protection.
- Gate-00 remains OPEN/BLOCKED: remaining semantic contract audits, applicable baseline archive/storage and authorization evidence, per-task evidence and secret scan outcome. Dedicated private infrastructure and integrated security remain at owning stages per ADR-015. No production data or external actions. Gate-01 and approved source-list dependencies remain open. S03-006 not started.

## Owner scheduling decision — 2026-11-26

- [PR #65](https://github.com/sameranism/ETEMAD-pre/pull/65) merged fixture workflow remediation; exact-main CI at `5ae55df26169b0034ebfc2a68e1ae66bbcf123cd` passed, including 167 backend tests and 336 negative contract cases. [PR #66](https://github.com/sameranism/ETEMAD-pre/pull/66) merged S00-041 audit at signed main `190649ad3b75969b7345beb3da71f1f21bc070a7`, exact-head mandatory CI PASS.
- [ADR-015](../decisions/ADR-015-stage-security-delivery.md) schedules advanced implementations at existing owning phases; no security baseline or dependency is waived. This documentation PR requires its own exact-head checks.
- Gate-00 remains OPEN/BLOCKED. Next: scoped fail-closed shared event routing for executive_private, applicable baseline security evidence and contract semantics. Then select the first eligible task in QUEUE. S03-006 still requires Gate-00/Gate-01 and source/dependency evidence. No production use, real private data or external side effects.

## Restricted routing remediation — 2026-11-26

- [PR #60](https://github.com/sameranism/ETEMAD-pre/pull/60) merged ADR-013 at signed main [`514c5d6f1be87ac58537fb3b0c1d16a592827599`](https://github.com/sameranism/ETEMAD-pre/commit/514c5d6f1be87ac58537fb3b0c1d16a592827599). Its exact-head [backend](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715186755), [contracts](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715186800), [bootstrap](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715186622), [Guardian](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715186900), and [CodeQL](https://github.com/sameranism/ETEMAD-pre/actions/runs/45715186951) all passed.
- [Ruleset 28111497](https://github.com/sameranism/ETEMAD-pre/rules/28111497) re-read: extra unattributed-change approval is now false; zero ordinary approvals, strict required checks, native CodeQL, signatures, linear history, squash PRs and no bypass actors retained.
- Scoped ADR-013 correction in this change: the frozen v1.0 event constructor accepts restricted; shared fixture bus and outbox reject restricted before delivery, deduplication or persistence, and recheck at dispatch. New tests exercise constructor compatibility, unknown version/classification, raw envelopes, idempotency, mutated pending entries and ordinary delivery. No wire schema or existing test changed. Local git access failed (DNS); fresh exact-head CI is required and not claimed here.
- Gate-00 remains OPEN/BLOCKED; authenticated restricted transport, executive-private routing, remaining semantic audits and permission/secret checks are not accepted. Gate-01 and allowed-source prerequisites remain open; S03-006 not started. No production use or external services authorized.

## Verified checkpoint — 2026-11-26 (Asia/Tehran), baseline `d1d773db8038ab3ac4b06f6c54ac450a2158ced7`

- [PR #58](https://github.com/sameranism/ETEMAD-pre/pull/58) is merged at [signed main commit](https://github.com/sameranism/ETEMAD-pre/commit/d1d773db8038ab3ac4b06f6c54ac450a2158ced7). The exact-head [bootstrap check](https://github.com/sameranism/ETEMAD-pre/actions/runs/45713010755), [backend](https://github.com/sameranism/ETEMAD-pre/actions/runs/45713010676), [contracts](https://github.com/sameranism/ETEMAD-pre/actions/runs/45713010784) and [CodeQL](https://github.com/sameranism/ETEMAD-pre/actions/runs/45713010804) report success.
- On this exact main SHA, [backend CI](https://github.com/sameranism/ETEMAD-pre/actions/runs/45713211748/job/139552603583) reports 142 passed, 15 warnings, PostgreSQL 18.7, including the migration round-trip/database-separation test. Lint, type checking and contract validation steps succeeded. [Contract CI](https://github.com/sameranism/ETEMAD-pre/actions/runs/45713211853/job/139552603853) reports 62 task preflights, 336 negative contract cases and passing boundary checks. Its separate [unit job](https://github.com/sameranism/ETEMAD-pre/actions/runs/45713211853/job/139552604220) reports 141 passed, 1 skipped (no PostgreSQL URL), 1 warning. [Main Guardian audit](https://github.com/sameranism/ETEMAD-pre/actions/runs/45713211848) and [CodeQL](https://github.com/sameranism/ETEMAD-pre/actions/runs/45713211725) succeeded.
- Reconciled the 223 rows in manifests/tasks.csv against the complete recursive Git tree at this SHA. Seven studio tasks remain deferred; 216 active, 111 active target paths present (51.39%; 111/223 = 49.78% overall). All 62 S00 and 30 S01 targets exist. Presence is not acceptance: the 62 S00 rows remain blocked; a complete per-task acceptance percentage cannot yet be verified.
- [Ruleset 28111497](https://github.com/sameranism/ETEMAD-pre/rules/28111497) is active with zero ordinary approvals, no bypass actors, strict four required status checks, native CodeQL, signed squash PRs, linear history, deletion and force-push prevention. The extra approval for unattributed changes remains true, contrary to ADR-012. The current connector exposes no ruleset write action; configuration requires an authorized administrative interface. No protection was changed.
- Gate-00 remains OPEN/BLOCKED. The frozen schema accepts restricted, but backend/core/events.py CLASSIFICATIONS omits it. The shared event behavior/routing and authorization decision requires explicit owner approval before code changes in this execution. Do not silently narrow or alter the frozen schema. See the gate register for missing semantic, privacy, secret and permission evidence.
- Gate-01: no acceptance register found in docs/gates at this revision. The coding path requires Gate-01 PASS and allowed source list for S03-002, S03-003 and S03-006. Verify these, and the task-specific acceptance logs for S03-002/003, before S03-006. No production integrations authorized.
- At the observed baseline there were zero open PRs and zero open issues. This checkpoint is documentation-only evidence maintenance; the old checkpoints and failed runs remain below. Rollback via a protected revert PR.

## Current checkpoint — 2026-11-26 (Asia/Tehran)

- [PR #56](https://github.com/sameranism/ETEMAD-pre/pull/56) merged
  `887e83f3609da993e75725538f5a93255031de30` as
  `e297b5f9de301e4d07ac108d808615e6e14a6cb7`, adopting ADR-012 and
  automatic development acceptance. [Post-merge Guardian](https://github.com/sameranism/ETEMAD-pre/actions/runs/45711967375)
  and [CodeQL on main](https://github.com/sameranism/ETEMAD-pre/actions/runs/45711967167)
  passed. Personal review for new development is NOT_REQUIRED under repository policy.
- [PR #57](https://github.com/sameranism/ETEMAD-pre/pull/57) merged
  `fabfcf8e3aacd0e8d0c18caaa774dd15e17548ba` as
  `58c2b53bf2e53234d42e7c9123a1a83c84cc91fc`. Its exact-head
  [backend CI](https://github.com/sameranism/ETEMAD-pre/actions/runs/45712445039)
  passed 140 tests on PostgreSQL 18 including separate central and domestic
  migration round trips. [Trusted Guardian](https://github.com/sameranism/ETEMAD-pre/actions/runs/45712444735)
  and [CodeQL](https://github.com/sameranism/ETEMAD-pre/actions/runs/45712445030)
  passed. The foreign fixture remained untouched; there is no foreign migration.
- The [first main audit attempt for #57](https://github.com/sameranism/ETEMAD-pre/actions/runs/45712663422/attempts/1)
  failed while the merge-to-PR association was unavailable. The GitHub API now
  maps the exact commit to merged PR #57. A bounded association retry preserves a
  failed audit when GitHub does not return the matching PR.
- The Gate-00 semantic audit reproduced a v1.0 producer mismatch for
  `event_envelope.classification=restricted`. Record exact contract
  and routing evidence before changing producer behavior. The approved
  source list remains a downstream prerequisite for S03-006.

- Canonical repository: [sameranism/ETEMAD-pre](https://github.com/sameranism/ETEMAD-pre), protected `main`.
- Security maintenance [PR #55](https://github.com/sameranism/ETEMAD-pre/pull/55)
  squash merged head `66c40b443413926a90feccac9d4d627fd1516644` as
  `48d0e77c1092a20150f5f000b5630d99bab2aab6`. All four native status contexts
  and CodeQL passed on its head. CodeQL also passed on
  [main run 45710579171](https://github.com/sameranism/ETEMAD-pre/actions/runs/45710579171).
- The prior Merge Guardian returned failure for missing sensitive-change approval on
  [PR #55](https://github.com/sameranism/ETEMAD-pre/actions/runs/45709344599)
  and its [main push](https://github.com/sameranism/ETEMAD-pre/actions/runs/45710579289).
  Both are historical results under the old policy. The status is outside the
  four required native status contexts for this merge.
- [Ruleset 28111497](https://github.com/sameranism/ETEMAD-pre/rules/28111497):
  active, no bypass actors, four strict CI requirements, CodeQL, signed squash-only
  PRs, deletion and force-push blocked. Unattributed-change approval is still on.
- S09-023: the exact-head [backend run](https://github.com/sameranism/ETEMAD-pre/actions/runs/45709344460)
  passed Ruff, Mypy, contract validation and Pytest and saved its test summary.
  Prior failed attempts remain in the history below.
- Gate-00: `OPEN / BLOCKED`. [Evidence and exact gaps](../gates/GATE-00.md).
  Gate-01 acceptance evidence has not been verified on the canonical repository.
- Next product task: `S03-006` after Gate-00, Gate-01, source scope and S03-002/S03-003
  acceptance. Local preflight passed for all three. The current processing repository
  is fixture-backed. The queue uses `canonical_url` and `content_hash`, while the
  existing migration uses `(source_id, original_url)` and an indexed
  `fingerprint`. Resolve the storage uniqueness and history criteria within the
  processing ownership boundary before wiring PostgreSQL.
- Inventory baseline: 111 of 223 target paths present (49.8% path coverage).
  Accepted-task progress is unmeasured because the per-task evidence is incomplete.
  Seven studio tasks remain deferred by the owner.
- Rollback: revert an accepted change through a protected PR, with the applicable
  checks and native CodeQL scanning still active.

## Historical checkpoint — previous repository

## Current task

- Task: `S09-023`
- Branch: `feat/s09-023-backend-ci`
- PR: [#45](https://github.com/etemadion/ETEMAD/pull/45) (draft)
- State: CI failed after two debug attempts. The remaining findings require changes to existing backend files outside the workflow target.

## Review and evidence

- Second agent reviewed the proposal locally. Its review does not constitute GitHub approval.
- Local checks passed: 62 manifest targets, relative links, 30 schemas and examples, and package boundaries including two negative fixtures.
- [OPS-001 PR #43](https://github.com/etemadion/ETEMAD/pull/43) was merged. The ADR remains proposed and Gate-00 remains open.

## Review debt

- OPS-002 / PR #44: self-review with evidence. Diff contains the workflow, ADR and state record. Read-only replay detected the unreviewed PR #43 and the eight reviewer-selection fixtures passed. No independent GitHub approval recorded.
- OPS-001 / PR #43: GitHub reports merged with no recorded reviews. Gate-00 remains open.

## Isolated follow-on work

- OPS-002 [CI](https://github.com/etemadion/ETEMAD/actions/runs/45277350200) passed. A read-only replay of main commit 7756736 reported PR #43 missing independent approval and returned the expected failure.
- S09-023: [attempt 1](https://github.com/etemadion/ETEMAD/actions/runs/45279433244) added jsonschema stubs (16 Ruff / 4 mypy findings). [Attempt 2](https://github.com/etemadion/ETEMAD/actions/runs/45279556236) set the repository import root (7 Ruff / 4 mypy findings). Both CI runs failed. Contract validation and all 106 backend tests passed.
- GitHub listed one collaborator, the PR author's account. The branch protection API returned 403.

## Baseline

- `main`: `2c60ac932c9675801614172992dbcc5e110bab03`
- [Baseline CI](https://github.com/samram-shipt-it/ETEMAD/actions/runs/45272942280): 106 passed, 1 warning.
- Gate-00: open, pending independent PASS.
- `main` branch protection: inactive at the last GitHub API check.
- Next isolated product task in [QUEUE.md](QUEUE.md): `S03-006`, subject to its repository and PostgreSQL prerequisites.

See the [Gate register](../gates/GATE-00.md) for task evidence and the
[ADR proposal](../decisions/ADR-010-gate00-conditional-acceptance.md) for closure conditions.
