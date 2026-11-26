# آغاز تیم B01 — بنیان / Etemad Core

**مدل پیشنهادی برای برنامه‌ریزی بسته:** Codex. **بازبین برنامه:** Codex مستقل.

## ضمائم لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/specs/B01_FOUNDATION_TECHNICAL_SPEC.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `manifests/tasks.csv`
- `cursor-kit/AGENTS.md`
- فایل‌های `__ATTACHMENTS.txt` کنار تسک‌های همین بسته (در زمان اجرای هر تسک).

## پرامپت آماده

You are the package lead for **B01 / Etemad Core** in ETEMAD Intelligent Newsroom. Read the master specification, THIS package technical specification, `AGENTS.md`, `manifests/tasks.csv`, related baseline JSON Schemas/examples, and the existing repository tree. Your current job is **planning only**: verify scope, inputs, outputs, owned DB tables, APIs and downstream consumers of this package. Do not code the entire package in one run.

List exactly which tasks below are ready, blocked or depend on other packages. Assign each file to the recommended model shown in the task's prompt; identify parallelizable tasks with non-overlapping files. Preserve all 29 project IDs and the latest UI stack (shadcn/Tailwind, not Mantine). Do not make up source URLs, CMS choice, brand colors, API endpoints, test results or legal approval. For unknowns, use a safe mock/placeholder and mark the real integration BLOCKED. No direct cross-package database access; no public path for EIC private reports; honor output switches. Report the actual test plan, acceptance criteria, external decision blockers, and proposed PR order.

**Do not change code or contracts during this kickoff.** Output a reviewable execution plan and the exact first ready task ID.

## فهرست تسک‌های این بسته (30)
- `S01-001` — `backend/app/main.py` | C | `prompts/01_FOUNDATION/B01/S01-001__main_py.md`
- `S01-002` — `backend/core/contracts.py` | C | `prompts/01_FOUNDATION/B01/S01-002__contracts_py.md`
- `S01-003` — `backend/core/settings_service.py` | C | `prompts/01_FOUNDATION/B01/S01-003__settings_service_py.md`
- `S01-004` — `backend/core/output_switches.py` | C | `prompts/01_FOUNDATION/B01/S01-004__output_switches_py.md`
- `S01-005` — `backend/core/sources_service.py` | C | `prompts/01_FOUNDATION/B01/S01-005__sources_service_py.md`
- `S01-006` — `backend/core/auth.py` | C | `prompts/01_FOUNDATION/B01/S01-006__auth_py.md`
- `S01-007` — `backend/core/permissions.py` | C | `prompts/01_FOUNDATION/B01/S01-007__permissions_py.md`
- `S01-008` — `backend/core/audit.py` | C | `prompts/01_FOUNDATION/B01/S01-008__audit_py.md`
- `S01-009` — `backend/core/secrets.py` | C | `prompts/01_FOUNDATION/B01/S01-009__secrets_py.md`
- `S01-010` — `backend/core/archive.py` | C | `prompts/01_FOUNDATION/B01/S01-010__archive_py.md`
- `S01-011` — `backend/core/events.py` | C | `prompts/01_FOUNDATION/B01/S01-011__events_py.md`
- `S01-012` — `backend/core/jobs.py` | C | `prompts/01_FOUNDATION/B01/S01-012__jobs_py.md`
- `S01-013` — `backend/core/outbox.py` | C | `prompts/01_FOUNDATION/B01/S01-013__outbox_py.md`
- `S01-014` — `backend/core/orchestrator.py` | C | `prompts/01_FOUNDATION/B01/S01-014__orchestrator_py.md`
- `S01-015` — `backend/core/ai_gateway.py` | C | `prompts/01_FOUNDATION/B01/S01-015__ai_gateway_py.md`
- `S01-016` — `backend/core/db.py` | C | `prompts/01_FOUNDATION/B01/S01-016__db_py.md`
- `S01-017` — `backend/core/object_store.py` | C | `prompts/01_FOUNDATION/B01/S01-017__object_store_py.md`
- `S01-018` — `backend/migrations/central/001_baseline.py` | C | `prompts/01_FOUNDATION/B01/S01-018__001_baseline_py.md`
- `S01-019` — `backend/tests/test_contracts.py` | C | `prompts/01_FOUNDATION/B01/S01-019__test_contracts_py.md`
- `S01-020` — `backend/tests/test_security.py` | C | `prompts/01_FOUNDATION/B01/S01-020__test_security_py.md`
- `S01-021` — `backend/tests/test_orchestration.py` | C | `prompts/01_FOUNDATION/B01/S01-021__test_orchestration_py.md`
- `S01-022` — `backend/tests/test_ai_gateway.py` | C | `prompts/01_FOUNDATION/B01/S01-022__test_ai_gateway_py.md`
- `S01-023` — `backend/alembic.ini` | C | `prompts/01_FOUNDATION/B01/S01-023__alembic_ini.md`
- `S01-024` — `backend/migrations/env.py` | C | `prompts/01_FOUNDATION/B01/S01-024__env_py.md`
- `S01-025` — `backend/app/dependencies.py` | C | `prompts/01_FOUNDATION/B01/S01-025__dependencies_py.md`
- `S01-026` — `backend/app/api_router.py` | C | `prompts/01_FOUNDATION/B01/S01-026__api_router_py.md`
- `S01-027` — `backend/core/errors.py` | C | `prompts/01_FOUNDATION/B01/S01-027__errors_py.md`
- `S01-028` — `backend/core/health.py` | C | `prompts/01_FOUNDATION/B01/S01-028__health_py.md`
- `S01-029` — `backend/core/observability.py` | C | `prompts/01_FOUNDATION/B01/S01-029__observability_py.md`
- `S01-030` — `backend/tests/conftest.py` | C | `prompts/01_FOUNDATION/B01/S01-030__conftest_py.md`


**ملاک موفقیت:** هر تسک دارای فایل هدف یکتا، ضمیمه مشخص، تست صریح و بازبینی مستقل باشد.
