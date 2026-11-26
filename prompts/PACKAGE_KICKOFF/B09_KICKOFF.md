# آغاز تیم B09 — دیدبان / Newsroom Dashboard

**مدل پیشنهادی برای برنامه‌ریزی بسته:** Grok in Cursor local Agent (UI preview). **پذیرش برنامه:** پیش‌نیازها و شواهد آزمون طبق ADR-012.

## ضمائم لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/specs/B09_INTERFACE_TECHNICAL_SPEC.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `manifests/tasks.csv`
- `cursor-kit/AGENTS.md`
- فایل‌های `__ATTACHMENTS.txt` کنار تسک‌های همین بسته (در زمان اجرای هر تسک).

## پرامپت آماده

You are the package lead for **B09 / Newsroom Dashboard** in ETEMAD Intelligent Newsroom. Read the master specification, THIS package technical specification, `AGENTS.md`, `manifests/tasks.csv`, related baseline JSON Schemas/examples, and the existing repository tree. Your current job is **planning only**: verify scope, inputs, outputs, owned DB tables, APIs and downstream consumers of this package. Do not code the entire package in one run.

List exactly which tasks below are ready, blocked or depend on other packages. Assign each file to the recommended model shown in the task's prompt; identify parallelizable tasks with non-overlapping files. Preserve all 29 project IDs and the latest UI stack (shadcn/Tailwind, not Mantine). Do not make up source URLs, CMS choice, brand colors, API endpoints, test results or legal approval. For unknowns, use a safe mock/placeholder and mark the real integration BLOCKED. No direct cross-package database access; no public path for EIC private reports; honor output switches. Report the actual test plan, acceptance criteria, external decision blockers, and proposed PR order.

**Do not change code or contracts during this kickoff.** Output a reviewable execution plan and the exact first ready task ID.

## فهرست تسک‌های این بسته (33)
- `S02-016` — `frontend/src/design-system/tokens.json` | G | `prompts/02_INGEST_AND_DESIGN/B09/S02-016__tokens_json.md`
- `S02-017` — `frontend/src/design-system/theme.css` | U | `prompts/02_INGEST_AND_DESIGN/B09/S02-017__theme_css.md`
- `S02-018` — `frontend/src/styles/globals.css` | U | `prompts/02_INGEST_AND_DESIGN/B09/S02-018__globals_css.md`
- `S02-019` — `frontend/src/design-system/README.md` | U | `prompts/02_INGEST_AND_DESIGN/B09/S02-019__README_md.md`
- `S02-020` — `frontend/src/assets/BRAND_ASSETS_REQUIRED.md` | U | `prompts/02_INGEST_AND_DESIGN/B09/S02-020__BRAND_ASSETS_REQUIRED_md.md`
- `S08-001` — `frontend/src/app/App.tsx` | U | `prompts/08_DASHBOARD/B09/S08-001__App_tsx.md`
- `S08-002` — `frontend/src/app/router.tsx` | U | `prompts/08_DASHBOARD/B09/S08-002__router_tsx.md`
- `S08-003` — `frontend/src/lib/api.ts` | C | `prompts/08_DASHBOARD/B09/S08-003__api_ts.md`
- `S08-004` — `frontend/src/lib/contracts.ts` | C | `prompts/08_DASHBOARD/B09/S08-004__contracts_ts.md`
- `S08-005` — `frontend/src/components/AppShell.tsx` | U | `prompts/08_DASHBOARD/B09/S08-005__AppShell_tsx.md`
- `S08-006` — `frontend/src/components/NewsTable.tsx` | U | `prompts/08_DASHBOARD/B09/S08-006__NewsTable_tsx.md`
- `S08-007` — `frontend/src/components/StatusBadge.tsx` | U | `prompts/08_DASHBOARD/B09/S08-007__StatusBadge_tsx.md`
- `S08-008` — `frontend/src/components/SourceCitation.tsx` | U | `prompts/08_DASHBOARD/B09/S08-008__SourceCitation_tsx.md`
- `S08-009` — `frontend/src/features/newsroom/NewsDesk.tsx` | G | `prompts/08_DASHBOARD/B09/S08-009__NewsDesk_tsx.md`
- `S08-010` — `frontend/src/features/editor/ArticleEditor.tsx` | G | `prompts/08_DASHBOARD/B09/S08-010__ArticleEditor_tsx.md`
- `S08-011` — `frontend/src/features/translation/TranslatorWorkspace.tsx` | G | `prompts/08_DASHBOARD/B09/S08-011__TranslatorWorkspace_tsx.md`
- `S08-012` — `frontend/src/features/analysis/PoliticalAnalysis.tsx` | G | `prompts/08_DASHBOARD/B09/S08-012__PoliticalAnalysis_tsx.md`
- `S08-013` — `frontend/src/features/executive/ExecutiveDashboard.tsx` | G | `prompts/08_DASHBOARD/B09/S08-013__ExecutiveDashboard_tsx.md`
- `S08-014` — `frontend/src/features/owner/OwnerDashboard.tsx` | G | `prompts/08_DASHBOARD/B09/S08-014__OwnerDashboard_tsx.md`
- `S08-015` — `frontend/src/features/staff/StaffDashboard.tsx` | U | `prompts/08_DASHBOARD/B09/S08-015__StaffDashboard_tsx.md`
- `S08-016` — `frontend/src/features/sources/SourcesManager.tsx` | U | `prompts/08_DASHBOARD/B09/S08-016__SourcesManager_tsx.md`
- `S08-017` — `frontend/src/features/publishing/PublishingCenter.tsx` | G | `prompts/08_DASHBOARD/B09/S08-017__PublishingCenter_tsx.md`
- `S08-018` — `frontend/src/features/studio/StudioWorkspace.tsx` | U | `prompts/08_DASHBOARD/B09/S08-018__StudioWorkspace_tsx.md`
- `S08-019` — `frontend/src/features/settings/Settings.tsx` | G | `prompts/08_DASHBOARD/B09/S08-019__Settings_tsx.md`
- `S08-020` — `frontend/src/features/auth/Login.tsx` | U | `prompts/08_DASHBOARD/B09/S08-020__Login_tsx.md`
- `S08-021` — `frontend/src/i18n/fa.ts` | U | `prompts/08_DASHBOARD/B09/S08-021__fa_ts.md`
- `S08-022` — `frontend/tests/access.spec.ts` | C | `prompts/08_DASHBOARD/B09/S08-022__access_spec_ts.md`
- `S08-023` — `frontend/tests/newsroom.spec.ts` | U | `prompts/08_DASHBOARD/B09/S08-023__newsroom_spec_ts.md`
- `S08-024` — `frontend/tests/design-system.spec.ts` | U | `prompts/08_DASHBOARD/B09/S08-024__design-system_spec_ts.md`
- `S08-025` — `frontend/src/lib/auth.ts` | C | `prompts/08_DASHBOARD/B09/S08-025__auth_ts.md`
- `S08-026` — `frontend/src/lib/query.ts` | C | `prompts/08_DASHBOARD/B09/S08-026__query_ts.md`
- `S08-027` — `frontend/src/components/PrivateReportGuard.tsx` | U | `prompts/08_DASHBOARD/B09/S08-027__PrivateReportGuard_tsx.md`
- `S08-028` — `frontend/src/components/ConfirmAction.tsx` | U | `prompts/08_DASHBOARD/B09/S08-028__ConfirmAction_tsx.md`


**ملاک موفقیت:** هر تسک دارای فایل هدف یکتا، ضمیمه مشخص، تست صریح و معیار پذیرش خودکار داشته باشد.
