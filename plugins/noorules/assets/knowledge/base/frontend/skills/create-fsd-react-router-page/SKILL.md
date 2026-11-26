---
name: create-fsd-react-router-page
description: Create or complete a Feature-Sliced Design page and register it with an installed React Router route tree after resolving page ownership, public APIs, path helpers, layouts, guards, error boundaries, navigation, and aliases. Use when the user asks to add, scaffold, generate, or integrate an FSD page or browser route in a React Router project; do not use for framework file routing or non-FSD repositories.
---

# Create FSD React Router Page

Create the page only after the repository confirms its routing and FSD
conventions.

## Resolve inputs

Obtain or infer:

- page purpose, domain name and route path;
- dynamic parameters and URL-backed state;
- required layout, authentication guard and error boundary;
- navigation visibility;
- scaffold-only versus complete route integration.

Request a missing choice when different routes or guard/layout ownership would
produce materially different results.

## Inspect before writing

1. Read applicable `AGENTS.md` files.
2. If present, read `.agents/manifest.json`, `ai-rules.config.json`, applicable
   `.agents/local/` rules and `.agents/workflows/adding-react-router-page.md`.
3. Inspect `package.json`, TypeScript/bundler aliases and the installed
   `react-router` version.
4. Inspect the route tree, path-helper contract and at least two sibling page
   slices when available.
5. Resolve source root, page layer, file casing, public API, route registration,
   layout/guard tree, error handling and navigation post-steps.
6. Report contradictions between docs, aliases and code before editing. Follow
   documented priority rather than silently choosing a convention.

Do not inspect router internals in `node_modules` when project documentation and
installed-version metadata resolve the operation.

## Plan

List:

- target page slice and required segments;
- route helper and route-tree insertion point;
- layouts, guards and error boundaries that will be reused;
- optional navigation changes;
- files that remain untouched.

Do not create empty segments, widgets, features or entities for hypothetical
reuse.

## Implement

Follow `.agents/workflows/adding-react-router-page.md`. Export the route component
through the page public API, register it with installed-version React Router
APIs and keep page-specific behavior in the page slice. Reuse existing path
helpers, layouts, guards and navigation structures. Add a menu entry only when
the requested route should be discoverable there.

Preserve existing routes and do not rewrite router architecture for a page-add
request.

## Verify and report

Exercise direct navigation, dynamic parameters, guarded access and error
handling as applicable. Run focused route checks plus project-required type,
lint, tests or build.

Report:

- created and changed files;
- resolved route/layout/guard ownership;
- skipped existing files and optional post-steps;
- checks and results;
- contradictions or remaining manual integration.
