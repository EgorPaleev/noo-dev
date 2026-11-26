# Code Review

## Purpose

Review a change for correctness, regression risk and instruction compliance
before discussing style.

## Applies when

Apply to diffs, pull requests and pre-delivery self-review.

## Does not apply when

Do not rewrite or fix code unless the review request explicitly authorizes
implementation.

## Steps

1. Read the task, applicable project rules and changed files.
2. Identify behavioral changes and affected callers.
3. Check correctness, security, data loss, runtime boundaries and error paths.
4. Check architecture, public APIs and dependency direction.
5. Check tests and verification in proportion to risk.
6. Confirm generated files and migrations match their source.
7. Report actionable findings by severity with precise locations.
8. State when no actionable findings were found and list residual test gaps.

## Checklist

- [ ] Findings describe real impact, not preference.
- [ ] Project overrides were applied before stack defaults.
- [ ] Changed behavior has appropriate verification.
- [ ] Locations and remediation are precise.
- [ ] Residual risks are explicit.

