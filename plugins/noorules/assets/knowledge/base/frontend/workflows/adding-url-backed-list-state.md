# Adding URL-Backed List State

## Purpose

Add shareable filters, sorting or pagination to a React list without creating a
second source of truth.

## Applies when

Apply when the project selected React URL query state and a list page needs
navigable state.

## Does not apply when

Do not use this workflow for transient presentation state or for a project that
uses a different documented state owner.

## Steps

1. Read the [React URL Query State rule](../rules/stacks/react/url-query-state.md)
   and project routing/data-flow rules.
2. Inspect the shared router adapter and one nearby URL-backed page model.
3. List every parameter, its serialized form, default, validation rule and
   dependent parameters.
4. Add or reuse adapter operations for reading one parameter and atomically
   updating several parameters without embedding domain names.
5. Parse and normalize values in the owning page or feature model.
6. Remove empty/default parameters according to the project's canonical URL
   policy and preserve unrelated parameters.
7. Reset the page when filters, sorting or page size changes.
8. Feed normalized values into request parameters and deterministic query keys.
9. Exercise direct links, browser back/forward navigation, invalid values,
   clearing filters and boundary pages.
10. Run focused type and project-required checks.

## Checklist

- [ ] Parameter contracts and defaults are explicit.
- [ ] The URL is the only durable state owner.
- [ ] Multi-parameter transitions are atomic.
- [ ] Invalid input falls back safely and canonically.
- [ ] Requests and query keys use normalized values.
- [ ] Navigation history behavior was exercised.
