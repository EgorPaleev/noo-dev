---
name: create-heroui-form-control
description: Create or update a typed field adapter between an installed HeroUI component and React Hook Form after resolving the exact HeroUI API, controlled value semantics, generic field-name contract, validation feedback, accessibility, and project wrapper conventions. Use when the user asks to add, scaffold, wrap, or fix a reusable HeroUI form control such as a search, number, date, select, autocomplete, or switch field.
---

# Create HeroUI Form Control

Adapt the installed component contract instead of copying a wrapper from a
different HeroUI version.

## Resolve inputs

Obtain or infer:

- target HeroUI component and wrapper name;
- controlled value and change-event shapes;
- null, undefined, empty-string and falsy-value semantics;
- label, description, validation and accessibility requirements;
- shared wrapper versus form-local integration scope.

Request clarification only when the value contract or ownership cannot be
resolved from installed types and nearby code.

## Inspect before writing

1. Read applicable `AGENTS.md` files.
2. If present, read `.agents/manifest.json`, `ai-rules.config.json`, applicable
   `.agents/local/` UI rules and the selected HeroUI/React Hook Form documents.
3. Inspect `package.json` and verify compatible `@heroui/react` and
   `react-hook-form` versions are installed.
4. Follow the official-source order in the selected HeroUI Components rule,
   inspect the target component's installed-version types and at least two
   nearby field adapters when available.
5. Resolve file casing, public exports, `FormProvider` usage, generic type
   conventions, styling and feedback composition.
6. Report contradictions between documentation, types and nearby code before
   editing. Installed-version APIs and documented project priority win.

## Plan

List the wrapper owner, generic value/name contract, vendor props to omit,
value conversions, rendered slots, feedback behavior, exports and files that
remain untouched.

Do not create a shared wrapper for a one-off field unless current reuse or the
user's explicit request justifies it.

## Implement

Follow the selected HeroUI React Hook Form rule and reference. Derive vendor
props from the component type, omit form-owned props and type `name` against the
owning `FieldValues`. Use `Controller` only when controlled integration is
required. Forward `name`, `onBlur`, value, change and invalid state according to
the installed API.

Keep value conversions explicit, render accessible naming, prefer validation
error over description in a shared feedback slot and keep schemas/business
validation in consuming slices. Preserve intentional rest-prop support without
allowing consumers to override form-owned props.

## Verify and report

Run focused type checks and, when available, interaction tests for normal,
empty, invalid, disabled and change/blur states. Run project-required lint,
tests or build in proportion to the change.

Report:

- component API and value semantics resolved;
- created and changed files;
- skipped existing files;
- checks and results;
- version-sensitive assumptions or remaining consumer migration.
