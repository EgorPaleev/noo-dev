# Adding an RTK Query Endpoint

## Purpose

Add an RTK Query endpoint with correct API ownership, cache identity,
invalidation and lifecycle behavior.

## Applies when

Apply when the project has selected RTK Query and the operation belongs in an
existing or explicitly justified API slice.

## Does not apply when

Do not create an endpoint for local-only state or duplicate an operation owned
by another selected server-state layer.

## Steps

1. Read the selected RTK Query, transport and architecture rules.
2. Inspect the store registration, base API, endpoint injection and nearby tag
   conventions.
3. Resolve the owning API slice and reuse its base query and error contract.
4. Define the result and single argument types, including every request input.
5. Add a query or mutation and transform transport data at the API boundary.
6. Define provided and invalidated tags for individual and collection caches.
7. Add lifecycle logic only when invalidation cannot express the behavior, and
   include failure handling and cleanup.
8. Export the endpoint, generated hooks or selectors through the established
   public API without registering duplicate middleware.
9. Integrate loading, error, empty and success states at the consumer boundary.
10. Test request construction, result/error mapping, cache effects and cleanup.

## Checklist

- [ ] The endpoint uses the correct API slice.
- [ ] Arguments determine the request and cache identity.
- [ ] Tags cover every affected cache scope.
- [ ] Manual updates have rollback or race-safe invalidation.
- [ ] Exports and consumer states follow project conventions.
- [ ] Endpoint and cache behavior has focused tests.
