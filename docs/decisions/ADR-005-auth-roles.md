# ADR-005 — Authentication, user roles and EIC confidentiality

**Status:** Proposed pending independent review. **Task:** S00-012.

## References
Master ETEMAD architecture, B01 foundation and B09 interface specifications, project P28 and `AGENTS.md`; exact permission contract remains subject to S00 contract audits.

## Proposed decision
- Enforce a maximum of **10 active human accounts** in the authoritative backend, including privileged users. Provide distinct owner, editor-in-chief and authorized staff role scopes, with separate relevant dashboards. Role checks and record-level restrictions must occur on each backend query/action; hidden menus are not security controls.
- Generate a **unique cryptographically random** initial credential per account and require secure one-time issuance, short validity and reset at first use. Store only password hashes, never an initial password in code, shared documentation, logs, tickets or commits. No default/shared account or hidden bypass.
- Require MFA for privileged operations in staging and production; restrict sessions, apply revocation, rate limits and audited login/role/privilege changes. Follow least privilege for staff and service identities.
- Three reports per day are explicitly `executive_private`, available **only** to the editor-in-chief's authorized scope. Even `owner` is denied without a separate, explicitly reviewed permission change. Isolate in database/storage/search/queue/retrieval; exports, API endpoints and studio/publishing must not leak them.
- Separate authentication identity from authorization and output-control policy. Audit actor, scope, action and decision without recording report content or secrets. Require human review for authorization expansion and changes to private data flows.

## Consequences and open details
Specific account enrollment, MFA provider, secret store, session TTL, device policy and exact permission matrix must be set during the owning P28 task with audited tests; this ADR does not invent these parameters or certify deployment.

## Test obligations
Check denied cross-role and object access, 10-user limit, initial credential reset, privileged MFA, session revocation and executive-report non-disclosure. Preserve originals and frozen schemas; report tests NOT_RUN until executable backend exists.

## Rollback
Close PR and retain secure deny-by-default implementation policy.
