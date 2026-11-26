# B09 — دیدبان (Newsroom Dashboard)

شناسه ثابت بسته: `B09` | مسیر مفهومی: `dashboard`
سند مرجع: `source/specs/B09_INTERFACE_TECHNICAL_SPEC.md`

تعداد تسک‌های برنامه: **33**

| مرحله | تسک | فایل خروجی | مدل | پرامپت |
|---:|---|---|---|---|
| 2 | `S02-016` | `frontend/src/design-system/tokens.json` | G | `prompts/02_INGEST_AND_DESIGN/B09/S02-016__tokens_json.md` |
| 2 | `S02-017` | `frontend/src/design-system/theme.css` | U | `prompts/02_INGEST_AND_DESIGN/B09/S02-017__theme_css.md` |
| 2 | `S02-018` | `frontend/src/styles/globals.css` | U | `prompts/02_INGEST_AND_DESIGN/B09/S02-018__globals_css.md` |
| 2 | `S02-019` | `frontend/src/design-system/README.md` | U | `prompts/02_INGEST_AND_DESIGN/B09/S02-019__README_md.md` |
| 2 | `S02-020` | `frontend/src/assets/BRAND_ASSETS_REQUIRED.md` | U | `prompts/02_INGEST_AND_DESIGN/B09/S02-020__BRAND_ASSETS_REQUIRED_md.md` |
| 8 | `S08-001` | `frontend/src/app/App.tsx` | U | `prompts/08_DASHBOARD/B09/S08-001__App_tsx.md` |
| 8 | `S08-002` | `frontend/src/app/router.tsx` | U | `prompts/08_DASHBOARD/B09/S08-002__router_tsx.md` |
| 8 | `S08-003` | `frontend/src/lib/api.ts` | C | `prompts/08_DASHBOARD/B09/S08-003__api_ts.md` |
| 8 | `S08-004` | `frontend/src/lib/contracts.ts` | C | `prompts/08_DASHBOARD/B09/S08-004__contracts_ts.md` |
| 8 | `S08-005` | `frontend/src/components/AppShell.tsx` | U | `prompts/08_DASHBOARD/B09/S08-005__AppShell_tsx.md` |
| 8 | `S08-006` | `frontend/src/components/NewsTable.tsx` | U | `prompts/08_DASHBOARD/B09/S08-006__NewsTable_tsx.md` |
| 8 | `S08-007` | `frontend/src/components/StatusBadge.tsx` | U | `prompts/08_DASHBOARD/B09/S08-007__StatusBadge_tsx.md` |
| 8 | `S08-008` | `frontend/src/components/SourceCitation.tsx` | U | `prompts/08_DASHBOARD/B09/S08-008__SourceCitation_tsx.md` |
| 8 | `S08-009` | `frontend/src/features/newsroom/NewsDesk.tsx` | G | `prompts/08_DASHBOARD/B09/S08-009__NewsDesk_tsx.md` |
| 8 | `S08-010` | `frontend/src/features/editor/ArticleEditor.tsx` | G | `prompts/08_DASHBOARD/B09/S08-010__ArticleEditor_tsx.md` |
| 8 | `S08-011` | `frontend/src/features/translation/TranslatorWorkspace.tsx` | G | `prompts/08_DASHBOARD/B09/S08-011__TranslatorWorkspace_tsx.md` |
| 8 | `S08-012` | `frontend/src/features/analysis/PoliticalAnalysis.tsx` | G | `prompts/08_DASHBOARD/B09/S08-012__PoliticalAnalysis_tsx.md` |
| 8 | `S08-013` | `frontend/src/features/executive/ExecutiveDashboard.tsx` | G | `prompts/08_DASHBOARD/B09/S08-013__ExecutiveDashboard_tsx.md` |
| 8 | `S08-014` | `frontend/src/features/owner/OwnerDashboard.tsx` | G | `prompts/08_DASHBOARD/B09/S08-014__OwnerDashboard_tsx.md` |
| 8 | `S08-015` | `frontend/src/features/staff/StaffDashboard.tsx` | U | `prompts/08_DASHBOARD/B09/S08-015__StaffDashboard_tsx.md` |
| 8 | `S08-016` | `frontend/src/features/sources/SourcesManager.tsx` | U | `prompts/08_DASHBOARD/B09/S08-016__SourcesManager_tsx.md` |
| 8 | `S08-017` | `frontend/src/features/publishing/PublishingCenter.tsx` | G | `prompts/08_DASHBOARD/B09/S08-017__PublishingCenter_tsx.md` |
| 8 | `S08-018` | `frontend/src/features/studio/StudioWorkspace.tsx` | U | `prompts/08_DASHBOARD/B09/S08-018__StudioWorkspace_tsx.md` |
| 8 | `S08-019` | `frontend/src/features/settings/Settings.tsx` | G | `prompts/08_DASHBOARD/B09/S08-019__Settings_tsx.md` |
| 8 | `S08-020` | `frontend/src/features/auth/Login.tsx` | U | `prompts/08_DASHBOARD/B09/S08-020__Login_tsx.md` |
| 8 | `S08-021` | `frontend/src/i18n/fa.ts` | U | `prompts/08_DASHBOARD/B09/S08-021__fa_ts.md` |
| 8 | `S08-022` | `frontend/tests/access.spec.ts` | C | `prompts/08_DASHBOARD/B09/S08-022__access_spec_ts.md` |
| 8 | `S08-023` | `frontend/tests/newsroom.spec.ts` | U | `prompts/08_DASHBOARD/B09/S08-023__newsroom_spec_ts.md` |
| 8 | `S08-024` | `frontend/tests/design-system.spec.ts` | U | `prompts/08_DASHBOARD/B09/S08-024__design-system_spec_ts.md` |
| 8 | `S08-025` | `frontend/src/lib/auth.ts` | C | `prompts/08_DASHBOARD/B09/S08-025__auth_ts.md` |
| 8 | `S08-026` | `frontend/src/lib/query.ts` | C | `prompts/08_DASHBOARD/B09/S08-026__query_ts.md` |
| 8 | `S08-027` | `frontend/src/components/PrivateReportGuard.tsx` | U | `prompts/08_DASHBOARD/B09/S08-027__PrivateReportGuard_tsx.md` |
| 8 | `S08-028` | `frontend/src/components/ConfirmAction.tsx` | U | `prompts/08_DASHBOARD/B09/S08-028__ConfirmAction_tsx.md` |

**قاعده:** پیش از ویرایش، ورودی‌های هر تسک در فایل `__ATTACHMENTS.txt` کنار پرامپت مشخص است.
**مرز:** خروجی‌ها فقط با API/Event نسخه‌دار و مجوز به بسته دیگر منتقل شوند.
