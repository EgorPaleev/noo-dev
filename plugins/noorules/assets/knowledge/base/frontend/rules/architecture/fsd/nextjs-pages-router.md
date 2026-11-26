# FSD with Next.js Pages Router

## Purpose

Separate Next.js Pages Router entries from Feature-Sliced app and pages layers
without forcing an unrelated migration of an established project structure.

## Applies when

Apply when both the `fsd` and `nextjs-pages-router` presets are selected.

## Does not apply when

Do not apply to App Router entries or non-FSD projects. In a hybrid Next.js
project, use the adapter that owns the route being changed.

## Rules

- Reserve the documented `pages` or `src/pages` directory for Next.js routing
  entries and distinguish it from the FSD pages layer.
- Prefer `_app` and `_pages` names for new FSD layers when they would collide
  with framework directories. Preserve a documented legacy layout unless the
  task explicitly includes migration.
- Keep route entries thin. Framework exports such as `getStaticProps`,
  `getStaticPaths`, `getServerSideProps`, page config and locale adaptation may
  remain at the entry boundary while domain mapping stays with its FSD owner.
- Compose the custom Next.js `_app` from providers and initialization owned by
  the FSD app layer; do not confuse the framework `_app` file with that layer.
- Keep API Route implementations in the project-owned application or
  infrastructure boundary and use `pages/api` as the framework adapter when
  the architecture defines that separation.
- Configure aliases for installed FSD layers and import external slice
  contracts through their public APIs.
- Do not introduce App Router-only files, directives or runtime assumptions
  into Pages Router slices.
- Record route roots, layer aliases, data-loading ownership and intentional
  legacy deviations in `.agents/local` project context.

## Checklist

- [ ] Framework routes and FSD layers have unambiguous names.
- [ ] Route entries keep framework adaptation separate from domain ownership.
- [ ] `_app` composes providers from the application layer.
- [ ] API Route placement follows the documented architecture.
- [ ] Aliases and legacy exceptions match project context.
