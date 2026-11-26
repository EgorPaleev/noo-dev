# MUI React Hook Form Fields

## Purpose

Build accessible, typed field adapters between Material UI and React Hook Form
without leaking controlled-component mechanics into every form.

## Applies when

Apply when compatible versions of `@mui/material` and `react-hook-form` are
installed and the project selected the `mui-react-hook-form` preset.

## Does not apply when

Do not add React Hook Form for a simple uncontrolled field, wrap a component
without a reuse need or infer value semantics from another MUI major version.

## Rules

- Follow the selected MUI component rule and verify the installed component's
  value, event, ref, slot and validation APIs before creating an adapter.
- Reuse the project's existing field adapters, form-provider boundary and
  naming conventions before introducing another abstraction.
- Type the form values with `FieldValues`, the field name with `Path<Values>`
  and `useFormContext` with the owning values type or a stricter project type.
- Derive vendor props from the installed component type and omit form-owned
  props such as `name`, `value` or `checked`, `defaultValue`, `onChange`,
  `onBlur`, the field ref and validation state.
- Use `Controller` only when the Material UI component needs controlled value
  integration. Prefer the project's native registration pattern when it fully
  supports the target component contract.
- Forward the controlled name, value, change, blur and focus ref through the
  exact MUI boundary. For example, a `TextField` commonly receives the RHF ref
  through `inputRef`, not the wrapper root ref.
- Define conversions explicitly for empty strings, `null`, `undefined`, zero,
  `false`, numeric input, single selection and multiple selection. Do not use a
  truthiness shortcut that changes a valid value.
- Compose an optional consumer callback only when the wrapper contract exposes
  it intentionally, and update React Hook Form in a documented order.
- Spread consumer props before form-owned props so they cannot replace the
  controlled value, handlers, ref or invalid state accidentally.
- Preserve accessible labels, IDs and descriptions. Show the validation error
  before optional helper text when both use the same feedback slot.
- Keep schemas, domain validation, option loading and product copy in the
  consuming slice; shared adapters remain business-agnostic.

## Checklist

- [ ] Installed MUI and React Hook Form APIs were verified.
- [ ] Field values and names are typed against the owning form.
- [ ] Form-owned props cannot be overridden accidentally.
- [ ] Empty, numeric, boolean and selection conversions are explicit.
- [ ] Name, blur, ref, invalid state and accessible feedback are forwarded.
- [ ] The adapter contains no domain validation or product behavior.
