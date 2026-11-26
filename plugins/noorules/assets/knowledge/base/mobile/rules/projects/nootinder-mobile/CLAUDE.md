# CLAUDE.md

You are working on **sovpa**: a Kotlin Multiplatform + Compose Multiplatform project (Android + iOS).

**Read and strictly follow [`docs/AGENTS.md`](docs/AGENTS.md)** before making changes.
Also use [`docs/architecture.md`](../../../references/projects/nootinder-mobile/docs/architecture.md) and [`docs/commands.md`](../../../references/projects/nootinder-mobile/docs/commands.md).

Architecture is still evolving. Prefer small, safe, reversible changes. Do not introduce large architectural refactors or new frameworks without explicit approval.

## Critical rules

- `commonMain` must stay platform-independent (no Android SDK / no iOS-only APIs).
- Android-only code → `androidMain`; iOS-only code → `iosMain`.
- Keep `expect`/`actual` declarations consistent across all platforms.
- Do not add dependencies without confirmation.
- Do not upgrade Kotlin / Compose Multiplatform / Gradle / AGP without confirmation.
- Use `gradle/libs.versions.toml` for versions; do not hardcode them.
- Prefer targeted Gradle tasks (`./scripts/check-fast.sh`) over `./gradlew build`.
- Do not run `./gradlew clean` by default.
- Run relevant tests after changes; do not delete failing tests.
- If iOS cannot be verified on this machine, say so explicitly.
- Do not commit secrets, `local.properties`, keystores, or API keys.
- Follow existing patterns; for a full feature slice prefer `feature-auth-*` as the reference.
- Do not add code comments or KDoc, even if nearby code has them; leave existing comments untouched unless asked.
