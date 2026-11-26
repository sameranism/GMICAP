# ADR-013 — Preserve v1.0 restricted event envelopes and fail closed on shared delivery

Status: Owner-authorized scope; proposed until this protected PR passes its checks.
Baseline: `20d8456ece9addeb7f6cf53434a4ae527b14eae1` (PR #59).
Related: S00-035; corrective maintenance of S01-011, S01-013 and S01-021.
This decision does not accept any of those tasks or close Gate-00.

## Context

The frozen [event envelope](../../source/contracts/schemas/event_envelope.schema.json)
permits public, internal, restricted and executive_private. The existing
[producer](../../backend/core/events.py) rejects restricted. Its fixture bus
dispatches solely by event type; the [fixture outbox](../../backend/core/outbox.py)
accepts a caller-supplied publish callback. Neither establishes a restricted
recipient's identity or artifact-level permission. The [service wiring](../../backend/app/dependencies.py)
uses both fixtures; the [orchestrator](../../backend/core/orchestrator.py)
currently emits internal news.ingested events. The master architecture requires
authenticated service identities, artifact references and private queues; B01
requires authorized data references. The [audit](../contract-audits/event_envelope.md)
records the wider prose/wire mismatch. The exact baseline contract job
[139557889120](https://github.com/sameranism/ETEMAD-pre/actions/runs/45714769452/job/139557889120)
reports S00-035 preflight PASS, 62 task preflights, 336 negative contract cases
and passing boundary checks. These are structural checks, not semantic acceptance.

## Decision

- Preserve the frozen v1.0 schema, examples, event names, required fields and
  wire representation. The constructor must accept restricted as an existing
  valid classification, preserve it verbatim and continue schema validation.
  It must reject unknown classifications; construction is not authorization.
- Restricted is not public or internal. Do not downgrade, relabel, broadcast,
  deliver to an unverified subscriber, enqueue for a generic dispatcher or
  fall back to an unrestricted queue. A reference and an event type do not
  establish a recipient's permission. Never put the payload itself in an envelope.
- Until a separately authenticated restricted route exists, the current shared
  fixture bus and generic fixture outbox must fail closed for restricted
  envelopes, including manually constructed valid envelopes. Reject before
  subscriber invocation, shared outbox persistence or dedupe state mutation;
  recheck at dispatch before calling any callback, since a pending entry can
  change. Return a typed rejection without echoing payload references. No
  caller-supplied boolean, wildcard subscription or label alone can authorize
  restricted delivery. The caller must handle the refusal explicitly; do not
  claim successful delivery or silently discard an event.
- Keep existing public/internal behavior, signatures, schema validation,
  idempotency rules, output switches, permissions and deployment isolation.
  Executive-private is a distinct classification; this correction does not
  authorize changes to executive-private routing or grant policies. The
  existing shared fixture's absence of classification-aware authorization
  remains a separate security finding; production use of private/restricted
  delivery is not approved.
- A future restricted delivery implementation belongs in an isolated,
  authenticated transport adapter with authoritative grants, scoped storage
  and queue access, and positive/negative integration evidence. Do not create
  that transport or widen API/storage access in this correction.
- The wider stream/type/timestamp prose mismatch remains open; no new stream
  field or wire version is authorized by this ADR.

## Follow-up scope and acceptance

After this ADR is merged with required exact-head CI, make one narrowly scoped
Gate-00 remediation PR (not a downstream product integration) covering only
`backend/core/events.py`, `backend/core/outbox.py`,
`backend/tests/test_orchestration.py` and the associated evidence register/audit
if required. These are the minimal producer/consumer/test boundaries, not a
declaration that the downstream S01 tasks have been accepted. Keep all other
core modules and contracts unchanged. If a different boundary must change, stop
and obtain explicit scope authorization.

Required tests:
1. All four existing v1.0 classifications construct unchanged valid envelopes;
   unknown classifications and unknown wire versions are rejected.
2. Directly constructed restricted envelopes cannot invoke shared handlers,
   mutate the bus dedupe set or persist in the generic outbox. A rejected
   restricted event must not consume the idempotency key of a later valid
   internal event. A pending entry reclassified as restricted cannot invoke a
   dispatch callback or be marked dispatched.
3. Existing public/internal delivery, deduplication, schema checks, executive
   privacy controls and all previous tests remain unchanged and passing.
4. Record the applicable preflights, exact-head backend CI (including
   PostgreSQL), contract/boundary tests, bootstrap, trusted Guardian and CodeQL.
   Record any skipped checks and remaining semantic/privacy gaps. Never infer
   full Gate-00 acceptance from this fix.

## Rollback and limits

Revert through a protected PR; never force-push, disable checks or alter the
frozen schema. No production credentials, publishing, deployment, real data
or external service calls are part of this decision.
