# Error Handling

## Purpose

Make expected failures stable for callers while preserving useful internal
diagnostics and preventing sensitive data exposure.

## Applies when

Apply to functions, workflows, background tasks, API boundaries and user-facing
operations that can fail.

## Does not apply when

Do not invent a global error envelope when the project or external protocol
already defines one. Do not catch errors only to discard them.

## Rules

- Distinguish expected operational failures from programming defects.
- Validate untrusted input at the boundary that first trusts it.
- Expose stable, documented information to callers and keep internal causes in
  server-side diagnostics.
- Never include secrets, credentials, private upstream URLs or raw internal
  payloads in user-facing errors.
- Preserve the original cause when wrapping an error if the runtime supports it.
- Make retryability explicit; do not retry validation, authorization or other
  permanent failures by default.
- Define project-specific status codes, messages and observability fields in
  project rules.

## Checklist

- [ ] Inputs are validated at a trust boundary.
- [ ] Expected and unexpected failures are distinguishable.
- [ ] Public errors contain no internal or secret data.
- [ ] Retry behavior is bounded and documented.
- [ ] Project-specific error contracts remain project-owned.

