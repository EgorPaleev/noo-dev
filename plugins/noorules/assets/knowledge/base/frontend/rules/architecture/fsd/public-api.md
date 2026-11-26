# Feature-Sliced Public API

## Purpose

Expose stable slice and shared-segment contracts without leaking internal
structure or mixing runtime environments.

## Applies when

Apply to projects using Feature-Sliced Design.

## Does not apply when

Do not add barrel files where the project explicitly avoids them or where they
would create an unsafe runtime graph.

## Rules

- Export a slice through its documented public entry point.
- Import a slice through that entry point from outside the slice.
- Keep public entry files limited to exports.
- Give shared segments separate entry points instead of one global shared
  barrel.
- Export only contracts required by external consumers.
- Add an environment-specific entry point only when one public entry cannot
  preserve a runtime boundary.
- Do not use wildcard exports when they expose internals accidentally.
- Keep project-specific entry filenames and aliases in project context.

## Checklist

- [ ] External imports use the owning public API.
- [ ] Entry files contain no implementation.
- [ ] Server-only exports cannot enter a client graph.
- [ ] Public surface is minimal.
- [ ] Shared segment boundaries remain explicit.
