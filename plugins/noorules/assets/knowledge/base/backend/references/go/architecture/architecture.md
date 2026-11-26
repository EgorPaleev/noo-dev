# Architecture

## Dependencies

```text
cmd/api          -> presentation, application, infrastructure, config
presentation     -> application, domain
infrastructure   -> application ports/data, domain, config
application      -> domain, shared application contracts
domain           -> other domain packages
```

- `domain` and `application` must not import `presentation`, `infrastructure`, or `cmd`.
- Infrastructure implements consumer-owned application ports.
- Do not couple features solely to reuse an implementation.

## Boundaries

- `domain`: entities, normalization, invariants, and domain errors; no HTTP, SQL, environment, or SDK types.
- `application/<feature>`: use cases, data, and minimal outbound ports; no transport or adapters.
- `presentation`: routes, auth, decoding, validation, and HTTP mapping; no business logic or storage.
- `infrastructure`: PostgreSQL, Redis, S3, JWT, and server lifecycle; no HTTP contracts or use-case policy.
- `config`: environment parsing and validation; `cmd/api`: process lifecycle and dependency wiring.

## Invariants

- Pass the request `context.Context`; do not replace it with `context.Background()`.
- Declare the smallest interface in the consuming package; do not export adapter types.
- Keep transport DTOs in `internal/presentation/dto`.
- An expected error belongs to the package that defines its condition; only presentation maps it to HTTP.
- Keep SQL access in `sql/`, generated queries in `internal/infrastructure/postgres/queries`, row mapping in `internal/infrastructure/postgres/mapper`, and repository adapters in `internal/infrastructure/postgres/repository`; the pool is private to `postgres.Client`.
- Do not store a raw secret or identifier when a digest is sufficient.
- A repository owns the transaction for an atomic port operation.
- For a database and external system, preserve the current flow's ordering, compensation, and best-effort boundaries.

## Domain model

- Keep mutable aggregate state private; create or restore aggregates through explicit domain factories, never through struct literals outside the owning package.
- Keep commands/aggregates separate from flat read projections; never create partial aggregates for reads.
- Put pure business invariants in domain; keep checks that require external data or transaction state in adapters.
