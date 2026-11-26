# Component UI Library

## Purpose

Use an installed component library consistently without coupling reusable rules
to a specific vendor.

## Applies when

Apply when the project has selected a component UI library.

## Does not apply when

Do not assume a vendor, styling system, variant API or class-merging utility
that is not documented by the project.

## Rules

- Verify APIs against documentation for the installed library version.
- Prefer existing project wrappers and primitives before adding a parallel
  abstraction.
- Keep vendor-specific imports and variants consistent with project context.
- Apply the selected frontend component rule for interaction states and
  accessibility; it remains the canonical owner of those invariants.
- Reuse design tokens and the documented class/style composition utility.
- Keep product-specific wrappers, notification patterns and modal registries in
  project rules.

## Checklist

- [ ] The library and version are installed.
- [ ] Existing wrappers were inspected.
- [ ] The selected frontend component checklist was applied.
- [ ] Styling uses project tokens and utilities.
- [ ] No unselected vendor convention was introduced.
