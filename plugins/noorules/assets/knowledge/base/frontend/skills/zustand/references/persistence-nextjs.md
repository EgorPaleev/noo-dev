# Zustand Persistence and Next.js

Load this reference only when storage, hydration or server rendering is part of
the task.

## Persisted state

- `persist` requires a unique `name`. Its default storage is equivalent to
  `createJSONStorage(() => localStorage)` when browser storage is available;
  `createJSONStorage` is optional, not a Zustand 5 migration requirement.
- Use `partialize` to exclude actions, transient values, credentials, tokens and
  other data that does not belong in durable client storage.
- Treat the stored payload as untrusted. `createJSONStorage` parses JSON but
  does not validate its runtime shape. Use a validating custom
  `PersistStorage`, or validate before merging data into trusted state.
- Increment `version` when the persisted schema changes. Keep `migrate`
  deterministic and return the complete persisted shape expected by the new
  version. Define a safe fallback for corrupt or unsupported data.
- Use a custom `merge` when shallow merge would lose nested defaults. Test both
  migrated and fresh data.
- Use `store.persist.clearStorage()`, `rehydrate()`, hydration listeners and
  `getOptions()` when middleware owns the storage lifecycle. Do not hard-code a
  direct `localStorage.removeItem` call for an abstract or changed backend.
- Async storage hydrates after store creation. Model the pre-hydration state and
  avoid rendering persisted values as though hydration were synchronous.

## Next.js request and render boundaries

A hydration flag addresses persisted-client timing; it does not isolate server
requests. For SSR-capable Next.js applications:

1. Define a vanilla `createStore` factory that accepts explicit initial state.
2. Create one store instance for each request/provider lifecycle.
3. Hold the instance in a Client Component provider and expose a typed hook
   that calls `useStore(store, selector)`.
4. Initialize server and client renders with equivalent data.
5. Keep React Server Components stateless with respect to Zustand. Pass
   serializable initial data into the client boundary instead of reading or
   mutating a store from the RSC.

Do not export a module-global store as server request state. A browser-only
module singleton remains a separate client architecture choice and must not be
presented as request isolation.

For persisted Next.js state, decide whether automatic hydration or
`skipHydration` plus an explicit `rehydrate()` produces the required first
render. Test server markup, the initial client render and post-hydration state.

Official references:

- https://zustand.docs.pmnd.rs/reference/middlewares/persist
- https://zustand.docs.pmnd.rs/reference/integrations/persisting-store-data
- https://zustand.docs.pmnd.rs/learn/guides/nextjs
- https://zustand.docs.pmnd.rs/learn/guides/ssr-and-hydration
