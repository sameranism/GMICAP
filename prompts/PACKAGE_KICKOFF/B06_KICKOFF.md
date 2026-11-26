# آغاز تیم B06 — ژرفان / Intelligence & Reports

**مدل پیشنهادی برای برنامه‌ریزی بسته:** Grok in Cursor Cloud Agent. **پذیرش برنامه:** پیش‌نیازها و شواهد آزمون طبق ADR-012.

## ضمائم لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/specs/B06_INTELLIGENCE_TECHNICAL_SPEC.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `manifests/tasks.csv`
- `cursor-kit/AGENTS.md`
- فایل‌های `__ATTACHMENTS.txt` کنار تسک‌های همین بسته (در زمان اجرای هر تسک).

## پرامپت آماده

You are the package lead for **B06 / Intelligence & Reports** in ETEMAD Intelligent Newsroom. Read the master specification, THIS package technical specification, `AGENTS.md`, `manifests/tasks.csv`, related baseline JSON Schemas/examples, and the existing repository tree. Your current job is **planning only**: verify scope, inputs, outputs, owned DB tables, APIs and downstream consumers of this package. Do not code the entire package in one run.

List exactly which tasks below are ready, blocked or depend on other packages. Assign each file to the recommended model shown in the task's prompt; identify parallelizable tasks with non-overlapping files. Preserve all 29 project IDs and the latest UI stack (shadcn/Tailwind, not Mantine). Do not make up source URLs, CMS choice, brand colors, API endpoints, test results or legal approval. For unknowns, use a safe mock/placeholder and mark the real integration BLOCKED. No direct cross-package database access; no public path for EIC private reports; honor output switches. Report the actual test plan, acceptance criteria, external decision blockers, and proposed PR order.

**Do not change code or contracts during this kickoff.** Output a reviewable execution plan and the exact first ready task ID.

## فهرست تسک‌های این بسته (10)
- `S05-001` — `backend/modules/intelligence/analysis.py` | G | `prompts/05_INTELLIGENCE/B06/S05-001__analysis_py.md`
- `S05-002` — `backend/modules/intelligence/evidence.py` | C | `prompts/05_INTELLIGENCE/B06/S05-002__evidence_py.md`
- `S05-003` — `backend/modules/intelligence/retrieval.py` | C | `prompts/05_INTELLIGENCE/B06/S05-003__retrieval_py.md`
- `S05-004` — `backend/modules/intelligence/chat.py` | G | `prompts/05_INTELLIGENCE/B06/S05-004__chat_py.md`
- `S05-005` — `backend/modules/intelligence/metrics.py` | G | `prompts/05_INTELLIGENCE/B06/S05-005__metrics_py.md`
- `S05-006` — `backend/modules/intelligence/public_reports.py` | G | `prompts/05_INTELLIGENCE/B06/S05-006__public_reports_py.md`
- `S05-007` — `backend/modules/intelligence/private_reports.py` | C | `prompts/05_INTELLIGENCE/B06/S05-007__private_reports_py.md`
- `S05-008` — `backend/modules/intelligence/repository.py` | C | `prompts/05_INTELLIGENCE/B06/S05-008__repository_py.md`
- `S05-009` — `backend/migrations/central/004_intelligence.py` | C | `prompts/05_INTELLIGENCE/B06/S05-009__004_intelligence_py.md`
- `S05-010` — `backend/tests/test_intelligence.py` | C | `prompts/05_INTELLIGENCE/B06/S05-010__test_intelligence_py.md`


**ملاک موفقیت:** هر تسک دارای فایل هدف یکتا، ضمیمه مشخص، تست صریح و معیار پذیرش خودکار داشته باشد.
