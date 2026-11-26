# MUI Styling and Theme

## Purpose

Choose the narrowest maintainable Material UI styling mechanism and preserve
the consuming project's theme contract.

## Applies when

Apply when `@mui/material` is installed, the `mui` preset is selected and a
task changes Material UI styling, responsive behavior or theme configuration.

## Does not apply when

Do not replace another selected styling system or invent design tokens, theme
structure, color modes or global defaults that the project does not own.

## Rules

- Inspect the current theme provider, token definitions, style organization and
  nearby components before choosing a styling mechanism.
- Translate the approved design source into semantic palette, typography,
  shape, spacing and component tokens. Preserve intentional contrast pairs and
  interactive states instead of treating raw design values as unrelated CSS.
- Follow the official customization guide for the installed major, discovered
  through the version-aware documentation process in [MUI
  Components](components.md): use `sx` for a local instance override,
  `styled` for a reusable styled component, theme `components` for
  application-wide defaults and overrides, and `GlobalStyles` only for
  intentional global rules.
- Split styles by ownership and reuse rather than an arbitrary component or
  line-count threshold.
- Prefer documented theme tokens for product design decisions. Keep deliberate
  intrinsic CSS values when they do not represent a reusable design token.
- Type extracted styles with the installed `SxProps<Theme>` contract or
  `satisfies` where it preserves useful inference. Verify the contract in the
  version-matched official `sx` guide and installed types. Account for arrays
  and callbacks when accepting and composing an `sx` prop.
- Pass a theme callback as the complete `sx` value when theme access is needed;
  do not use deprecated callbacks as individual property values.
- Use breakpoint-responsive values for visual adaptation. Keep DOM-dependent
  behavior and accessibility semantics out of CSS-only breakpoints.
- Prefer inline CSS custom properties for highly dynamic values that would
  otherwise cause a new `sx` style object to be inserted repeatedly.
- Keep palette, typography and custom theme keys type-safe through the
  installed version's module-augmentation contract. Do not use the reserved
  private `theme.vars` key for project extensions.
- Keep substantial palette, typography and component override definitions in
  separately owned typed modules when that matches the project's organization.
  Type component entries through `Components["MuiComponent"]` or the installed
  version's equivalent instead of maintaining parallel handwritten contracts.
- Create or memoize derived themes at the provider boundary instead of creating
  a new theme during every component render.
- Keep theme overrides aligned with public component names and slots. Avoid
  unstable generated class selectors and document intentional global changes.
- Adapt the neutral [MUI Theme Customization
  Reference](../../../examples/mui/theme-customization.md) when a task introduces
  a project theme, custom tokens or reusable component overrides.

## Checklist

- [ ] The styling mechanism matches the scope of the change.
- [ ] Existing tokens, theme types and style organization were preserved.
- [ ] Design values have semantic names and intentional contrast relationships.
- [ ] Extracted and composed `sx` values remain type-safe.
- [ ] Responsive and dynamic styles use the appropriate MUI mechanism.
- [ ] Theme creation and global overrides have stable ownership.
- [ ] No arbitrary file threshold or project-specific token was introduced.
