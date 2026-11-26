# Backend-for-Frontend Boundary

## Purpose

Define data and transport responsibilities between browser code, a Next.js
Backend-for-Frontend and one or more upstream services.

## Applies when

Apply when a Next.js project explicitly selects a BFF architecture.

## Does not apply when

Do not add a BFF to a static application, a direct-client API architecture or a
project with a different trusted boundary.

## Rules

- Browser code calls the BFF rather than private upstream services.
- The BFF owns server-only credentials, upstream URL construction and the
  stable application-facing response contract.
- Validate untrusted inputs and required request-security signals before an
  unsafe side effect.
- Validate upstream responses before mapping fields that the application
  relies on.
- Attach authorization explicitly according to the project auth contract.
- Bound upstream requests with cancellation or timeouts.
- Keep private responses non-cacheable unless the project defines a safe cache
  strategy.
- Map upstream failures to a stable project-owned error contract.
- Do not expose raw upstream payloads, URLs, headers or credentials.
- Keep authentication refresh, CSRF and role rules in project documentation.

### Application-contract mapping

- Map backend-specific DTOs to application models in the BFF. Browser code
  must not know upstream field names or response shapes.
- Perform upstream field renaming, nullable or optional normalization,
  multi-endpoint aggregation, removal of unnecessary or sensitive fields, and
  contract-level type conversion in the BFF.
- Keep the resulting application DTO stable when an upstream contract changes.
  Do not move upstream-owned business decisions into the BFF merely to reshape
  their representation.

```ts
interface BackendItemDto {
  item_id: number;
  item_name: string;
  priority: number;
}

interface Item {
  id: number;
  name: string;
  priority: number;
}

const mapItem = (item: BackendItemDto): Item => ({
  id: item.item_id,
  name: item.item_name,
  priority: item.priority,
});
```

Use this flow:

```text
External backend DTO
        ↓
   BFF validation
        ↓
     BFF mapping
        ↓
Application/frontend DTO
        ↓
    Client query
        ↓
Presentation mapping
        ↓
        UI
```

### Sorting ownership

- Treat an invariant order with business meaning as part of the data contract.
  Prefer the backend when it owns and guarantees that order; otherwise sort in
  the BFF before returning the application DTO.
- Keep sorting on the client when it depends on the current screen, filter,
  user choice or another presentation state.
- Do not repeat application-wide ordering in every client query selector. For
  example, if `priority` always defines item order, apply this once in the
  backend or BFF:

```ts
const orderedItems = [...items].sort(
  (first, second) => first.priority - second.priority,
);
```

### Presentation mapping

- Keep transformations for a concrete interface on the client, including
  component props, colors, icons, CSS or UI state, card and table shapes, and
  locale-dependent date or number formatting.
- Map an application model to a component-specific shape only in the client:

```ts
const options = items.map((item) => ({
  label: item.name,
  value: item.id,
}));
```

- Do not make the BFF return `label`/`value` pairs or another component's
  presentation contract.

### Decision rule

> If a transformation answers "What should the data look like in our
> application's contract?", it belongs in the BFF. If it answers "How should
> this data appear in this interface?", it belongs in the client.

> If an array must always have the same semantic order, order it in the backend
> or BFF. If order depends on the screen, filter, user choice or UI state, order
> it in the client.

### Anti-patterns

- Returning raw backend DTOs and renaming their fields in browser query code.
- Duplicating invariant sorting in client `select` functions or components.
- Returning component-specific display shapes from the BFF.
- Formatting locale-dependent display strings before the client presentation
  boundary.

## Checklist

- [ ] The browser does not need private upstream knowledge.
- [ ] Backend DTOs are validated and mapped to a stable application contract.
- [ ] Nullable values, types, aggregation and field removal have the correct
  BFF owner.
- [ ] Invariant ordering is owned by the backend or BFF and is not duplicated.
- [ ] Screen-specific mapping and sorting remain in the client.
- [ ] Inputs and unsafe-request security are validated.
- [ ] Upstream calls are bounded.
- [ ] Errors and caching follow the project contract.
- [ ] No credential or raw upstream detail is exposed.
