# Code Quality

## Purpose

Keep changes focused, maintainable, reviewable and consistent with the
repository that receives them.

## Applies when

Apply to implementation, refactoring, review and generated code in every
project.

## Does not apply when

Do not use these rules to override a more specific project convention or to
perform unrelated cleanup outside the requested scope.

## Rules

- Inspect nearby code, project instructions and existing utilities before
  creating a new abstraction.
- Make the smallest coherent change that satisfies the requested behavior.
- Preserve user changes and unrelated worktree modifications.
- Remove imports, branches and comments made obsolete by the change.
- Do not leave debug output, commented-out implementations or unexplained
  suppression directives.
- Avoid weakening types to bypass a design or validation problem.
- Prefer explicit ownership and error paths over hidden side effects.
- Run the checks documented by the project; do not invent unavailable commands.
- Report checks that could not run and the concrete reason.

## Checklist

- [ ] Existing patterns and utilities were inspected.
- [ ] The diff contains no unrelated rewrite.
- [ ] Dead code and debug output were removed.
- [ ] Available focused checks were run.
- [ ] Unverified behavior and remaining risks were reported.

