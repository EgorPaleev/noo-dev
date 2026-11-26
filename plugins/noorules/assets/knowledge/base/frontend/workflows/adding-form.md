# Adding a Form

## Purpose

Add a React Hook Form form with optional Zod validation and the project's
approved mutation transport.

## Applies when

Apply when React Hook Form is selected; apply Zod steps only when Zod is also
selected.

## Does not apply when

Do not add these libraries to a project or simple form that does not need them.

## Steps

1. Read project UI, form, validation and mutation rules.
2. Inspect existing field wrappers, resolver setup and submit patterns.
3. Define the form value contract in the owning slice.
4. Add a schema only when runtime validation is required and the validator is
   installed.
5. Initialize form state and integrate fields through existing wrappers.
6. Submit through the approved project transport.
7. Keep boundary validation authoritative.
8. Render invalid, pending, success and error states without losing user input
   on recoverable failure.
9. Add focused validation and submission checks.

## Checklist

- [ ] Installed dependencies and wrappers were verified.
- [ ] Form and boundary contracts are not conflated.
- [ ] The approved submission path was exercised through focused checks.
- [ ] All relevant states are rendered.
- [ ] Recoverable failures preserve user work.
