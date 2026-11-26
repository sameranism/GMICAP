# ETEMAD — Agent operating rules (bootstrap)

## Source of truth and stop conditions
- Read repository files and the approved ETEMAD roadmap before changing code. Do not infer missing contracts.
- The Stage S00 gate is **not passed**. No B01–B09 implementation or deployment is authorized by this bootstrap.
- If a required master spec, task manifest, attachment list, or schema is absent, report BLOCKED with the missing path. Never fabricate its contents.
- Work on a task-specific branch. Open a draft pull request. Never push directly to main, force-push, or merge without explicit approval.
- Preserve existing code, security, access control, audit and rollback. Prefer extension-first changes and versioned contracts.
- Never write secrets, access tokens, credentials, production data or personal data into git; use secret references and approved secret stores.
- No external publishing, third-party API call, production deployment, or database migration without authorized review and safety gates.
- One canonical processing result; channel-specific formatting belongs in separate output adapters.
- Before edits: inventory relevant files, list exact task ID, affected paths, dependencies and acceptance criteria. Avoid out-of-scope edits.
- After edits: provide changed-file list, commands actually executed, test output, remaining risks and next task. Never claim an unexecuted test passed.

## Stage S00 prerequisites
Expected roadmap references include `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `manifests/tasks.csv`, `guides/FIRST_PROMPT_CODEX.md`, `prompts/00_BOOTSTRAP/SHARED/S00-001__AGENTS_md.md`, its `__ATTACHMENTS.txt`, and `prompts/GATES/GATE-00-REVIEW.md`. These references are **not yet present**; obtain and inspect approved originals before treating this file as final S00-001 output.

## Review gate
S00 is complete only after master and package specs, 30 contracts and examples, rules consistency, technical decisions, secret review, and real contract checks are reviewed. CI bootstrap checks do not equal the contract gate.
