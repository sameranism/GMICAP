# ADR-002 — UI design system: shadcn/ui + Tailwind v4 replaces Mantine

- **Status:** Accepted
- **Date:** 2026-11-23
- **Task:** S00-009
- **Supersedes:** Mantine references in the v1.1 source documents (B09)
- **Source:** `source/specs/B09_INTERFACE_TECHNICAL_SPEC.md`, ADR-001

## Context

The v1.1 interface documents still name Mantine. The client later chose shadcn/ui + Tailwind v4.
The code already ships React 19, Vite 6, Tailwind 4 (`frontend/package.json`). Two UI libraries in one
repository would double the design surface and split component ownership.

## Decision

1. **Stack:** React 19 + TypeScript (strict) + Vite + **Tailwind CSS v4** + **shadcn/ui** components,
   with React Aria primitives where accessibility gaps exist. **No Mantine anywhere.**
2. **Tokens:** a single design-token layer (DTCG-compatible naming) consumed by Tailwind theme
   variables. Components read tokens, never raw hex values.
3. **RTL first:** `dir="rtl"`, `lang="fa"` at the document root; logical CSS properties
   (`margin-inline`, `inset-inline`) instead of left/right; Persian typography via token, not inline font names.
4. **Editor:** Tiptap (rich text) and **tables:** TanStack Table, both behind thin wrappers so they can be
   replaced without touching feature code.
5. **Brand assets are placeholders.** Official logo, palette and typography are not supplied; the build
   must render neutral placeholders and keep the asset swap in one module. Do not invent a newspaper logo.
6. **Accessibility:** every interactive component exposes focus, disabled and error states; contrast
   checks are part of the component review, not a later pass.

## Consequences

- `frontend/components.json` (S00-060) configures the shadcn generator; component versions are pinned.
- Any Mantine import is a review failure and can be blocked by lint.
- The newsroom UI written early (`App.tsx`, `NewsDesk.tsx`) is a demo shell only; it is rewritten against
  real contracts in G2, not extended.

## Impacted contracts

None directly. Indirect: `article`, `public_report`, `image_manifest` rendering in B09.

## Open external dependencies

- Official Etemad brand package (logo, colors, typefaces) — BLOCKED until supplied.
- Confirmation of the shadcn version against the installed CLI before generator use.
