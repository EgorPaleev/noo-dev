---
name: commit
description: Create a Git commit using Conventional Commits with a concise Russian description. Use when the user explicitly asks to commit the current repository changes or invokes $commit; inspect the exact diff, stage only understood files, create one intentional commit, verify the result, and never push automatically.
---

# Commit

Create one intentional commit for the current repository changes.

## Inspect the repository

1. Confirm that the current directory belongs to a Git repository.
2. Read applicable `AGENTS.md` files, project-owned instructions and package
   metadata for commit or verification conventions.
3. Run `git status`, inspect recent commit messages and read both staged and
   unstaged diffs.
4. Identify unrelated changes, generated artifacts, secrets and files whose
   purpose is unclear.
5. If the worktree contains no commit-worthy changes, do not create an empty
   commit; report that the repository is clean.

Do not modify implementation files merely to manufacture a commit.

## Select the commit scope

- Commit only files that belong to one coherent change.
- Preserve unrelated user changes and leave them unstaged.
- Never stage `.env`, `.env.local`, credentials, private keys or other secrets.
- Stage explicit paths with `git add <path>`. Do not use `git add -A` or an
  equivalent command that hides the selected scope.
- Review the staged diff before committing.

## Write the message

Follow repository-specific commit conventions when they exist. Otherwise use:

```text
type(scope): краткое описание на русском языке
```

Allowed default types:

- `feat` — new behavior;
- `fix` — bug fix;
- `refactor` — structural change without new behavior;
- `docs` — documentation only;
- `chore` — maintenance and configuration;
- `style` — formatting only;
- `test` — tests;
- `perf` — performance;
- `ci` — CI/CD;
- `build` — build system.

Derive an optional scope from the affected module. Omit it for a repository-wide
change. Keep the description lowercase, concise, in Russian and without a final
period.

Examples:

```text
feat(auth): добавить обновление сессии
fix(frontend): исправить валидацию формы
docs: обновить инструкции проекта
chore: синхронизировать общие правила
```

## Commit and verify

Create the commit without bypassing hooks:

```bash
git commit -m "$(cat <<'EOF'
type(scope): описание на русском
EOF
)"
```

Then run `git status` and inspect the new commit. Report:

- commit hash and message;
- committed files or scope;
- remaining staged or unstaged changes;
- hooks or checks that failed.

Do not use `--no-verify`, `--amend`, create tags or push unless the user asks
for that action explicitly.
