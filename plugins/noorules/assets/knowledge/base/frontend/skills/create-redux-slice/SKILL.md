---
name: create-redux-slice
description: Create or update a Redux Toolkit slice after resolving client-state ownership, the installed Toolkit API, reducer registration, public actions, selectors and project architecture. Use when the user asks to add, scaffold, extend or fix a createSlice-based state module; do not use for server data owned by RTK Query or another query cache.
---

# Create Redux Slice

Add the smallest client-state owner that fits the project's existing store and
architecture.

## Resolve inputs

Obtain or infer:

- state responsibility and owning module;
- initial state and serializable public action payloads;
- static or dynamic reducer registration;
- selectors and public exports consumers require;
- external actions or async lifecycle events the slice must observe.

Request clarification only when state ownership or public behavior cannot be
resolved from selected rules and nearby code.

## Inspect before writing

1. Read applicable `AGENTS.md` files.
2. If present, read `.agents/manifest.json`, `ai-rules.config.json`, applicable
   `.agents/local/` state rules and selected Redux Toolkit documents.
3. Inspect `package.json` and verify a compatible `@reduxjs/toolkit` version is
   installed. Do not install or upgrade it.
4. Inspect store creation, typed hooks, reducer registration, public APIs and at
   least two nearby slices when available.
5. Confirm the requested state is client-owned and is not already represented
   by RTK Query or another query cache.
6. Report contradictions between project rules, installed types and nearby code
   before editing. Installed APIs and documented project priority win.

Do not run remote installers, codemods or network commands as part of this
workflow.

## Plan

List the owning module, state and action contracts, reducers, external actions,
selectors, registration, exports, tests and files that remain untouched.

Do not invent a directory, reducer-injection system or global store access when
the project has no established convention for it.

## Implement

Follow the selected Redux Toolkit rule and `Adding a Redux Toolkit Slice`
workflow. Reuse the existing store types, typed hooks and public API. Keep state
minimal and serializable, reducers deterministic, external actions in the
`extraReducers` builder and selectors aligned with the actual root-state key.

Generate nondeterministic payload values before reducer execution. Preserve the
store's default middleware and development checks. Export only the public
actions, selectors, reducer and types required by consumers.

## Verify and report

Run focused reducer and selector tests, then available type checks, lint, tests
or build in proportion to the change.

Report:

- ownership, store key and registration convention resolved;
- created and changed files;
- skipped existing files;
- checks and results;
- version-sensitive assumptions or unresolved contradictions.
