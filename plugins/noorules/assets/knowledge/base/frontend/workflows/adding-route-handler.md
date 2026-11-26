# Adding a Route Handler

## Purpose

Add a validated Next.js HTTP boundary and integrate it with the project's
architecture and security contract.

## Applies when

Apply when a requested operation requires an App Router Route Handler.

## Does not apply when

Do not introduce an HTTP boundary when local server code or the project's
approved mutation mechanism is sufficient.

## Steps

1. Read installed Next.js Route Handler docs and project API/security rules.
2. Inspect sibling handlers and shared response utilities.
3. Define method, path, inputs, success response, failures and cache behavior.
4. Validate params, query, headers and body at the boundary.
5. Apply project authentication, authorization, origin and CSRF checks.
6. Call the approved server-only transport with explicit timeout/cancellation.
7. Normalize errors through the project contract.
8. Keep the route entry thin if a framework adapter owns implementation.
9. Add focused tests or checks for validation, security and error mapping.

## Checklist

- [ ] The HTTP boundary is justified.
- [ ] Every input and required security signal is checked.
- [ ] Upstream details remain private.
- [ ] Response and cache contracts are stable.
- [ ] Failure-path checks were run.

