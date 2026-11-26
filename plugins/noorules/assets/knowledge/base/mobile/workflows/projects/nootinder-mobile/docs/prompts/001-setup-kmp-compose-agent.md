# 001. Setup KMP + Compose agent tooling

**Как использовать:** `@docs/prompts/001-setup-kmp-compose-agent.md` — выполнить Prompt ниже. В этом репо SSOT уже `docs/AGENTS.md` (в тексте ниже может быть `docs/AGENT.md` — это то же самое, дубликат не создавать). Модули/таски в примерах шаблонные — брать реальные из проекта.

---

## Prompt

Ок, теперь задача понятна: тебе нужен **универсальный агент для разработки KMP-проекта с Compose UI**, который работает в рамках кодовой базы, помогает писать код, запускать Gradle/тесты, ускорять разработку и не ломать проект. Ниже — схема, которая хорошо подходит и для **Cursor**, и для **Claude/Claude Code**, и для похожих agentic-инструментов.

Главная мысль:

> Для корректной работы агента важна не «магическая нейронка», а **подготовленный репозиторий + правила + контекст + инструменты + проверяемый цикл сборки/тестов + ограничения**.

Особенно для KMP, потому что там много неочевидных для LLM вещей: `commonMain`, `androidMain`, `iosMain`, `expect/actual`, разные Gradle-таски, платформенные зависимости, Compose Multiplatform, версии Kotlin/Compose, ограничения iOS-сборки и т.д.

---

# 1. Что нужно агенту для правильной работы

Для Cursor/Claude агенту нужны 5 вещей:

| Компонент | Зачем нужен |
|---|---|
| **Правила проекта** | Чтобы агент понимал стиль, архитектуру, запреты, соглашения |
| **Контекст проекта** | Чтобы он не выдумывал классы, модули, зависимости и API |
| **Инструменты** | Чтобы мог читать файлы, искать код, запускать Gradle, тесты, git |
| **Проверка результата** | Чтобы агент не говорил «я всё сделал», а доказывал сборкой и тестами |
| **Ограничения** | Чтобы не удалял лишнее, не менял версии, не ломал KMP/Gradle/секреты |

Если чего-то из этого нет, агент начинает:
- выдумывать несуществующие модули;
- использовать Android-only API в `commonMain`;
- ломать `expect/actual`;
- добавлять зависимости, которые не работают в KMP;
- запускать слишком тяжёлые Gradle-таски;
- чинить Android, ломая iOS;
- предлагать архитектуру, которая не совпадает с текущей.

---

# 2. Универсальный подход для Cursor и Claude

У разных инструментов разные файлы правил:

- Cursor обычно читает:
  - `.cursorrules`
  - или `.cursor/rules/*.md` / `*.mdc`, в зависимости от версии
- Claude Code обычно читает:
  - `CLAUDE.md`
- Многие agentic-инструменты понимают:
  - `AGENTS.md`

Чтобы не дублировать одно и то же в трёх местах, сделай **единый источник истины**:

```text
docs/AGENT.md
```

А уже Cursor/Claude будут на него ссылаться.

Например:

```md
# CLAUDE.md

Read and strictly follow `docs/AGENT.md` before making changes.
This project is Kotlin Multiplatform + Compose Multiplatform.
Do not assume Android-only patterns unless explicitly working in androidMain.
```

И аналогично:

```md
# .cursorrules

Read and strictly follow `docs/AGENT.md` before making changes.
This project is Kotlin Multiplatform + Compose Multiplatform.
Do not assume Android-only patterns unless explicitly working in androidMain.
```

Лучше, если `.cursorrules` и `CLAUDE.md` содержат хотя бы краткие правила напрямую, а не только ссылку. Потому что некоторые агенты могут не всегда автоматически читать внешние файлы.

Самый надёжный вариант:

```text
docs/AGENT.md        # основной подробный документ
CLAUDE.md            # краткие правила + ссылка на docs/AGENT.md
.cursorrules         # краткие правила + ссылка на docs/AGENT.md
```

Или сделать симлинки, если удобно:

```bash
ln -s docs/AGENT.md CLAUDE.md
ln -s docs/AGENT.md .cursorrules
```

Но на Windows с симлинками могут быть проблемы, поэтому часто проще хранить краткие копии или генерировать их скриптом.

---

# 3. Что должно быть в репозитории, чтобы агент работал хорошо

## 3.1. `docs/AGENT.md`

Это главный файл для агента. В нём должно быть:

- что это за проект;
- какой стек;
- какие модули есть;
- какая архитектура сейчас;
- что пока не определено;
- какие команды запускать;
- какие тесты запускать;
- что нельзя менять;
- как агент должен проверять результат.

Для твоего случая: KMP, Compose, архитектура в процессе, Gradle и тесты разрешены.

---

