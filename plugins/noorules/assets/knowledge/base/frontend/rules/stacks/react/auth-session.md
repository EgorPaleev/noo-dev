# React SPA Auth Session

## Purpose

Define secure authentication and bounded, seamless token refresh for a
browser-rendered React application that calls an API directly.

## Applies when

Apply when a React SPA without a server-side BFF owns its API client and uses
access and refresh tokens for a browser session.

## Does not apply when

Do not use this rule when a BFF keeps upstream tokens outside the browser, the
application uses a server-managed opaque session without token refresh, or a
native client owns the session.

## Rules

- Choose and document exactly one session profile before implementation:
  - Prefer cookie-only when the API can authenticate requests from cookies.
    The server sets both access and refresh cookies and browser code never
    receives, reads or forwards either token.
  - Use memory-access only when the API requires bearer authentication. The
    server keeps the refresh token in a cookie and returns a short-lived access
    token for storage in memory only.
- Never persist access or refresh tokens in `localStorage`, `sessionStorage`,
  IndexedDB, a JavaScript-readable cookie, a URL or application logs. React
  state and module memory are not protection against active XSS; memory-access
  only limits persistence and token lifetime.
- Set token cookies from the server with `Secure`, `HttpOnly`, an explicit
  `SameSite` policy, host-only scope and the narrowest compatible path and
  lifetime. Browser JavaScript cannot add `HttpOnly`. Use a `__Host-` prefix
  when its required `Path=/` scope is compatible with the session contract.
- Use credentialed requests for cookie transport. For cross-origin SPA/API
  deployments, allow credentials only from exact trusted origins; never
  combine credentials with a wildcard CORS origin. Confirm that the selected
  `SameSite` policy works for the deployed site relationship.
- Protect every cookie-authenticated unsafe operation against CSRF. Validate a
  project-owned CSRF token or an equivalently strong custom-header and origin
  policy on the server, with Fetch Metadata as defense in depth. `SameSite`
  alone is not the default CSRF control. In memory-access mode this requirement
  still covers login, refresh, logout and any other cookie-authenticated
  operation.
- Bootstrap the browser-readable CSRF value before the first unsafe session
  operation. Keep it distinct from authentication tokens and never expose an
  access or refresh token to make the cookie-to-header pattern work.
- Model login, refresh and logout as unsafe `POST` operations. The server owns
  refresh-token rotation and revocation; successful logout expires its cookies
  with the same scope used to create them. Do not return a refresh token in a
  response body.
- Let only an explicit project-owned signal, such as HTTP `401` with the
  machine-readable code `access_expired`, initiate refresh. Invalid
  credentials, revoked sessions, forbidden responses and ordinary `401`
  responses do not initiate refresh.
- Send refresh through a dedicated client that cannot enter the protected
  client's refresh interceptor. Deduplicate concurrent refresh attempts within
  a tab with one shared in-flight promise.
- Coordinate refresh across tabs when practical, but treat browser locks and
  messaging as best effort. The server must define a safe outcome for
  concurrent refresh-token rotation through serialization, a bounded grace
  window, idempotency or an equivalent project-owned mechanism.
- Replay a failed request at most once after successful refresh. Replay safe
  methods by default; replay an unsafe request only when its body is reusable
  and the server guarantees that the rejected attempt performed no side
  effect. Never replay login, refresh or logout through this mechanism.
- Bootstrap authentication before rendering protected routes. Cookie-only
  clients query a session or identity operation; memory-access clients obtain a
  new access token through the documented refresh bootstrap because memory is
  empty after reload.
- On final refresh failure, clear the in-memory token, authentication state and
  user-scoped caches, then follow the project's navigation policy. Avoid
  duplicate cleanup and user notifications for requests waiting on the same
  refresh.

## Checklist

- [ ] One session profile and its server contract are documented.
- [ ] No access or refresh token is stored in browser-persistent or
  JavaScript-readable storage.
- [ ] Token cookies are server-set, `Secure`, `HttpOnly` and explicitly scoped.
- [ ] Cookie-authenticated unsafe operations have server-validated CSRF
  protection.
- [ ] Only the explicit expired-access signal starts one single-flight refresh.
- [ ] Each eligible request is replayed at most once.
- [ ] Rotation remains safe across concurrent requests and tabs.
- [ ] Bootstrap, server logout and final session cleanup are covered by tests.
