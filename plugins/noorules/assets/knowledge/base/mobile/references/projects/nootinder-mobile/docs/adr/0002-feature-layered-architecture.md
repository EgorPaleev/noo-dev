# 0002. Feature layered architecture (Presentation / Domain / Data)

## Status

Proposed

## Context

We need a repeatable internal structure for features so UI, business rules, and data access stay separated, while still fitting the existing `feature-*-api` / `feature-*-impl` Gradle split ([ADR 0001](0001-modular-feature-api-impl.md)).

Team diagrams define a Clean Architecture–style feature slice with explicit mappers and a repository as SSOT. Auth already approximates this; other features are flatter.

## Decision

**Intended pattern for a mature feature:**

| Layer | Module | Contents |
|---|---|---|
| Presentation | `*-impl` | Compose UI, ViewModel + State, intents/events, VO, `MapperEntity2Vo` |
| Domain | `*-api` | Entity, UseCase interfaces, Repository interfaces |
| Data | `*-impl` | `RepositoryImpl` (SSOT), Dto, `MapperDto2Entity`, wiring to core Network/DB |
| Core | `data-source:*` / future `core:*` | Ktor client, DB, shared infra |

Control flow:

`UI → ViewModel → UseCaseImpl → UseCase → Repository → RepositoryImpl → Core (Ktor / DB)`

Mapping: **Dto → Entity → VO**. UI observes ViewModel state; it does not talk to repositories or APIs directly.

**Adoption rules:**

- Prefer this shape when adding real contracts/tests (copy **auth**).
- Do not force empty UseCase/Repository layers onto thin UI-only features in the same PR.
- No Compose, Ktor, or Room types in Domain (`*-api`).

## Consequences

- Clear place for tests (domain + repository with fakes).
- More boilerplate (mappers, api/impl) for small screens — accept only when the feature needs contracts or Offline-First.
- Follow-up: promote placeholder apis and summit when those features need shared contracts.
- Diagram: [../architecture/diagrams/02-feature-layers.png](../../../../../assets/projects/nootinder-mobile/docs/architecture/diagrams/02-feature-layers.png).