## 3.2. `docs/architecture.md`

Так как архитектура ещё не готова, агенту особенно важно знать **текущее состояние**, а не выдумывать идеальную архитектуру.

Опиши:

- какие модули существуют;
- какой у них смысл;
- где UI;
- где бизнес-логика;
- где сеть;
- где хранение;
- где платформенный код;
- какие паттерны уже используются;
- какие решения ещё не приняты.

Пример:

```md
# Architecture status

Architecture is still evolving.

Current state:
- shared module contains common domain logic
- composeApp contains Compose Multiplatform UI
- Android-specific code goes to androidMain
- iOS-specific code goes to iosMain
- no final navigation solution selected yet
- repository pattern is used partially

Agent rules:
- do not introduce heavy architecture frameworks without explicit approval
- prefer small, reversible changes
- if a pattern is missing, propose the simplest consistent option
- document architectural decisions in docs/adr
```

Почему это важно:

> Если архитектура не описана, агент начнёт приносить кто в лес кто по дрова: сегодня Clean Architecture, завтра MVI, завтра MVVM, завтра просто гигантские ViewModel.

---

## 3.3. `docs/adr/`

ADR = Architecture Decision Records.

Очень полезно для проекта, который ещё формируется.

Пример структуры:

```text
docs/adr/
  0001-use-kotlin-multiplatform.md
  0002-use-compose-multiplatform.md
  0003-navigation-approach.md
  0004-state-management.md
  0005-network-layer.md
```

Шаблон:

```md
# 0004. State management

## Status
Proposed / Accepted / Deprecated

## Context
We need a simple way to manage UI state in Compose Multiplatform screens.

## Decision
Use unidirectional state with screen state holder and events.

## Consequences
- simple to test
- no heavy framework required
- may need migration if navigation/state becomes complex
```

Почему это важно:

> Агент должен понимать, какие решения уже приняты, а какие ещё нет. Иначе он будет «оптимизировать» проект против вашей текущей стратегии.

---

## 3.4. `docs/commands.md`

Отдельный файл с командами для агента и разработчиков.

Например:

```md
# Commands

## Environment
./gradlew --version

## Discover tasks
./gradlew tasks

## Android app build
./gradlew :composeApp:assembleDebug

## Shared tests
./gradlew :shared:testDebugUnitTest
./gradlew :shared:jvmTest

## iOS tests, only on macOS with Xcode
./gradlew :shared:iosSimulatorArm64Test

## Lint Android
./gradlew :composeApp:lintDebug

## Static analysis
./gradlew ktlintCheck
./gradlew detekt
```

Почему это важно:

> KMP-проекты имеют разные таски в разных проектах. Агент не должен гадать. Лучше дать ему проверенные команды.

---

## 3.5. `scripts/check.sh` или `scripts/check-fast.sh`

Агенту нужна быстрая петля проверки.

Плохо:

```bash
./gradlew build
```

Для KMP это может быть очень долго: Android, iOS, metadata, все таски, lint, тесты и т.д.

Лучше сделать отдельные скрипты.

Например:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Running fast checks"

./gradlew --version

# Replace module names with actual module names
./gradlew :shared:testDebugUnitTest --console=plain
./gradlew :composeApp:assembleDebug --console=plain
```

И отдельный полный:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Running full checks"

./gradlew :shared:testDebugUnitTest --console=plain
./gradlew :composeApp:assembleDebug --console=plain
./gradlew :composeApp:lintDebug --console=plain
./gradlew ktlintCheck --console=plain
./gradlew detekt --console=plain
```

Почему это важно:

> Агент должен быстро получать сигнал: сломал он что-то или нет. Если каждая проверка занимает 20 минут, разработка замедлится, а агент будет делать слишком большие изменения.

---

# 4. Особенности KMP, которые агент должен понимать

Это критичный раздел.

## 4.1. Source sets

В KMP код живёт в разных source sets:

```text
shared/src/commonMain/...
shared/src/androidMain/...
shared/src/iosMain/...
shared/src/commonTest/...
shared/src/androidUnitTest/...
shared/src/iosTest/...
```

Агент должен понимать:

| Source set | Что туда можно класть |
|---|---|
| `commonMain` | Только общий код, без Android/iOS-specific API |
| `androidMain` | Android-код, `Context`, Android SDK, `SharedPreferences` и т.д. |
| `iosMain` | iOS-код, `platform.UIKit`, `NSUserDefaults`, Kotlin/Native specifics |
| `commonTest` | Общие тесты |
| `androidUnitTest` / `androidAndroidTest` | Android-тесты |
| `iosTest` | iOS-тесты |

Главное правило:

> В `commonMain` нельзя использовать `android.*`, `androidx.*`, если это не multiplatform-совместимо, и нельзя использовать iOS-specific API.

