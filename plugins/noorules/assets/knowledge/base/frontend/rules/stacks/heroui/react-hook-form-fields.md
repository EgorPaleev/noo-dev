# HeroUI React Hook Form Fields

## Purpose

Build accessible, typed field adapters between HeroUI and React Hook Form
without leaking form mechanics into every consuming form.

## Applies when

Apply when compatible versions of `@heroui/react` and `react-hook-form` are
installed and the project explicitly selected this integration.

## Does not apply when

Do not add React Hook Form for simple native forms, wrap uncontrolled HeroUI
components without need or assume APIs from another HeroUI major version.

## Rules

- Follow the official-source policy in [HeroUI
  Components](components.md), then verify the installed component contract
  before implementing slots, controlled values or validation props.
- Reuse the project's existing field adapters and naming conventions before
  creating another abstraction.
- Type the form owner with `FieldValues` and the field name with `Path` or the
  project's stricter equivalent.
- Derive vendor props from the component type and omit props owned by the form
  adapter, including `name`, `value`, `onChange`, `onBlur` and composed
  `children` when applicable.
- Use `Controller` only for components that require controlled integration and
  obtain the form control through the project's documented boundary.
- Forward `name`, `onBlur`, the controlled value and validation state to the
  HeroUI primitive according to its installed-version API.
- Define conversions between form values and HeroUI values explicitly. Do not
  conflate `null`, `undefined`, an empty string, zero or `false`.
- Render an accessible label or accessible-name alternative. Render validation
  error before optional description when both occupy the same feedback slot.
- Forward rest props only when the wrapper intentionally preserves the vendor
  contract and cannot override form-owned props.
- Keep domain validation and form schemas in the consuming slice; shared field
  adapters remain business-agnostic.

## Checklist

- [ ] Installed HeroUI and React Hook Form APIs were verified.
- [ ] Generic field names are type-safe.
- [ ] Form-owned props cannot be overridden accidentally.
- [ ] Empty, null and falsy conversions are explicit.
- [ ] Labels, errors and descriptions remain accessible.
- [ ] The adapter contains no domain validation or business behavior.
