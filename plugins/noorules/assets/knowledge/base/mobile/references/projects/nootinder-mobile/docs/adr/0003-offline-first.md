# 0003. Offline-First data strategy

## Status

Proposed

## Context

Product features should remain usable with poor or no connectivity. The target architecture treats `RepositoryImpl` as SSOT over local DB, with remote sync when online. The stack target includes **Room** as the local database.

**Current code:** Room + `CachedRemoteRepository` already power profile / summit / history caches. Walkthrough: [../data-flow-offline-first.md](../data-flow-offline-first.md). This ADR still captures the intended product policy; keep it in sync as conflict/migration rules harden.

## Decision

**Intended Offline-First flow** (for features that opt in):

1. Screen reads via Repository.
2. Repository reads **Local DB** first and exposes that to the UI immediately.
3. If the device is online, fetch **Remote**, write into Local DB.
4. UI updates from the local source of truth (streams / refresh of cached data).

```text
Screen → Repository → Local DB → show user
                         ↓ (if online)
                      Remote → update DB
```

**Constraints:**

- Repository remains the SSOT boundary; UI and ViewModels do not call remote APIs for cached domain data.
- Room (or equivalent multiplatform DB already approved by the team) lives under core / data-source, not inside feature UI packages.
- Not every feature must be Offline-First from day one; choose explicitly when adding network+cache for a feature.
- Adding Room or a DB dependency requires confirmation (versions via `gradle/libs.versions.toml`).

## Consequences

- Better UX offline; more complexity (cache invalidation, conflict handling, migrations).
- Auth token storage stays separate from Room feature caches.
- Prefer extending `CachedRemoteRepository` + Room cache tables over inventing a second ad-hoc DB stack.
- Diagram: [../architecture/diagrams/03-stack-offline-multitenant.png](../../../../../assets/projects/nootinder-mobile/docs/architecture/diagrams/03-stack-offline-multitenant.png).
- How-to / end-to-end: [../data-flow-offline-first.md](../data-flow-offline-first.md).