Пример плохой идеи в `commonMain`:

```kotlin
import android.content.Context
```

Или:

```kotlin
import platform.UIKit.UIViewController
```

Это должно быть в `androidMain` / `iosMain` или через `expect/actual`.

---

## 4.2. `expect/actual`

Агент должен аккуратно работать с `expect/actual`.

Пример:

```kotlin
// commonMain
expect class PlatformLogger() {
    fun log(tag: String, message: String)
}
```

```kotlin
// androidMain
actual class PlatformLogger {
    actual fun log(tag: String, message: String) {
        android.util.Log.d(tag, message)
    }
}
```

```kotlin
// iosMain
actual class PlatformLogger {
    actual fun log(tag: String, message: String) {
        println("$tag: $message")
    }
}
```

Типичные ошибки агента:
- добавил `expect`, но забыл `actual`;
- добавил `actual` только для Android;
- поменял signature в `expect`, не поменяв `actual`;
- пытается использовать платформенную реализацию из `commonMain`.

Правило в `AGENT.md`:

```text
When changing expect/actual declarations, always update all platform implementations.
Never add platform-specific imports to commonMain.
```

---

## 4.3. Зависимости в KMP

Агент должен понимать, что не всякая библиотека может быть добавлена в `commonMain`.

Правила:

- В `commonMain` добавлять только multiplatform-совместимые зависимости.
- Android-only библиотеки — в `androidMain` или Android-модуль.
- iOS-only вещи — в `iosMain`.
- Версии зависимостей держать в `gradle/libs.versions.toml`.
- Не добавлять новые зависимости без подтверждения.

Пример:

```toml
# gradle/libs.versions.toml

[versions]
kotlin = "..."
compose-multiplatform = "..."
coroutines = "..."

[libraries]
kotlinx-coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }
```

Почему это важно:

> LLM часто предлагает популярные Android-библиотеки, не понимая, что они не работают в KMP commonMain.

---

## 4.4. Compose Multiplatform

Для Compose Multiplatform агент должен различать:

- общий Compose UI;
- Android-specific Compose;
- платформенные ресурсы;
- навигацию;
- lifecycle;
- insets / safe area;
- permissions.

Правила:

```text
Use Compose Multiplatform APIs in common UI unless task is Android-specific.
Do not use Android R resources directly in commonMain.
Use project resource generation / Res APIs if configured.
Do not mix Android-only navigation APIs into common code.
```

Если у вас Compose Multiplatform, важно не путать:
- `org.jetbrains.compose`
- `androidx.compose`
- multiplatform-версии библиотек
- Android-only реализации

Правило:

```text
Do not change Kotlin, Compose Multiplatform, AGP, Gradle versions unless explicitly asked.
Versions compatibility is fragile.
```

---

## 4.5. iOS-ограничения

Если проект таргетируется на iOS:

- iOS-сборка обычно требует macOS + Xcode.
- На Linux/Windows iOS-таски могут не работать.
- Агент не должен считать сборку успешной для iOS, если он не мог собрать iOS.

Правило:

```text
If running on non-macOS environment, do not attempt iOS build/test tasks.
If iOS verification is impossible, explicitly state that iOS changes are unverified.
```

Это очень важно, потому что агент может сказать:
> «Всё работает»

а на самом деле он собрал только Android/JVM/metadata.

---

# 5. Gradle: что нужно агенту

## 5.1. Gradle Wrapper

Агент должен использовать только wrapper:

```bash
./gradlew
```

а не глобальный `gradle`.

Потому что версия Gradle должна совпадать с проектом.

---

## 5.2. `gradle/libs.versions.toml`

Все версии лучше держать здесь.

Правило агенту:

```text
All dependency versions must be taken from gradle/libs.versions.toml.
Do not hardcode versions in build.gradle.kts files.
```

---

## 5.3. Быстрые и полные проверки

Для скорости агенту лучше не запускать каждый раз:

```bash
./gradlew build
```

Вместо этого использовать целевые таски.

Например:

| Цель | Команда |
|---|---|
| Проверить, что Android app собирается | `./gradlew :composeApp:assembleDebug` |
| Прогнать unit-тесты shared-модуля для Android | `./gradlew :shared:testDebugUnitTest` |
| Прогнать JVM-тесты, если есть JVM target | `./gradlew :shared:jvmTest` |
| Проверить iOS simulator tests | `./gradlew :shared:iosSimulatorArm64Test` |
| Android lint | `./gradlew :composeApp:lintDebug` |
| Статический анализ | `./gradlew ktlintCheck` / `./gradlew detekt` |
| Посмотреть доступные таски | `./gradlew tasks` |

Имена модулей нужно заменить на ваши.

Например, у вас может быть не `:composeApp`, а `:app`, `:androidApp`, `:mobileApp` и т.д.

---

