# B01 — بنیان (Etemad Core)

شناسه ثابت بسته: `B01` | مسیر مفهومی: `core`
سند مرجع: `source/specs/B01_FOUNDATION_TECHNICAL_SPEC.md`

تعداد تسک‌های برنامه: **30**

| مرحله | تسک | فایل خروجی | مدل | پرامپت |
|---:|---|---|---|---|
| 1 | `S01-001` | `backend/app/main.py` | C | `prompts/01_FOUNDATION/B01/S01-001__main_py.md` |
| 1 | `S01-002` | `backend/core/contracts.py` | C | `prompts/01_FOUNDATION/B01/S01-002__contracts_py.md` |
| 1 | `S01-003` | `backend/core/settings_service.py` | C | `prompts/01_FOUNDATION/B01/S01-003__settings_service_py.md` |
| 1 | `S01-004` | `backend/core/output_switches.py` | C | `prompts/01_FOUNDATION/B01/S01-004__output_switches_py.md` |
| 1 | `S01-005` | `backend/core/sources_service.py` | C | `prompts/01_FOUNDATION/B01/S01-005__sources_service_py.md` |
| 1 | `S01-006` | `backend/core/auth.py` | C | `prompts/01_FOUNDATION/B01/S01-006__auth_py.md` |
| 1 | `S01-007` | `backend/core/permissions.py` | C | `prompts/01_FOUNDATION/B01/S01-007__permissions_py.md` |
| 1 | `S01-008` | `backend/core/audit.py` | C | `prompts/01_FOUNDATION/B01/S01-008__audit_py.md` |
| 1 | `S01-009` | `backend/core/secrets.py` | C | `prompts/01_FOUNDATION/B01/S01-009__secrets_py.md` |
| 1 | `S01-010` | `backend/core/archive.py` | C | `prompts/01_FOUNDATION/B01/S01-010__archive_py.md` |
| 1 | `S01-011` | `backend/core/events.py` | C | `prompts/01_FOUNDATION/B01/S01-011__events_py.md` |
| 1 | `S01-012` | `backend/core/jobs.py` | C | `prompts/01_FOUNDATION/B01/S01-012__jobs_py.md` |
| 1 | `S01-013` | `backend/core/outbox.py` | C | `prompts/01_FOUNDATION/B01/S01-013__outbox_py.md` |
| 1 | `S01-014` | `backend/core/orchestrator.py` | C | `prompts/01_FOUNDATION/B01/S01-014__orchestrator_py.md` |
| 1 | `S01-015` | `backend/core/ai_gateway.py` | C | `prompts/01_FOUNDATION/B01/S01-015__ai_gateway_py.md` |
| 1 | `S01-016` | `backend/core/db.py` | C | `prompts/01_FOUNDATION/B01/S01-016__db_py.md` |
| 1 | `S01-017` | `backend/core/object_store.py` | C | `prompts/01_FOUNDATION/B01/S01-017__object_store_py.md` |
| 1 | `S01-018` | `backend/migrations/central/001_baseline.py` | C | `prompts/01_FOUNDATION/B01/S01-018__001_baseline_py.md` |
| 1 | `S01-019` | `backend/tests/test_contracts.py` | C | `prompts/01_FOUNDATION/B01/S01-019__test_contracts_py.md` |
| 1 | `S01-020` | `backend/tests/test_security.py` | C | `prompts/01_FOUNDATION/B01/S01-020__test_security_py.md` |
| 1 | `S01-021` | `backend/tests/test_orchestration.py` | C | `prompts/01_FOUNDATION/B01/S01-021__test_orchestration_py.md` |
| 1 | `S01-022` | `backend/tests/test_ai_gateway.py` | C | `prompts/01_FOUNDATION/B01/S01-022__test_ai_gateway_py.md` |
| 1 | `S01-023` | `backend/alembic.ini` | C | `prompts/01_FOUNDATION/B01/S01-023__alembic_ini.md` |
| 1 | `S01-024` | `backend/migrations/env.py` | C | `prompts/01_FOUNDATION/B01/S01-024__env_py.md` |
| 1 | `S01-025` | `backend/app/dependencies.py` | C | `prompts/01_FOUNDATION/B01/S01-025__dependencies_py.md` |
| 1 | `S01-026` | `backend/app/api_router.py` | C | `prompts/01_FOUNDATION/B01/S01-026__api_router_py.md` |
| 1 | `S01-027` | `backend/core/errors.py` | C | `prompts/01_FOUNDATION/B01/S01-027__errors_py.md` |
| 1 | `S01-028` | `backend/core/health.py` | C | `prompts/01_FOUNDATION/B01/S01-028__health_py.md` |
| 1 | `S01-029` | `backend/core/observability.py` | C | `prompts/01_FOUNDATION/B01/S01-029__observability_py.md` |
| 1 | `S01-030` | `backend/tests/conftest.py` | C | `prompts/01_FOUNDATION/B01/S01-030__conftest_py.md` |

**قاعده:** پیش از ویرایش، ورودی‌های هر تسک در فایل `__ATTACHMENTS.txt` کنار پرامپت مشخص است.
**مرز:** خروجی‌ها فقط با API/Event نسخه‌دار و مجوز به بسته دیگر منتقل شوند.
