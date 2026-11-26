# Testing Zod Schemas

Test the runtime contract owned by the schema. Avoid tests that merely restate
the implementation or lock private Zod error wording.

## Test matrix

Cover as applicable:

- the smallest valid value and representative ordinary value;
- each meaningful invalid type or format;
- boundary values immediately below, at and above a limit;
- omitted, `undefined`, `null` and defaulted values where their meanings differ;
- unknown-key behavior for object schemas;
- coercion inputs that JavaScript would interpret unexpectedly;
- input and output values for transforms, pipes and codecs;
- all discriminated-union variants and an unknown discriminator;
- async refinement success, failure and rejection behavior;
- the project's public error mapping and field paths;
- compatibility inputs retained during a migration.

Use `safeParse()` in tests when assertions need both branches without exception
control flow. Use `parse()` with an exception assertion when throwing is the
behavior under test.

```ts
const result = Schema.safeParse(candidate);

expect(result.success).toBe(false);
if (!result.success) {
  expect(result.error.issues).toEqual(
    expect.arrayContaining([
      expect.objectContaining({ path: ["field"] }),
    ]),
  );
}
```

Assert stable contract properties such as success, parsed output, issue path and
application error code. Avoid snapshotting a complete `ZodError` unless the
serialized error itself is an intentional public contract.

## Generated and randomized data

- Hand-write small fixtures for critical boundaries and failure modes.
- Use faker or property-based libraries only when already installed or
  explicitly requested; do not add them automatically.
- Validate generated fixtures with the schema before using them in unrelated
  tests so generator drift fails near its source.
- For recursive data, bound generated depth and add cycles only when the exact
  installed Zod version and application contract support them.

## Schema changes

When changing a shared schema, run focused schema tests and tests for important
consumers. Treat input widening and output narrowing separately: either can
break a caller even when the schema still compiles.
