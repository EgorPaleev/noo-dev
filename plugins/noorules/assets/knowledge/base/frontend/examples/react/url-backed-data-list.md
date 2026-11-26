# URL-Backed React Data List Reference

## Purpose

Illustrate how normalized URL state, TanStack Query and TanStack Table can form
one server-backed list without duplicating filter or pagination ownership.

## Applies when

Apply when the project has selected the `react-data-list-reference` preset and
uses React, React Hook Form, Zod, TanStack Query v5 and TanStack Table v8 with
a compatible query parameter adapter.

## Does not apply when

Do not use this composition for a static list, client-only collection or a
project whose router, request layer or pagination contract requires a different
owner. This reference does not define API response fields or UI components for
the consuming product.

## Reference

Normalize URL values once in the owning page model. The adapter below is the
small contract illustrated by the separate router reference:

```ts
import { z } from "zod";

type QueryValue = string | null | undefined;

type QueryStateAdapter = {
  getParam(key: string): string | null;
  setParams(values: Record<string, QueryValue>): void;
};

const listStateSchema = z.object({
  page: z.coerce.number().int().positive().catch(1),
  pageSize: z.coerce.number().int().min(10).max(100).catch(20),
  search: z.string().trim().catch(""),
});

export type ListState = z.infer<typeof listStateSchema>;

export function createListState(adapter: QueryStateAdapter) {
  const state = listStateSchema.parse({
    page: adapter.getParam("page") ?? undefined,
    pageSize: adapter.getParam("pageSize") ?? undefined,
    search: adapter.getParam("search") ?? undefined,
  });

  return {
    state,
    setPage(page: number) {
      adapter.setParams({ page: String(Math.max(1, page)) });
    },
    setPageSize(pageSize: number) {
      adapter.setParams({ page: null, pageSize: String(pageSize) });
    },
    setSearch(search: string) {
      const normalized = search.trim();
      adapter.setParams({ page: null, search: normalized || null });
    },
    clearFilters() {
      adapter.setParams({ page: null, search: null });
    },
  };
}
```

Include the complete normalized state in a deterministic query option factory.
Adapt `listItems` and its response at the project-owned request boundary:

```ts
import { keepPreviousData, queryOptions } from "@tanstack/react-query";

import type { ListState } from "./list-state";

export type ItemRow = { id: string; label: string };
export type ItemPage = { rows: ItemRow[]; total: number };

declare function listItems(input: ListState): Promise<ItemPage>;

export const itemQueries = {
  all: () => ["items"] as const,
  list: (state: ListState) =>
    queryOptions({
      queryKey: [...itemQueries.all(), "list", state] as const,
      queryFn: () => listItems(state),
      placeholderData: keepPreviousData,
    }),
};
```

Compose data states and manual server pagination in the view. The router hook
is injected here to keep this example independent of Next.js or React Router:

```tsx
import { useQuery } from "@tanstack/react-query";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { itemQueries, type ItemRow } from "./item-queries";
import { createListState } from "./list-state";

const column = createColumnHelper<ItemRow>();
const columns = [
  column.accessor("label", {
    header: "Label",
    cell: (context) => context.getValue(),
  }),
];

type QueryStateAdapter = Parameters<typeof createListState>[0];

function ListFilters({
  search,
  onApply,
}: {
  search: string;
  onApply: (search: string) => void;
}) {
  const form = useForm<{ search: string }>({
    defaultValues: { search },
  });

  useEffect(() => {
    form.reset({ search });
  }, [form, search]);

  return (
    <form onSubmit={form.handleSubmit(({ search }) => onApply(search))}>
      <input {...form.register("search")} aria-label="Search" />
      <button type="submit">Apply</button>
    </form>
  );
}

export function ItemList({ adapter }: { adapter: QueryStateAdapter }) {
  const { state, setPage, setPageSize, setSearch } = createListState(adapter);
  const query = useQuery(itemQueries.list(state));
  const rows = query.data?.rows ?? [];

  // TanStack Table exposes function fields that React Compiler cannot memoize.
  // eslint-disable-next-line react-hooks/incompatible-library
  const table = useReactTable({
    columns,
    data: rows,
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
    rowCount: query.data?.total ?? 0,
    state: {
      pagination: {
        pageIndex: state.page - 1,
        pageSize: state.pageSize,
      },
    },
  });

  if (query.isPending) return <p>Loading…</p>;
  if (query.isError) {
    return <button onClick={() => query.refetch()}>Retry</button>;
  }

  return (
    <section aria-busy={query.isFetching}>
      <ListFilters search={state.search} onApply={setSearch} />

      {rows.length === 0 ? (
        <p>No results</p>
      ) : (
        <table>
          <thead>
            {table.getHeaderGroups().map((group) => (
              <tr key={group.id}>
                {group.headers.map((header) => (
                  <th key={header.id} scope="col">
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext(),
                        )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <button disabled={state.page === 1} onClick={() => setPage(state.page - 1)}>
        Previous
      </button>
      <button
        disabled={rows.length === 0 || !table.getCanNextPage()}
        onClick={() => setPage(state.page + 1)}
      >
        Next
      </button>
      <label>
        Rows per page
        <select
          value={state.pageSize}
          onChange={(event) => setPageSize(Number(event.target.value))}
        >
          {[10, 20, 50, 100].map((size) => (
            <option key={size} value={size}>{size}</option>
          ))}
        </select>
      </label>
    </section>
  );
}
```

## Adaptation notes

- Follow the [URL query state](../../rules/stacks/react/url-query-state.md),
  [TanStack Query](../../rules/stacks/tanstack-query/data-fetching.md) and
  [TanStack Table](../../rules/stacks/tanstack-table/tables.md) rules; they remain
  the canonical owners of their invariants.
- Use the [router adapter reference](url-query-state-adapters.md) only for the
  router installed by the consuming project.
- Replace neutral parameter names, request types and response mapping with the
  contracts documented in `.agents/local`; do not infer them from this example.
- When a filter form uses React Hook Form, synchronize its displayed values
  from normalized URL state and keep submission as the only URL transition.
- Add installed UI components, sorting, row actions and mutations as separate
  composition concerns.

## Checklist

- [ ] The normalized URL is the only durable list-state owner.
- [ ] Filter and page-size changes reset the page atomically.
- [ ] Query keys include every normalized request input.
- [ ] Server pagination uses authoritative total metadata.
- [ ] Pending, fetching, error, empty and success states remain distinct.
