# Adding a Table

## Purpose

Add a typed TanStack Table view while preserving the project's data, UI and
pagination ownership.

## Applies when

Apply when the `tanstack-table` preset is selected.

## Does not apply when

Do not use this workflow for static lists, a different table system or a
project-specific table contract that supersedes it.

## Steps

1. Read project data-flow, UI and pagination rules.
2. Inspect a sibling table and its row/column ownership.
3. Define or reuse the row contract and typed columns.
4. Create the table state in the owning client component.
5. Render headers and cells through the installed library adapter.
6. Add loading, empty, error and pagination behavior required by the project.
7. Run focused checks for row types, state transitions and pagination inputs.

## Checklist

- [ ] Column and row ownership are explicit.
- [ ] A sibling ownership pattern was inspected before adding table state.
- [ ] Empty and error states are accessible.
- [ ] Focused checks cover the selected pagination transitions.
- [ ] Project UI conventions are applied separately.
