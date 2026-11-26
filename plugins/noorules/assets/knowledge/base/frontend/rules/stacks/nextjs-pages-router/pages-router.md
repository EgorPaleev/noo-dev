# Next.js Pages Router

## Purpose

Define stable routing, rendering and data-loading boundaries for projects that
use the Next.js Pages Router without duplicating installed-version framework
documentation.

## Applies when

Apply when Next.js routes are owned by a `pages` or `src/pages` directory.

## Does not apply when

Do not apply these rules to App Router entries. In a hybrid project, apply the
router-specific rules to each route. Project architecture may add stricter
placement and composition boundaries.

## Rules

- Read the documentation for the installed Next.js version before changing
  routing, data fetching, caching, middleware, configuration or API Routes.
- Treat page files, `_app`, `_document`, error pages and `pages/api` files as
  framework entry points. Keep them thin when the project defines a separate
  composition layer.
- Select `getStaticProps`, `getStaticPaths`, `getServerSideProps` or client
  fetching from the route's freshness, personalization and runtime needs; do
  not copy a neighboring choice without checking those constraints.
- Keep `getStaticPaths` fallback behavior, missing-param handling and supported
  locales explicit for dynamic routes.
- Define ISR `revalidate`, stale-content and upstream-failure behavior in
  project context. Do not convert every transient fetch failure into `notFound`.
- Return serializable page props and map transport-specific data before it
  spreads through presentation code.
- Keep application providers and global styles in `_app`. Keep `_document`
  limited to the document shell and framework-supported document concerns.
- Treat `router.query` values as unavailable until the router is ready when
  code runs on the client, and narrow `string | string[] | undefined` inputs.
- Treat API Routes as HTTP boundaries: validate untrusted input and apply the
  project's authentication, authorization, error and response contracts.
- Do not introduce App Router conventions such as Server Components, Server
  Actions, Route Handlers or metadata exports into a Pages Router entry.

## Checklist

- [ ] The installed-version API and rendering mode were checked.
- [ ] The route entry contains only framework adaptation and composition.
- [ ] Dynamic params, fallback and missing-content behavior are explicit.
- [ ] Props and router query values are narrowed and serializable.
- [ ] Caching, localization and API response contracts follow project rules.