## 5.4. Полезные флаги Gradle

Для агента удобно:

```bash
--console=plain
```

Чтобы логи были проще для чтения.

При ошибках:

```bash
--stacktrace
```

Иногда:

```bash
--continue
```

чтобы собрать несколько ошибок за один запуск.

Пример:

```bash
./gradlew :shared:testDebugUnitTest --console=plain --stacktrace
```

---

## 5.5. Не чистить проект без необходимости

Агент не должен по умолчанию делать:

```bash
./gradlew clean
```

Потому что это замедляет разработку и убивает инкрементальную сборку.

Правило:

```text
Do not run clean unless explicitly required to reproduce an issue.
Prefer incremental builds.
```

---

# 6. Тесты: как агенту проверять изменения

Для KMP-проекта тесты особенно важны, потому что изменения могут сломать несколько платформ.

## Минимальный набор

### Общие тесты

В `commonTest`:

```kotlin
import kotlin.test.Test
import kotlin.test.assertEquals

class SomeUseCaseTest {
    @Test
    fun test() {
        assertEquals(2, 1 + 1)
    }
}
```

Там лучше использовать:
- `kotlin-test`;
- `kotlinx-coroutines-test`;
- `Turbine` для Flow, если используете;
- фейки вместо тяжёлых моков;
- минимум платформенных зависимостей.

Почему фейки лучше в commonTest:

> Не все mock-библиотеки одинаково хорошо работают во всех KMP-таргетах. Фейки проще и переносимее.

---

### Android unit tests

Если есть Android-specific логика:

```text
shared/src/androidUnitTest/
```

или

```text
app/src/test/
```

Там можно использовать:
- JUnit;
- MockK, если он уместен;
- Robolectric, если нужен Android framework без эмулятора.

---

### UI tests

Пока проект ранний, не обязательно сразу строить тяжёлые UI-тесты.

Но если агент будет менять UI, полезно иметь хотя бы:
- smoke-тесты экранов;
- snapshot/screenshot тесты, если настроены;
- compose UI tests для критичных компонентов.

Для Compose Multiplatform UI-тестирование может быть сложнее, чем обычный Android Compose, поэтому лучше начинать с unit-тестов логики.

---

# 7. Правила для агента в KMP + Compose проекте

Вот базовый набор правил, который стоит положить в `docs/AGENT.md`.

```md
# Agent rules

You are working on a Kotlin Multiplatform project with Compose Multiplatform UI.

Project state:
- architecture is still evolving;
- do not introduce large architectural changes without explicit approval;
- prefer small, safe, reversible changes;
- if a pattern is missing, propose the simplest option consistent with existing code.

General rules:
- Use Kotlin.
- Do not use Java unless explicitly requested.
- Do not add new dependencies without confirmation.
- Do not change Kotlin, Compose Multiplatform, Gradle, AGP versions without confirmation.
- Do not hardcode dependency versions; use gradle/libs.versions.toml.
- Do not commit secrets, local.properties, keystores, API keys.
- Do not remove existing public APIs unless explicitly requested.
- Do not run `./gradlew clean` unless necessary.

KMP rules:
- commonMain must not contain android.*, androidx.* unless the library is explicitly multiplatform-compatible.
- commonMain must not contain iOS-specific imports.
- Platform-specific code must be placed in androidMain, iosMain or other platform source sets.
- When changing expect declarations, update all actual implementations.
- When adding a library to commonMain, verify that it supports all required targets.
- If a change affects iOS but iOS cannot be built in current environment, mark iOS as unverified.

Compose rules:
- Use Compose Multiplatform APIs for common UI.
- Do not use Android-only Compose APIs in common UI unless explicitly working in Android app.
- Keep UI state unidirectional where possible.
- Move strings/resources to resource files instead of hardcoding.
- Avoid heavy object creation inside composables.
- Use remember/derivedStateOf only when appropriate.

Testing rules:
- New business logic should have tests in commonTest when possible.
- Platform-specific logic should have platform tests where appropriate.
- Prefer fakes over platform-specific mocking in commonTest.
- Do not delete failing tests just to make build pass.
- If test fails, analyze the failure and fix root cause.

Verification:
- After code changes, run the relevant compile/test tasks.
- Prefer targeted Gradle tasks instead of full build.
- Report exactly which commands were run and their results.
```

---

# 8. Шаблон `docs/AGENT.md` под твой случай

Ниже — практический шаблон. Его можно адаптировать под ваши названия модулей.

