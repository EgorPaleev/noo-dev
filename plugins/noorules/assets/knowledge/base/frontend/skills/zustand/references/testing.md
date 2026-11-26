# Testing Zustand Stores

Test the public state contract without sharing mutable store instances between
cases.

## Store behavior

- Prefer a vanilla store factory for unit tests and framework/provider code. A
  fresh factory result per test avoids order-dependent state leakage.
- Exercise public actions, then assert `getState()` or a focused selector.
- Test `subscribe()` when notification count, selected values or cleanup are
  observable requirements. Always unsubscribe resources created by a test.
- Cover merge and full-replacement behavior when callers use both forms.
- For async actions, cover success, expected failure, overlap and cancellation
  when those cases are part of the action contract.

## React selectors

- Use the project's installed React test tools; do not add a hook library just
  for Zustand tests.
- Assert rendered behavior or selector results. Add a render-count assertion
  only when avoiding unrelated updates is an intentional performance contract.
- Exercise constructed selector results through `useShallow` and verify stable
  behavior after unrelated state changes.
- When a Context provides the store, test two provider instances when isolation
  is important.

## Persistence and SSR

- Use a deterministic in-memory `StateStorage` or `PersistStorage`; do not read
  or delete real browser storage owned by another test.
- Cover a fresh store, valid persisted state, corrupt state, version mismatch,
  migration and explicit clearing as applicable.
- Await asynchronous rehydration and assert both pre- and post-hydration states.
- For Next.js-compatible factories, create two stores with different initial
  data and prove mutations do not cross request/provider boundaries.

Reset module-owned singleton stores between tests through an explicit project
helper or a complete known state. Do not expose a production-only reset API
solely for the test suite.

Run focused tests first, then the project's type check, lint, broader tests and
build in proportion to the change.
