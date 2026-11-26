# ETEMAD — Intelligent newsroom

> **Status: pre-release, not operational.** Contract layer and foundation are under construction.
> Nothing in this repository publishes, fetches live sources, or calls external AI by default.

## What exists today

- `backend/` — FastAPI scaffold: health, safe error envelope, contract loading, permission decisions,
  versioned settings service. Five of thirty foundation tasks are present.
- `frontend/` — React 19 + Vite 6 + Tailwind 4 demo shell (newsroom list). Synthetic data only.
- `source/contracts/` — **30 JSON Schema (Draft 2020-12, `schema_version` 1.0) with 30 examples.**
  These are the authority; product code must conform to them.
- `docs/decisions/` — ADR-001 .. ADR-006 (architecture, UI stack, storage, publishing gates, roles, AI gateway).
- `tools/validate_contracts.py` — validates every schema and example; exit 1 on any violation.
- `tools/preflight.py` — blocks a task when its required attachments or contracts are missing.
- `.cursor/rules/` + `AGENTS.md` — binding rules for coding agents.

## Contracts are read-only evidence

Never edit a schema or example to make code pass. A required field, enum or semantic change needs a new
ADR, a version bump and producer/consumer tests.

## Local checks

```bash
python tools/validate_contracts.py      # must print CONTRACT-CHECK: PASS (30 schemas, 30 examples)
python tools/preflight.py S02-001 --pack <pack-root>
```

The preflight expects the task pack (manifests + specs). Vendor it at `docs/pack/` (preferred) or pass
`--pack`. If it prints `BLOCKED`, stop: do not invent stubs, do not proceed.

## Blocked by external decisions

- Real CMS and destination APIs: unknown — adapters stay mock, publishing stays off.
- Source licensing and republication rights: not approved — text stays `metadata`/`link_only`.
- Official brand assets (logo, palette): not supplied — placeholders only.
- Deployment target (VPS) and database topology: not finalized.

## Read first

`AGENTS.md`, then `docs/decisions/ADR-001-architecture.md`, then the relevant package spec under
`source/specs/`. The task prompt defines the only files you may change.
