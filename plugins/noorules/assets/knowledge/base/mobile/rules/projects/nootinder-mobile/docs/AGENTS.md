# AGENT.md

Single source of truth for coding agents (Cursor, Claude Code, and similar).
Also read [architecture.md](../../../../references/projects/nootinder-mobile/docs/architecture.md), [commands.md](../../../../references/projects/nootinder-mobile/docs/commands.md), and reusable automation prompts in [prompts/](../../../../../../navigation/1a84aff89f89ce27.md).

## Project overview

**sovpa** is a Kotlin Multiplatform project with Compose Multiplatform UI targeting **Android** and **iOS**.

The project is under active development. Architecture is **not final**. Prefer small, safe, reversible changes. Do not introduce large architectural frameworks or rewrites without explicit approval.

Primary goals for the agent:

- accelerate development;
- keep changes small and safe;
- avoid breaking cross-platform compatibility;
- verify changes with Gradle and tests;
- document non-trivial architectural decisions in `docs/adr/`.

## Tech stack

Versions live in `gradle/libs.versions.toml`. Do not hardcode versions in `build.gradle.kts`.

| Component | Notes |
|---|---|
| Kotlin | Multiplatform |
| Compose Multiplatform | Shared UI |
| Gradle Kotlin DSL + version catalog | Wrapper only: `./gradlew` |
| Koin | DI |
| Ktor | Networking |
| Navigation3 | App navigation in `:shared` |
| androidx.lifecycle ViewModel + StateFlow | Screen state |
| Targets | Android, iOS (`iosArm64`, `iosSimulatorArm64`) |
| Tests | `kotlin.test`, fakes in `commonTest`, Android host tests |

## Module map

| Module | Role |
|---|---|
| `:androidApp` | Android entry (`Application`, `MainActivity`) |
| `iosApp/` | Native iOS wrapper (Swift); hosts Compose via `Shared` framework |
| `:shared` | App shell: Compose host, Navigation3, Koin composition root, iOS `MainViewController` |
| `:core:presentation` | Theme, shared UI components, icons, camera/notification permissions (expect/actual) |
| `:core:test-utils` | Test helpers (dispatcher, sync/await) |
| `:features:feature-auth-api` | Auth contracts (entities, repository, use cases) |
| `:features:feature-auth-impl` | Auth UI, ViewModels, DI, repository impl; **most mature feature + real commonTest** |
| `:features:feature-summit-impl` | Summit UI (no api module yet) |
| `:features:feature-profile-api` | Placeholder (little/no commonMain code) |
| `:features:feature-profile-impl` | Profile / edit profile UI + VM + DI |
| `:features:feature-events-history-api` | History entity contracts |
| `:features:feature-events-history-impl` | Events history UI + VM + DI |
| `:features:feature-main-screen-api` | Placeholder |
| `:features:feature-main-screen-impl` | Main screen UI + VM + DI |
| `:data-source:network` | Ktor client, Auth/Profile/Summit APIs, Koin `networkModule` |
| `:data-source:local` | `TokenStorage` / `SecureTokenStorage` (expect/actual) |

Packages: app/shared use `ru.noosoft.sovpa`; features/data/core use `ru.sovpa.*`.

See [architecture.md](../../../../references/projects/nootinder-mobile/docs/architecture.md) for current patterns and open decisions.

## Source set rules

### commonMain

- Multiplatform-compatible code only.
- No `android.*` / platform Android SDK imports.
- No `androidx.*` unless the library is explicitly multiplatform-compatible and already used that way in the project.
- No `platform.UIKit` / iOS-only APIs.
- Prefer Compose Multiplatform APIs for shared UI.

### androidMain

- Android implementations, `Context`, Android resources/permissions, OkHttp engine, EncryptedSharedPreferences, etc.

### iosMain

- iOS / Kotlin Native implementations, Darwin engine, Keychain-style storage, `platform.*` interop.

### Tests

- Prefer `commonTest` + fakes for business logic (`:core:test-utils` when helpful).
- Android host tests: `androidHostTest` (task: `testAndroidHostTest`).
- Do not delete failing tests to make the build green.

## expect / actual

When changing an `expect` declaration, update **all** `actual` implementations (Android and iOS at minimum).

Known expect/actual areas today:

- `SecureTokenStorage`, `platformLocalModule` (`:data-source:local`)
- HTTP engine (`:data-source:network`)
- Camera / notification permission helpers (`:core:presentation`)
- `SoftInputAdjustResizeEffect` — режим клавиатуры окна Android, на iOS no-op (`:core:presentation`)
- `Platform` (`:shared`)

Never call platform-only APIs from `commonMain`; abstract via expect/actual or interfaces.

