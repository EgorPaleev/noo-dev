# React URL Query State Adapter Reference

## Purpose

Illustrate one small query-parameter adapter contract for Next.js App Router
and React Router.

## Applies when

Apply only when the corresponding router is installed and the project selected
the React URL query state reference.

## Does not apply when

Do not copy both adapters into one project or use this reference to decide
domain parameter names, defaults or validation.

## Reference

The domain-facing contract is intentionally small:

```ts
type QueryValue = string | null | undefined;

type QueryStateAdapter = {
  getParam(key: string): string | null;
  setParam(key: string, value: QueryValue): void;
  setParams(values: Record<string, QueryValue>): void;
};
```

Next.js App Router adapter:

```tsx
"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";

type QueryValue = string | null | undefined;

export function useQueryParams() {
  const pathname = usePathname();
  const router = useRouter();
  const searchParams = useSearchParams();

  const setParams = (values: Record<string, QueryValue>) => {
    const next = new URLSearchParams(searchParams);
    for (const [key, value] of Object.entries(values)) {
      value == null || value === "" ? next.delete(key) : next.set(key, value);
    }
    const query = next.toString();
    router.replace(query ? `${pathname}?${query}` : pathname, { scroll: false });
  };

  return {
    getParam: (key: string) => searchParams.get(key),
    setParam: (key: string, value: QueryValue) => setParams({ [key]: value }),
    setParams,
  };
}
```

React Router adapter:

```tsx
import { useSearchParams } from "react-router";

type QueryValue = string | null | undefined;

export function useQueryParams() {
  const [searchParams, setSearchParams] = useSearchParams();

  const setParams = (values: Record<string, QueryValue>) => {
    setSearchParams((current) => {
      const next = new URLSearchParams(current);
      for (const [key, value] of Object.entries(values)) {
        value == null || value === "" ? next.delete(key) : next.set(key, value);
      }
      return next;
    }, { replace: true });
  };

  return {
    getParam: (key: string) => searchParams.get(key),
    setParam: (key: string, value: QueryValue) => setParams({ [key]: value }),
    setParams,
  };
}
```

## Adaptation notes

- Follow the [React URL Query State
  rule](../../rules/stacks/react/url-query-state.md) for ownership and transitions.
- Adapt push/replace and scroll behavior to the consuming project.
- Keep parsing, defaults and domain parameter names outside these adapters.
- Add memoization only when measured consumers require stable identities.

## Checklist

- [ ] Only the installed router adapter is used.
- [ ] Unrelated parameters are preserved.
- [ ] Empty-value semantics match project policy.
- [ ] Domain parsing remains outside shared infrastructure.
