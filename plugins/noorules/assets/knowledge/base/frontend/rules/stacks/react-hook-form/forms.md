# React Hook Form

## Purpose

Keep form state, field integration and submit lifecycle cohesive when using
React Hook Form.

## Applies when

Apply when `react-hook-form` is installed and selected for the form.

## Does not apply when

Do not add React Hook Form to a simple native form or a project that has chosen
another form library.

## Rules

- Define the form value type at the owning UI or use-case boundary.
- Use the project's documented resolver only when its validation dependency is
  installed.
- Use controlled-field adapters only for components that require them.
- Keep submission through the mutation transport selected by project rules.
- Treat client validation as user feedback, not a replacement for boundary
  validation.
- Preserve user input and keep overlays open when a submission fails unless the
  product explicitly requires reset/close behavior.
- Render invalid, pending, success and error states.
- Avoid duplicating remote server state in form state after submission.

## Checklist

- [ ] Form values and defaults are typed.
- [ ] Field integration matches the component contract.
- [ ] Server-side validation still exists where required.
- [ ] Pending and failure behavior protects user input.
- [ ] The selected submit transport follows project rules.

