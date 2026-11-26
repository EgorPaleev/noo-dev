# TanStack Table

## Purpose

Build typed table state and rendering with TanStack Table without imposing a
product-specific UI library or pagination contract.

## Applies when

Apply when TanStack Table is installed and selected by the project.

## Does not apply when

Do not introduce TanStack Table for simple static data or when another table
system is already documented.

## Rules

- Keep row types explicit and column definitions close to their owning view.
- Use the library's typed column helpers and rendering adapters.
- Keep loading, empty and error presentation in the owning UI layer.
- Keep server pagination and URL state in the project's data-flow owner.
- Do not assume a UI component library, CSS utility or pagination hook.

## Checklist

- [ ] Row type and columns are explicit.
- [ ] Table state belongs to the owning client component.
- [ ] Empty and failure states are rendered.
- [ ] Pagination behavior follows project data-flow rules.
- [ ] Vendor-specific presentation is delegated to project rules.
