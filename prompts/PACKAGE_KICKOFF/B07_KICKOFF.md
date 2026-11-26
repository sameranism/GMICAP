# آغاز تیم B07 — آوانما / AI News Studio

**مدل پیشنهادی برای برنامه‌ریزی بسته:** Grok in Cursor Cloud Agent. **بازبین برنامه:** Codex مستقل.

## ضمائم لازم
- `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`
- `source/specs/B07_STUDIO_TECHNICAL_SPEC.md`
- `source/technical/project_package_map.csv`
- `source/technical/dependency_edges.csv`
- `source/technical/database_dictionary.csv`
- `manifests/tasks.csv`
- `cursor-kit/AGENTS.md`
- فایل‌های `__ATTACHMENTS.txt` کنار تسک‌های همین بسته (در زمان اجرای هر تسک).

## پرامپت آماده

You are the package lead for **B07 / AI News Studio** in ETEMAD Intelligent Newsroom. Read the master specification, THIS package technical specification, `AGENTS.md`, `manifests/tasks.csv`, related baseline JSON Schemas/examples, and the existing repository tree. Your current job is **planning only**: verify scope, inputs, outputs, owned DB tables, APIs and downstream consumers of this package. Do not code the entire package in one run.

List exactly which tasks below are ready, blocked or depend on other packages. Assign each file to the recommended model shown in the task's prompt; identify parallelizable tasks with non-overlapping files. Preserve all 29 project IDs and the latest UI stack (shadcn/Tailwind, not Mantine). Do not make up source URLs, CMS choice, brand colors, API endpoints, test results or legal approval. For unknowns, use a safe mock/placeholder and mark the real integration BLOCKED. No direct cross-package database access; no public path for EIC private reports; honor output switches. Report the actual test plan, acceptance criteria, external decision blockers, and proposed PR order.

**Do not change code or contracts during this kickoff.** Output a reviewable execution plan and the exact first ready task ID.

## فهرست تسک‌های این بسته (6)
- `S07-001` — `backend/modules/studio/tts.py` | G | `prompts/07_STUDIO/B07/S07-001__tts_py.md`
- `S07-002` — `backend/modules/studio/subtitles.py` | G | `prompts/07_STUDIO/B07/S07-002__subtitles_py.md`
- `S07-003` — `backend/modules/studio/renderer.py` | G | `prompts/07_STUDIO/B07/S07-003__renderer_py.md`
- `S07-004` — `backend/modules/studio/repository.py` | C | `prompts/07_STUDIO/B07/S07-004__repository_py.md`
- `S07-005` — `backend/migrations/central/006_studio.py` | C | `prompts/07_STUDIO/B07/S07-005__006_studio_py.md`
- `S07-006` — `backend/tests/test_studio.py` | C | `prompts/07_STUDIO/B07/S07-006__test_studio_py.md`


**ملاک موفقیت:** هر تسک دارای فایل هدف یکتا، ضمیمه مشخص، تست صریح و بازبینی مستقل باشد.
