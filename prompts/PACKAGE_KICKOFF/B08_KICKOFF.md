# آغاز تیم B08 — رسان / Publishing Engine

**مدل پیشنهادی برای برنامه‌ریزی بسته:** Codex. **بازبین برنامه:** Codex مستقل.

## ضمائم لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/specs/B08_PUBLISHING_TECHNICAL_SPEC.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `manifests/tasks.csv`
- `cursor-kit/AGENTS.md`
- فایل‌های `__ATTACHMENTS.txt` کنار تسک‌های همین بسته (در زمان اجرای هر تسک).

## پرامپت آماده

You are the package lead for **B08 / Publishing Engine** in ETEMAD Intelligent Newsroom. Read the master specification, THIS package technical specification, `AGENTS.md`, `manifests/tasks.csv`, related baseline JSON Schemas/examples, and the existing repository tree. Your current job is **planning only**: verify scope, inputs, outputs, owned DB tables, APIs and downstream consumers of this package. Do not code the entire package in one run.

List exactly which tasks below are ready, blocked or depend on other packages. Assign each file to the recommended model shown in the task's prompt; identify parallelizable tasks with non-overlapping files. Preserve all 29 project IDs and the latest UI stack (shadcn/Tailwind, not Mantine). Do not make up source URLs, CMS choice, brand colors, API endpoints, test results or legal approval. For unknowns, use a safe mock/placeholder and mark the real integration BLOCKED. No direct cross-package database access; no public path for EIC private reports; honor output switches. Report the actual test plan, acceptance criteria, external decision blockers, and proposed PR order.

**Do not change code or contracts during this kickoff.** Output a reviewable execution plan and the exact first ready task ID.

## فهرست تسک‌های این بسته (15)
- `S06-001` — `backend/modules/publishing/scheduler.py` | C | `prompts/06_PUBLISHING/B08/S06-001__scheduler_py.md`
- `S06-002` — `backend/modules/publishing/destinations.py` | C | `prompts/06_PUBLISHING/B08/S06-002__destinations_py.md`
- `S06-003` — `backend/modules/publishing/formatter.py` | G | `prompts/06_PUBLISHING/B08/S06-003__formatter_py.md`
- `S06-004` — `backend/modules/publishing/dispatcher.py` | C | `prompts/06_PUBLISHING/B08/S06-004__dispatcher_py.md`
- `S06-005` — `backend/adapters/base.py` | C | `prompts/06_PUBLISHING/B08/S06-005__base_py.md`
- `S06-006` — `backend/adapters/telegram.py` | G | `prompts/06_PUBLISHING/B08/S06-006__telegram_py.md`
- `S06-007` — `backend/adapters/bale.py` | G | `prompts/06_PUBLISHING/B08/S06-007__bale_py.md`
- `S06-008` — `backend/adapters/eitaa.py` | G | `prompts/06_PUBLISHING/B08/S06-008__eitaa_py.md`
- `S06-009` — `backend/adapters/rubika.py` | G | `prompts/06_PUBLISHING/B08/S06-009__rubika_py.md`
- `S06-010` — `backend/adapters/whatsapp.py` | G | `prompts/06_PUBLISHING/B08/S06-010__whatsapp_py.md`
- `S06-011` — `backend/adapters/cms.py` | C | `prompts/06_PUBLISHING/B08/S06-011__cms_py.md`
- `S06-012` — `backend/adapters/registry.py` | C | `prompts/06_PUBLISHING/B08/S06-012__registry_py.md`
- `S06-013` — `backend/modules/publishing/repository.py` | C | `prompts/06_PUBLISHING/B08/S06-013__repository_py.md`
- `S06-014` — `backend/migrations/central/005_publishing.py` | C | `prompts/06_PUBLISHING/B08/S06-014__005_publishing_py.md`
- `S06-015` — `backend/tests/test_publishing.py` | C | `prompts/06_PUBLISHING/B08/S06-015__test_publishing_py.md`


**ملاک موفقیت:** هر تسک دارای فایل هدف یکتا، ضمیمه مشخص، تست صریح و بازبینی مستقل باشد.
