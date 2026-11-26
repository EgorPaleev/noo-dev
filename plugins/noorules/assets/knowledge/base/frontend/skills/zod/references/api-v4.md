# Zod 4 API Decisions

Use this reference to avoid common Zod 3 assumptions. Confirm version-sensitive
behavior against the installed package and current official documentation.

## Parsing and types

- `parse()` returns parsed data or throws `ZodError`. Use it when failure is an
  exception at that boundary.
- `safeParse()` returns a discriminated success/error result. Use it for
  expected validation failure.
- Use `parseAsync()` or `safeParseAsync()` when any refinement or transform is
  async.
- `z.infer<typeof Schema>` and `z.output<typeof Schema>` describe parsed output.
  Use `z.input<typeof Schema>` when preprocessing, transforms or codecs change
  the input type.
- Avoid explicit safe-parse return annotations when inference is sufficient. If
  an exported annotation is required, use the installed Zod 4 public type such
  as `z.ZodSafeParseResult<T>`, not Zod 3's `SafeParseReturnType`.

## Schemas and composition

- `z.object()` strips unknown keys. Use `z.strictObject()` to reject them or
  `z.looseObject()` to preserve them when the contract requires that behavior.
- `z.coerce.boolean()` uses JavaScript `Boolean()` semantics, so the non-empty
  string `"false"` becomes `true`. Use `z.stringbool()` for configurable
  string-to-boolean parsing.
- Use `z.number()` for ordinary finite numbers, `z.int()` for safe integers,
  and `z.float32()` or `z.float64()` for the corresponding ranges. There is no
  public `z.float()` constructor.
- Prefer `z.enum()` for string arrays, enum-like objects and TypeScript enums.
  `z.nativeEnum()` still exists in Zod 4 but is deprecated.
- Prefer documented top-level string formats such as `z.email()`, `z.uuid()` and
  `z.url()` in new Zod 4 code. Chained string-format methods may remain for
  compatibility and should not be described as already removed.
- For functions, use the documented object configuration:

  ```ts
  const Predicate = z.function({
    input: [z.string()],
    output: z.boolean(),
  });
  ```

## Recursive schemas

Both `z.lazy(() => Schema)` and recursive object getters are supported Zod 4
techniques. Choose the form that matches existing code and produces stable
TypeScript inference.

Do not make an unqualified claim that cyclical input is always supported or
always fails:

- full Zod 4.3 and 4.4 can overflow the stack on cyclic input;
- full Zod 4.5 supports cyclic input for recursive object schemas;
- Zod Mini may require its documented memoization pattern.

If cyclic data is a real contract requirement, verify the exact installed minor
version and add a regression test.

## Refinements and transforms

- Use `.refine()` for a boolean predicate and `.superRefine()` when multiple
  targeted issues are required. Refinement callbacks should not throw.
- In `.superRefine()`, report failures with `ctx.addIssue()`.
- In a transform that must report a validation issue, follow the installed Zod
  4 API; current documented examples append to `ctx.issues` and return
  `z.NEVER`.
- Use `.pipe()` when the output of one schema must be validated by another.
- Keep transforms pure. A validated URL is still attacker-selected input and is
  not authorization to perform a network request.

```ts
const AvatarInput = z.object({ avatar: z.url() });
const parsed = AvatarInput.safeParse(input);

if (parsed.success) {
  // Perform retrieval later through the project's outbound service, which
  // owns protocol, destination, redirect, timeout and response-size policy.
  await imageService.fetch(parsed.data.avatar);
}
```

## Errors, registries and Mini

- Prefer the Zod 4 `error` parameter. The `message` parameter remains supported
  but deprecated; `required_error` and `invalid_type_error` were removed.
- Use `z.flattenError()`, `z.treeifyError()` and `z.prettifyError()` according to
  the consumer. `z.formatError()` is deprecated, not removed.
- Inspect `z.ZodIssue` from the installed package instead of copying Zod 3 issue
  codes or fields such as `invalid_string`, `invalid_enum_value` or `received`.
- Add registry metadata with `registry.add(schema, metadata)` or
  `schema.register(registry, metadata)`. A registry does not expose
  `registry.register(...)`.
- Prefer the documented `zod/mini` import for new bundle-sensitive code. Other
  exported compatibility paths, including `zod/v4/mini`, are not a reason to
  hard-code obsolete bundle-size or feature claims; measure the actual bundle
  and inspect the installed exports.

Official references:

- https://zod.dev/api
- https://zod.dev/error-formatting
- https://zod.dev/metadata
- https://zod.dev/packages/mini
