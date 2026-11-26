# TypeScript Documentation Comments

## Purpose

Keep TypeScript API documentation brief, useful and close to the contract it
explains without restating types or implementation details.

## Applies when

Apply when TypeScript is configured, the project selects the
`typescript-doc-comments` preset, and an agent creates or substantially changes
a public API or non-obvious contract.

## Does not apply when

Do not require docblocks for obvious local callbacks, generated or vendor code,
or declarations governed by a different project convention. Do not perform a
repository-wide documentation backfill unless it is explicitly requested.

## Rules

- Inspect project instructions, configured documentation or lint tooling, and
  nearby docblocks before choosing wording or tags. Write docblock prose in
  Russian by default; follow an explicit project-owned language convention when
  it requires another language, and keep code identifiers unchanged.
- Use `/** ... */` docblocks for exported functions, hooks and components,
  public methods, and internal contracts with non-obvious constraints or side
  effects.
- Start with a short summary of responsibility and observable behavior. Explain
  information that the declaration and TypeScript types do not already convey.
- Use one `@param name - description` block for a parameter when its semantics,
  units, constraints, default or nullable behavior need explanation. Do not
  repeat its TypeScript type, and do not use `@params`.
- Use `@returns` when the meaning, fallback or absence behavior of the result is
  not obvious. Do not add `@returns JSX` or another statement that only repeats
  the signature.
- Use `@throws` only for caller-relevant exceptions that are part of the
  contract. Use `@typeParam`, `@remarks` and `@example` only when they add
  information and are supported by the project's documentation tooling.
- For an exported React component, describe its UI responsibility and document
  non-obvious properties beside their fields in the exported props type. Do not
  add a content-free `@param props - Component props` block.
- For a hook, document relevant runtime boundaries, side effects,
  subscriptions, cache or identity guarantees, and the contract of returned
  helpers when they are not evident from types.
- Keep documentation next to its declaration and update or remove it whenever
  behavior changes. Never leave a stale description or placeholder tag.

### Example

```ts
/**
 * Предоставляет доступ для чтения текущих параметров URL.
 *
 * @returns Методы, связанные с текущим адресом браузера.
 */
export const useQueryParams = () => {
  const [searchParams] = useSearchParams();

  /**
   * Возвращает параметр строки запроса по ключу.
   *
   * @param key - Ключ параметра без начального вопросительного знака.
   * @returns Текущее значение или `null`, если ключ отсутствует.
   */
  const getParam = (key: string): string | null => searchParams.get(key);

  return { getParam };
};
```

### Anti-patterns

```ts
/** Получает параметр. */
const getParam = (key: string): string | null => searchParams.get(key);
```

This comment only restates the function name and omits the useful absence and
input contract, regardless of the language used.

## Checklist

- [ ] Only public or non-obvious changed contracts received new docblocks.
- [ ] The summary explains behavior that names and types do not already express.
- [ ] Parameter, return and exception tags add caller-relevant semantics.
- [ ] Components and hooks document their meaningful UI or runtime contract.
- [ ] Docblock prose uses Russian unless project rules explicitly require
  another language, and supported tags match project tooling.
- [ ] No stale, placeholder or bulk-generated comment was introduced.

## References

- [TSDoc `@param`](https://tsdoc.org/pages/tags/param/)
- [TSDoc `@returns`](https://tsdoc.org/pages/tags/returns/)
- [TSDoc `@throws`](https://tsdoc.org/pages/tags/throws/)
- [TSDoc tag kinds](https://tsdoc.org/pages/spec/tag_kinds/)
