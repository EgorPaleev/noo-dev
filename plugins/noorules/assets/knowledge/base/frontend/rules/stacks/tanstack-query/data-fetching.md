# TanStack Query Data Fetching

## Purpose

Use TanStack Query for remote server state with deterministic keys, explicit
ownership and bounded retry behavior.

## Applies when

Apply when `@tanstack/react-query` is installed and selected for client-side
server state.

## Does not apply when

Do not move local UI state into the query cache or require client queries where
the project deliberately uses another server-fetching strategy.

## Rules

- Place request functions, key factories and query/mutation options in the
  slice or module that owns the use case.
- Let project architecture decide whether ownership is page-local,
  domain-level or shared infrastructure.
- Build deterministic query keys and include every input that affects data.
- Reuse query option factories instead of recreating keys in components.
- Invalidate or update every affected cache scope after a successful mutation.
- Keep mutation retries disabled unless the operation is demonstrably safe and
  the project explicitly opts in.
- Bound query retries and exclude permanent failures.
- Create and configure the `QueryClient` at the application-initialization
  boundary. Keep global retry, freshness and refetch policy in that owner.
- In server-rendered applications, isolate clients by request and preserve one
  client per browser provider lifecycle; never share a module-level cache
  across server requests.
- Use global query or mutation cache callbacks only for genuinely cross-cutting
  reporting. Avoid showing both a global error and a duplicate local error for
  the same failure.
- Keep authentication-driven cache clearing or session transitions in a
  project-owned integration around the provider, not in reusable query rules.
- Use prior data for paginated transitions only when it represents a valid
  intermediate UI.
- Keep server state out of client-only stores.

## Checklist

- [ ] Ownership matches project architecture.
- [ ] Keys include all data-affecting inputs.
- [ ] Components consume shared query options.
- [ ] Mutation cache effects are complete.
- [ ] Retry behavior is bounded and safe.
- [ ] Global provider policy and local overrides do not duplicate feedback.