```md
# AGENT.md

## Project overview

This is a Kotlin Multiplatform project with Compose Multiplatform UI.
The project is under active development and architecture is not final yet.

Primary goals for the agent:
- accelerate development;
- keep changes small and safe;
- avoid breaking cross-platform compatibility;
- verify changes with Gradle and tests;
- document uncertain architectural decisions.

## Tech stack

- Kotlin Multiplatform
- Compose Multiplatform
- Gradle Kotlin DSL
- Version catalog: gradle/libs.versions.toml
- Targets: Android, iOS, possibly JVM/desktop
- Tests: kotlin.test, coroutines-test, platform-specific tests where needed

## Current module map

Replace with actual modules.

- :shared — common logic, domain, data, platform abstractions
- :composeApp — Compose Multiplatform application
- :iosApp — native iOS app wrapper, if exists

## Source set rules

### commonMain
- only multiplatform-compatible code
- no android.*
- no androidx.* unless explicitly multiplatform-compatible
- no platform.UIKit
- no iOS/Native specific APIs

### androidMain
- Android implementations
- Context-based code
- Android resources
- Android permissions

### iosMain
- iOS implementations
- platform.*
- Kotlin/Native specific code
- interop with Swift/Objective-C where required

## Architecture status

Architecture is still evolving.

Agent must:
- not impose a heavy final architecture if not asked;
- follow existing patterns;
- if pattern is absent, choose the simplest consistent approach;
- record important decisions in docs/adr;
- avoid premature overengineering.

## Preferred code style

- Kotlin only.
- Prefer immutable state.
- Prefer small functions.
- Prefer constructor injection.
- Prefer interfaces for platform abstractions.
- Prefer fakes in commonTest.
- Avoid global singletons unless already used.
- Avoid business logic inside UI composables.
- Keep UI state and side effects explicit.

## Gradle rules

Use Gradle wrapper only:

```bash
./gradlew
```

Do not use global gradle.

Prefer targeted tasks:

```bash
./gradlew :shared:testDebugUnitTest --console=plain
./gradlew :composeApp:assembleDebug --console=plain
```

Use full build only when necessary:

```bash
./gradlew build
```

Do not run clean by default.

## Verification commands

Android debug build:

```bash
./gradlew :composeApp:assembleDebug --console=plain
```

Shared Android unit tests:

```bash
./gradlew :shared:testDebugUnitTest --console=plain
```

JVM tests, if JVM target exists:

```bash
./gradlew :shared:jvmTest --console=plain
```

iOS simulator tests, only on macOS:

```bash
./gradlew :shared:iosSimulatorArm64Test --console=plain
```

Lint Android:

```bash
./gradlew :composeApp:lintDebug --console=plain
```

Static analysis:

```bash
./gradlew ktlintCheck --console=plain
./gradlew detekt --console=plain
```

## Definition of Done

A change is done only if:
- code compiles for affected targets;
- relevant tests pass;
- no new lint/static analysis errors;
- KMP source sets are not polluted by platform code;
- expect/actual declarations remain consistent;
- no secrets are added;
- architectural impact is documented if non-trivial.

## Forbidden actions

- do not change Kotlin/Compose/Gradle/AGP versions without confirmation;
- do not add new dependencies without confirmation;
- do not merge PRs;
- do not push directly to main/develop;
- do not delete tests to make build green;
- do not modify signing config;
- do not commit local.properties, keystores, tokens, API keys;
- do not use Android-only APIs in commonMain;
- do not assume iOS build passes if iOS cannot be built locally.
```

---

# 9. Краткие правила для `.cursorrules`

Для Cursor можно сделать компактный файл.

```md
# Cursor rules

Read and follow `docs/AGENT.md`.

This is a Kotlin Multiplatform + Compose Multiplatform project.
Architecture is still evolving. Prefer small, safe changes.

Important rules:
- Do not use Android-only APIs in commonMain.
- Do not use iOS-only APIs in commonMain.
- Use expect/actual carefully and update all platforms.
- Do not add dependencies without confirmation.
- Do not change Kotlin, Compose, Gradle, AGP versions without confirmation.
- Use gradle/libs.versions.toml for versions.
- Prefer targeted Gradle tasks instead of full build.
- Run relevant tests after changes.
- If iOS build/test cannot run in current environment, mark iOS as unverified.
- Do not delete failing tests.
- Do not introduce heavy architecture changes without approval.
```

Если Cursor поддерживает rules-файлы в `.cursor/rules`, можно положить туда же:

```text
.cursor/rules/kmp-agent.md
```

---

# 10. Краткие правила для `CLAUDE.md`

```md
# CLAUDE.md

You are working on a Kotlin Multiplatform + Compose Multiplatform project.
Read and follow `docs/AGENT.md`.

Critical rules:
- commonMain must remain platform-independent.
- Android-only code goes to androidMain.
- iOS-only code goes to iosMain.
- Keep expect/actual declarations consistent.
- Do not add dependencies without confirmation.
- Do not upgrade Kotlin/Compose/Gradle versions without confirmation.
- Prefer targeted Gradle tasks.
- Run tests after changes.
- If iOS cannot be verified on this machine, explicitly say so.
- Architecture is not final; avoid large unsolicited refactors.
```

