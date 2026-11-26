# Next.js App Router

## Purpose

Define stable guardrails for projects that use the Next.js App Router without
duplicating version-specific framework documentation.

## Applies when

Apply when the project uses Next.js with the `app` router.

## Does not apply when

Do not apply to the Pages Router or to another React framework. Project routing
adapters may add stricter placement rules.

## Rules

- Read the documentation shipped with the installed Next.js version before
  changing routing, layouts, metadata, caching, middleware, configuration,
  Server Actions or Route Handlers.
- Treat `page`, `layout`, `route`, `loading`, `error` and metadata files as
  framework entry points.
- Keep entry points thin when the project defines a separate composition layer.
- Preserve server rendering unless client capabilities are required.
- Keep runtime-specific imports out of the opposite runtime's module graph.
- Pass only serializable values from Server Components to Client Components.
- Avoid initializing environment-dependent clients during module evaluation
  when build-time evaluation can occur.
- Put application-specific route registries, aliases and wrappers in project
  context.

## Checklist

- [ ] Installed-version docs were checked for the changed API.
- [ ] The route entry contains only its intended responsibility.
- [ ] Server/client imports respect runtime boundaries.
- [ ] Cross-boundary props are serializable.
- [ ] No runtime environment requirement was moved to build-time evaluation.

