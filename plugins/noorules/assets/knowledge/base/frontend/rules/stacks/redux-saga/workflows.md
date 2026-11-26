# Redux-Saga Workflows

## Purpose

Use Redux-Saga for explicit, cancellable workflows while preserving correct
task relationships, error propagation and testable effect descriptions.

## Applies when

Apply when `redux-saga` is installed and the `redux-saga` preset is selected.
Verify the installed version before relying on optional helpers or TypeScript
integration packages.

## Does not apply when

Do not introduce sagas for ordinary cached server state, a bounded thunk, or a
small reactive workflow already owned by RTK Query, `createAsyncThunk`, or
listener middleware. Do not imply that Redux Toolkit requires Redux-Saga.

## Rules

- Yield effect descriptors to execute them, or compose descriptors inside a
  yielded `all` or `race`. A missing `yield` skips an effect; it freezes the
  runtime only when it participates in a tight synchronous loop.
- Prefer `call` for declarative invocation, correct method context and focused
  tests. Yielding a Promise directly is supported, but neither form aborts the
  underlying I/O unless the Promise implements Saga cancellation or the worker
  wires cancellation to an `AbortController` or equivalent API.
- Select `takeEvery`, `takeLatest` or `takeLeading` from the operation's
  concurrency contract. `takeLatest` cancels older workers and
  `takeLeading` ignores triggers while one worker runs; neither guarantees
  server-side idempotency. Require a server-supported idempotency key for
  irreversible or retried writes.
- Use `fork` for attached tasks whose errors and completion belong to the
  parent. Use `spawn` only for intentionally detached supervision: errors are
  isolated from the parent task but remain observable through local handling
  or the middleware `onError` hook.
- Do not place an immediately completing non-blocking effect such as `fork`
  directly in `race`. Race blocking effects or tasks whose completion is the
  event being compared; losing effects are cancelled automatically.
- Put cancellation cleanup in `finally` and check `cancelled()` only where the
  worker owns resources or state that needs cleanup. `cancel` is non-blocking;
  `join` a task when the caller must wait for its cleanup to finish.
- Use `actionChannel` with an intentional buffer when actions must be queued or
  serialized. For `eventChannel`, choose a buffer deliberately, never emit
  `null` or `undefined`, propagate `END` intentionally and close the channel in
  `finally`.
- Start the saga middleware after creating the store. With Redux Toolkit, add
  it through `configureStore({ middleware: getDefaultMiddleware =>
  getDefaultMiddleware().concat(sagaMiddleware) })` and keep the defaults.
- Reuse Redux Toolkit action creators and their `.type` or `.match` helpers in
  watchers rather than duplicating string action types.
- Test observable workflow behavior with the project's selected Saga test
  strategy. Do not invent partial matchers: `redux-saga-test-plan` has no
  `matchers.race.fn`. Supply plain resolved values from providers, not effect
  descriptors such as `delay(...)`; test races with an exact or dynamic
  provider, controlled Promises, fake timers, or `runSaga` as appropriate.
- Use typed Saga helpers only when their package is installed and selected.
  Otherwise type generators, action payloads, task results and API boundaries
  with the installed Redux-Saga and TypeScript APIs.

## Checklist

- [ ] The workflow needs Saga-level orchestration.
- [ ] Watcher concurrency matches the operation contract.
- [ ] Cancellation reaches owned resources and cleanup when required.
- [ ] Fork, spawn, race and channel lifetimes are intentional.
- [ ] Errors remain observable at the correct boundary.
- [ ] Tests use APIs and matchers available in installed packages.
