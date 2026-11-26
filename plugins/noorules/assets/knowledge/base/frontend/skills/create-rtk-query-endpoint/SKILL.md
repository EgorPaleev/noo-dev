---
name: create-rtk-query-endpoint
description: Create or update an RTK Query endpoint after resolving the owning API slice, installed Toolkit API, transport contract, cache arguments, tags, lifecycle behavior and public exports. Use when the user asks to add, inject, extend or fix an RTK Query query or mutation.
---

# Create RTK Query Endpoint

Extend the correct API slice without duplicating transport, middleware or
server state.

## Resolve inputs

Obtain or infer:

- read versus server-changing operation;
- owning API slice and base-query contract;
- result, error and single endpoint-argument types;
- individual and collection cache relationships;
- hooks, selectors or endpoint exports consumers require;
- lifecycle, optimistic update, polling or refetch requirements.

Request clarification only when the API owner or cache behavior cannot be
resolved from selected rules and nearby endpoints.

## Inspect before writing

1. Read applicable `AGENTS.md` files.
2. If present, read `.agents/manifest.json`, `ai-rules.config.json`, applicable
   `.agents/local/` transport rules and selected RTK Query documents.
3. Inspect `package.json` and verify a compatible `@reduxjs/toolkit` version is
   installed. Do not install or upgrade it.
4. Inspect store registration, the base API, base query, tag types, endpoint
   injection, error mapping and at least two nearby endpoints when available.
5. Resolve the project's React or core RTK Query entry point and public export
   convention.
6. Report contradictions between project rules, installed types and nearby code
   before editing. Installed APIs and documented project priority win.

Do not run remote installers, codemods or network commands as part of this
workflow.

## Plan

List the API owner, endpoint kind, argument and result contracts, transport
mapping, tags, lifecycle behavior, exports, tests and files that remain
untouched.

Do not create a second API slice, reducer or middleware registration unless a
distinct transport/cache boundary is explicitly established.

## Implement

Follow the selected RTK Query rule and `Adding an RTK Query Endpoint` workflow.
Reuse the owning API slice and transport. Keep arguments serializable and
complete, transform data at the API boundary, and express cache effects with
tags before adding manual updates.

If lifecycle code is required, handle rejected requests and release resources.
For optimistic cache updates, retain the patch result and provide rollback or a
race-safe invalidation path. Export through the established public API without
mirroring query data into a regular slice.

## Verify and report

Run focused endpoint tests for request construction, success, error, cache
effects and lifecycle cleanup, then available type checks, lint, tests or build.

Report:

- API ownership, cache identity and tag strategy resolved;
- created and changed files;
- skipped existing files;
- checks and results;
- version-sensitive assumptions or unresolved contradictions.
