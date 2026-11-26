# Delivery Checklist

## Purpose

Provide a framework-neutral final pass before handing off an implementation.

## Applies when

Apply after code, configuration, documentation or generated artifacts change.

## Does not apply when

Do not claim unavailable checks passed. Use project commands instead of
inventing generic ones.

## Checklist

- [ ] The requested scope is complete.
- [ ] Project, stack and core instructions were applied in priority order.
- [ ] Lint, typecheck, tests and build were run when configured and relevant.
- [ ] Focused failure paths were verified.
- [ ] No unused import, dead code, debug output or accidental secret remains.
- [ ] Documentation and generated artifacts match behavior.
- [ ] The final report lists changed files, checks and remaining risks.

