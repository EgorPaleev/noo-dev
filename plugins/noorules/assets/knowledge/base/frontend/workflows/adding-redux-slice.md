# Adding a Redux Toolkit Slice

## Purpose

Add a Redux Toolkit slice with project-aligned ownership, typed public actions
and selectors, and focused state-transition tests.

## Applies when

Apply when the project has selected Redux Toolkit for client state and a new or
extended slice is justified.

## Does not apply when

Do not create a slice for remote data already owned by RTK Query or another
query cache, or when nearby code has a more local state owner.

## Steps

1. Read the selected Redux Toolkit and architecture rules.
2. Inspect the store, typed hooks, reducer registration and neighboring slices.
3. Resolve the state owner, runtime registration and public export boundary.
4. Define the minimal serializable state and initial-state contract.
5. Add deterministic case reducers and generated actions with `createSlice`.
6. Handle external actions through the `extraReducers` builder when needed.
7. Add selectors that accept the project's actual root-state shape.
8. Register the reducer through the existing static or dynamic convention.
9. Export only the public reducer, actions, selectors and types consumers need.
10. Test initial state, transitions, selectors and relevant integration paths.

## Checklist

- [ ] The state is client-owned and minimally scoped.
- [ ] State and action payloads are serializable.
- [ ] Reducers are deterministic.
- [ ] Registration and selectors match the store shape.
- [ ] Public exports follow project architecture.
- [ ] Focused tests cover observable behavior.
