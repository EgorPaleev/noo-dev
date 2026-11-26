---
name: create-mui-form-control
description: Create or update a typed field adapter between an installed Material UI component and React Hook Form after resolving the exact MUI API, controlled value semantics, focus ref, validation feedback, accessibility and project wrapper conventions. Use when the user asks to add, scaffold, wrap or fix a reusable MUI form control such as a text, number, select, autocomplete, checkbox, switch, slider or toggle field.
---

# Create MUI Form Control

Adapt the installed component contract instead of copying a wrapper from a
different Material UI version.

## Resolve inputs

Obtain or infer:

- target MUI component and wrapper name;
- controlled value, change-event and focus-ref shapes;
- empty-string, null, undefined, zero and false semantics;
- label, helper text, validation and accessibility requirements;
- shared wrapper versus form-local integration scope.

Request clarification only when the value contract or ownership cannot be
resolved from installed types, selected rules and nearby code.

## Inspect before writing

1. Read applicable `AGENTS.md` files.
2. If present, read `.agents/manifest.json`, `ai-rules.config.json`, applicable
   `.agents/local/` UI rules and the selected MUI/React Hook Form documents.
3. Inspect `package.json` and verify compatible `@mui/material` and
   `react-hook-form` versions are installed. Do not install or upgrade them.
4. Inspect the target component's installed-version exports and types, the
   project's theme/provider boundary and at least two nearby field adapters
   when available.
5. Resolve file casing, public exports, `FormProvider` usage, generic type
   conventions, style organization, value conversion and feedback composition.
6. Report contradictions between documentation, installed types and nearby
   code before editing. Installed APIs and documented project priority win.

Do not run remote installers, codemods or network commands as part of this
workflow.

## Plan

List the wrapper owner, generic values/name contract, vendor props to omit,
value conversions, event/ref mapping, validation feedback, exports and files
that remain untouched.

Do not create a shared wrapper for a one-off field unless current reuse or the
user's explicit request justifies it.

## Implement

Follow the selected MUI React Hook Form rule and reference. Derive vendor props
from the installed component type, omit form-owned props and type `name` against
the owning `FieldValues`. Use `Controller` only when controlled integration is
required.

Spread consumer props before form-owned values and handlers. Forward name,
blur, value or checked state, change and the focus ref through the target
component's exact API. Keep empty and falsy conversions explicit. Preserve
accessible naming and show validation error before optional helper text in a
shared feedback slot.

Keep schemas, option loading and business validation in consuming slices.

## Verify and report

Run focused type checks and, when available, interaction tests for normal,
empty, invalid, disabled, change, blur and focus-error states. Run project lint,
tests or build in proportion to the change.

Report:

- component API, event/ref and value semantics resolved;
- created and changed files;
- skipped existing files;
- checks and results;
- version-sensitive assumptions or remaining consumer migration.
