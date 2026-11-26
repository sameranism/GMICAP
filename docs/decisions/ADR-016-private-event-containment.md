# ADR-016 — Contain executive-private envelopes on shared fixture routes

Date: 2026-11-26 (Asia/Tehran).
Status: owner-authorized baseline containment, effective upon protected merge.
Baseline: signed main f7d8e876cd66c5da2d96dabab08c2dfdcf2d3e91, [PR #67](https://github.com/sameranism/ETEMAD-pre/pull/67).
Related: ADR-004, ADR-005, ADR-013, ADR-015; S00-035 and S00-041.
No downstream task or Gate acceptance is conferred.

## Context

The frozen event_envelope v1.0 permits executive_private; construction is not
authorization. The current shared bus and generic outbox validate the wire
shape, but their common validate_shared_event guard rejects only restricted.
Neither fixture establishes an authorized recipient. The master requires
separate service identities and private queues; S00-041 documents the gap.
ADR-015 defers dedicated private infrastructure, not containment.

## Decision

Keep all four classifications in the frozen schema, constructor and examples.
Reject executive_private explicitly in the shared guard after schema validation
and before any shared subscription delivery, dedupe reservation, outbox append
or dispatch callback. Use a distinct typed PermissionError subclass without
echoing payload references or sensitive identifiers. Preserve the existing
RestrictedEventRoutingError and its behavior; preserve ordinary public/internal
delivery and deduplication. Raw valid envelopes must be treated identically to
constructor output; revalidate pending outbox entries at dispatch as already
done for restricted. Do not silently downgrade, drop, reroute, or create an
authorization override. No access grants or private route are introduced.
The guard is not artifact authorization and cannot establish that labels are
truthful. Private records must not be fed to generic fixtures.

## Follow-up scope

After protected acceptance of this ADR, a scoped maintenance PR may change
backend/core/events.py, backend/tests/test_orchestration.py and associated
audit/evidence documentation only. The outbox already calls the same guard
on append and dispatch; change it only if the existing implementation cannot
enforce this decision, within a separately recorded scope. No other core,
permissions, storage, job, wire, CI or deployment changes.

Required tests: all four constructors continue validating; unknown classification
and wire version stay rejected; raw executive_private cannot call a shared
subscriber or consume the ordinary event idempotency key; generic outbox
append refuses private before persistence; a pending entry relabeled private
cannot invoke a callback or be marked dispatched. Existing restricted,
public/internal and lifecycle regression tests must pass. Test errors without
echoing the payload reference. Record exact-head backend/contract/CodeQL,
bootstrap, Guardian and applicable main evidence, including skipped checks.
Prior exact-head [contract job](https://github.com/sameranism/ETEMAD-pre/actions/runs/45719772548/job/139574866061)
reports S00-035/S00-041 preflight PASS, 62 preflights, 336 negative cases
and boundary PASS. Frozen schema blob 6cb35988557e365dab5f3f5f299d3a25228a7fb9;
example a6941845157bc6241eafae75490255e285240468 unchanged.

Dedicated private queue/storage, durable transport, trustworthy producer
classification, authorization and cross-package retrieval/permission evidence
remain assigned to their owning stages per ADR-015. Gate-00 still requires its
remaining semantic and baseline secret/permission evidence. No production data
or external services authorized. Rollback via protected revert PR.
