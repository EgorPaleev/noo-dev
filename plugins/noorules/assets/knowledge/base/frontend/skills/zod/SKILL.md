---
name: zod
description: Create, update, migrate, debug, test, or review Zod 4 schemas after resolving the installed Zod version, validation boundary, input/output contract, error handling, and project conventions. Use for Zod schema work; do not apply Zod 4 APIs to projects that still use Zod 3.
---

# Zod 4

Work with the installed Zod 4 API while preserving the contract owned by the
project.

## Resolve the task

Determine or infer:

- the untrusted boundary and the module that owns it;
- input and parsed-output shapes, including transform-induced differences;
- expected versus exceptional validation failures;
- unknown-key, coercion, default and error-reporting behavior;
- synchronous or asynchronous parsing requirements;
- public types, exports, callers and compatibility constraints.

Ask only when these choices cannot be resolved from project context or nearby
code. Do not invent fields, error payloads, limits or business validation.

## Inspect before editing

1. Read applicable `AGENTS.md` files, `ai-rules.config.json`, selected project
   rules and local instructions.
2. Inspect package metadata and the installed `zod/package.json`. This skill
   supports Zod 4.x only. If the installed major is 3, report the mismatch and
   do not upgrade the dependency.
3. Inspect the installed public exports or types before using an API whose
   availability or behavior may differ by minor version.
4. Inspect the owning boundary, nearby schemas, consumers, tests, error mapping
   and public exports.
5. Report contradictions instead of silently selecting a convention.

Use sources in this order: the direct user request, project-owned instructions,
the installed Zod package and public types, current official Zod documentation,
then this skill's references. Do not run remote installers or change package
versions as part of schema work.

## Load only relevant references

- Read [references/api-v4.md](references/api-v4.md) when choosing or checking a
  Zod API, recursive schema, transform, error formatter, registry or Zod Mini.
- Read [references/migration-v4.md](references/migration-v4.md) only for Zod 3
  to 4 migrations or when deprecated syntax is present.
- Read [references/testing.md](references/testing.md) when adding, changing or
  reviewing schema tests.

The selected `Zod Validation` stack rule remains the owner of boundary,
placement, coercion and public error-contract requirements. Do not duplicate or
override it here.

## Plan and implement

When structure or public behavior is ambiguous, write a change plan before
editing. Keep the schema at the boundary that owns the runtime contract and
reuse established helpers and naming.

- Use `safeParse()` when invalid input is an expected result. Use `parse()` when
  failure is intentionally exceptional and the caller already handles it.
- Use async parsing whenever a refinement or transform is async.
- Infer output types from the owning schema. Use `z.input` and `z.output` when a
  transform or codec makes the two sides differ.
- Make unknown-key, coercion and default behavior intentional. Do not treat
  JavaScript truthiness as string-to-boolean parsing.
- Keep refinements and transforms deterministic and free of network,
  filesystem, process and other external side effects. Perform those effects
  after successful parsing through the project's controlled service boundary.
- Do not log raw input or enable input reporting when it can expose secrets or
  personal data.
- Prefer documented public APIs. Treat deprecated APIs as migration targets,
  not as APIs that have already been removed.

Do not create a new architecture, shared schema registry, error format or
observability contract when the project has no established owner for it.

## Verify and report

Run focused tests for valid, invalid and boundary values, then available type
checks, lint, tests or build in proportion to the change.

Report:

- detected Zod version and any version-sensitive choices;
- resolved boundary, input/output contract and error behavior;
- changed and skipped files;
- checks and results;
- remaining compatibility assumptions or contradictions.
