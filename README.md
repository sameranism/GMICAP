# ETEMAD — Intelligent newsroom

> **Status: pre-release, not operational.** Contract layer and foundation are under construction.
> Nothing in this repository publishes, fetches live sources, or calls external AI by default.

##  semantic change needs a new
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