---

# 11. Как агент должен ускорять разработку

Чтобы агент реально ускорял, а не создавал хаос, он должен работать по чёткому циклу.

## Правильный цикл

```text
1. Понять задачу
2. Найти существующий похожий код
3. Прочитать связанные модули
4. Предложить минимальный план
5. Сделать маленькое изменение
6. Запустить релевантный Gradle task
7. Запустить тесты
8. Починить ошибки
9. Повторить
10. Сделать commit/PR с описанием
```

Плохой цикл:

```text
Задача → сразу переписать полпроекта → сборка упала → агент не понимает почему
```

Хороший цикл:

```text
Задача → найти контекст → маленький diff → тесты → фикс → следующий шаг
```

---

# 12. Как агенту работать с незавершённой архитектурой

Это очень важный момент.

Если архитектура ещё не готова, агент не должен:
- сразу тащить Clean Architecture на 20 слоёв;
- добавлять тяжёлые фреймворки;
- переписывать навигацию;
- менять DI без необходимости;
- создавать параллельные архитектурные системы.

Вместо этого агент должен:

1. Искать текущий стиль в коде.
2. Следовать ему.
3. Если стиля нет — предлагать минимально простой.
4. Фиксировать решения в ADR.
5. Не делать необратимых архитектурных изменений без запроса.

Хорошая формулировка в правилах:

```md
If architecture is unclear, do not invent a new global architecture.
Choose the smallest consistent solution that fits existing code.
If multiple approaches exist, list trade-offs and ask which one to use.
```

---

# 13. Что агенту делать при добавлении новой фичи

Для ускорения разработки хорошо иметь шаблон фичи.

Например:

```text
feature/
  some-feature/
    src/commonMain/kotlin/
      ui/
      state/
      domain/
      data/
```

Но пока проект маленький, можно проще:

```text
screens/
  profile/
    ProfileScreen.kt
    ProfileScreenState.kt
    ProfileEvents.kt
    ProfileRepository.kt
```

Агенту можно дать правило:

```md
When adding a new feature:
1. Find existing similar feature.
2. Reuse its structure.
3. Do not create new architectural layers unless necessary.
4. Add tests for new business logic.
5. Keep UI dumb where possible.
```

---

# 14. Какие команды Gradle должны быть у агента

Ниже — практический набор. Названия модулей нужно подставить ваши.

## Посмотреть окружение

```bash
java -version
./gradlew --version
```

Зачем:
- агент понимает JDK;
- понимает версию Gradle;
- видит, что wrapper работает.

---

## Посмотреть таски

```bash
./gradlew tasks
```

или:

```bash
./gradlew :shared:tasks
```

Зачем:
- KMP-проекты разные;
- агент не должен угадывать таски.

---

## Быстрая проверка Android UI

```bash
./gradlew :composeApp:assembleDebug --console=plain
```

Зачем:
- быстро проверить, что UI-модуль собирается.

---

## Проверка shared-логики

Варианты:

```bash
./gradlew :shared:testDebugUnitTest --console=plain
```

или, если есть JVM target:

```bash
./gradlew :shared:jvmTest --console=plain
```

или, если нужно собрать только metadata/common:

```bash
./gradlew :shared:assemble --console=plain
```

Но точные таски лучше discover через:

```bash
./gradlew :shared:tasks
```

---

## Проверка iOS

Только на macOS с Xcode:

```bash
./gradlew :shared:iosSimulatorArm64Test --console=plain
```

или compile:

```bash
./gradlew :shared:compileKotlinIosSimulatorArm64 --console=plain
```

Зачем:
- агент должен понимать, когда iOS действительно проверен, а когда нет.

---

## Линт и статический анализ

Android lint:

```bash
./gradlew :composeApp:lintDebug --console=plain
```

Ktlint:

```bash
./gradlew ktlintCheck --console=plain
```

Detekt:

```bash
./gradlew detekt --console=plain
```

---

# 15. Как ускорить Gradle для агента и разработчиков

Агент будет быстрее, если Gradle быстрее.

## 15.1. `gradle.properties`

Разумные настройки:

```properties
org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true
kotlin.incremental=true
```

Но configuration-cache может быть несовместим с некоторыми плагинами, поэтому включать аккуратно.

Почему это важно:

> Если каждая сборка долгая, агент будет делать меньше итераций и хуже проверять свои изменения.

---

## 15.2. Не гонять `build` без необходимости

Для быстрой обратной связи лучше:

```bash
./gradlew :shared:testDebugUnitTest
./gradlew :composeApp:assembleDebug
```

А полный:

```bash
./gradlew build
```

оставить для CI или финальной проверки.

---

## 15.3. Использовать тестовые фильтры

