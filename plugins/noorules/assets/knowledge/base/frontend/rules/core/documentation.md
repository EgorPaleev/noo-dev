# Documentation Maintenance

## Purpose

Keep agent documentation compact, non-duplicative, discoverable and backed by
observed engineering needs.

## Applies when

Apply when adding, splitting, merging, reviewing or deprecating durable
instructions, workflows, checklists and skills.

## Does not apply when

Do not turn one-off implementation details, temporary workarounds, product
business logic or framework documentation into shared rules.

## Rules

- Search existing rules before creating a new owner.
- Prefer extending one clear owner over repeating guidance in another file.
- Require either an explicit documentation request or evidence from repeated
  implementations, tasks or review feedback.
- Keep stable invariants in rules, ordered procedures in workflows and final
  verification in checklists.
- Put concrete product paths, components, endpoints and security contracts in
  project documentation.
- State applicability, exclusions and required dependencies.
- Update incoming links, indexes and task routing after moving content.
- Deprecate versioned identifiers before removal.

## Checklist

- [ ] The content has one owner.
- [ ] Shared, stack and project scope were classified explicitly.
- [ ] No project detail leaked into reusable modules.
- [ ] Links and catalog entries were updated.
- [ ] The change has an appropriate SemVer impact.

