# ETEMAD — اتاق خبر هوشمند اعتماد

**Current state: Stage S00 under review. This repository contains the authoritative planning pack, provisional agent rules and task-specific draft PRs; it is NOT a running newsroom or an approved deployment.**

## Approved baseline

- Six conceptual layers; nine delivery packages **B01–B09** and 29 projects **P01–P29**.
- Three independent PostgreSQL/queue environments: domestic ingestion, foreign ingestion and the central platform with a secured bridge.
- Python/FastAPI and a provider-neutral AI gateway; React/TypeScript/shadcn/ui/Tailwind CSS v4 for a Persian RTL interface subject to ADR-002 review.
- Versioned JSON Schema Draft 2020-12, 30 read-only baseline schemas and examples, with task-scoped changes only.
- Max ten active human accounts; backend-enforced role permissions and editor-in-chief-only `executive_private` reporting.
- Independent `public_analysis`, `studio` and `publishing` output controls. Live publishing, paid model calls, CMS integration and production deployment remain OFF unless separately authorized.

## Start reading

1. [Master architecture](source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md) and the nine additional Markdown technical specifications under `source/specs/`.
2. [Task matrix](manifests/tasks.csv), [manifest](manifests/manifest.json), and [operational guide](guides/CURSOR_START_FA.md).
3. [Agent operating rules](AGENTS.md), `.cursor/rules/`, and the exact prompt and `__ATTACHMENTS.txt` for the current S00 task.
4. [Project mapping](source/technical/project_package_map.csv), [dependency edges](source/technical/dependency_edges.csv), and [database ownership draft](source/technical/database_dictionary.csv).
5. [Frozen data contracts](source/contracts/schemas/), corresponding [examples](source/contracts/examples/), and [Gate-00 independent reviewer prompt](prompts/GATES/GATE-00-REVIEW.md).

## Packages

| Code | Persian title | Responsibility |
|---|---|---|
| B01 | بنیان | Contracts, source registry, settings, identity, archive and coordination |
| B02 | ایران‌بان | Domestic ingestion |
| B03 | جهان‌بان | Foreign discovery and ingestion |
| B04 | خبرپرداز | Normalization, deduplication and routing |
| B05 | نگار | Policy, translation, article and image workflows |
| B06 | ژرفان | Evidence-based intelligence, chat and public/private reports |
| B07 | آوانما | Optional audio/video studio |
| B08 | رسان | Verified destinations, controlled scheduling and publishing |
| B09 | دیدبان | Persian RTL newsroom interface and role-specific dashboards |

## Safe local workflow

Work from a task-specific branch named in its prompt. Read references and existing code, change only the allowed TARGET, run applicable tests, collect command exit status and open a **draft PR**. A code or prompt file appearing in the repository does not mean the related task has passed independent review.

Once S00-017's validator has merged, install its Python dependency (`jsonschema==4.26.0`) in a disposable Python environment and run:

```sh
python tools/validate_contracts.py
```

GitHub Actions S00-018 provides a baseline contract check; Stage S00 is not accepted until all required task outputs and independent Gate-00 evidence are reviewed. Do not interpret a passing CI schema test as a production acceptance test.

No secrets, real news API tokens, personal records or production data should be committed. Unknown brand/CMS/provider/legal details must remain **BLOCKED** rather than guessed.

## Deployment

**None authorized for the current stage.** In particular, do not deploy to the VPS, apply proposal SQL migrations, call real provider APIs or publish articles from this repository during S00.