## Architecture status

Architecture is still evolving. **Current state + target vision** (modules, feature layers, Offline-First, multi-tenant): [architecture.md](../../../../references/projects/nootinder-mobile/docs/architecture.md). ADRs: [adr/](../../../../../../navigation/68b922d06aa8ea6a.md).

Agent must:

- follow existing patterns in the nearest similar feature (prefer **auth** as the reference);
- not impose Clean Architecture / new navigation / new DI stacks / Room / tenant theming without approval — move toward [architecture.md](../../../../references/projects/nootinder-mobile/docs/architecture.md) only when the task asks for it;
- if a pattern is missing, choose the **smallest consistent** option and ask when trade-offs are large;
- record important decisions in `docs/adr/`.

## Preferred code style

- Kotlin only (no Java unless explicitly requested).
- Prefer immutable state, small functions, constructor injection.
- Prefer interfaces for platform abstractions and repository contracts where the feature already uses them.
- Prefer fakes over heavy mocks in `commonTest`.
- Avoid global singletons unless already used.
- Keep business logic out of composables; put it in ViewModels / use cases / repositories.
- User-facing text goes to the feature's `composeResources/values/strings.xml` (no string literals in UI / ViewModel / Reducer); state holds `UiText`, `StringProvider` only for text needed outside Compose. See [ADR 0006](../../../../references/projects/nootinder-mobile/docs/adr/0006-localization-strings.md).
- Do not add code comments or KDoc to code you write or change, even if nearby code has them. Leave existing comments as they are unless asked to change them.

## Gradle rules

- Use **only** the wrapper: `./gradlew`.
- Prefer **targeted** tasks over `./gradlew build`.
- Do **not** run `./gradlew clean` unless needed to reproduce an issue.
- Do not change Kotlin, Compose Multiplatform, AGP, or Gradle versions without confirmation.
- Do not add new dependencies without confirmation; if approved, add versions via `gradle/libs.versions.toml`.
- Useful flags: `--console=plain`, on failure `--stacktrace`.

Command reference: [commands.md](../../../../references/projects/nootinder-mobile/docs/commands.md).

## Verification

After code changes, run relevant compile/test tasks and report exactly what ran.

Fast loop:

```bash
./scripts/check-fast.sh
```

Or manually:

```bash
./gradlew :features:feature-auth-impl:testAndroidHostTest --console=plain
./gradlew :androidApp:assembleDebug --console=plain
```

iOS (macOS + Xcode only):

```bash
./gradlew :shared:compileKotlinIosSimulatorArm64 --console=plain
./gradlew :shared:iosSimulatorArm64Test --console=plain
```

If the environment is not macOS, or Xcode is unavailable: **explicitly mark iOS as unverified**. Do not claim “everything works” after only Android/host checks.

## Definition of Done

A change is done only if:

- code compiles for affected targets that can be built here;
- relevant tests pass;
- KMP source sets are not polluted by platform-only code;
- expect/actual remain consistent;
- no secrets committed;
- non-trivial architectural impact is noted (ADR or response section).

## Forbidden actions

- Do not change Kotlin / Compose / Gradle / AGP versions without confirmation.
- Do not add dependencies without confirmation.
- Do not merge PRs or push to `main` / `develop` unless explicitly asked.
- Do not force-push or rewrite published history unless explicitly asked.
- Do not delete tests to green the build.
- Do not add code comments or KDoc.
- Do not modify signing config or commit `local.properties`, keystores, tokens, API keys.
- Do not use Android-only or iOS-only APIs in `commonMain`.
- Do not assume iOS passes if iOS was not built/tested.
- Do not run `./gradlew publish`, release bundles, or destructive `rm -rf` of project trees.

## Working cycle

1. Understand the task.
2. Find similar existing code (start with auth / same layer).
3. Read related modules and source sets.
4. Propose a minimal plan when the change is non-trivial.
5. Make a small change.
6. Run targeted Gradle tasks / tests.
7. Fix failures at the root cause.
8. Repeat.
9. Commit/PR only when asked, with a clear summary.

## Response format

When finishing a non-trivial change, structure the answer roughly as:

```md
## Summary
...

## Files changed
...

## Commands run
...

## Result
Android / host: pass|fail
iOS: verified|unverified (reason)

## Risks
...
```

## Adding a new feature

1. Find the closest existing feature (prefer `feature-auth-*`).
2. Reuse its structure (`api` contracts when present, `impl` for UI/VM/DI/data).
3. Register Koin modules in `:shared` composition root if needed.
4. Wire navigation destinations in `:shared` if the feature has screens.
5. Add tests for new business logic in `commonTest` when possible.
6. Do not invent new architectural layers unless necessary.
