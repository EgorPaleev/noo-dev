# Zustand React Modal Manager Reference

## Purpose

Illustrate a typed Zustand store that can open either a component-local modal
or an application-registered modal without storing product behavior or remote
server state.

## Applies when

Apply when `react` and `zustand` are installed, the project already needs an
application-level modal manager, and the
`react-modal-manager-zustand-reference` preset is selected.

## Does not apply when

Do not introduce this store for a modal owned by one component, or when the
project uses another overlay manager. The example does not select a UI library
or prescribe repository paths.

## Reference

Define the generic manager contract and keep the payload map open for
application-level augmentation:

```tsx
import type { ComponentType } from "react";

// Extended only by the application registry.
// eslint-disable-next-line @typescript-eslint/no-empty-object-type
export interface ModalPayloadMap {}

export type ModalName = keyof ModalPayloadMap;

type PayloadArgs<Payload> = undefined extends Payload
  ? [payload?: Payload]
  : [payload: Payload];

export type ModalProps<Payload> = {
  isOpen: boolean;
  onClose: () => void;
  payload: Payload;
};

export type ModalComponent<Payload> = ComponentType<ModalProps<Payload>>;

export type ModalPayloadArgs<Name extends ModalName> = PayloadArgs<
  ModalPayloadMap[Name]
>;

export type LocalModalPayload<Component> =
  Component extends ModalComponent<infer Payload> ? Payload : never;

export type LocalModalPayloadArgs<Component> = PayloadArgs<
  LocalModalPayload<Component>
>;

export type ModalRegistry = {
  [Name in ModalName]: ModalComponent<ModalPayloadMap[Name]>;
};
```

Store only the active overlay identity and payload. The public overloads make
required payloads mandatory and payload-free modals callable without a
placeholder argument:

```ts
import { create } from "zustand";

import type {
  LocalModalPayloadArgs,
  ModalComponent,
  ModalName,
  ModalPayloadArgs,
} from "./modal-contract";

type RegistryEntry = {
  source: "registry";
  target: ModalName;
  payload: unknown;
};

type LocalEntry = {
  source: "local";
  target: unknown;
  payload: unknown;
};

type ModalEntry = RegistryEntry | LocalEntry;

type OpenModal = {
  <Name extends ModalName>(
    target: Name,
    ...payload: ModalPayloadArgs<Name>
  ): void;
  <Component>(
    target: Component,
    ...payload: LocalModalPayloadArgs<Component>
  ): void;
};

type ModalStore = {
  entry: ModalEntry | null;
  open: OpenModal;
  close: () => void;
  updatePayload: (payload: unknown) => void;
};

export const useModalStore = create<ModalStore>((set) => ({
  entry: null,
  open: ((target: unknown, ...payload: [unknown?]) => {
    set({
      entry:
        typeof target === "string"
          ? { source: "registry", target: target as ModalName, payload: payload[0] }
          : { source: "local", target, payload: payload[0] },
    });
  }) as OpenModal,
  close: () => set({ entry: null }),
  updatePayload: (payload) =>
    set((state) => ({
      entry: state.entry ? { ...state.entry, payload } : null,
    })),
}));

export const modal = {
  open: useModalStore.getState().open,
  close: () => useModalStore.getState().close(),
  updatePayload: (payload: unknown) =>
    useModalStore.getState().updatePayload(payload),
};
```

The host resolves registered components but remains unaware of their product
behavior:

```tsx
import type {
  ModalComponent,
  ModalPayloadMap,
  ModalRegistry,
} from "./modal-contract";
import { useModalStore } from "./modal-store";

export function ModalHost({ registry }: { registry: ModalRegistry }) {
  const entry = useModalStore((state) => state.entry);
  const close = useModalStore((state) => state.close);

  if (!entry) return null;

  const Component = (
    entry.source === "registry"
      ? registry[entry.target as keyof ModalPayloadMap]
      : entry.target
  ) as ModalComponent<unknown> | undefined;

  return Component ? (
    <Component isOpen onClose={close} payload={entry.payload} />
  ) : null;
}
```

Compose product-owned registrations at the application boundary:

```tsx
import { EditItemModal } from "<owning-slice>";
import type { ModalRegistry } from "<modal-manager>";

declare module "<modal-contract-module>" {
  interface ModalPayloadMap {
    editItem: { itemId: string };
  }
}

export const modalRegistry = {
  editItem: EditItemModal,
} satisfies ModalRegistry;
```

## Adaptation notes

- Follow the [React Modal Manager
  rule](../../rules/stacks/react/modal-manager.md) for ownership and lifecycle
  semantics; it remains the canonical owner.
- Match the installed Zustand version and the project's selector conventions.
- Keep the casts inside generic infrastructure and preserve fully typed public
  `open` calls.
- Decide whether opening replaces the active modal, queues it or supports a
  stack, then document that project-level behavior.
- Mount one host through the project's application composition boundary and
  keep concrete modal imports out of shared infrastructure.

## Checklist

- [ ] `zustand` is already installed and selected intentionally.
- [ ] Local and registry calls enforce their payload types.
- [ ] The store contains only overlay lifecycle state.
- [ ] The application owns concrete registry composition.
- [ ] The installed UI library supplies accessible modal behavior.
