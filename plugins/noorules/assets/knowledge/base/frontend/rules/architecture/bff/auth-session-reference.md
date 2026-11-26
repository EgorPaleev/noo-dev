# BFF Auth Session Reference

## Purpose

Describe a cookie-based browser session for a same-origin Next.js BFF with
session-bound signed double-submit CSRF protection and coordinated refresh.

## Applies when

Apply when a Next.js BFF owns browser session cookies, obtains access to an
upstream service, uses Zod for boundary validation and the project selected
`bff-auth-session-reference`.

## Does not apply when

Do not use this reference for direct-browser API access, bearer tokens stored
in browser storage, a non-cookie session model, or a project with a different
CSRF mechanism.

## Rules

- Define a project-owned session contract before implementation: cookie scope
  and lifetime, bootstrap and session operations, token rotation behavior,
  trusted origin policy, timeouts, public errors and end-session UX.
- Keep access and refresh tokens server-readable only. Browser code calls only
  same-origin BFF operations and never receives upstream tokens.
- Mark access and refresh cookies `Secure` and `HttpOnly`; set an explicit
  `SameSite` policy and keep them host-only unless a documented integration
  requires broader scope. Prefer `__Host-` cookie names when its required
  `Path=/` scope is compatible with the project.
- Issue a browser-readable CSRF cookie through a project-owned same-origin
  bootstrap operation before the first unsafe request. Mark it `Secure`, leave
  it non-`HttpOnly` only so browser code can send it in a custom header, and
  apply an explicit `SameSite` policy.
- Build every CSRF token from a cryptographically random nonce and an HMAC that
  binds the nonce to a current session-specific value available only to the
  BFF. Rotate or replace the token when that session binding changes.
- For every unsafe request, check same-origin intent, available Fetch Metadata,
  exact cookie-to-header equality and the session-bound CSRF HMAC before
  parsing input or performing a side effect.
- Treat the project's explicit refresh-required signal as the only reason to
  refresh. A forbidden response never triggers refresh.
- Deduplicate refreshes within a tab and coordinate tabs when the browser
  supports it, but treat browser coordination as best effort. Define how the
  BFF and upstream safely serialize, reject or make concurrent refresh
  rotation idempotent.
- Replay a failed request at most once, only after successful refresh and only
  when its body can be replayed safely. A refresh operation and a request that
  lost a concurrent refresh race never enter an unbounded refresh-and-replay
  loop.
- On final refresh failure, clear local session state and follow the project
  navigation and cache-cleanup policy.
- Validate untrusted bootstrap, refresh and upstream responses at their BFF
  boundary; keep their schemas and public error mapping project-owned.

## Checklist

- [ ] Session cookies are server-readable only and have explicit secure scope.
- [ ] A same-origin bootstrap operation issues a session-bound CSRF token.
- [ ] Unsafe requests reject missing, mismatched or invalid header tokens before
  side effects.
- [ ] Concurrent refresh has a documented safe BFF/upstream outcome.
- [ ] At most one replay occurs and forbidden responses do not refresh.
- [ ] Failed refresh clears session state without exposing token details.
