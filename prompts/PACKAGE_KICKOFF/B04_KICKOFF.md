# آغاز تیم B04 — خبرپرداز / News Processor

**مدل پیشنهادی برای برنامه‌ریزی بسته:** Grok in Cursor Cloud Agent. **پذیرش برنامه:** پیش‌نیازها و شواهد آزمون طبق ADR-012.

## ضمائم لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/specs/B04_PREPROCESSING_TECHNICAL_SPEC.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `manifests/tasks.csv`
- `cursor-kit/AGENTS.md`
- فایل‌های `__ATTACHMENTS.txt` کنار تسک‌های همین بسته (در زمان اجرای هر تسک).

## پرامپت آماده

You are the package lead for **B04 / News Processor** in ETEMAD Intelligent Newsroom. Read the master specification, THIS package technical specification, `AGENTS.md`, `manifests/tasks.csv`, related baseline JSON Schemas/examples, and the existing repository tree. Your current job is **planning only**: verify scope, inputs, outputs, owned DB tables, APIs and downstream consumers of this package. Do not code the entire package in one run.

List exactly which tasks below are ready, blocked or depend on other packages. Assign each file to the recommended model shown in the task's prompt; identify parallelizable tasks with non-overlapping files. Preserve all 29 project IDs and the latest UI stack (shadcn/Tailwind, not Mantine). Do not make up source URLs, CMS choice, brand colors, API endpoints, test results or legal approval. For unknowns, use a safe mock/placeholder and mark the real integration BLOCKED. No direct cross-package database access; no public path for EIC private reports; honor output switches. Report the actual test plan, acceptance criteria, external decision blockers, and proposed PR order.

**Do not change code or contracts during this kickoff.** Output a reviewable execution plan and the exact first ready task ID.

## فهرست تسک‌های این بسته (8)
- `S03-001` — `backend/modules/processing/extractor.py` | G | `prompts/03_PROCESSING/B04/S03-001__extractor_py.md`
- `S03-002` — `backend/modules/processing/normalizer.py` | G | `prompts/03_PROCESSING/B04/S03-002__normalizer_py.md`
- `S03-003` — `backend/modules/processing/deduplicator.py` | G | `prompts/03_PROCESSING/B04/S03-003__deduplicator_py.md`
- `S03-004` — `backend/modules/processing/classifier.py` | G | `prompts/03_PROCESSING/B04/S03-004__classifier_py.md`
- `S03-005` — `backend/modules/processing/router.py` | C | `prompts/03_PROCESSING/B04/S03-005__router_py.md`
- `S03-006` — `backend/modules/processing/repository.py` | C | `prompts/03_PROCESSING/B04/S03-006__repository_py.md`
- `S03-007` — `backend/migrations/central/002_processing.py` | C | `prompts/03_PROCESSING/B04/S03-007__002_processing_py.md`
- `S03-008` — `backend/tests/test_processing.py` | C | `prompts/03_PROCESSING/B04/S03-008__test_processing_py.md`


**ملاک موفقیت:** هر تسک دارای فایل هدف یکتا، ضمیمه مشخص، تست صریح و معیار پذیرش خودکار داشته باشد.
