# Adding a Client Query

## Purpose

Add a TanStack Query operation with project-aligned ownership, deterministic
keys and complete UI/cache behavior.

## Applies when

Apply when TanStack Query is installed and the project has selected client-side
querying for the data.

## Does not apply when

Do not force client querying onto server-rendered public data or another
project-approved data strategy.

## Steps

1. Read project data-flow, FSD and API rules.
2. Inspect sibling services, keys, query options and mutations.
3. Resolve the owning page, feature, entity or shared API module from project
   context; do not infer ownership from the resource name alone.
4. Define or reuse validated request/response contracts.
5. Add the request through the approved client transport.
6. Add deterministic keys and query/mutation options beside the owner.
7. Export through the required public API.
8. Render loading, retryable error, empty and success states.
9. Add cache invalidation/update behavior for mutations.
10. Run focused checks for keys, input changes and failure behavior.

## Checklist

- [ ] Ownership follows project architecture.
- [ ] Keys include every data-affecting input.
- [ ] Transport and contracts are reused.
- [ ] UI states and retry policy are complete.
- [ ] Mutation cache effects cover all consumers.

