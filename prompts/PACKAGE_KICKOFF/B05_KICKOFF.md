# آغاز تیم B05 — نگار / Editorial AI

**مدل پیشنهادی برای برنامه‌ریزی بسته:** Grok in Cursor Cloud Agent. **پذیرش برنامه:** پیش‌نیازها و شواهد آزمون طبق ADR-012.

## ضمائم لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/specs/B05_CONTENT_TECHNICAL_SPEC.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `manifests/tasks.csv`
- `cursor-kit/AGENTS.md`
- فایل‌های `__ATTACHMENTS.txt` کنار تسک‌های همین بسته (در زمان اجرای هر تسک).

## پرامپت آماده

You are the package lead for **B05 / Editorial AI** in ETEMAD Intelligent Newsroom. Read the master specification, THIS package technical specification, `AGENTS.md`, `manifests/tasks.csv`, related baseline JSON Schemas/examples, and the existing repository tree. Your current job is **planning only**: verify scope, inputs, outputs, owned DB tables, APIs and downstream consumers of this package. Do not code the entire package in one run.

List exactly which tasks below are ready, blocked or depend on other packages. Assign each file to the recommended model shown in the task's prompt; identify parallelizable tasks with non-overlapping files. Preserve all 29 project IDs and the latest UI stack (shadcn/Tailwind, not Mantine). Do not make up source URLs, CMS choice, brand colors, API endpoints, test results or legal approval. For unknowns, use a safe mock/placeholder and mark the real integration BLOCKED. No direct cross-package database access; no public path for EIC private reports; honor output switches. Report the actual test plan, acceptance criteria, external decision blockers, and proposed PR order.

**Do not change code or contracts during this kickoff.** Output a reviewable execution plan and the exact first ready task ID.

## فهرست تسک‌های این بسته (9)
- `S04-001` — `backend/modules/editorial/glossary.py` | C | `prompts/04_EDITORIAL/B05/S04-001__glossary_py.md`
- `S04-002` — `backend/modules/editorial/policy.py` | C | `prompts/04_EDITORIAL/B05/S04-002__policy_py.md`
- `S04-003` — `backend/modules/editorial/quality.py` | C | `prompts/04_EDITORIAL/B05/S04-003__quality_py.md`
- `S04-004` — `backend/modules/editorial/translator.py` | G | `prompts/04_EDITORIAL/B05/S04-004__translator_py.md`
- `S04-005` — `backend/modules/editorial/editor.py` | G | `prompts/04_EDITORIAL/B05/S04-005__editor_py.md`
- `S04-006` — `backend/modules/editorial/image_processor.py` | G | `prompts/04_EDITORIAL/B05/S04-006__image_processor_py.md`
- `S04-007` — `backend/modules/editorial/repository.py` | C | `prompts/04_EDITORIAL/B05/S04-007__repository_py.md`
- `S04-008` — `backend/migrations/central/003_editorial.py` | C | `prompts/04_EDITORIAL/B05/S04-008__003_editorial_py.md`
- `S04-009` — `backend/tests/test_editorial.py` | C | `prompts/04_EDITORIAL/B05/S04-009__test_editorial_py.md`


**ملاک موفقیت:** هر تسک دارای فایل هدف یکتا، ضمیمه مشخص، تست صریح و معیار پذیرش خودکار داشته باشد.
