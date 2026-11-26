# RTK Query Data Fetching

## Purpose

Use RTK Query for declarative remote-data fetching, cache ownership and
invalidation without duplicating server state in client slices.

## Applies when

Apply when `@reduxjs/toolkit` is installed, the project uses RTK Query, and the
`rtk-query` preset is selected. Verify the installed version and import from
`@reduxjs/toolkit/query/react` only when React hooks are required.

## Does not apply when

Do not use RTK Query for local UI state or force it into a project that selected
another server-state strategy. The presence of `@reduxjs/toolkit` alone does
not prove that RTK Query is in use.

## Rules

- Reuse the API slice that owns the relevant transport and cache domain.
  Prefer one API slice per base URL or cohesive backend boundary because each
  API middleware instance has a runtime cost.
- Register an API slice reducer and middleware exactly once. Preserve Redux
  Toolkit's default middleware through the `configureStore` callback.
- Use the core `@reduxjs/toolkit/query` entry point outside React. Use the React
  entry point only for generated hooks, and call `setupListeners` only when
  focus or reconnect refetch behavior is selected.
- Define reads with `build.query<Result, Arg>` and server-changing operations
  with `build.mutation<Result, Arg>`. Keep the single endpoint argument typed
  and include every value that changes the request or cache identity.
- Keep query arguments serializable and stable. Transform transport responses
  at the API boundary; a custom `queryFn` must return a `{ data }` or `{ error }`
  result in the form expected by RTK Query.
- Model cache relationships with `providesTags` and `invalidatesTags`. Use a
  stable list tag when mutations must refresh collections as well as individual
  entities.
- Prefer automated invalidation over manual cache edits. For optimistic or
  pessimistic `updateQueryData`, retain the returned patch and undo it on
  failure, or invalidate on overlapping-request races where rollback is unsafe.
- Use `onQueryStarted` for one request lifecycle. Use `onCacheEntryAdded` for
  the lifetime of a cache entry, await its lifecycle promises, and release
  subscriptions or sockets when the entry is removed.
- Treat cache entries as scoped by endpoint plus serialized arguments. Do not
  assume different endpoints share one normalized entity cache.
- Use an injected endpoint to split code while preserving the same API object.
  Do not register another reducer or middleware for an injected endpoint.
- Do not mirror RTK Query results into a regular slice. Derive view state from
  query results and use selectors or endpoint cache updates when needed.
- Use a mutation trigger's `.unwrap()` only when imperative success/error
  control is needed. Keep retries, polling and refetch policies explicit and
  bounded.
- In server-rendered applications, isolate stores by request and follow the
  project's hydration and cleanup convention.
- Test success and error contracts, argument-sensitive caching, invalidation,
  lifecycle cleanup and manual rollback where those behaviors are present.

## Checklist

- [ ] The owning API slice and transport boundary are reused.
- [ ] Reducer and middleware are registered exactly once.
- [ ] Endpoint arguments fully determine requests and cache identity.
- [ ] Tags cover individual and collection cache effects.
- [ ] Lifecycle handlers clean up resources and handle failures.
- [ ] Server state is not duplicated in a client slice.
