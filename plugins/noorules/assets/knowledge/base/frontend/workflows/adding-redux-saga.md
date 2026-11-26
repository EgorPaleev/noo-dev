# Adding a Redux-Saga Workflow

## Purpose

Add a Redux-Saga workflow with an explicit concurrency contract, cancellable
resources, observable errors and reliable tests.

## Applies when

Apply when Redux-Saga is selected and the use case requires multi-step or
long-lived orchestration beyond the project's simpler async mechanisms.

## Does not apply when

Do not add a saga for cache ownership, a single request lifecycle, or a small
reaction already handled by the selected query, thunk or listener mechanism.

## Steps

1. Read the selected Redux-Saga, state and architecture rules.
2. Inspect saga middleware setup, root supervision, actions and nearby workers.
3. Describe the trigger, completion, failure, cancellation and concurrency
   contract before choosing helpers.
4. Add a worker whose effects, errors and owned resources follow that contract.
5. Add a watcher with the required every, latest, leading, queue or custom
   scheduling semantics.
6. Wire attached or detached tasks deliberately and keep root errors observable.
7. Add cleanup for channels, subscriptions, abortable requests and state that
   the worker owns.
8. Export and register the watcher through the established root-saga boundary.
9. Test success, failure, overlap, cancellation and cleanup paths with the
   project's installed test APIs.
10. Run focused type checks and the relevant integration tests.

## Checklist

- [ ] Saga is the appropriate async owner.
- [ ] Watcher concurrency is documented and tested.
- [ ] Cancellation and cleanup cover owned resources.
- [ ] Errors are visible at the intended boundary.
- [ ] Root registration follows existing supervision.
- [ ] Tests cover overlap and cancellation, not only success.
