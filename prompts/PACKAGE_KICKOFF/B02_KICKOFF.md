# آغاز تیم B02 — ایران‌بان / Iran Monitor

**مدل پیشنهادی برای برنامه‌ریزی بسته:** Grok in Cursor Cloud Agent. **بازبین برنامه:** Codex مستقل.

## ضمائم لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/specs/B02_DOMESTIC_INGEST_TECHNICAL_SPEC.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `manifests/tasks.csv`
- `cursor-kit/AGENTS.md`
- فایل‌های `__ATTACHMENTS.txt` کنار تسک‌های همین بسته (در زمان اجرای هر تسک).

## پرامپت آماده

You are the package lead for **B02 / Iran Monitor** in ETEMAD Intelligent Newsroom. Read the master specification, THIS package technical specification, `AGENTS.md`, `manifests/tasks.csv`, related baseline JSON Schemas/examples, and the existing repository tree. Your current job is **planning only**: verify scope, inputs, outputs, owned DB tables, APIs and downstream consumers of this package. Do not code the entire package in one run.

List exactly which tasks below are ready, blocked or depend on other packages. Assign each file to the recommended model shown in the task's prompt; identify parallelizable tasks with non-overlapping files. Preserve all 29 project IDs and the latest UI stack (shadcn/Tailwind, not Mantine). Do not make up source URLs, CMS choice, brand colors, API endpoints, test results or legal approval. For unknowns, use a safe mock/placeholder and mark the real integration BLOCKED. No direct cross-package database access; no public path for EIC private reports; honor output switches. Report the actual test plan, acceptance criteria, external decision blockers, and proposed PR order.

**Do not change code or contracts during this kickoff.** Output a reviewable execution plan and the exact first ready task ID.

## فهرست تسک‌های این بسته (7)
- `S02-001` — `backend/modules/domestic/feed_client.py` | G | `prompts/02_INGEST_AND_DESIGN/B02/S02-001__feed_client_py.md`
- `S02-002` — `backend/modules/domestic/collector.py` | G | `prompts/02_INGEST_AND_DESIGN/B02/S02-002__collector_py.md`
- `S02-003` — `backend/modules/domestic/scheduler.py` | G | `prompts/02_INGEST_AND_DESIGN/B02/S02-003__scheduler_py.md`
- `S02-004` — `backend/modules/domestic/repository.py` | C | `prompts/02_INGEST_AND_DESIGN/B02/S02-004__repository_py.md`
- `S02-005` — `backend/modules/domestic/api.py` | G | `prompts/02_INGEST_AND_DESIGN/B02/S02-005__api_py.md`
- `S02-006` — `backend/migrations/domestic/001_ingest.py` | C | `prompts/02_INGEST_AND_DESIGN/B02/S02-006__001_ingest_py.md`
- `S02-007` — `backend/tests/test_domestic.py` | C | `prompts/02_INGEST_AND_DESIGN/B02/S02-007__test_domestic_py.md`


**ملاک موفقیت:** هر تسک دارای فایل هدف یکتا، ضمیمه مشخص، تست صریح و بازبینی مستقل باشد.
