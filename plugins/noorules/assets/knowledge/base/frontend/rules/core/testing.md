# Testing

## Purpose

Keep unit and component tests focused on observable behavior, deterministic
outcomes and maintainable failure signals.

## Applies when

Apply when a project selects the `testing` preset and adds, changes or reviews
unit, component or regression tests.

## Does not apply when

Do not use this rule as an end-to-end, visual-regression, performance or
security-testing strategy. Follow the project's more specific test policy when
it defines stronger requirements.

## Rules

- Inspect the configured runner, scripts, nearby tests, fixtures and naming
  conventions before adding a test or helper.
- Write `describe`, `it` and `test` names and explanatory test comments in
  Russian by default. Follow an explicit project-owned language convention when
  it requires another language, and keep code identifiers unchanged.
- Test observable behavior through a public contract. Do not assert private
  state, internal call order or implementation details without a boundary
  reason.
- Give each test one clear behavioral reason to fail and name it by the expected
  outcome.
- Cover the primary success path, meaningful boundary cases and failures that
  callers must handle. Add a regression test that reproduces a reported defect
  before relying on its fix.
- Keep tests deterministic. Control network access, time, randomness, storage
  and mutable global state instead of relying on the host environment.
- Replace external, expensive or nondeterministic boundaries with the smallest
  useful fake or mock. Do not mock the unit under test or duplicate its logic in
  assertions.
- Keep fixtures minimal and relevant to the behavior. Introduce builders only
  when they remove meaningful repetition without hiding important inputs.
- Await asynchronous work and assert its settled observable result. Do not use
  arbitrary sleeps to make a test pass.
- Test components through rendered output and user-visible interactions. Prefer
  accessible roles and names over CSS selectors, test IDs or component internals
  when the installed renderer supports them.
- Restore mutated globals, timers, spies and shared state so tests remain
  independent of execution order.
- Use snapshots only for a small, stable and intentionally reviewed output.
  Prefer focused assertions when a snapshot would obscure the behavior under
  test.
- Treat coverage as a discovery signal, not proof of correctness. Do not add
  assertions solely to increase a percentage.

## Checklist

- [ ] The test verifies an observable contract rather than an implementation
  detail.
- [ ] Test names and explanatory comments use Russian unless project rules
  explicitly require another language.
- [ ] Primary, boundary and failure scenarios are proportionate to the risk.
- [ ] External state and nondeterminism are controlled at their boundaries.
- [ ] Async work is awaited without arbitrary delays.
- [ ] Component assertions reflect user-visible and accessible behavior.
- [ ] Mocks, timers and globals cannot leak into another test.
