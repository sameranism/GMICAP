# S00 repository readiness — verified baseline

Status: **PARTIAL / BLOCKED**. This is a preparation record, not Stage S00 acceptance.

## Verified repository baseline (2026-11-22)
- Default branch: `main`, initial commit `bc383adcb8d23a6a6b24cad0fc152fbbd6ed4073`.
- At audit time, the sole tracked file was `README.md` containing `# ETEMAD`.
- No pre-existing PRs or GitHub Actions runs were observed at audit time.
- Stage zero is defined in the prior operational guide as S00-001 through S00-062; the source package must be imported before contract audits.

## Completed in this bootstrap branch
- Non-destructive agent guidelines (provisional; not yet reconciled with full S00-001 prompt).
- Ignore patterns for local secrets and build artifacts.
- Minimal bootstrap verification workflow (presence only, not contract tests).
- Scope and dependency tracking for subsequent task-specific PRs.

## Missing required sources / blocked tasks
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md` and the nine package documents.
- `source/contracts/schemas/`: original versioned JSON Schemas and valid/invalid examples (30-contract audit must not be simulated).
- `manifests/tasks.csv`: 223-task matrix and exact prompt/attachment paths.
- `prompts/00_BOOTSTRAP/`, `prompts/PACKAGE_KICKOFF/`, `prompts/GATES/` and `guides/`: original package instructions.
- Approved architectural decisions and the original document pack; do not substitute guessed files.
- Contract test tooling, executable application code, and staging configuration: not implemented.

## S00 gate checklist
- [ ] Full approved source package imported with version/provenance.
- [ ] 10 technical docs reviewed and references resolved.
- [ ] 30 data contracts plus examples audited with results per contract.
- [ ] `AGENTS.md` aligned with final `.cursor/rules` and task prompt.
- [ ] UI library decision (shadcn/ui vs previous Mantine) recorded in decision log.
- [ ] Actual contract check executed in CI or precise blocker recorded.
- [ ] Secret leak and permissions review completed.
- [ ] Gate-00 accepted through the required checks in the current Gate register.

## Next safe action
Import the original ETEMAD Cursor v2 document/prompt/contract package **without modifying its contents** in a separate change; verify file inventory, checksums and unresolved contradictions. Then perform S00-001 in its task branch; do not start B01 until gate acceptance.
