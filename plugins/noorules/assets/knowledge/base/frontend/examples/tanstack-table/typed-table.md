# TanStack Table Reference

## Purpose

Provide a small, library-neutral reference for a typed TanStack Table view.

## Applies when

Apply when `@tanstack/react-table` is installed and the project selected the
`tanstack-table-reference` preset.

## Does not apply when

Do not use this reference for a static list, a different table library, or to
choose a UI library, data transport, pagination strategy or file layout.

## Reference

```tsx
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";

type Row = {
  id: string;
  name: string;
};

const column = createColumnHelper<Row>();

const columns = [
  column.accessor("name", {
    header: "Name",
    cell: (info) => info.getValue(),
  }),
];

export function DataTable({ rows }: { rows: Row[] }) {
  // TanStack Table exposes function fields that React Compiler cannot memoize.
  // eslint-disable-next-line react-hooks/incompatible-library
  const table = useReactTable({
    columns,
    data: rows,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
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
  );
}
```

## Adaptation notes

- Replace `Row`, columns and markup with the owning view and installed UI
  adapter.
- Read the selected TanStack Table and project UI rules before adapting the
  example; they remain the canonical owners of state, accessibility and
  pagination behavior.

## Checklist

- [ ] Row type and column definitions are explicit.
- [ ] Columns and table state have one owning view.
- [ ] The installed UI adapter renders headers and cells accessibly.
- [ ] Project data and pagination conventions are applied separately.
