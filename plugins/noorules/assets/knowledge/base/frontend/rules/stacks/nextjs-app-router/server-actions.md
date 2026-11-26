# Next.js Server Actions

## Purpose

Use Server Actions as explicit server mutation boundaries without assuming a
particular validation, authentication or action-wrapper library.

## Applies when

Apply when the installed Next.js version supports Server Actions and project
rules allow the requested operation to use one.

## Does not apply when

Do not use a Server Action when project security or transport rules require a
Route Handler, browser-managed flow, external API contract or another mutation
mechanism.

## Rules

- Confirm that a Server Action is the project-approved transport before
  implementing it.
- Validate untrusted input on the server. Use Zod only when the project has
  selected the Zod preset or already uses it.
- Authorize every side effect at the boundary that performs it.
- Return a stable project-defined result and avoid leaking internal errors.
- Keep framework cache invalidation and navigation effects explicit.
- Treat action wrapper libraries, including safe-action libraries, as optional
  adapters with their own project rules.
- Do not read, refresh or mutate authentication state unless the project
  explicitly assigns that responsibility to Server Actions.

## Checklist

- [ ] Project rules permit this operation as a Server Action.
- [ ] Input is validated and the side effect is authorized.
- [ ] Optional libraries are installed before their patterns are used.
- [ ] Result and error contracts match the project.
- [ ] Cache or navigation effects are explicit.

