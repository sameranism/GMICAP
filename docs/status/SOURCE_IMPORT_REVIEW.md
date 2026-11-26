# ETEMAD source import review — 2026-11-22
Status: source import prepared for review; S00 and Gate-00 NOT PASSED.

## First unfinished operation
The one-time preparation in guides/CURSOR_START_FA.md requires the original source/prompt/manifest/guide package in the repository before S00-001. Import the complete v2 package unchanged. Do not execute S00-001 in this change.

## Observed repository baseline
- main: dd9415e4aad90d9711828aacb088b051747c3e39, seven tracked files; no backend/frontend product code, schemas, manifests or original specs.
- PR #1 merged, despite its BLOCKED description. That merge does not establish S00 completion.
- PR #2 is a draft at bb891459031588ad468a8a296e283e0b1f46abdb, adding only a source receipt and a proposed UI ADR.
- Existing bootstrap-check.yml checks four files for presence, not product behavior or contracts.
- Both observed branches report protected=false. No security settings changed.
- Root AGENTS.md is provisional. Its historical statement about missing references remains unchanged in this import and must be reconciled by S00-001.
- No full prior chat transcripts, local Windows checkout or Cursor account configuration were available for verification.

## Imported evidence and scope
602 files from ETEMAD_CURSOR_PROMPTS_STAGE0_TO_RELEASE_v2.zip; archive SHA-256:
24c331720587c53da130506705c9929435558c10019ba980350cc9104c2a305a
Per-file SHA-256 and Git blob IDs are in SOURCE_IMPORT_HASHES.json.
Original paths including source/original-docx/ are retained. The draft receipt in PR #2 suggested a different original-document location; the actual operational guide and package layout are preserved here.
Starter instructions remain under cursor-kit/. No existing root file is overwritten. Activating/reconciling instructions is separate from this source import.
No product implementation, dependency installation, migration, deployment, paid model call or publication.

## Verification actually executed
- Read the operational guide from repository preparation through S10, S00-001 entry gate and Gate-00 criteria, master/package specifications, decisions and starter rules.
- Parsed all 223 task rows: unique IDs and target paths; 62 S00 tasks.
- Resolved every task prompt path, attachment-list path and each reference in those lists: zero missing paths.
- Compared 10 package DOCX files byte-for-byte with the uploaded standalone documents: all matched; both standalone master copies matched.
- Compared matching contract files in both standalone contract ZIPs to source/contracts/: no differences.
- Standalone ETEMAD_CURSOR_TASK_MATRIX.csv equals manifests/tasks.csv byte-for-byte.
- Ran: python source/contracts/validate_examples.py (from the extracted original package). Exit 0: Validated 30 example files against JSON Schema Draft 2020-12.
- Scanned package text for GitHub/OpenAI token patterns and private-key headers: zero matches. This is a bounded pattern scan, not a comprehensive security certification.
- Shell git clone failed because this environment has no GitHub shell credentials. GitHub connector was used instead.
- Formal negative/semantic contract audits, product tests and independent Gate-00 review: NOT RUN.

## Findings preserved for subsequent tasks
1. Master/B09 v1.1 mention Mantine; v2 CLIENT_DECISIONS specifies shadcn/ui + Tailwind v4. S00-009 owns the formal ADR. PR #2's proposal uses docs/adr/ADR-002-frontend-library.md, whereas the roadmap target is docs/decisions/ADR-002-ui-design-system.md. No source silently changed.
2. Master section 7 lists malformed package owners as "B 0"; source/technical/project_package_map.csv and architecture_packages.json provide explicit B01..B09 ownership. Reconcile in the planned architecture review, preserving originals.
3. Master section 6's prose event fields differ from the actual frozen event_envelope schema (e.g. type/timestamp versus event_type/occurred_at). Passing examples proves only structural validation; do not invent fields or silently alter contracts.
4. The attached v0.1 codebase is a separate reference implementation, not evidence of deployed or merged product functionality. It has not been imported as product code.
5. CMS, official brand assets, platform access, legal approval, hosting/secrets and AI budget remain open. These do not prevent source import; real integrations remain blocked.
6. Cursor Cloud environment/model selection and branch policy enforcement remain unverified prerequisites for their respective workflows.

## Acceptance and next action
Before review, read back the new Git tree and compare every imported blob ID against locally computed IDs, and verify all seven baseline blobs unchanged.
Merge requires explicit approval under existing AGENTS.md. This change remains a draft.
After source-import review/acceptance: S00-001 — canonical agent rules, only AGENTS.md.
Rollback before merge: close the draft; main remains unchanged.
