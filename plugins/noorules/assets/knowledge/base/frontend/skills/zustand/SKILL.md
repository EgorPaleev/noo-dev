---
name: zustand
description: Create, update, migrate, debug, test, or review Zustand stores after resolving the installed version, state owner, store API, selector behavior, middleware, persistence, rendering boundary, and project conventions. Use for Zustand 5 work and explicit Zustand 4-to-5 migrations; do not apply Zustand 5 behavior to ordinary Zustand 4 tasks.
---

# Zustand 5

Work with the installed Zustand API while preserving the state contract and
architecture owned by the project.

## Resolve the task

Determine or infer:

- the state owner and why it must outlive a component;
- React hook, vanilla store or framework-provider boundary;
- state, actions, selectors and public exports;
- middleware order and optional peer dependencies;
- persistence, hydration, request isolation and migration requirements;
- expected tests and compatibility constraints.

Ask only when ownership or public behavior cannot be resolved from project
context and nearby code. Do not invent a root store, slice layout, storage key,
remote-data policy or retry contract.

## Inspect before editing

1. Read applicable `AGENTS.md`, `ai-rules.config.json`, selected rules and local
   instructions.
2. Inspect package metadata and the installed `zustand/package.json`. Ordinary
   work requires Zustand 5.x. For 4.x, proceed only when the user explicitly
   requested a v4-to-v5 migration; otherwise report the mismatch.
3. Inspect installed public exports or types before choosing an overload,
   middleware or version-sensitive API.
4. Inspect store creation, providers, middleware, selectors, consumers, public
   exports and focused tests. Check nearby conventions before proposing a new
   store or slice.
5. Report contradictions instead of silently selecting a convention.

Use sources in this order: the direct user request, project-owned instructions,
the installed Zustand package and public types, current official Zustand
documentation, then this skill's references. Do not run version lookups,
installers, codemods or other network commands merely to apply this skill.

## Load only relevant references

- Read [references/api-v5.md](references/api-v5.md) when choosing store,
  selector, equality, update, slice or middleware APIs.
- Read [references/persistence-nextjs.md](references/persistence-nextjs.md) for
  persisted stores, hydration, Next.js SSR or request isolation.
- Read [references/migration-v5.md](references/migration-v5.md) only for an
  explicit v4-to-v5 migration or deprecated v4 syntax.
- Read [references/testing.md](references/testing.md) when adding, changing or
  reviewing store tests.

The selected `Zustand State Management` stack rule remains the owner of state
boundaries, selector stability, persistence and Next.js requirements. Do not
duplicate or override it here.

## Plan and implement

When ownership, integration or public behavior is ambiguous, write a change
plan before editing. Reuse the established store factory, middleware, typed
hooks and exports.

- Keep the store no broader than its consumers require and avoid duplicating
  server data or component-local state.
- Match the installed overloads. Do not label a compiling direct `create<T>`
  call invalid solely because a curried form also exists.
- Keep selector results stable. For multiple selected values on the standard
  Zustand 5 hook, use `useShallow`; use traditional equality APIs only when the
  project has selected and installed them.
- Make merge versus full replacement explicit and preserve actions on complete
  replacement.
- Async actions are valid. Keep their error, cancellation and service behavior
  consistent with the owning project boundary.
- Validate persisted data, version schema changes and account for hydration.
- In Next.js, use a per-request vanilla store and a client provider; never use a
  module-global store as shared request state or access it from an RSC.

If an explicit migration includes dependency changes, use the project's package
manager and update its lockfile only within that scope. Do not perform a remote
installation without the required authorization. If dependency changes are out
of scope, prepare compatible code and report the remaining migration step.

## Verify and report

Run focused tests for state transitions, selectors and subscriptions, plus
persistence, hydration, request isolation or migration cases when applicable.
Then run available type checks, lint, tests or build in proportion to the
change.

Report:

- detected Zustand version and version-sensitive choices;
- resolved owner, store boundary and public contract;
- changed and skipped files;
- checks and results;
- remaining dependency, hydration or compatibility assumptions.
