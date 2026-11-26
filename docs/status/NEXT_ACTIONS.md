# S00 handoff — task sequencing

1. Recover the **original** Cursor v2 package and confirm its provenance/version. Do not synthesize contract schemas or prompt attachments.
2. Inventory all named file paths in the original `manifests/tasks.csv` and the master specification. Record missing dependencies and conflicts in an issue or separate PR.
3. Complete S00-001 using `prompts/00_BOOTSTRAP/SHARED/S00-001__AGENTS_md.md` and its exact attachment list, then reconcile this provisional `AGENTS.md`.
4. Complete S00-002–S00-062 in small, scoped, reviewable PRs, including schema checks and UI decisions.
5. Independently execute `prompts/GATES/GATE-00-REVIEW.md` and record **actual** CI run URLs and checks. Only after passing gate S00, begin B01.

Never merge this draft without reviewing its diff and confirming the imported roadmap does not conflict with these temporary bootstrap rules.
