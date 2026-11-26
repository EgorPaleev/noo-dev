---
name: review-changes
description: Review a working-tree diff, commit, branch, or pull request for actionable correctness and regression problems using the project's selected rules. Use for code review, change review, ревью изменений, or a pre-merge assessment; report findings, verdict, risk, checks, and residual gaps without modifying code.
---

# Review Changes

Perform an evidence-backed, read-only review. Do not edit, format, stage, commit,
push, publish comments, or change configuration. If the request says “review and
fix”, complete only the review and offer to handle fixes in a separate request.

## Resolve the review target

Use an explicitly named target when one is provided. Otherwise review the current
working tree:

1. Inspect `git status --short`.
2. Inspect both the unstaged and staged diffs.
3. Inventory untracked files with Git and inspect relevant source, tests,
   configuration, migrations, and documentation.
4. Exclude ignored files and unrelated pre-existing changes from the conclusion.

For an explicit commit, inspect that commit and its parent. For a branch, compare
it with the stated base or the locally available merge base. For a pull request,
use the supplied diff or an available integration. Do not fetch from the network
unless the user explicitly requests and authorizes it. If the target or base
cannot be established reliably, stop with a blocked verdict.

Do not read `.env` files, credentials, secret stores, or binary contents merely
to make the review exhaustive. Record a relevant file as an uninspected gap when
its contents are necessary but unsafe or unavailable.

## Load the active project context

Before judging the change:

1. Read every applicable root and nested `AGENTS.md` file.
2. Read `ai-rules.config.json`, `.agents/manifest.json`, and the configured
   project rules when they exist.
3. Run the configured ruleset's local `check` command when its CLI is available
   and the command is read-only. Never run `sync`, `configure`, or another repair
   command during review.
4. Use the manifest as the source of active preset and document IDs. Use the task
   routing in `AGENTS.md` to open only selected rules relevant to the changed
   areas. Do not treat every document in the pinned ruleset source as active.
5. Read the selected code-review workflow when it is present.
6. Inspect package metadata, nearby implementations, callers, public exports,
   tests, and naming conventions needed to understand the changed behavior.

If the manifest is absent, use the project instructions and available local
rules, but report the missing selection evidence. If `check` reports drift, do
not repair it: explain which review conclusions may be unreliable and use a
blocked verdict when the applicable rules cannot be established.

Apply instructions in this order:

1. Direct user request.
2. Project-owned local rules.
3. Selected architecture and stack rules.
4. Selected core rules.
5. General engineering guidance.

Report contradictions rather than silently choosing a convention.

## Analyze the change

Trace changed behavior through relevant callers and runtime boundaries. Review:

- correctness, regressions, edge cases, failure paths, and error handling;
- security boundaries, authorization, sensitive data, destructive operations,
  parsing, and validation;
- persistence, cache, concurrency, lifecycle, and state transitions;
- public APIs, serialized contracts, types, compatibility, and dependency use;
- ownership, layer boundaries, imports, generated artifacts, and migrations;
- whether tests cover the changed behavior and meaningful failure modes.

Review generated output only for consistency and identify its owning source.
Avoid duplicate findings against both generated output and its source. Do not
raise findings for taste, speculative improvements, or formatting preferences
without a concrete observable risk. This skill is not a substitute for a deep
security audit.

## Run only safe checks

Inspect scripts before running them. Run a check only when it is relevant, local,
available, and known not to:

- use `--fix`, update snapshots, or rewrite generated or tracked files;
- install or update dependencies;
- require network access, credentials, external services, release, or deploy;
- mutate databases or other persistent external state.

Capture Git status before and after checks. If an unexpected mutation occurs,
stop, do not revert user work, and report it. List useful checks that were not run
and the reason for each omission.

## Classify findings and verdict

Use these severities:

- `critical`: exploitable security failure, irreversible data loss, or another
  release-blocking failure with severe impact.
- `high`: likely production failure, major user-visible regression, or serious
  security or data-integrity problem.
- `medium`: concrete contract, edge-case, or reliability defect with meaningful
  impact.
- `low`: localized actionable defect with limited impact. Do not use it for
  personal preference.

Sort findings from `critical` to `low`. Overall risk is the highest finding
severity. When there are no findings, use `low`. When evidence is insufficient,
use a conservative `high` risk unless observed evidence requires `critical`.

Choose exactly one verdict:

- `approve`: no actionable findings.
- `changes requested`: at least one `low`, `medium`, or `high` finding and no
  `critical` finding.
- `blocked`: at least one `critical` finding, or insufficient data for a reliable
  review.

## Report

Put findings first. For each finding include:

```text
[severity] Concise title — path/to/file:line
Evidence: the specific changed behavior and how it was verified.
Impact: the concrete failure or risk.
Fix: a bounded correction, without implementing it.
```

Use exact changed-file locations whenever possible. Keep evidence concise and do
not quote secrets or large source passages.

After findings, report:

- `Verdict`: `approve`, `changes requested`, or `blocked`.
- `Overall risk`: `low`, `medium`, `high`, or `critical`.
- `Reviewed scope`: target, diff types, and relevant supporting files.
- `Applied context`: selected preset and rule IDs actually used.
- `Checks`: commands run, results, and skipped checks with reasons.
- `Residual gaps`: anything not inspected or verified.

When no problems are found, start with “No actionable findings found.” Still
include the verdict, risk, scope, applied context, checks, and residual gaps.
