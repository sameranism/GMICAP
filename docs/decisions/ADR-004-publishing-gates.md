# ADR-004 — Publication, editorial rights and output gates

**Status:** Proposed pending S00/Gate-00 independent review. **Task:** S00-011.

## References
Master architecture v1.1, B05 editorial and B08 publishing specifications, `AGENTS.md`, `source/contracts/schemas/` frozen v1.0 contracts, and the client decisions guide.

## Proposed decision
1. Publication is deny-by-default and requires a recorded, current, rights-aware editorial policy decision; preserve source attribution, legal uncertainty, approved revision and destination-specific consent. Never assert compliance with Iranian publishing law until human legal/editorial review.
2. Keep backend output switches `public_analysis`, `studio` (audio/video) and `publishing` (domestic, foreign, public reports) independently scoped and revisioned. Recheck applicable switches **immediately before each side effect**, and again on held-job resumption. Switching public outputs off must not stop ingestion, archiving or confidential EIC reports.
3. Treat P19's three `executive_private` reports as **structurally not publishable**. They must not be transformable to publication jobs or reach public search, studio, message queues, destination adapters or public object buckets. Enforce this before queueing and again at each sink; a UI-only check is insufficient.
4. B08 formats **one approved canonical AI/editorial output independently per destination adapter**, without modifying its source or replaying generation centrally. Use destination-scoped idempotency, bounded retry, expiry checks and a blocked/unknown outcome for ambiguous provider acknowledgment; do not cause duplicate messages on retry.
5. Real destinations (Telegram, Bale, Eitaa, Rubika, WhatsApp Business, other channels) remain disabled until official interfaces, contractual access, credentials, permissions and testing are verified. Unknown Etemad CMS remains a replaceable **mock adapter**.
6. No external paid model operation, real content publishing or legal assertions are authorized by acceptance of this document alone. Require separate scope-specific authorization and evidence.

## Testing and acceptance
Prove forbidden publication of EIC-private items (including malformed payloads), disabled-switch side-effect suppression, approval/revision invalidation, destination isolation and idempotent retry using mocks before any real integration. Actual test evidence and independent review are required; current status is documentation only.

## Rollback
Close/revert this ADR PR; keep publishing disabled.
