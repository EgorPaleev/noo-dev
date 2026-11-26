# Zod Validation

## Purpose

Use Zod schemas at trust boundaries while keeping schemas close to the contract
they validate.

## Applies when

Apply when `zod` is installed and selected for runtime validation.

## Does not apply when

Do not add Zod to a project that uses another validator. Do not validate
already trusted internal values repeatedly without a boundary reason.

## Rules

- Validate untrusted values at the first boundary that relies on their shape.
- Keep API, domain and form schemas separate when they represent different
  contracts.
- Infer TypeScript types from schemas when the schema owns the runtime contract.
- Place schemas with the slice or module that owns the validated contract.
- Use safe parsing when validation failure is an expected result.
- Map validation issues to the project's public error and UI contracts.
- Avoid coercion that silently accepts ambiguous or unsafe input.
- Do not expose raw internal validation details when the public contract is
  intentionally stable.

## Checklist

- [ ] The schema owns a real trust boundary.
- [ ] Placement matches contract ownership.
- [ ] Inferred and declared types cannot drift.
- [ ] Coercion and defaults are intentional.
- [ ] Public validation errors follow project rules.

