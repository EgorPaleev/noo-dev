# Migrating from Zustand 4 to 5

Read this reference only for an explicit migration. First inspect the installed
v4 version, imports, equality behavior, persist configuration, `setState`
replacement calls, SSR integration and tests. Preserve observable behavior
before changing syntax.

## Dependency baseline

- Prefer updating to the latest compatible Zustand 4 release before the major
  migration so deprecation warnings are visible.
- Zustand 5 requires React 18 or newer for React bindings and TypeScript 4.5 or
  newer for package types.
- `createWithEqualityFn` and `useStoreWithEqualityFn` move equality-aware React
  behavior to `zustand/traditional` and require the
  `use-sync-external-store` peer dependency.
- Do not install or update dependencies unless the explicit migration scope
  includes package metadata and lockfile changes.

## Behavioral and API changes

- Replace removed default imports and deprecated entry points with installed v5
  named exports.
- The standard v5 `create` hook no longer accepts a custom equality function.
  Prefer stable selectors and `useShallow`; use the traditional APIs only when
  custom equality is part of the contract.
- Make every selector output stable. Inline arrays, objects or fallback
  functions that worked accidentally in v4 can produce an infinite update loop
  in v5.
- When `setState` uses `replace: true`, pass a complete state object. Update
  dynamic replace calls using `Parameters<typeof store.setState>` or an
  equivalent installed public type.
- Persist no longer writes the initial state during store creation. Explicitly
  set a generated initial value after creation when storage must receive it.
- Review removed UMD/SystemJS and ES5 outputs only when the consuming build
  depended on them.

Curried `create<State>()(initializer)` and `createJSONStorage` are not new v5
features. Do not rewrite working code merely to claim a major-version syntax
change. `createJSONStorage` is optional when its default local-storage behavior
already matches the contract.

## Verification

- Type-check every store, middleware composition, selector and public hook.
- Test stable selector output, full replacement and persisted initialization.
- Verify each storage migration from representative v4 payloads.
- For Next.js, verify per-request isolation and matching server/client initial
  state rather than adding only a hydration flag.
- Run important consumer and rendering tests before removing v4 compatibility
  code.

Official migration reference:
https://zustand.docs.pmnd.rs/reference/migrations/migrating-to-v5
