# Commands

Use the Gradle wrapper only: `./gradlew`. Prefer targeted tasks. Do not run `clean` or full `build` unless necessary.

Also see [AGENTS.md](../../../../rules/projects/nootinder-mobile/docs/AGENTS.md).

## Environment

```bash
java -version
./gradlew --version
```

## Discover tasks

```bash
./gradlew tasks
./gradlew :shared:tasks --all
./gradlew :features:feature-auth-impl:tasks --all
./gradlew :androidApp:tasks --all
```

This project uses Android **host** tests (`testAndroidHostTest`), not classic `testDebugUnitTest` names from older Android app modules.

## Fast check (preferred for agents)

```bash
./scripts/check-fast.sh
```

Equivalent manual steps:

```bash
./gradlew :features:feature-auth-impl:testAndroidHostTest --console=plain
./gradlew :androidApp:assembleDebug --console=plain
```

`testAndroidHostTest` on `feature-auth-impl` runs the meaningful `commonTest` suite (ViewModels, repository, fakes) on the Android host.

## Full check

```bash
./scripts/check-full.sh
```

On macOS this also runs iOS simulator compile/tests for `:shared`. On other OS it reports iOS as unverified.

## Android

```bash
./gradlew :androidApp:assembleDebug --console=plain
./gradlew :androidApp:assembleRelease --console=plain
```

## Store release (signed)

Signing keys are never committed. Copy `keystore.properties.example` to `keystore.properties` in the project root and fill it in, or pass the same values as environment variables (`upload.store.file` → `SOVPA_UPLOAD_STORE_FILE`, `app.key.password` → `SOVPA_APP_KEY_PASSWORD`, etc.). Without keys, release builds are produced unsigned.

```bash
# Google Play: AAB signed with the upload key
./gradlew :androidApp:bundleProdRelease --console=plain

# RuStore: APK signed with the app signing key (same key as Play App Signing)
./gradlew :androidApp:assembleProdRelease -Psigning=rustore --console=plain
```

## Shared module tests / compile

```bash
./gradlew :shared:testAndroidHostTest --console=plain
./gradlew :shared:compileKotlinIosSimulatorArm64 --console=plain
```

## Feature tests (auth reference)

```bash
# Host + commonTest (fast, primary)
./gradlew :features:feature-auth-impl:testAndroidHostTest --console=plain

# All targets for the module (slower; includes iOS when available)
./gradlew :features:feature-auth-impl:allTests --console=plain

# Single test filter example
./gradlew :features:feature-auth-impl:testAndroidHostTest --tests '*LoginViewModelTest*' --console=plain
```

## iOS (macOS + Xcode only)

```bash
./gradlew :shared:compileKotlinIosSimulatorArm64 --console=plain
./gradlew :shared:iosSimulatorArm64Test --console=plain
./gradlew :features:feature-auth-impl:iosSimulatorArm64Test --console=plain
```

Run the iOS app from Xcode: open `iosApp/`.

If not on macOS, do not attempt these tasks; state that iOS is unverified.

## Useful flags

```bash
--console=plain
--stacktrace
--continue
```

## Avoid by default

```bash
./gradlew clean          # kills incremental builds
./gradlew build          # very heavy for KMP; use for CI / final checks only
```

## Static analysis

ktlint, detekt, and project-wide Android lint plugins are **not** configured as standard agent gates yet. Do not invent `./gradlew ktlintCheck` / `detekt` until they exist in the build.
