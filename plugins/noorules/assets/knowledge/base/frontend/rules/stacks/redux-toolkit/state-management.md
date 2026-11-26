# Redux Toolkit State Management

## Purpose

Use Redux Toolkit for predictable client-state ownership, typed actions and
reducers, and safe store configuration.

## Applies when

Apply when `@reduxjs/toolkit` is installed and the `redux-toolkit` preset is
selected. Verify the installed version before using optional or recently added
APIs.

## Does not apply when

Do not move remote server state out of its selected query cache, introduce a
Redux store into a project that uses another state strategy, or require Redux
Toolkit when the dependency is absent.

## Rules

- Keep each slice beside the module that owns its state and public actions.
  Let the selected architecture decide the directory and export boundary.
- Create the store at the application initialization boundary with
  `configureStore`. Add middleware through the callback form and preserve the
  defaults with `getDefaultMiddleware().concat(...)` or `.prepend(...)`.
- Keep the serializability and immutability checks enabled. Narrow an ignored
  action or state path only for a verified integration that cannot be made
  serializable; Redux-Saga effect descriptors alone do not require disabling
  these checks.
- Use `createSlice` for related state, reducers and generated actions. A case
  reducer may mutate the Immer draft or return replacement state, but must not
  do both.
- Generate IDs, timestamps and other nondeterministic values before reducer
  execution, including in a `prepare` callback when the action owns them.
- Reuse generated action creators and their `.type` or `.match` helpers instead
  of duplicating action-type strings.
- Handle external actions with the `extraReducers` builder callback. Keep
  cross-slice coordination explicit and avoid importing another slice's
  reducer internals.
- Export selectors from the state owner. Match their root-state input to the
  store's actual reducer key, including any established dynamic-injection
  convention.
- Infer `RootState` and `AppDispatch` from the configured store and expose the
  project's typed dispatch and selector hooks where React is used. Do not
  import a global store into feature code.
- Use RTK Query for cached remote server state. Use `createAsyncThunk` for a
  bounded request lifecycle, listener middleware for lightweight reactive
  workflows, and Redux-Saga only when the project has selected it for more
  complex orchestration.
- Follow the project's existing static or dynamic reducer-registration model;
  do not introduce reducer injection as part of an unrelated slice change.
- Test reducer transitions, action contracts and selectors as observable
  behavior. Add store-level tests when middleware or cross-slice behavior is
  part of the change.

## Checklist

- [ ] The slice has a clear owner and public API.
- [ ] Store defaults and development checks remain enabled.
- [ ] Reducers are deterministic and action payloads are serializable.
- [ ] Server state remains in the selected query cache.
- [ ] Selectors and typed hooks match the actual store shape.
- [ ] Reducer, selector and integration behavior is covered by focused tests.
