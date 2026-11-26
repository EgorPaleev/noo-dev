# FSD with Next.js App Router

## Purpose

Resolve the naming and routing collision between Next.js App Router entries and
Feature-Sliced app/pages layers.

## Applies when

Apply when both the `fsd` and `nextjs-app-router` presets are selected.

## Does not apply when

Do not apply to the Next.js Pages Router or to a non-FSD project.

## Rules

- Keep Next.js routing directories as framework entry points.
- Place FSD layers under the source root and use distinct app/pages layer names
  when they would collide with framework directories.
- Prefer `_app` and `_pages` for new Next.js FSD projects.
- Keep route entries thin; permit a minimal adapter for framework route inputs
  when project composition needs parsed values.
- Keep application providers and initialization in the FSD app layer.
- Keep Route Handler implementations in the location selected by project
  architecture; document any entry adapter.
- Configure explicit aliases for every installed FSD layer.
- Split public APIs only when required by the server/client module graph.

## Checklist

- [ ] Framework and FSD directories cannot be confused.
- [ ] Route entries contain only framework adaptation.
- [ ] Providers belong to application initialization.
- [ ] Aliases match real layers.
- [ ] Runtime-specific exports stay isolated.
