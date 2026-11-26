# ADR-011 — Report independent review after a push to main

**Superseded policy.** See [ADR-012](ADR-012-automated-acceptance.md) for current acceptance. Historical decisions and findings below retain their original status.

- **Status:** Historical proposal; superseded for routine development once the single-owner ADR and native protection are effective
- **Task:** OPS-002
- **Date:** 2026-11-24

GitHub reported `protected: false` on `main`. The branch protection endpoint
returned HTTP 403 and identified the account plan or repository visibility as
the limitation. The collaborator endpoint listed only the PR author's account.

Run a read-only GitHub Actions job after each push to `main`. Report every new
first-parent commit and fail the job when it lacks a linked merged PR with a
current-head approval from a distinct eligible reviewer. Contract validation and
backend tests remain in `contract-check.yml`, which runs separately on main pushes.

GitHub Actions reports failures after a push. Keep independent approval, the
Gate-00 decision, and native branch protection as separate controls. Do not
merge, revert, open issues, alter permissions, or deploy automatically.

The pull request runs review-selection fixtures. Verify live push behavior only
once this workflow reaches `main` through an approved PR. Close the draft to
withdraw the proposal or revert the two files through a reviewed PR.

The successor policy is documented in [ADR-011 single-owner development](ADR-011-single-owner-development.md). Existing review evidence is historical and must not be rewritten.
