# Feature-Sliced Design Core

## Purpose

Apply Feature-Sliced Design with deferred extraction and explicit layer
boundaries.

## Applies when

Apply only when the project explicitly uses Feature-Sliced Design.

## Does not apply when

Do not retrofit FSD into a repository that has another documented architecture.
Do not create layers or slices for hypothetical reuse.

## Rules

- Start with minimal layers and add slices only for stable, current reuse.
- Keep single-use and uncertain code in its consuming slice.
- Follow import direction from higher layers to lower layers.
- Avoid cross-imports between same-layer slices; resolve ownership or compose
  from a higher layer.
- Keep infrastructure without business logic in shared.
- Reserve entities for reusable domain models or logic, not every API resource.
- Reserve features for reusable user interactions, not every user action.
- Do not create empty layer or segment directories.
- Record intentional deviations in project architecture.

## Checklist

- [ ] The target layer is justified by current use.
- [ ] No empty or speculative layer was created.
- [ ] Imports follow layer direction.
- [ ] Shared contains no business logic.
- [ ] Any deviation is explicit in project context.