Если агент чинит один тест:

```bash
./gradlew :shared:testDebugUnitTest --tests "com.example.SomeTest"
```

Это намного быстрее, чем весь тестовый набор.

---

# 16. Что должно быть в `.gitignore` / ignore для агента

Чтобы Cursor/Claude не тянули в контекст мусор, исключай:

```text
build/
.gradle/
.kotlin/
local.properties
*.keystore
*.jks
secrets/
xcuserdata/
DerivedData/
*.hprof
captures/
```

Для Cursor можно дополнительно использовать `.cursorignore`, если поддерживается:

```text
build/
.gradle/
.kotlin/
local.properties
*.keystore
*.jks
secrets/
xcuserdata/
DerivedData/
```

Почему важно:

> Индексация build-артефактов загрязняет контекст, увеличивает расход токенов и может заставить агента ссылаться на сгенерированные файлы.

---

# 17. Безопасность и ограничения

Агенту можно разрешать Gradle и тесты, но нужно ограничивать опасные действия.

## Разрешить:

```text
read files
edit files
run ./gradlew assembleDebug
run ./gradlew testDebugUnitTest
run ./gradlew lintDebug
run git status
run git diff
run git add
run git commit
```

## Не разрешать без человека:

```text
git push origin main
git push --force
rm -rf
./gradlew publish
./gradlew bundleRelease
./gradlew clean (по умолчанию)
changing signing config
adding production secrets
changing Kotlin/Compose/Gradle versions
merging PRs
deleting modules
```

Для Claude Code, если версия поддерживает permissions, можно настроить allow/deny. Но даже если не поддерживает, просто пропиши запреты в `CLAUDE.md`.

Для Cursor — аналогично через rules и ручное подтверждение команд.

---

# 18. Как настроить модель/режим агента

## Для архитектуры и сложных задач

Лучше использовать более сильную модель и режим планирования.

Пример:
- Claude Sonnet/Opus для планирования и сложных изменений;
- более быстрая модель для мелких правок, если есть.

## Температура

Для кода лучше низкая:

```text
temperature: 0.0–0.2
```

Для архитектурных brainstorm можно выше, но для реализации лучше ниже.

## Контекст

Не давай агенту весь проект сразу.

Лучше:
- конкретная задача;
- список модулей;
- 5–20 релевантных файлов;
- ошибки сборки;
- правила проекта.

В Cursor лучше явно указывать файлы через `@Files`, особенно в KMP, потому что `@Codebase` может подтянуть не тот source set.

Например:

```text
@shared/src/commonMain/kotlin/.../AuthRepository.kt
@shared/src/androidMain/kotlin/.../AuthRepository.android.kt
@shared/src/iosMain/kotlin/.../AuthRepository.ios.kt
```

---

# 19. Как должен выглядеть хороший запрос к агенту

Плохо:

> Сделай авторизацию.

Хорошо:

> Нужно добавить экран входа.
> Сначала прочитай `docs/AGENT.md`, `docs/architecture.md` и найди существующие экраны.
> Предложи минимальный план без новой архитектуры.
> Изменения делай в `feature/auth`.
> Общую логику клади в `commonMain`, платформенные вещи в `androidMain`/`iosMain`.
> После изменений запусти `./gradlew :shared:testDebugUnitTest` и `./gradlew :composeApp:assembleDebug`.
> Если iOS проверить нельзя, явно скажи это.

---

# 20. Формат ответа агента

Хороший агент должен отвечать примерно так:

```md
## Summary
Добавил репозиторий авторизации в shared-модуль.

## Plan
1. Нашел существующие репозитории.
2. Добавил AuthRepository в commonMain.
3. Добавил platform implementations в androidMain/iosMain.
4. Добавил тест в commonTest.

## Files changed
- shared/src/commonMain/kotlin/.../AuthRepository.kt
- shared/src/androidMain/kotlin/.../AuthRepository.android.kt
- shared/src/iosMain/kotlin/.../AuthRepository.ios.kt
- shared/src/commonTest/kotlin/.../AuthRepositoryTest.kt

## Commands run
./gradlew :shared:testDebugUnitTest --console=plain
./gradlew :composeApp:assembleDebug --console=plain

## Result
Android build passed, shared tests passed.
iOS not verified because current environment is not macOS.

## Risks
- нужно проверить реальный token storage;
- нужно решить, используем ли we secure storage.
```

Это намного лучше, чем:

> Готово, всё работает.

---

# 21. Что особенно важно для KMP-агента

Короткий список самых важных запретов:

```text
Не используй android.* в commonMain.
Не используй iOS API в commonMain.
Не ломай expect/actual.
Не добавляй Android-only зависимости в commonMain.
Не меняй версии Kotlin/Compose/Gradle без спроса.
Не считай iOS проверенным, если iOS-сборка не запускалась.
Не гоняй ./gradlew build для каждой мелочи.
Не удаляй тесты ради зелёной сборки.
Не вноси глобальную архитектуру без запроса.
```

