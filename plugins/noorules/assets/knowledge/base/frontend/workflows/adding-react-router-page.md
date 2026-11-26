# Adding an FSD React Router Page

## Purpose

Add an FSD page and register it with React Router without inventing project
navigation, authentication or layout conventions.

## Applies when

Apply when the `fsd-react-router` preset is selected and a task adds a browser
route or FSD page.

## Does not apply when

Do not use for framework file routing, non-FSD projects or repositories with a
different documented route adapter.

## Steps

1. Read project architecture and the [FSD React Router
   rule](../rules/architecture/fsd/react-router.md).
2. Inspect the installed React Router version, route tree, path helpers and at
   least two sibling page slices when available.
3. Resolve the route path, dynamic parameters, owning page slice, layout,
   authentication, error boundary and navigation visibility.
4. Create only the page segments required by current behavior and expose the
   route component through the page public API.
5. Add or reuse the typed path builder according to project convention.
6. Register the route under the resolved layout and guard tree using APIs from
   the installed router version.
7. Add a navigation item only when the route is intended to be visible there.
8. Keep page-only filters, data access and composition in the page slice; do
   not extract lower layers for hypothetical reuse.
9. Exercise direct navigation, dynamic parameters, error handling and guarded
   access as applicable.
10. Run focused route tests plus project-required type, lint and build checks.

## Checklist

- [ ] Page ownership and route placement are explicit.
- [ ] Only required segments were created.
- [ ] Route imports use public APIs.
- [ ] Paths, guards, layouts and navigation are synchronized.
- [ ] Installed-version router APIs were verified.
