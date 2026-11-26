---
name: commit
description: Create a series of topical Git commits using Conventional Commits with concise Russian descriptions. Use when the user explicitly asks to commit the current repository changes or invokes $commit; inspect and group all understood changes, stage each group precisely, verify every commit, and never push automatically.
---

# Commit

Create a complete, intentional series of topical commits for the current
repository changes. A single topic still produces one commit.

## Inspect the repository

1. Confirm that the current directory belongs to a Git repository.
2. Read applicable `AGENTS.md` files, project-owned instructions and package
   metadata for commit or verification conventions.
3. Run `git status`, inspect recent commit messages and read both staged and
   unstaged diffs. Include untracked files in the inspection.
4. Identify generated artifacts, secrets and files whose purpose is unclear.
   Never stage `.env`, `.env.local`, credentials, private keys or other
   secrets. Leave generated or unrecognised files out of staging and record
   them as skipped.
5. If the worktree contains no understood, commit-worthy changes, do not
   create an empty commit; report that the repository is clean or explain what
   was skipped.

Do not modify implementation files merely to manufacture a commit.

## Plan topical commits

- Group every understood change by user-facing purpose and affected module,
  rather than solely by file path. A group may contain implementation, tests,
  documentation and configuration needed for the same change.
- Create one commit per coherent group. Keep independent features, fixes,
  refactors and documentation changes separate even when they were made in one
  working session.
- When a change is ambiguous, attach it to the closest topical group and note
  that decision in the final report. If no meaningful group exists, skip it
  rather than inventing a commit theme.
- Before changing the index, present a concise written plan: each proposed
  commit, its purpose, message and included files or hunks, plus skipped files.
- Treat staged and unstaged changes as one input set. After the plan is ready,
  use `git reset` without `--hard` to clear only the index; never discard or
  overwrite working-tree changes.
- If independent groups modify the same file, stage their separate hunks with
  `git add -p` or another equally precise patch-staging operation. If the
  overlapping hunk cannot be separated safely, include it in the closest
  topical group and report that choice.

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

## Commit every group and verify

For each planned group, in dependency-aware order:

1. Stage only its explicit paths and selected hunks. Do not use `git add -A`
   or an equivalent command that hides the selected scope.
2. Inspect the staged diff and confirm that it contains the whole group and no
   unrelated change.
3. Create the commit without bypassing hooks:

```bash
git commit -m "$(cat <<'EOF'
type(scope): описание на русском
EOF
)"
```

4. Inspect the created commit and run `git status`. Continue with the next
   group until every understood change is committed.

If Git or a hook fails, stop immediately. Do not use `--no-verify`, alter the
failed commit or continue with later groups; report the commits already created
and the exact remaining staged and unstaged changes.

After a successful series, report:

- every commit hash, message and included files or scope;
- skipped secrets, generated artifacts or unrecognised files;
- decisions that assigned an ambiguous or inseparable hunk to a group;
- remaining staged or unstaged changes, if any;
- hooks or checks that failed.

Explain that the commits are local. The user must run `git push` separately to
send the full series to the remote repository.

Do not use `--no-verify`, `--amend`, create tags or push unless the user asks
for that action explicitly.