---

# 22. Минимальный набор файлов, который стоит сделать прямо сейчас

Я бы начал с этого:

```text
docs/AGENT.md
docs/architecture.md
docs/commands.md
CLAUDE.md
.cursorrules
scripts/check-fast.sh
scripts/check-full.sh
gradle/libs.versions.toml
.editorconfig
```

Опционально:

```text
docs/adr/
.cursorignore
.clinerules
.github/workflows/ci.yml
```

---

# 23. Пример `scripts/check-fast.sh`

Важно: команды нужно заменить на реальные таски вашего проекта.

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Environment:"
java -version
./gradlew --version

echo "Fast check started"

# Replace module names with actual ones
./gradlew :shared:testDebugUnitTest --console=plain
./gradlew :composeApp:assembleDebug --console=plain

echo "Fast check finished"
```

Сделать исполняемым:

```bash
chmod +x scripts/check-fast.sh
```

Почему это полезно:

> Агент может запускать одну понятную команду вместо того чтобы каждый раз выбирать Gradle-таски вслепую.

---

# 24. Пример `docs/commands.md`

```md
# Commands

## Environment

```bash
java -version
./gradlew --version
```

## Discover tasks

```bash
./gradlew tasks
./gradlew :shared:tasks
./gradlew :composeApp:tasks
```

## Fast check

```bash
./scripts/check-fast.sh
```

## Android build

```bash
./gradlew :composeApp:assembleDebug --console=plain
```

## Shared tests

```bash
./gradlew :shared:testDebugUnitTest --console=plain
```

## iOS tests, macOS only

```bash
./gradlew :shared:iosSimulatorArm64Test --console=plain
```

## Lint

```bash
./gradlew :composeApp:lintDebug --console=plain
```

## Static analysis

```bash
./gradlew ktlintCheck --console=plain
./gradlew detekt --console=plain
```
```

---

# 25. Чек-лист для твоего проекта

Проверь, что есть:

## Репозиторий

- [ ] `README.md`
- [ ] `docs/AGENT.md`
- [ ] `docs/architecture.md`
- [ ] `docs/commands.md`
- [ ] `docs/adr/` для решений
- [ ] `gradle/libs.versions.toml`
- [ ] Gradle wrapper
- [ ] `.gitignore` без секретов
- [ ] `.cursorrules`
- [ ] `CLAUDE.md`

## KMP

- [ ] commonMain не содержит Android-only кода
- [ ] androidMain содержит Android-only код
- [ ] iosMain содержит iOS-only код
- [ ] `expect/actual` синхронизированы
- [ ] зависимости в commonMain действительно multiplatform
- [ ] iOS-сборка явно помечается как unverified, если агента нет на macOS

## Gradle

- [ ] есть быстрые таски проверки
- [ ] есть полные таски проверки
- [ ] агент не запускает `build` без необходимости
- [ ] агент не делает `clean` без необходимости
- [ ] включены parallel/caching, если не ломают сборку

## Тесты

- [ ] commonTest существует
- [ ] новые use-case/repository/viewmodel-логики тестируются
- [ ] агент умеет запускать конкретный тест
- [ ] фейки используются вместо тяжёлых платформенных моков там, где возможно

## Агент

- [ ] может читать файлы
- [ ] может искать код
- [ ] может запускать Gradle
- [ ] может читать ошибки сборки
- [ ] может делать маленькие патчи
- [ ] не мержит сам
- [ ] не меняет версии без спроса
- [ ] не трогает секреты
- [ ] явно пишет, какие платформы проверены

---

# 26. Итоговая формула

Для Cursor/Claude в KMP + Compose проекте тебе нужно не «обучить нейронку», а сделать:

```text
docs/AGENT.md
+ CLAUDE.md
+ .cursorrules
+ docs/architecture.md
+ docs/commands.md
+ scripts/check-fast.sh
+ Gradle wrapper
+ version catalog
+ targeted Gradle/test commands
+ KMP guardrails
+ запрет на опасные действия
```

И главное:

> Агент должен работать маленькими итерациями, проверять каждое изменение Gradle/тестами и явно понимать, какой таргет он проверил: Android, JVM, iOS simulator или только common metadata.

---

Если хочешь, следующим сообщением скинь мне примерно:
- названия модулей;
- есть ли iOS target;
- какие Gradle-таски у вас реально существуют;
- используете ли вы навигацию/DI;
- есть ли уже тесты;

и я соберу тебе готовый `docs/AGENT.md`, `.cursorrules`, `CLAUDE.md` и `scripts/check-fast.sh` конкретно под твой KMP-проект.
