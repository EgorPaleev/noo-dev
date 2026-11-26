# Conventions

## Go

- Follow the style of the neighboring package; run `gofmt`.
- Package names are short and lowercase. Create a package only for a separate responsibility.
- Create a helper only for actual duplication, a distinct rule, or a noticeable simplification for the caller. Do not extract one-off linear code. Keep helpers unexported and next to their callers.
- Do not introduce an interface unless an implementation needs to be substituted.
- Wrap errors with `%w`; check expected errors with `errors.Is`/`errors.As`.
- Pass `context.Context` as the first parameter.

## Domain

- Put domain normalization, validation, and state changes on value objects, commands, or aggregates; do not add free domain helpers for them.
- Keep value-object representations private. Normalization must preserve optional-state semantics and must not mutate or leak mutable input/state.
- Use `New<Type>` for creation, `Restore<Type>`/`Rehydrate<Type>` for persistence, `<Type>State` for persistence data, and `<Type>View` for read data.
- Use `Apply<Type>`, `Change<Type>`, `Set<Type>`, and `Validate<Type>` for domain behavior; do not create generic domain `utils`/`helpers` packages.

## Changes

- Trace the flow: route → handler → application/domain → port → adapter.
- A handler decodes, validates transport data, and maps to HTTP; business logic remains in application/domain.
- Auth routes use `middleware.Authenticate`; obtain identity with `middleware.UserID`.
- Map errors to HTTP through a mapper in `internal/presentation/response`.
- Preserve constructor injection; create concrete dependencies in `cmd/api/main.go`.

## Contracts and storage

- An endpoint change keeps the route, DTO, status, auth, error mapping, and OpenAPI in sync.
- Error `code` values in `UPPER_SNAKE_CASE` are stable; validation uses `VALIDATION_FAILED` and `fields`.
- SQL is parameterized with explicit columns; a schema change requires a new sequential `up`/`down` migration.
- A configuration change keeps `config.go`, `.env.example`, and `docker-compose.yml` in sync.
- Redis is not a source of truth; the S3 bucket is private; object keys are not public.

## Documentation and review

- Do not duplicate information that is easily read from a source of truth. Run commands from the repository root.
- Review the diff and flow first; then review correctness, security, data, contracts, boundaries, and checks.
- A finding includes priority, file/line, condition, impact, and correction. If there are no findings, state residual risks and omitted checks.
