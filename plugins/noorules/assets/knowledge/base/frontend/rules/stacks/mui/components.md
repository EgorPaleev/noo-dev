# MUI Components

## Purpose

Use installed Material UI components consistently without assuming an API from
another major version or bypassing project-owned wrappers.

## Applies when

Apply when `@mui/material` is installed and the project selected the `mui`
preset.

## Does not apply when

Do not assume Material UI in an unselected project or apply these rules to MUI
X packages, which have independent versions and component contracts.

## Rules

- Before using a version-sensitive API, read the installed `@mui/material`
  major from package metadata and the lockfile. Treat installed public exports
  and TypeScript types as the exact local API contract.
- Consult only the matching official Material UI documentation version. Resolve
  its domain from the official [version
  index](https://mui.com/material-ui/getting-started/versions/), then use that
  domain's `/material-ui/llms.txt` index to discover the relevant guide and API
  reference. For example, a v7 project uses the official [v7 documentation
  index](https://v7.mui.com/material-ui/llms.txt), not the unversioned latest
  documentation.
- For a component task, check both its version-matched usage guide and API
  reference when available. Do not copy props, slots, imports or examples from
  a different major version. If the documentation disagrees with installed
  public types or exports, follow the installed contract and report the
  mismatch instead of guessing.
- Use migration documentation only when the task changes the installed major
  version or evaluates such a migration. The official [v7 upgrade
  guide](https://v7.mui.com/material-ui/migration/upgrade-to-v7/) applies to a
  migration to v7, not to routine v7 component work.
- Follow the project import convention and use only public package exports.
  Top-level imports and supported component entry points are valid; private
  multi-level deep imports are not.
- Prefer existing project wrappers, provider composition and shared primitives
  before importing a vendor component directly or creating a parallel wrapper.
- Apply the selected component UI rule for interaction states, accessibility
  and ownership; it remains the canonical owner of vendor-neutral invariants.
- Use the installed version's slots and `slotProps` contract. Do not copy a
  deprecated `*Props` customization API or slot name from another major.
- For Material UI v7, follow the official [v7 Grid
  contract](https://v7.mui.com/material-ui/react-grid/) and use `Grid` with `size`
  and `offset`. Do not introduce removed `Grid2` or `item`, or pass legacy item
  sizes such as `xs` and `sm` directly instead of through `size`.
- Treat layout `Grid` and MUI X data grids as different components. Do not add
  an MUI X dependency to implement an ordinary responsive layout.
- Preserve accessible names, label-control associations, descriptions and
  validation relationships. Provide stable IDs when server rendering or
  hydration makes generated associations insufficient.
- Keep routing adapters, notification APIs, modal registries, theme values and
  product-specific component defaults in project-owned rules.

## Checklist

- [ ] The installed Material UI major, public types and exports were checked.
- [ ] Guides and API references came from the matching official version.
- [ ] Imports use public exports and match the project convention.
- [ ] Existing wrappers and provider composition were reused where applicable.
- [ ] Slots, responsive props and events match the installed major version.
- [ ] Accessible naming, state and feedback remain connected.
- [ ] No MUI X or project-specific contract was introduced implicitly.
