# Zustand 5 API Decisions

Confirm version-sensitive behavior against the installed package and current
official documentation. Zustand 5 React bindings require React 18 or newer and
the package types require TypeScript 4.5 or newer; a consuming project may set
higher minimums.

## Store APIs and TypeScript

- `create` creates a React-bound store hook. `createStore` from
  `zustand/vanilla` creates a framework-independent store; bind it with
  `useStore` when a provider or injected store instance owns the lifecycle.
- Inspect the installed overloads before changing syntax. Current Zustand 5
  types can expose both a direct initializer and a curried form. The documented
  `create<State>()(initializer)` form is useful when annotating state and
  composing middleware, but a valid direct form is not automatically a bug.
- Export the hook, vanilla API or factory that matches the existing ownership
  boundary. Providers are optional for a module-owned client singleton but are
  required when callers must receive an isolated store instance.

## Selectors and equality

- Select the smallest value needed by a component. Primitive and stable object
  references work with the standard hook without a custom comparator.
- Zustand 5 requires stable selector output. Wrap a selector that constructs an
  array or object with `useShallow`:

  ```ts
  import { useShallow } from "zustand/shallow";

  const { count, increment } = useStore(
    useShallow((state) => ({
      count: state.count,
      increment: state.increment,
    })),
  );
  ```

- The hook returned by standard `create` does not accept `shallow` as a second
  argument. When a custom equality function is required, inspect
  `createWithEqualityFn` or `useStoreWithEqualityFn` from `zustand/traditional`
  and verify `use-sync-external-store` is installed.
- Keep fallback functions, arrays and objects outside selectors or otherwise
  memoized so unchanged state produces an equal result.

## Updating state

- `set(partial)` and `set(updater)` shallow-merge by default. Replace state only
  when that is the intended public operation.
- `setState(nextState, true)` requires a complete state in Zustand 5. Do not
  erase actions by replacing with a partial object.
- When the `replace` flag is dynamic, type the complete argument tuple from the
  installed `setState` signature instead of weakening it with casts.
- Use immutable updates unless the store is wrapped with the Immer middleware.
  Immer is an optional peer dependency and must already be installed or be
  explicitly added within task scope.

## Actions, slices and middleware

- Zustand actions may be synchronous or asynchronous. Define observable error,
  cancellation and overlap behavior according to the owning service rather
  than treating every action like a Redux reducer.
- Compute nondeterministic values before a deterministic updater when tests or
  replayability require it.
- With the slices pattern, type each slice against the combined store and apply
  middleware once when the final store is created. Do not wrap individual
  slices independently.
- Preserve middleware order and installed mutator types. Add `persist`,
  `devtools`, `subscribeWithSelector`, `combine`, `redux` or `immer` only for an
  established requirement.

Official references:

- https://zustand.docs.pmnd.rs/reference/apis/create
- https://zustand.docs.pmnd.rs/reference/apis/create-store
- https://zustand.docs.pmnd.rs/learn/guides/advanced-typescript
- https://zustand.docs.pmnd.rs/reference/migrations/migrating-to-v5
