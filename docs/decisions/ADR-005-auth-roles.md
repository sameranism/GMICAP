# ADR-005 — Accounts, roles and access decisions

- **Status:** Accepted
- **Date:** 2026-11-23
- **Task:** S00-012
- **Source:** `source/specs/B01_FOUNDATION_TECHNICAL_SPEC.md`, `source/contracts/schemas/access_decision.schema.json`

## Context

The newsroom is small: a limited number of named humans, each with a different level of access.
The risk is not scale, it is privilege: the editor-in-chief's private reports must never reach the
owner by default, and no shared or default password may exist.

## Decision

1. **At most 10 active human accounts.** No anonymous API access except health and explicit public
   read-only endpoints.
2. **Three base roles:** `owner` (مدیرمسئول), `editor_in_chief` (سردبیر), `staff` (دبیر سرویس/تحلیل‌گر),
   plus per-resource grants. Roles are checked **in the backend** on every request and every record.
3. **Default deny.** Every access decision is an explicit `access_decision` record
   (`allow`/`deny` with reason). Missing grant means deny, never a permissive fallback.
4. **The three `executive_private` reports require an explicit grant to `editor_in_chief`.** Ownership of
   the system does not imply access; an `owner` needs a separately recorded grant.
5. **Credentials:** individually generated first-use credentials, mandatory reset on first login,
   hashed at rest (memory-hard KDF), never logged, never committed. **MFA required for privileged roles**
   in staging/production. No default, shared, or seeded password; no hidden admin bypass.
6. **Sessions** carry a subject id and role claims; every privileged action writes an audit entry
   (`audit.py`) with actor, action, target, decision and correlation id.

## Consequences

- `permissions.py` must be wired to a real identity and grant store before any privileged endpoint ships;
  current code returns deny for everything, which is safe but not functional.
- Access tests are mandatory (`test_security.py`): missing identity, wrong role, missing grant, private
  report leakage, and audit presence.

## Impacted contracts

`access_decision`, `private_report`, `validation_decision`, `settings`-related `output_controls`.

## Open external dependencies

- Whether the newspaper wants SSO/AD later — deferred to phase 2, not a blocker.
- Identity of the 10 humans and their role assignment — client input required before production.
