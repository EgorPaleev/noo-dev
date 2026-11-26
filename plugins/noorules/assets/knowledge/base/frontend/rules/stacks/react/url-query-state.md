# React URL Query State

## Purpose

Use the URL as the canonical source for shareable list filters, sorting and
pagination while isolating router-specific navigation mechanics.

## Applies when

Apply when a React page intentionally exposes state through query parameters
and the installed router provides browser search-parameter navigation.

## Does not apply when

Do not put transient UI state, secrets, large payloads or non-serializable
values in the URL. Do not add a router dependency to code that does not need
navigable state.

## Rules

- Keep router-specific read/write mechanics in a shared adapter with a small
  project-owned API.
- Parse, validate and normalize domain values in the owning page or feature
  model, not in the generic adapter.
- Treat the current URL as the source of truth; do not mirror the same state in
  a client store or long-lived component state.
- Update related parameters atomically so observers never receive an invalid
  intermediate combination.
- Reset dependent pagination when filters, sorting or page size changes.
- Remove empty and documented default values when a canonical compact URL is
  desired; distinguish absence from meaningful falsy values such as `0` or
  `false`.
- Preserve unrelated query parameters unless the owning workflow explicitly
  replaces the entire query string.
- Choose push versus replace intentionally. Prefer replace for rapid filter
  synchronization that should not create one history entry per edit.
- Keep framework navigation options, such as scroll behavior, inside the
  adapter contract rather than leaking them into domain parsing.
- Derive request inputs from normalized URL state and include them in the
  owning query key.

## Checklist

- [ ] URL-backed state is shareable and serializable.
- [ ] Router mechanics and domain parsing have separate owners.
- [ ] Related updates are atomic and preserve unrelated parameters.
- [ ] Filter and page-size changes reset dependent pagination.
- [ ] Empty, default and falsy values have explicit semantics.
- [ ] Query keys use normalized URL-derived inputs.
