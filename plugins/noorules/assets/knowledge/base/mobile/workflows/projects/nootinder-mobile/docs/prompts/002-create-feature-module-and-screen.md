# 002. Как создать feature-модуль и экран (чеклист)

**Как использовать:** `@docs/prompts/002-create-feature-module-and-screen.md` + короткое имя фичи и макет (если есть).

---

# Как создать feature-модуль и экран (чеклист)

Плейбук по образцу `feature-meeting-api` / `feature-meeting-impl`.
Эталон структуры: `feature-events-history-*`, эталон UI-разбиения: `feature-meeting-impl`.

Подставь вместо `{name}` короткое имя фичи в kebab/snake (`meeting`, `faq`, `participants`).

---

## 0. Что спросить / зафиксировать до кода

- HTML/CSS-макет экрана (или ссылка на кейс).
- Нужна ли интеграция в `shared` (навигация, InitKoin) **сейчас**, или живём только в модуле.
- Какие иконки нужны — сначала проверить `core/presentation` → `NootinderIcons` / `composeResources/drawable`.

---

## 1. Gradle-модули

### 1.1. Создать каталоги

```
features/feature-{name}-api/
features/feature-{name}-impl/
```

### 1.2. Зарегистрировать в `settings.gradle.kts`

```kotlin
include(":features:feature-{name}-api")
include(":features:feature-{name}-impl")
```

### 1.3. `build.gradle.kts`

Скопировать с `feature-events-history-api` / `feature-events-history-impl` и заменить:

| Поле | api | impl |
|------|-----|------|
| iOS `baseName` | `Feature{Name}Api` | `Feature{Name}Impl` |
| `android.namespace` | `ru.sovpa.feature_{name}_api` | `ru.sovpa.feature_{name}_impl` |
| deps | `projects.core.presentation` | + `projects.features.feature{Name}Api`, Koin, Compose |

В impl нужны плагины: `composeMultiplatform` + `composeCompiler`.

### 1.4. Минимальные файлы модулей

- `.gitignore` → `/build`
- `src/androidMain/AndroidManifest.xml` (пустой `<manifest/>`)

### 1.5. Интеграция в app (только если нужно)

- `shared/build.gradle.kts` — зависимости на api + impl
- `InitKoin.kt` — `modules(..., {name}Module)`
- `NavigationDestination` + `NavigationImpl` + entry в `App.kt`

**По умолчанию для новой фичи можно отложить шаг 1.5** и сначала сверстать экран в модуле.

---

## 2. Именование пакетов

| Что | Паттерн |
|-----|---------|
| Gradle | `feature-{name}-api` / `feature-{name}-impl` |
| Kotlin / Android namespace | `ru.sovpa.feature_{name}_api` / `ru.sovpa.feature_{name}_impl` |
| Entity | `...api.entity` |
| Screen | `...impl.presentation` |
| UI-части | `...impl.presentation.components` |
| State | `...impl.models` |
| ViewModel | `...impl.vm` |
| Koin | `...impl.di` |

---

## 3. Иконки (core)

1. Нужная иконка уже есть в `NootinderIcons`? → использовать её.
2. Нет → добавить:
   - XML: `core/presentation/src/commonMain/composeResources/drawable/ic_{snake}.xml`
   - Property в `NootinderIcons.kt` через `painterResource(Res.drawable.ic_{snake})`
3. Не класть иконки внутрь feature, если они общие для продукта.

Reuse из meeting-кейса: `arrowBack`, `plus`, `search`, `close`, `calendar`, `check`, `clock`, `bell`.

---

## 4. API: entity

В `feature-{name}-api/.../entity/`:

- data-классы контракта списка/карточки (то, что потом уйдёт в репозиторий).
- enum статусов / направлений при необходимости.
- Готовить «готовые к UI» строки (`meta`, `searchBlob`) лучше в моках/VM, чтобы экран только рисовал.

Пример:

```kotlin
data class {Name}Item(
    val id: String,
    val title: String,
    val meta: String,
    // ...
)
```

---

## 5. Impl: state + VM + DI

### 5.1. State — `models/{Name}State.kt`

