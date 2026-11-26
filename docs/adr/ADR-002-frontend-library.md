# ADR-002 — UI component library selection (proposed)

Status: **PROPOSED / pending repository source package and formal approval**

## Context
ETEMAD Master Specification v1.1 and B09 Interface Technical Specification v1.1 mention React/TypeScript/Mantine. The subsequently supplied Cursor Prompt Pack v2.0 explicitly states the employer's updated decision is shadcn/ui + Tailwind CSS v4, and that this discrepancy must be resolved in ADR-002 rather than silently editing original docs.

## Proposed decision
For new ETEMAD B09 UI work, use React/TypeScript with shadcn/ui and Tailwind CSS v4 as the current proposed basis. Keep UI design tokens and brand assets replaceable, preserve Persian RTL and accessibility, and enforce permissions on the server. Do not claim any component implementation or migration exists.

## Consequences and controls
- The source DOCX files remain immutable historical baselines.
- Before coding B09, verify versions and dependency compatibility; capture changes in the accepted ADR and relevant task manifest.
- If any earlier implementation using Mantine already exists in another branch/environment, inventory it before changing dependencies or rewriting UI.
- The S00 review gate remains blocked until source contracts and actual project checks have been verified.
