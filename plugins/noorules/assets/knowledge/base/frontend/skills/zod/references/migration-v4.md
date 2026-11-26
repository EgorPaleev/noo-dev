# Migrating to Zod 4

Read this reference only for an explicit migration or when nearby code contains
deprecated Zod 3 patterns. Preserve behavior before replacing syntax.

## Establish the baseline

1. Read the installed `zod/package.json`, lockfile and import paths.
2. Find schema consumers, inferred types, error mappers, custom error maps,
   tests, generated JSON Schema and framework adapters.
3. Record current parsing, coercion, unknown-key, default and error behavior.
4. Check ecosystem packages for Zod 4 compatibility. Do not upgrade them or
   Zod without explicit authorization.

## API changes

- Replace `required_error` and `invalid_type_error` with one `error` function
  that branches on the issue input when distinct messages are required.
- Replace schema-level `errorMap` configuration with `error`. Preserve the
  precedence and return `undefined` when a lower-priority error map should run.
- Prefer `error` over deprecated `message`, but do not claim existing `message`
  usage is ignored.
- Prefer `z.enum(EnumLike)` over deprecated `z.nativeEnum(EnumLike)`.
- Prefer top-level string-format schemas for new code. Treat chained formats as
  deprecated compatibility syntax unless the installed version says otherwise.
- Replace explicit Zod 3 error types and issue-code switches with Zod 4 public
  types and the installed issue union.
- Replace old positional `z.function()` examples with the documented
  `{ input, output }` form.

Do not replace `z.lazy()` merely because the project migrated to Zod 4; it is a
supported API. A recursive getter is an alternative, not a mandatory migration.

## Compatibility verification

- Type-check every public schema and consumer affected by input/output changes.
- Test representative invalid inputs and exact public error mapping, not private
  Zod wording.
- Test unknown keys, defaults, coercion, refinements and async parsing.
- If recursive schemas can receive cyclic objects, add a version-specific test;
  behavior differs between Zod 4 minors.
- Re-run JSON Schema generation or framework adapter tests when those outputs
  are part of the project contract.

Official migration reference: https://zod.dev/v4/changelog
