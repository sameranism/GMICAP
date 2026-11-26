# Contract audit - `private_report`

## ADR-016 baseline containment correction — 2026-11-26

[ADR-016](../decisions/ADR-016-private-event-containment.md) merged in [PR #68](https://github.com/sameranism/ETEMAD-pre/pull/68) at signed main `1fc80f48ab46500ee8fbb2647223f7e119ea737e`. Its exact-head [backend](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720153275), [contract](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720153339), [CodeQL](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720153351), [bootstrap](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720153317) and [Guardian](https://github.com/sameranism/ETEMAD-pre/actions/runs/45720153084) passed. The correction adds typed executive_private rejection to the existing shared guard, used by both bus and outbox at append and dispatch. The five new test cases cover constructor and raw envelopes, shared dedupe preservation, no persistence or callback, and mutated pending entries. Existing restricted and public/internal behavior and all previous tests remain intact. No frozen contract, grant, storage, queue infrastructure or external service changes. Exact-head CI is required for these new tests; their success is not yet asserted in this entry. No local execution claimed. Dedicated private storage and authenticated transport remain deferred per ADR-015. This correction is not full semantic or privacy acceptance; Gate-00 remains BLOCKED.

## Semantic and privacy audit — 2026-11-26

**Disposition: PARTIAL / BLOCKED.** Human or independent development review is NOT_REQUIRED under ADR-012; missing automated evidence is not waived.

Baseline: protected signed main [`5ae55df26169b0034ebfc2a68e1ae66bbcf123cd`](https://github.com/sameranism/ETEMAD-pre/commit/5ae55df26169b0034ebfc2a68e1ae66bbcf123cd), merged [PR #65](https://github.com/sameranism/ETEMAD-pre/pull/65). S00-041 scope is this document only. All four prompt attachments and the task row, coding path, master and B06 specs, package map, dependency edges, ADR-004/005, root instructions, security rules, current fixture code and test inventory were inspected. The exact-main [contract job](https://github.com/sameranism/ETEMAD-pre/actions/runs/45719009835/job/139572295004) reports S00-041 preflight PASS, four attachments, 62 task preflights and 336 negative contract cases. [Backend CI](https://github.com/sameranism/ETEMAD-pre/actions/runs/45719009954/job/139572295987) reports 167 passed, 15 warnings, Ruff and Mypy PASS with PostgreSQL 18.7. [CodeQL](https://github.com/sameranism/ETEMAD-pre/actions/runs/45719010101) and [main provenance audit](https://github.com/sameranism/ETEMAD-pre/actions/runs/45719010004) pass. These results establish fixture/structural evidence, not end-to-end private report isolation. No separate local tests were run in this audit.

### Frozen contract and intended consumers

- P19/B06 produces the three private report types; `visibility=executive_private`, `owner_role=editor_in_chief`, and **`publishable` is const false**, not merely an arbitrary boolean. No public publication, studio, public search or public replica is permitted.
- The original consumer inventory below is incomplete: the master/B06 specification, project map and dependency edges identify P27 and P16 as private consumers only when authorized. P16 requires access filtering before retrieval; P27 requires server-side authorization per resource. Neither a role label nor a report identifier is a permission.
- `created_by_project` is only a nonempty string in the schema, so P19 ownership and provenance must be established by trusted server state. Slots 5–7 and daily uniqueness, chronological time ranges, rights and reference ACLs are semantic requirements, not schema guarantees. Do not change the frozen schema or sample.
- ADR-005 and master prose mention a separately recorded owner grant while the current fixture denies owner access even with a grant. Retain the stricter denial; no widening of role access in this audit. A distinct authorization decision is needed before changing that behavior.

### Concrete fixture findings (static inspection, not a demonstrated live incident)

| Boundary | Observed implementation | Required corrective evidence |
| --- | --- | --- |
| P29 event bus and outbox | [events.py](../../backend/core/events.py) validates all four classifications but shared-route guard rejects only restricted. An executive_private envelope can reach generic subscribers or outbox; [outbox.py](../../backend/core/outbox.py) uses the same guard. No authenticated private queue is wired. | Separate narrowly scoped ADR and protected corrective PR: refuse executive_private in both shared routes before delivery, dedupe/persistence or callback; retain constructor compatibility and restricted denial. Test raw envelopes, mutated pending records, and ordinary events. |
| P26 archive | [archive.py](../../backend/core/archive.py) accepts classification and returns records by ID without actor or grant checks. | Separate scoped storage decision: refuse private data on generic fixture paths; design a distinct authenticated private archive adapter. Test denied direct access and no cross-namespace exposure. |
| P26 object storage | [object_store.py](../../backend/core/object_store.py) implements path containment, not classification or authorization. Shared [service wiring](../../backend/app/dependencies.py) exposes a generic local object store. | Private objects must not be placed under a shared readable root. Use isolated role/bucket and trusted classification; verify direct reads, listing, overwrite, references and public-worker access. Path traversal tests alone do not demonstrate ACLs. |
| P28 grants | [permissions.py](../../backend/core/permissions.py) denies owner/staff and requires an explicit EIC read grant; existing security tests exercise this fixture. | Verify trusted identity/classification, per-resource ACL, revocation and deny-before-retrieval at actual boundaries. Fixture grant store is not authoritative production identity. |
| P19/P16/P27/P22/P24/P25 | Private report, retrieval and publishing integration is not present in the inspected backend module tree. | Do not claim an implemented private production flow. Require negative integration tests for public search, publishing, studio, direct API and storage; positive EIC-only access in a future authorized private adapter. |

### Proposed corrective scope and stop criteria

First address the confirmed shared-event classification gap through a separate ADR extending fail-closed behavior without changing the wire contract or granting access. Then separately address generic archive and object storage isolation; keep interfaces and ownership stable and avoid treating a path prefix, caller boolean or role string as trusted authorization. Full P16/P19/P27 and public-publishing integrations remain dependency-gated. Production deployment, real reports, external model calls and live publishing are not authorized. No real private data was accessed.

Independent secret-scanning alert evidence could not be retrieved through the connector (the security alerts endpoint was rejected with HTTP 400). This is UNKNOWN, not a clean secret scan. Gate-00 remains BLOCKED until the applicable secret/permission evidence, privacy failure paths and remaining semantic audits are complete. Rollback this document through a protected revert PR.

- **Task:** `S00-041` (phase 0)
- **Status:** draft - generated from the frozen schema; independent review pending (Gate-00)
- **Schema:** `source/contracts/schemas/private_report.schema.json`
- **Example:** `source/contracts/examples/private_report.example.json`
- **Schema id:** `https://contracts.etemad.example/schemas/private_report.schema.json`
- **Producer:** P19 | **Consumers:** P27 (editor_in_chief only) | **Owning package:** B06

## Required root fields

- `schema_version`
- `report_id`
- `title`
- `sections`
- `source_refs`
- `generated_at`
- `time_range`
- `generation_status`
- `created_by_project`
- `visibility`
- `report_type`
- `owner_role`
- `publishable`

## Field inventory

- `schema_version`: enum ['1.0']
- `report_id`: string
- `title`: string
- `sections`: array
- `source_refs`: array
- `generated_at`: string (date-time)
- `time_range`: object
- `generation_status`: enum ['draft', 'ready_for_policy', 'completed']
- `created_by_project`: string
- `visibility`: enum ['executive_private']
- `report_type`: enum ['media_narratives', 'political_public_affairs', 'editorial_decision_support']
- `owner_role`: enum ['editor_in_chief']
- `publishable`: boolean

## Enumerations

- `schema_version` = ['1.0']
- `generation_status` = ['draft', 'ready_for_policy', 'completed']
- `visibility` = ['executive_private']
- `report_type` = ['media_narratives', 'political_public_affairs', 'editorial_decision_support']
- `owner_role` = ['editor_in_chief']

## Structural notes

- Root `additionalProperties: false`: yes
- Nested objects closed: 3/3
- Example top-level keys (13): `created_by_project`, `generated_at`, `generation_status`, `owner_role`, `publishable`, `report_id`, `report_type`, `schema_version`, `sections`, `source_refs`, `time_range`, `title`, `visibility`
- `schema_version` in example: `1.0`

## Semantic checks the schema does NOT enforce

- Uniqueness of ids across records (enforced by storage keys, not JSON Schema).
- Cross-contract joins (for example `normalized_news` -> `cluster_result`) are referential, not validated here.
- Provenance/rights truthfulness: the schema records a value, it cannot prove it is correct.
- Time correctness beyond `format: date-time` (UTC normalisation is producer responsibility).

## Compatibility rules

- v1.0 is frozen: no silent field rename or enum narrowing.
- A required-field or enum change needs a new version, an ADR and producer/consumer tests.
- Consumers must reject unknown `schema_version` and warn with the record id.
