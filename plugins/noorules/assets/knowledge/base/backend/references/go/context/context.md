# Context

Nootinder is a layered Go/Fiber API with PostgreSQL, Redis, and private S3 storage.

## Domain model

- `User` is a global account and the user's primary profile.
- `Summit` is an event boundary: time, time zone, archived state, participants, and program.
- `SummitProfile` is both a user's summit membership and their summit-specific profile. Do not confuse it with the global `User`.
- `SummitInvitation` is a single-use credential; redeeming it creates a `SummitProfile`.
- `SummitProgram` is an event within a summit. Its host, attendees, and interested users are represented by profiles from that summit.
- `Dictionaries` are global reference data for `SummitProfile` and `SummitProgram`.

## Sources of truth

- Behavior: code; HTTP: `internal/presentation/openapi/openapi.yaml`.
- Schema: `migrations`; configuration: `internal/config/config.go`.
- Local environment: `.env.example`, `docker-compose.yml`.
- Commands and CI: `Makefile`, `.gitlab-ci.yml`.

The process neither loads `.env` nor runs migrations.
