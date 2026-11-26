# 0001. Modular feature api/impl split

## Status

In progress

## Context

The app is growing multiple product areas (auth, profile, main screen, events history, summit). We need a repeatable module boundary so shared contracts can be consumed without depending on UI implementations, while Compose screens stay isolated per feature.

The split is already present in Gradle (`feature-*-api` / `feature-*-impl`), but maturity differs by feature.

## Decision

**Observed / intended pattern (not a frozen law yet):**

- `feature-*-api` holds public contracts: entities, repository/use case interfaces when needed by other modules (**Domain** on the top-level diagram).
- `feature-*-impl` holds Compose UI, ViewModels, Koin modules, and data implementations (**Data** + **UI**).
- Core infrastructure (Network, Database, Navigation) is shared; features depend on core APIs, not on other features’ impl.
- `:shared` / app modules compose navigation and DI; they should not become a dumping ground for feature business logic.
- The reference vertical slice is **auth** (`feature-auth-api` + `feature-auth-impl` + tests).
- Internal layers inside a feature: [ADR 0002](0002-feature-layered-architecture.md).

**Current exceptions (allowed until cleaned up deliberately):**

- `feature-profile-api` and `feature-main-screen-api` are largely placeholders.
- `feature-summit-impl` has no api module yet.
- Not every feature must get a full use-case layer; match the nearest sibling unless building a shared contract.

## Consequences

- Agents should copy auth when introducing real contracts/tests.
- Do not mass-refactor all features to “perfect” api/impl in an unrelated task.
- When promoting a placeholder api or adding a missing api module, record follow-up here or in a new ADR and update [architecture.md](../architecture.md).
- Diagram: [../architecture/diagrams/01-modules-and-kmp.png](../../../../../assets/projects/nootinder-mobile/docs/architecture/diagrams/01-modules-and-kmp.png).
