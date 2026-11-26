# ADR-004 — Publishing gates and output controls

- **Status:** Accepted
- **Date:** 2026-11-23
- **Task:** S00-011
- **Source:** `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/specs/B08_PUBLISHING_TECHNICAL_SPEC.md`,
  `source/contracts/README-fa.md`

## Context

Publishing is the only package that can cause an external, irreversible side effect. The client has not
authorized real publishing, has no confirmed CMS, and has not approved API rights for destinations.
Iranian publishing also requires a human legal/editorial signoff that no agent can self-grant.

## Decision

1. **Three independent output controls** — `public_analysis`, `studio` (audio/video), `publishing`
   (domestic/foreign/public_reports) — are each enforced **in the backend, before any side effect**.
   Turning one off must not stop ingestion, archiving, or the three EIC private reports.
2. **Publishing additionally requires**, in order: a `validation_decision` with `approved`, a recorded
   reuse-rights status for the source, an explicit destination configuration with `credential_ref`, and
   the publishing switch on. Any missing element means the job stays `held`.
3. **Destination adapters default to mock/dry-run.** A real adapter exists only for an officially verified
   API. Unknown CMS stays an adapter contract; no invented endpoints.
4. **`executive_private` reports are structurally excluded** from the publishing queue, adapters, public
   API and object storage paths readable by publish workers. This is enforced at backend, DB/queue and
   retrieval levels — hiding a button in the UI is not a control.
5. **Held jobs are not backfilled automatically.** On resume, every held job is revalidated against the
   current switches and rights before it can proceed.
6. **Publishing results are recorded** (`publication_result`) including failure reason; retries are
   idempotent per destination and job id.

## Consequences

- B08 can be fully built and tested with mocks while real publishing stays `BLOCKED`.
- Publishing tests must reject adapter call paths that do not enforce the gates above.
- The client must sign off any first real publish, outside the code path.

## Impacted contracts

`output_controls`, `validation_decision`, `publication_job`, `publication_result`, `destination_config`,
`destination_payload`, `private_report`, `public_report`.

## Open external dependencies

- CMS identity and its official API — BLOCKED.
- Legal review of republication rights per source — BLOCKED.
- Credentials for each destination, delivered through a secret store — not in the repo.
