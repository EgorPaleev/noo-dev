# TanStack Query Reference

## Purpose

Provide a small reference for colocated query keys, query options and mutation
cache effects.

## Applies when

Apply when `@tanstack/react-query` is installed and the project selected the
`tanstack-query-reference` preset.

## Does not apply when

Do not use this reference to choose a transport, request ownership, retry
policy or cache scope for a project.

## Reference

```tsx
import {
  keepPreviousData,
  MutationCache,
  QueryCache,
  QueryClient,
  QueryClientProvider,
  queryOptions,
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";
import { useState, type ReactNode } from "react";

type ListParams = { page: number; search?: string };
type Item = { id: string; name: string };

declare function fetchItems(params: ListParams): Promise<{ items: Item[] }>;
declare function createItem(payload: { name: string }): Promise<Item>;

export const itemQueryKeys = {
  all: ["items"] as const,
  lists: () => [...itemQueryKeys.all, "list"] as const,
  list: (params: ListParams) => [...itemQueryKeys.lists(), params] as const,
};

export const itemQueries = {
  list: (params: ListParams) =>
    queryOptions({
      queryKey: itemQueryKeys.list(params),
      queryFn: () => fetchItems(params),
      placeholderData: keepPreviousData,
    }),
};

export function useCreateItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createItem,
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: itemQueryKeys.lists() }),
  });
}

const createQueryClient = (reportError: (error: unknown) => void) =>
  new QueryClient({
    defaultOptions: {
      mutations: { retry: false },
      queries: { retry: 1, staleTime: 30_000 },
    },
    mutationCache: new MutationCache({ onError: reportError }),
    queryCache: new QueryCache({ onError: reportError }),
  });

export function QueryProvider(props: {
  children: ReactNode;
  reportError: (error: unknown) => void;
}) {
  const { children, reportError } = props;
  const [queryClient] = useState(() => createQueryClient(reportError));

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}
```

## Adaptation notes

- Replace declared transport functions, item contracts and cache scope with the
  owning project's choices.
- Replace `reportError` with the project notification or telemetry boundary and
  prevent duplicate local feedback for failures handled globally.
- Keep session-driven cache clearing in the project provider integration.
- Read the selected TanStack Query rule before adapting the example; it remains
  the canonical owner of key, retry and cache invariants.

## Checklist

- [ ] Keys are deterministic and complete.
- [ ] Components consume query option factories instead of recreating keys.
- [ ] Mutation cache effects cover affected list and detail scopes.
- [ ] Transport and retry behavior follow local policy.
