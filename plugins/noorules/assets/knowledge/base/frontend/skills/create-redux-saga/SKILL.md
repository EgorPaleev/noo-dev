---
name: create-redux-saga
description: Create or update a Redux-Saga workflow after resolving the installed Saga API, action contracts, watcher concurrency, task supervision, cancellation, cleanup and testing strategy. Use when the user asks to add, orchestrate, extend, debug or fix a saga worker, watcher, channel or root registration.
---

# Create Redux Saga

Add a saga only when the workflow needs Saga-level orchestration and make its
task lifetime explicit.

## Resolve inputs

Obtain or infer:

- trigger actions and success, failure or completion outputs;
- every, latest, leading, queued or custom concurrency semantics;
- parent-child task relationship and root supervision;
- cancellation and owned resource cleanup;
- API calls, channels and test strategy.

Request clarification only when concurrency or cancellation semantics would
materially change observable behavior and cannot be resolved locally.

## Inspect before writing

1. Read applicable `AGENTS.md` files.
2. If present, read `.agents/manifest.json`, `ai-rules.config.json`, applicable
   `.agents/local/` async rules and selected Redux-Saga documents.
3. Inspect `package.json` and verify compatible `redux-saga` and test-library
   versions are installed. Do not install or upgrade them.
4. Inspect saga middleware setup, root saga, action creators, API cancellation
   support and at least two nearby watchers or workers when available.
5. Confirm that RTK Query, a thunk or listener middleware does not already own
   the requested behavior.
6. Report contradictions between project rules, installed types and nearby code
   before editing. Installed APIs and documented project priority win.

Do not run remote installers, codemods or network commands as part of this
workflow.

## Plan

List the worker and watcher owner, action flow, concurrency helper, task
attachment, cancellation path, cleanup, registration, tests and files that
remain untouched.

Do not invent a root-saga hierarchy, channel protocol or test matcher that is
not supported by the project and installed packages.

## Implement

Follow the selected Redux-Saga rule and `Adding a Redux-Saga Workflow`
workflow. Yield or compose every effect that must execute. Prefer `call` for
declarative invocation, keep errors observable, and distinguish attached
`fork` tasks from detached `spawn` tasks.

Choose watcher concurrency from the required behavior, not convention alone.
Wire cancellation to owned requests or subscriptions, close channels in
`finally`, and wait for cleanup with `join` only when the caller requires it.
Use existing action creators and root registration.

## Verify and report

Run focused tests for success, failure, overlap, cancellation and cleanup with
the installed test APIs, then available type checks, lint, tests or build.

Report:

- concurrency, supervision and cancellation semantics resolved;
- created and changed files;
- skipped existing files;
- checks and results;
- version-sensitive assumptions or unresolved contradictions.
