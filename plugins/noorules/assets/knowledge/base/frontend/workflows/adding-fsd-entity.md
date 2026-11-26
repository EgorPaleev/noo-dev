# Adding an FSD Entity

## Purpose

Decide whether a stable reusable domain boundary justifies an FSD entity before
creating one.

## Applies when

Apply when the project uses FSD and a task proposes a new entity or extraction
to the entities layer.

## Does not apply when

Do not create an entity merely because an API resource, DTO or database table
exists.

## Steps

1. Read project FSD deviations and inspect current consumers.
2. Confirm current reuse across independent higher-layer consumers or another
   explicit project criterion.
3. Keep single-use or unstable logic in its consuming slice.
4. Reject generic CRUD, session infrastructure and raw transport types unless
   project rules explicitly assign them to entities.
5. Choose an isolated domain boundary that avoids sibling cross-imports.
6. Create only required segments and domain-named files.
7. Define a minimal public API and any required runtime-specific entry.
8. Update consumers through public imports.
9. Run architecture, type and focused behavior checks.

## Checklist

- [ ] Current reuse or a project override justifies extraction.
- [ ] The boundary is domain-focused and isolated.
- [ ] No empty segment was created.
- [ ] Public API and import direction are valid.
- [ ] Existing consumers still pass checks.

