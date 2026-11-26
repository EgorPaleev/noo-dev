---
name: create-server-action
description: Create or complete a Next.js Server Action after verifying that project authentication, BFF, mutation, validation, error, and cache rules permit that transport. Use when the user asks to add, scaffold, generate, or implement a Server Action; route the work to the project's approved alternative when Server Actions are forbidden for the operation.
---

# Create Server Action

Pass the project transport gate before writing an Action.

## Resolve inputs

Obtain or infer:

- requested side effect;
- caller and runtime;
- untrusted input;
- authorization requirement;
- result/error contract;
- cache invalidation or navigation effect.

Stop and request a choice when the action's ownership or public behavior cannot
be inferred safely.

## Inspect before writing

1. Read applicable `AGENTS.md` files.
2. If present, read `.agents/manifest.json`, applicable `.agents/local/` overrides,
   `ai-rules.config.json`, and `.agents/workflows/adding-server-action.md`.
3. Inspect `package.json` for Next.js, validation and optional action-wrapper
   dependencies.
4. Inspect sibling Actions and the project's Route Handler/client-mutation
   alternatives.
5. Read installed-version Next.js docs only when project documentation does not
   resolve a version-sensitive API or explicitly requires that check.
6. Resolve naming, location, authentication, authorization, validation, error,
   cache and revalidation conventions.
7. Report documentation/code contradictions before editing.

## Select the transport

Use a Server Action only when project rules permit the requested operation.

Do not use it when the project assigns the operation to:

- a BFF Route Handler;
- a browser-managed retry or refresh flow;
- a client mutation;
- another server transport.

When Server Actions are forbidden, explain the matched rule and implement the
approved alternative only if that remains within the user's requested scope.

## Plan

List the Action file, caller changes, input/result contracts, validation,
authorization, cache effects and checks before writing. Do not modify code
until the transport and contract are resolved.

## Implement

Follow the canonical domain sequence in
`.agents/workflows/adding-server-action.md`. Apply the resolved transport, contract,
security and cache choices, reuse existing utilities, and preserve existing
files through targeted edits.

## Verify and report

Run focused success, validation, authorization and failure checks plus required
project checks.

Report:

- transport decision;
- created and changed files;
- skipped files;
- checks and results;
- contradictions or unverified security behavior.
