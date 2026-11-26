# TypeScript Naming and Types

## Purpose

Keep TypeScript contracts explicit and names consistent with their domain and
the consuming repository.

## Applies when

Apply when TypeScript is configured in the project.

## Does not apply when

Do not impose the examples below on generated code, external or serialized
contracts, framework-defined names, compatibility-sensitive public APIs or a
repository with a different documented naming convention. Preserve required
names at those boundaries and translate them inside project-owned code when
that improves clarity.

## Rules

- Follow the nearest project naming rules before applying generic examples.
- Apply these rules to identifiers introduced or changed by the task. Do not
  perform unrelated repository-wide renaming or silently break a public
  contract to improve a name.
- Use PascalCase for components, classes and type-level declarations.
- Use camelCase for values, functions and hooks; prefix React hooks with `use`.
- Choose intention-revealing, pronounceable and searchable names from the
  project's domain vocabulary. Include enough context to distinguish the
  concept without repeating context already supplied by its module or owner.
- Name variables with noun phrases. Use plural nouns for collections and add a
  unit such as `timeoutMs` or `sizeBytes` when the numeric unit is otherwise
  ambiguous.
- Name boolean values as predicates with `is`, `has`, `can` or `should` when
  those prefixes form a natural question. Prefer positive names such as
  `isEnabled` over double negatives such as `isNotDisabled`.
- Name functions and methods with verb phrases that describe their observable
  action or result. Do not hide I/O, mutation or another important side effect
  behind a vague or query-like name.
- Use `on<Event>` for a callback supplied by a caller and `handle<Event>` for
  the internal implementation that handles that callback. Preserve a library
  or repository convention when it intentionally uses another distinction.
- Give operation verbs stable meanings within a codebase. Distinguish
  `create` or `build`, `parse`, `format`, `to<Type>`, and
  `get`/`find`/`fetch`/`load` according to actual behavior instead of using
  them interchangeably.
- Use one term for one concept across related APIs. Do not use synonyms for the
  same operation or reuse one broad word for concepts that change for different
  reasons.
- Replace generic names such as `data`, `info`, `value`, `item`, `object`,
  `manager`, `helper`, `process` and `do` when a domain or behavioral role is
  available. A short generic name is acceptable in a tiny scope where the type
  and operation make its meaning immediate.
- Avoid unexplained abbreviations, type encodings and redundant affixes such as
  `strName`, `itemsArray` or `userObject`. Keep established domain acronyms and
  their casing consistent with project rules.
- Reserve one-letter names for conventional indices, coordinates, mathematical
  expressions or equally small scopes. Rename identifiers that require the
  reader to remember a private mental mapping.
- Name files for the domain responsibility, not broad buckets such as
  `types.ts`, `utils.ts` or `helpers.ts`.
- Prefer inferred local types and explicit exported boundary types.
- Model unknown input as `unknown` and narrow it; do not use `any` as an escape
  hatch.
- Keep request, response and domain types distinct when their semantics differ.
- Avoid unsafe casts that bypass runtime validation.
- Match the repository's chosen filename casing and suffix conventions.

Compact examples:

```tsx
// Avoid: the name hides meaning, unit and side effects.
const t = 5000;
const archive = record.status === "archived";
async function processData(value: unknown) {
  return client.post(value);
}

// Prefer: names reveal role, state and observable behavior.
const retryDelayMs = 5000;
const isArchived = record.status === "archived";
async function submitRecord(payload: unknown) {
  return client.post(payload);
}

type SearchProps = {
  onSearchSubmit: (query: string) => void;
};

function SearchButton({ onSearchSubmit }: SearchProps) {
  const handleSearchSubmit = () => onSearchSubmit("normalized query");
  return <button type="button" onClick={handleSearchSubmit}>Search</button>;
}
```

## Checklist

- [ ] Names describe domain responsibility.
- [ ] Variables, collections, units and boolean predicates communicate their
      roles without a mental mapping.
- [ ] Function and method names reveal actions, results and important side
      effects.
- [ ] Callback props and internal handlers follow the project `on`/`handle`
      distinction.
- [ ] Operation verbs and domain terms are used consistently.
- [ ] Generic or abbreviated names remain only where their small scope makes
      the meaning immediate.
- [ ] No unrelated identifier or compatibility-sensitive contract was renamed.
- [ ] Exported boundaries are typed.
- [ ] Unknown data is narrowed or validated.
- [ ] No new unnecessary `any` or unsafe cast was introduced.
- [ ] Filename conventions match project context.