Экран получает **уже отфильтрованные / готовые** данные:

```kotlin
data class {Name}State(
    val isLoading: Boolean = true,
    // вкладки, query, секции/списки...
)
```

### 5.2. ViewModel — `vm/{Name}ViewModel.kt`

- Приватный source моков (TODO: заменить репозиторием).
- `StateFlow<{Name}State>`.
- Методы: смена вкладки, поиск, clear и т.д. → пересчёт state.
- Опционально короткий `delay` для skeleton (`isLoading`).
- **Не** хранить NavController; колбэки навигации — параметры Screen.

### 5.3. Koin — `di/{Name}Module.kt`

```kotlin
val {name}Module = module {
    viewModelOf(::{Name}ViewModel)
}
```

В shared регистрировать только когда подключаете фичу к приложению.

---

## 6. Presentation: экран + components

### 6.1. Thin Screen

`presentation/{Name}Screen.kt`:

- `koinViewModel()` + `collectAsStateWithLifecycle()`
- делегирует в `{Name}ScreenContent`
- колбэки: `onBackClick`, клики по элементам и т.п.

**Не вешать `@Preview` на Screen** — в preview нет Koin → `KoinApplication has not been started`.

### 6.2. Preview без Koin

`presentation/{Name}ScreenFilled.kt`:

```kotlin
@Preview
@Composable
fun {Name}ScreenFilled() {
    AppNootinderTheme {
        {Name}ScreenContent(state = previewState())
    }
}
```

При необходимости отдельный preview для skeleton / empty.

### 6.3. Разбиение UI — `presentation/components/`

Не сваливать весь макет в один файл. Типичный набор:

```
{Name}ScreenContent.kt      // TopBar + scroll + ветвление loading/content
{Name}Skeleton.kt           // если есть скелетон
…Tabs / Search / Section / Card / EmptyState / StatusIcon …
```

Content принимает `state` + callbacks, без ViewModel.

### 6.4. Что брать из core (не дублировать)

| Макет | Core |
|-------|------|
| Шапка | `NootinderTopBar` + `CircleIconButton` |
| Сегмент вкладок | `NootinderSegmentedControl` (pill, active = accentSpark) |
| Поиск | `NootinderSearchField` (компактный mtg/uch-стиль) |
| Аватар | `NootinderAvatar` |
| Тема | `NootinderTheme.colors/typography/spacing/radius` |

Если макет отличается от core — **править/расширять core**, а не копипастить стили в feature (если компонент общий).

Demo-panel / status-bar / constellation / home-nav из HTML-витрины **не переносить**.

---

## 7. Данные на экран — эффективный путь

```
VM (моки / repo)
  → пересчёт секций, фильтр, подписи
  → MeetingState / {Name}State
  → Screen collectAsState
  → ScreenContent + components (только render)
```

Не фильтровать списки заново в каждом composable — отдавать готовые списки из state.

---

## 8. Порядок работ (коротко)

1. Иконки в core (если не хватает)
2. api + impl Gradle + `settings.gradle.kts`
3. entity → state → VM (моки) → Koin module
4. components + Screen + ScreenFilled preview
5. (опционально) shared deps + InitKoin + навигация

Проверка сборки:

```bash
./gradlew :features:feature-{name}-impl:compileAndroidMain
```

Проверка UI: preview `*ScreenFilled`, не сам `*Screen`.

---

## 9. Быстрый diff по файлам (скелет)

```
features/feature-{name}-api/
  build.gradle.kts
  src/androidMain/AndroidManifest.xml
  src/commonMain/kotlin/ru/sovpa/feature_{name}_api/entity/{Name}Item.kt

features/feature-{name}-impl/
  build.gradle.kts
  src/androidMain/AndroidManifest.xml
  src/commonMain/kotlin/ru/sovpa/feature_{name}_impl/
    di/{Name}Module.kt
    models/{Name}State.kt
    vm/{Name}ViewModel.kt
    presentation/{Name}Screen.kt
    presentation/{Name}ScreenFilled.kt
    presentation/components/{Name}ScreenContent.kt
    presentation/components/…
```

Референс в репозитории: `features/feature-meeting-*`.
