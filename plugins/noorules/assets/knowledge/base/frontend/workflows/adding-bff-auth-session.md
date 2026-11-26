# Adding a BFF Auth Session

## Purpose

Add or review a cookie-based BFF auth session without copying another
application's cookie, endpoint or error contract.

## Applies when

Apply when the project selected `bff-auth-session-reference` and needs refresh
or session-bound signed double-submit CSRF behavior.

## Does not apply when

Do not add this workflow to a direct-client API, a token-in-storage design or
a session mechanism already owned by a different security boundary.

## Steps

1. Read the local auth, BFF, error and navigation contracts and the
   [BFF auth session reference](../rules/architecture/bff/auth-session-reference.md)
   before choosing implementation details.
2. Record the local session contract: cookie attributes and paths, trusted
   origin policy, CSRF bootstrap lifecycle, refresh semantics, upstream
   timeout, public errors and end-session UX.
3. Implement the cookie, CSRF and unsafe-request guards required by the
   reference before proxying any unsafe operation.
4. Keep access and refresh token transport server-only; validate upstream
   refresh responses with the selected Zod schemas before replacing local
   session state.
5. In the browser client, attach the CSRF header for unsafe same-origin calls,
   recognize only the local refresh-required signal and exclude the refresh
   operation from refresh recursion.
6. Implement the documented concurrent-refresh outcome, then replay each
   eligible failed request once at most.
7. On unrecoverable refresh failure, clear local session state, invalidate
   affected caches and follow the project's navigation policy.
8. Test successful bootstrap, rejected CSRF cases, cookie scope, concurrent
   refresh, one replay, forbidden responses and session cleanup.

## Checklist

- [ ] The reference owns all reusable CSRF, cookie and refresh invariants.
- [ ] Local security contract owns every cookie, route and public error detail.
- [ ] Security-focused bootstrap, refresh, replay and cleanup cases were tested.
- [ ] Browser, BFF and upstream responsibilities were integrated as planned.
- [ ] Unresolved security decisions and verification gaps were reported.
