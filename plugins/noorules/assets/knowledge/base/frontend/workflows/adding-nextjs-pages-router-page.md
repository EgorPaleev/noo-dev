# Adding an FSD Next.js Pages Router Page

## Purpose

Add a Next.js Pages Router entry backed by an FSD page slice without assuming
project-specific rendering, localization, SEO or transport contracts.

## Applies when

Apply when `fsd-nextjs-pages-router` is selected and a Pages Router route is
being added or substantially changed.

## Does not apply when

Do not use for App Router, non-FSD projects or a repository with another
documented route adapter.

## Steps

1. Read project architecture, route-root, naming and navigation rules.
2. Inspect sibling framework routes and FSD page slices.
3. Resolve the pathname, dynamic params, locale behavior and required
   rendering mode.
4. Choose `getStaticProps`, `getStaticPaths`, `getServerSideProps` or client
   fetching from the route's actual freshness and runtime requirements.
5. Create only the FSD page segments required by current behavior and expose a
   minimal public API.
6. Add the thin Pages Router entry and keep framework-specific exports at that
   boundary.
7. Define fallback, `notFound`, redirects, ISR and failure behavior when they
   apply.
8. Add project-owned SEO, translation namespaces, navigation and analytics
   integration only when required by local rules.
9. Run the documented focused checks and verify the route in every supported
   rendering state.

## Checklist

- [ ] Route and FSD page ownership are explicit.
- [ ] Rendering mode and dynamic path behavior are justified.
- [ ] The framework entry remains thin and version-correct.
- [ ] Slice imports use the documented public API.
- [ ] Project-specific post-steps and checks are complete.
