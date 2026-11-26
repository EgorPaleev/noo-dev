# Next.js Route Handlers

## Purpose

Create explicit HTTP boundaries in the App Router while leaving security,
upstream transport and response contracts project-owned.

## Applies when

Apply to `route` entry points in a Next.js App Router project.

## Does not apply when

Do not introduce a Route Handler only to wrap local code without an HTTP or
runtime-boundary reason.

## Rules

- Read the installed Next.js Route Handler documentation before implementation.
- Validate path params, query values, headers and bodies before trusting them.
- Apply authentication, authorization, CSRF and origin policies documented by
  the project.
- Keep upstream credentials and server-only transports out of browser code.
- Return the project's stable status, body, headers and caching contract.
- Normalize upstream failures without exposing private payloads or URLs.
- Keep route entry files thin when an architecture adapter owns implementation
  placement.
- Add bounded cancellation or timeout behavior when calling an upstream service.

## Checklist

- [ ] Installed-version Route Handler docs were checked.
- [ ] Every untrusted input is validated.
- [ ] Required security checks run before the side effect.
- [ ] Server-only data is not exposed.
- [ ] Response and cache behavior follow project rules.

