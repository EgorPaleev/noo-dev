# Zod Reference

## Purpose

Provide small examples of separate Zod contracts for form input and untrusted
query input.

## Applies when

Apply when `zod` is installed and the project selected the `zod-reference`
preset.

## Does not apply when

Do not use this reference to define a project's public error payload, API
response format, default limits or business validation policy.

## Reference

```ts
import { z } from "zod";

export const editItemSchema = z.object({
  name: z.string().trim().min(1).max(120),
});

export type EditItemValues = z.infer<typeof editItemSchema>;

export const listQuerySchema = z.object({
  page: z.coerce.number().int().positive(),
  search: z.string().trim().optional(),
});

export type ListQuery = z.infer<typeof listQuerySchema>;
```

## Adaptation notes

- Replace fields, limits and messages with the owning project contract.
- Read the selected Zod rule before adapting the example; it remains the
  canonical owner of boundary, coercion and error-mapping invariants.

## Checklist

- [ ] Each schema protects a real trust boundary.
- [ ] Form and transport contracts are not conflated.
- [ ] Coercion, optionality and defaults are intentional.
- [ ] Inferred types cannot drift from runtime validation.
