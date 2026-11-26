# React Modal Manager

## Purpose

Coordinate typed modals and drawers without moving product UI or business
mutations into application infrastructure.

## Applies when

Apply when a React project uses an application-level modal manager so unrelated
components can open overlays without threading local state through the tree.

## Does not apply when

Do not add a global manager for a dialog owned and rendered by one component.
Do not require Zustand, a registry or a specific component library unless the
project has selected them.

## Rules

- Prefer component-local state for overlays whose opener and content share one
  ownership boundary.
- Keep reusable manager infrastructure in the project's shared infrastructure
  layer and mount one host from application initialization.
- Keep concrete modal UI, validation and business mutations in the page,
  feature or widget that owns the interaction.
- Open a local overlay by its typed component when no unrelated module needs a
  stable identifier.
- Add a registry identifier only when independent consumers must open the same
  overlay; keep its payload type and component registration synchronized.
- Type payload presence so required payloads cannot be omitted and overlays
  without payloads do not require placeholder values.
- Keep modal and drawer presentation inside the concrete component; the host
  resolves and renders entries but does not know product behavior.
- Define close, replace and payload-update semantics explicitly. Preserve an
  open overlay and user input after recoverable submission failure.
- Keep remote server state out of the modal store. Store only overlay identity,
  payload and UI lifecycle state there.
- Do not let shared manager modules import pages, features, widgets or domain
  entities. Perform application-level registry composition from the app layer.

## Checklist

- [ ] Local state was considered before adding a global entry.
- [ ] The concrete overlay remains with its owning use case.
- [ ] Registry names and payloads are fully typed when used.
- [ ] One application host renders the active entry.
- [ ] Failure behavior preserves recoverable user work.
- [ ] Shared infrastructure contains no product behavior or server state.
