# Adding a Page

## Purpose

Add a Next.js App Router page through an FSD page slice without assuming
project-specific route registries, metadata or navigation shells.

## Applies when

Apply when both `fsd-nextjs` and `nextjs-app-router` are selected.

## Does not apply when

Do not use for Pages Router, non-FSD projects or projects with a different
documented routing adapter.

## Steps

1. Read project architecture, naming and navigation rules.
2. Inspect sibling page slices and route entries.
3. Resolve the route, dynamic params, runtime needs and owning page slice.
4. Create only the segments required by current behavior.
5. Add the page component and its minimal public API.
6. Add a thin App Router entry using the installed-version API.
7. Add metadata only when required and supported by the route.
8. Perform project-specific route registry, navigation and breadcrumb steps.
9. Run the documented focused checks.

## Checklist

- [ ] Route and page ownership are explicit.
- [ ] Created segments match the written plan.
- [ ] The route entry is thin and version-correct.
- [ ] Imports use public APIs.
- [ ] Project navigation post-steps are complete.
