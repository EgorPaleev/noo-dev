# Zustand State Management

## Purpose

Keep shared client state explicit, version-aware and isolated from request,
rendering and persistence boundaries when a React project uses Zustand 5.

## Applies when

Apply when `zustand` 5.x is installed and the `zustand` preset is selected for
creating, changing, testing or reviewing a React or vanilla Zustand store.

## Does not apply when

Do not introduce Zustand for component-local state, an existing query cache or
a store owned by another state library. For Zustand 4, apply this rule only as
the target behavior of an explicit v4-to-v5 migration.

## Rules

- Inspect the installed `zustand/package.json`, public types, store composition,
  middleware and nearby selectors before changing a store. Do not install or
  upgrade Zustand merely to apply this rule.
- Keep state with the narrowest owner that needs it. Distinguish local render
  state, shared client state and remote data already owned by a query cache or
  framework boundary; do not mirror one owner into another without a concrete
  synchronization requirement.
- Use the installed `create`, `createStore` and `useStore` overloads. Do not
  reject a direct `create<State>(initializer)` form when the installed types
  accept it; use the curried form when middleware typing or the established
  project convention requires it.
- Select only the values a component needs. A selector that returns a fresh
  object or array must return a stable result; in Zustand 5, wrap such a
  selector with `useShallow` or use a project-approved equality-aware API.
- Use `createWithEqualityFn` or `useStoreWithEqualityFn` only when custom
  equality is required and the traditional entry point and its peer dependency
  are installed. The standard Zustand 5 hook does not accept an equality
  function as a second argument.
- Treat `set` as a shallow merge unless replacement is explicitly requested.
  When `replace` is `true`, provide the complete state including actions; type
  dynamic replace arguments from the installed `setState` signature.
- Keep updates immutable unless the store deliberately uses the Immer
  middleware. Async actions and other effects are allowed, but their error,
  cancellation, retry and ownership behavior must follow the project's
  established service boundary.
- Apply middleware at the combined store boundary, not independently inside
  each slice. Preserve middleware order, mutator types, devtools action naming
  and the project's public exports.
- Treat persisted data as untrusted runtime input. Persist only intended fields,
  exclude secrets, use a unique key, version schema changes, migrate old data
  deterministically and validate deserialized state before trusting it.
- Account for synchronous versus asynchronous hydration. Use the persist API
  for hydration and storage lifecycle instead of reaching into a storage key
  when the middleware owns it.
- In server-rendered Next.js applications, create a vanilla store per request
  and provide it through a client Context boundary. Initialize server and
  client with equivalent data, and do not read from or write to a Zustand store
  in a React Server Component.
- Test store behavior through public actions, selectors and subscriptions.
  Isolate store instances between tests and cover persistence migration,
  hydration or request isolation when those behaviors are part of the contract.

## Checklist

- [ ] Installed Zustand major and relevant public types were inspected.
- [ ] State ownership is shared client state rather than accidental duplication.
- [ ] Selector outputs and equality behavior are stable for Zustand 5.
- [ ] Merge, replacement, middleware and async-action behavior are intentional.
- [ ] Persisted state is minimal, versioned and validated when applicable.
- [ ] Next.js stores are request-scoped and excluded from Server Components.
- [ ] Focused store, selector and boundary tests pass.
