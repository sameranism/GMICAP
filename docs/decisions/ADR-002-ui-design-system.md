# ADR-002 — ETEMAD interface design system and UI stack

- **Status:** Proposed for independent S00 review
- **Scope:** S00-009 / B09 / P27
- **References:** `source/specs/00_MASTER_ETEMAD_ARCHITECTURE.md`, `source/specs/B09_INTERFACE_TECHNICAL_SPEC.md`, `guides/CLIENT_DECISIONS.md`, `AGENTS.md`

## Context and conflict

The earlier B09 technical specification refers to **Mantine**. The subsequent explicit client decision recorded in `guides/CLIENT_DECISIONS.md` selects **React/TypeScript + shadcn/ui + Tailwind CSS v4**, with DTCG-compatible design tokens and accessible UI primitives. The original B09 document remains historical baseline evidence and must not be silently overwritten. The new decision applies to implementation of B09 UI only; backend architecture and frozen wire schemas are unaffected.

## Proposed decision

1. Use React and TypeScript, **shadcn/ui** components and **Tailwind CSS v4** as the base interface toolkit. Use **React Aria where required** for accessible interactions not covered by those primitives. Do not add Mantine to new code.
2. Define a project-owned **Etemad Editorial Design System** using DTCG-compatible token definitions and mappings. Keep product components independent from any library-specific CSS classes as far as practical; enable reversible migration.
3. Use Persian-first RTL across dashboards, filters, forms, tables, charts and editor tools, while properly isolating URLs, IDs and other LTR content. Use Vazirmatn only with verified distribution rights and font availability. Adopt Lucide icons, Tiptap editor and TanStack utilities as needed by individual authorized tasks; avoid installing unused libraries.
4. Use a restrained newspaper-inspired visual language (paper, dark ink, provisional editorial red), but **do not claim official brand conformance**. Logo, official colors, approved assets and usage rights remain pending.
5. Apply keyboard accessibility, semantic labels, visible focus styles, adequate contrast, responsive navigation, loading/empty/error/forbidden states and reduced motion.
6. UI hides unauthorized controls for usability but must not be trusted for authorization. P28 enforces server-side role scopes; executive-private reports are never exposed to owner/staff/public search or publishing; output switches are enforced before backend side effects.

## Alternatives

- **Mantine**: previously specified; rejected for new B09 implementation due to the more recent client decision, not because of a measured benchmark.
- Fully custom components: maximum control but higher maintenance and accessibility burden.
- shadcn/ui + Tailwind v4: selected by client; requires a carefully managed local design-token layer.

## Impacts and follow-up

S00-005 frontend rules and later B09 tasks must follow this ADR once independently accepted. UI snapshots, contrast, keyboard flows, RTL layouts and role-based screens require actual automated/manual checks when executable UI exists. Do not confuse this decision document with an implemented interface or successful build.

## Open decisions and rollback

Obtain official logo/colors/font permissions and confirm relevant version compatibility during scaffolding. Revert this ADR and its dependent UI implementation PRs if the client later approves a different interface stack; leave the original source specification unaltered.
