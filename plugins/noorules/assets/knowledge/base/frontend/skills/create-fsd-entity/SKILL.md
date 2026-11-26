---
name: create-fsd-entity
description: Decide whether a domain model belongs in an FSD entity and create or complete it only when current reuse or an explicit project override justifies extraction. Use when the user asks to add, scaffold, generate, extract, or place an FSD entity/domain model; keep single-use logic local and do not mirror API resources automatically.
---

# Create FSD Entity

Treat entity creation as an architecture decision, not a directory-generation
shortcut.

## Resolve inputs

Obtain or infer:

- domain responsibility;
- current consumers;
- required model, API, UI or library behavior;
- scaffold-only versus consumer migration scope.

Do not infer an entity from a DTO, endpoint, table or CRUD resource name alone.

## Inspect before writing

1. Read applicable `AGENTS.md` files.
2. If present, read `.agents/manifest.json`, applicable `.agents/local/` overrides,
   `ai-rules.config.json`, and `.agents/workflows/adding-fsd-entity.md`.
3. Inspect installed dependencies, aliases and existing FSD layers.
4. Search current consumers and inspect sibling entity plus page-local models.
5. Resolve:
   - the project's extraction threshold;
   - API ownership;
   - public API and runtime-specific entry points;
   - filename casing and segment conventions.
6. Report contradictions between generic FSD guidance and project deviations.
   Project rules win.

Do not inspect `node_modules` when project documentation and installed package
metadata already answer the placement question.

## Decide placement

Prefer the consuming page, feature or widget when:

- the logic has one current consumer;
- the boundary is unstable;
- reuse is only hypothetical.

Prefer shared infrastructure when the code is generic transport, session
infrastructure or non-domain utility.

Create an entity only when:

- current independent consumers reuse a stable domain boundary; or
- project rules explicitly define another threshold.

If extraction is not justified, explain the decision and implement locally only
when that remains inside the user's requested scope.

## Plan

List the chosen owner, evidence, required segments, public exports and affected
consumers before editing. Report whether the plan relies on a project override.

## Implement

Follow the canonical domain sequence in
`.agents/workflows/adding-fsd-entity.md`. Create only the files justified by the
resolved plan, do not invent placeholder business fields or optional
dependencies, and refuse to overwrite a non-empty slice without a targeted
merge plan.

## Verify and report

Run available architecture, type, lint, test and build checks required by the
project.

Report:

- placement decision and evidence;
- created and changed files;
- skipped files;
- checks and results;
- contradictions, overrides and remaining consumer migrations.
