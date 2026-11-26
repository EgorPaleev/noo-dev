---
name: create-fsd-page
description: Create or complete a Feature-Sliced Design page in a Next.js App Router project after resolving the repository's page layer, route-entry adapter, naming, metadata, navigation, and public-API conventions. Use when the user asks to add, scaffold, generate, or create an FSD page or route; do not use for non-FSD projects or to invent a new project architecture.
---

# Create FSD Page

Create a page only after the repository confirms the target structure.

## Resolve inputs

Obtain or infer:

- page purpose and domain name;
- route path and dynamic parameters;
- whether metadata, authentication, navigation or breadcrumbs are required;
- whether the user requests scaffold-only or complete route integration.

Stop and request the missing choice when different routes or ownership decisions
would produce materially different results.

## Inspect before writing

1. Read applicable `AGENTS.md` files.
2. If present, read `.agents/manifest.json`, applicable `.agents/local/` overrides,
   `ai-rules.config.json`, and `.agents/workflows/adding-page.md`.
3. Inspect `package.json`, TypeScript aliases and the installed router.
4. Inspect at least two sibling page slices and their route entries when
   available.
5. Resolve:
   - source root and FSD page layer;
   - component/file casing;
   - public API shape;
   - route-entry and metadata pattern;
   - project route registry, navigation and breadcrumb post-steps.
6. Report contradictions between docs and code before editing. Follow the
   documented priority; do not silently choose one convention.

Do not inspect framework internals in `node_modules` when project documentation
already resolves the operation. Read installed-version framework docs only when
the API remains version-sensitive or project instructions require it.

## Plan

Before changing files, list:

- target page slice;
- route entry;
- required files;
- optional project post-steps;
- files that will remain untouched.

Do not create empty `model`, `config`, `api` or other segments. Do not create
widgets, features or entities for hypothetical reuse.

## Implement

Follow the canonical domain sequence in `.agents/workflows/adding-page.md`. Use the
resolved project naming and public-API conventions, preserve existing content,
reuse nearby components, and do not add behavior outside a scaffold-only
request.

## Verify and report

Run available focused checks plus project-required lint, typecheck, tests or
build in proportion to the change.

Report:

- created files;
- changed files;
- skipped existing files;
- checks and results;
- unresolved contradictions or manual post-steps.
