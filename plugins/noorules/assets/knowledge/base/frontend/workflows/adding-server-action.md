# Adding a Server Action

## Purpose

Add a Server Action only after confirming it is the approved transport for the
requested side effect.

## Applies when

Apply when the project uses Next.js Server Actions and permits the operation.

## Does not apply when

Do not use when project auth, BFF, browser retry or external transport rules
require a Route Handler or another mechanism.

## Steps

1. Read installed Next.js Server Action docs and project mutation rules.
2. Compare the operation with existing Actions, Route Handlers and client
   mutations.
3. Record why a Server Action owns this side effect.
4. Define the input and stable result contract.
5. Validate untrusted input using the selected project validator.
6. Authorize the side effect at execution time.
7. Implement the mutation without leaking internal failures.
8. Apply explicit cache invalidation or navigation behavior.
9. Add focused success, validation, authorization and failure checks.

## Checklist

- [ ] The project permits this Server Action.
- [ ] A more appropriate transport was considered.
- [ ] Input and authorization are enforced server-side.
- [ ] Result, cache and navigation behavior are explicit.
- [ ] Failure paths are verified.

