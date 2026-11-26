---
name: create-react-modal
description: Create or extend a typed React modal, drawer, or alert dialog after deciding whether it should stay component-local or use the project's application modal manager. Use when the user asks to add, scaffold, register, or refactor an overlay; preserve the installed UI library, ownership, payload, accessibility, and submission conventions instead of inventing a new manager.
---

# Create React Modal

Resolve overlay ownership before writing code.

## Resolve inputs

Obtain or infer:

- overlay purpose and owning page, feature or widget;
- modal, drawer or alert-dialog presentation;
- openers and whether they cross ownership boundaries;
- payload, close and success behavior;
- scaffold-only versus complete interaction scope.

Request a missing choice only when different ownership or presentation choices
would materially change the implementation.

## Inspect before writing

1. Read applicable `AGENTS.md` files.
2. If present, read `.agents/manifest.json`, `ai-rules.config.json`, applicable
   `.agents/local/` rules and `.agents/workflows/adding-modal.md`.
3. Inspect `package.json`, the installed component/state libraries, the current
   modal host and its public API.
4. Inspect at least two nearby overlays when available, including one local and
   one registered example when both exist.
5. Resolve component naming, payload types, registry location, styling,
   notification and mutation conventions.
6. Report contradictions between documentation, installed APIs and nearby code
   before editing. Follow documented priority.

Do not inspect `node_modules` when project documentation and package metadata
resolve the contract. Verify installed-version types or official documentation
only when the component API remains uncertain.

## Decide local or registered ownership

Keep the overlay local when its opener and content share one owner. Open it by
component when the existing manager supports local component entries.

Use a registry identifier only when independent consumers need stable access to
the same overlay. Update the payload map and registry together.

Do not create a global manager merely because the requested UI is a modal. If
the repository has no documented manager, use its existing local-state pattern
unless the user explicitly asks for shared infrastructure.

## Plan

List the owner, overlay kind, local versus registry decision, payload contract,
files to change, success/failure lifecycle and files that remain untouched.

## Implement

Follow `.agents/workflows/adding-modal.md`. Reuse the installed UI primitives and
manager API. Keep concrete UI, schemas and business mutations with the owning
slice. Preserve input on recoverable failure and close or replace only after the
documented success condition. Add accessible naming, focus, escape/backdrop and
pending/disabled/error behavior required by the installed library.

Do not move remote server state into the modal store, import product slices from
shared infrastructure or invent registry names outside project convention.

## Verify and report

Run focused type and interaction checks plus project-required lint, tests or
build in proportion to the change.

Report:

- ownership and local/registry decision;
- created and changed files;
- skipped existing files;
- checks and results;
- contradictions or remaining manual integration.
