# Adding a React Data List Page

## Purpose

Compose URL-backed filters, TanStack Query, React Hook Form and TanStack Table
into a cohesive list page without changing their canonical ownership rules.

## Applies when

Apply when the project selected the `react-data-list` preset and the requested
page needs its full installed stack.

## Does not apply when

Do not introduce these libraries for a static list, a server-only page or a
project with a different documented data-flow strategy.

## Steps

1. Read project architecture plus the selected URL state, query, form and table
   rules. Treat those documents as canonical for their invariants.
2. Inspect one nearby list page and resolve page ownership, request ownership,
   row type, filter contract and pagination response shape.
3. Define normalized URL-backed filter and pagination state in the owning page
   model. Reset pagination when dependent inputs change.
4. Add or reuse the approved request, deterministic query keys and query option
   factory at the project-selected owner.
5. Add the filter form with explicit defaults and synchronize it from URL state
   without creating a second durable source of truth.
6. Define typed columns close to the owning view and render them through the
   installed table and UI-library adapters.
7. Compose pending, background-fetching, retryable error, empty and success
   states. Disable conflicting controls during transitions when required.
8. Add pagination from normalized URL state and server response metadata; do
   not infer availability from client rows alone when pagination is server-side.
9. Wire row actions through the owning mutation and modal patterns, then update
   all affected cache scopes.
10. Exercise direct links, clearing filters, invalid URLs, page boundaries,
    request failure, empty data and mutation success/failure.
11. Run focused type, interaction and project-required checks.

## Checklist

- [ ] Each library keeps one documented owner.
- [ ] URL state is normalized and drives request/query keys.
- [ ] Forms do not become a second durable filter store.
- [ ] Server pagination uses authoritative response metadata.
- [ ] Loading, background, error, empty and success states are distinct.
- [ ] Mutations update every affected cache scope.
