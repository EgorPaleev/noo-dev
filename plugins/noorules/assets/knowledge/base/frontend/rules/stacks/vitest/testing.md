# Vitest Testing

## Purpose

Apply Vitest-specific execution and isolation practices to the shared
[testing rules](../../core/testing.md).

## Applies when

Apply when Vitest is installed and the project explicitly selects the `vitest`
preset for unit or component tests.

## Does not apply when

Do not install or introduce Vitest only because this rule is available. Do not
apply Vitest APIs to a project that selected another runner, and do not treat
Vitest component tests as an end-to-end strategy.

## Rules

- Verify the installed Vitest major version and read its matching official
  documentation before changing configuration or runner APIs.
- Inspect `vitest.config.*`, applicable `vite.config.*` files, package scripts,
  setup files, test projects, installed renderers and nearby tests before
  choosing placement or syntax.
- Preserve the project's existing choice between explicit imports and Vitest
  globals. Do not enable globals or add type declarations without a project
  requirement.
- Use the `node` environment for tests that do not require browser APIs. For
  component tests, reuse the configured `jsdom`, `happy-dom` or Browser Mode
  setup that provides the required fidelity.
- Do not add Browser Mode or a browser provider automatically. Select it only
  when real browser behavior is required and the project owns the added
  dependency and execution cost.
- Use Vitest test projects only when distinct environments or configurations
  cannot be expressed clearly by the existing setup.
- Prefer dependency injection, a small fake or `vi.spyOn` at an owned boundary
  over a broad module mock. Account for `vi.mock` hoisting and avoid mocks that
  reproduce the implementation under test.
- Clear call history or restore implementations according to the test's
  isolation need. Restore stubbed globals, environment values, system time and
  real timers after tests that change them.
- Use Vitest fake timers for time-dependent behavior and advance them
  explicitly. Do not combine fake timers with arbitrary real-time waits.
- Await asynchronous assertions, rejected promises and component interactions
  so a passing test represents completed behavior.
- Use `vitest run` for non-watch CI execution. Reuse the project's existing
  watch script for local development instead of inventing another command.

## Checklist

- [ ] The installed Vitest version, configuration and sibling tests were read.
- [ ] The selected environment matches the runtime APIs under test.
- [ ] No renderer, browser provider or globals mode was introduced implicitly.
- [ ] Module mocks are boundary-focused and account for hoisting.
- [ ] Mocks, globals, environment values and timers are restored safely.
- [ ] CI uses a bounded non-watch command.

## References

- [Vitest getting started](https://vitest.dev/guide/)
- [Vitest test environment](https://vitest.dev/config/environment.html)
- [Vitest mocking](https://vitest.dev/guide/mocking)
- [Vitest Browser Mode](https://vitest.dev/guide/browser/)
