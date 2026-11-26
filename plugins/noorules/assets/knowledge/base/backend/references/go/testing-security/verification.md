# Verification

Use `make help`. Choose checks based on the changed area.

## Always

```bash
git status --short
git diff --check
```

- Check untracked files, the final diff, secrets, and unrelated changes.
- For Markdown, check links, paths, and commands.

## Domain

For domain changes, also verify:

- no free domain helpers for normalization, validation, or state changes;
- no aggregate struct literals outside the owning domain package;
- tests cover value objects, aggregate methods, read projections, rehydration, boundaries, errors, optional states, and mutation/ownership.

## Go

```bash
test -z "$(find . -path './.cache' -prune -o -path './.git' -prune -o -type f -name '*.go' -print | xargs gofmt -l)"
go vet ./...
go test ./...
go build ./...
```

- Add tests for changed behavior, including boundary and failure cases.

## By area

- Compose or `.env.example`: run `docker compose config -q` with test secrets.
- Dockerfile: run `docker compose build api`.
- HTTP: compare OpenAPI with routes, DTOs, statuses, and errors.
- Migration: on a disposable database, run up → down → up.
