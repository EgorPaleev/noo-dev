# Adding a React Modal or Drawer

## Purpose

Add a typed React overlay while preserving local ownership, registry boundaries
and submission lifecycle behavior.

## Applies when

Apply when the project selected the React modal-manager pattern and a task adds
or changes a modal, drawer or alert dialog.

## Does not apply when

Do not introduce a global manager when local component state is sufficient or
when the project documents a different overlay architecture.

## Steps

1. Read the project UI rules and the [React Modal Manager
   rule](../rules/stacks/react/modal-manager.md).
2. Inspect the existing host, manager public API and two nearby overlays when
   available.
3. Resolve the owning page, feature or widget and choose modal, drawer or alert
   dialog from the interaction requirements.
4. Choose local component opening by default. Choose a registry name only when
   independent consumers require stable cross-boundary access.
5. Define the typed payload and concrete component props using the existing
   manager contract.
6. Implement UI, validation and mutations in the owning slice; keep the shared
   manager generic.
7. For a registry entry, update its payload map and application registry in the
   same change.
8. Keep the overlay open and preserve input on recoverable failure; close or
   replace it only after the documented success condition.
9. Verify focus handling, accessible naming, escape/backdrop behavior and
   pending/disabled/error states with the installed component library.
10. Run focused type, interaction and project-required checks.

## Checklist

- [ ] Local versus registry ownership is justified.
- [ ] Payload and component props agree at compile time.
- [ ] Product behavior remains outside shared infrastructure.
- [ ] Success and recoverable failure behavior are explicit.
- [ ] Accessibility and relevant UI states were exercised.
