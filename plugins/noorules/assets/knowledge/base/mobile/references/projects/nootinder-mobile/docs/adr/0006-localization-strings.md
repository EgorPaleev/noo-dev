# 0006. Локализация: строковые ресурсы, UiText и StringProvider

## Status

Proposed

## Context

До этой задачи в проекте не было строковых ресурсов: пользовательский текст жил литералами
в Composable, ViewModel, Reducer, data-слое, превью и моках (около 950 строк в ~25 модулях).
Compose Multiplatform Resources (`compose.components.resources`) уже подключены во всех
`*-impl` и в `:core:presentation`, поэтому новая библиотека не нужна.

Ограничения:

- вне Composable `getString()` из Compose Resources есть только в suspend-варианте. Его нельзя
  вызвать из `CoroutineExceptionHandler`, из синхронного `buildState()` или из чистого
  Reducer'а;
- ViewModel переживает пересоздание Activity, поэтому строка, разрешённая в VM, после смены
  языка остаётся на старом языке.

## Decision

- **Где лежат строки.** У каждой фичи свой файл
  `features/<feature>-impl/src/commonMain/composeResources/values/strings.xml` со своим
  `internal` `Res`. Общие строки лежат в `:core:presentation` и доступны фичам через обёртку
  `ru.sovpa.presentation.text.CommonStrings` (по образцу `NootinderIcons`, без
  `publicResClass`).
- **Язык по умолчанию.** `values/` — русский. Другие языки добавляются папками `values-<lang>`.
- **Ключи.** `<screen>_<element>[_<qualifier>]` в snake_case (`login_title`,
  `login_error_request_code`); общие — `common_*`.
- **Аргументы.** Только позиционные `%1$s` / `%1$d`: Compose Resources не подставляет
  непозиционные `%s`.
- **Плюралы.** Только через `<plurals>` (one/few/many/other); самописные функции склонения
  не используются.
- **ViewModel / Reducer.** Пользовательский текст в state хранится как
  `ru.sovpa.presentation.text.UiText`:
  - `uiText(Res.string.x, args…)` — строка из ресурсов;
  - `uiPlural(Res.plurals.x, n, args…)` — плюрал;
  - `throwable.toUiText(Res.string.fallback)` (`ru.sovpa.data.error`) — текст по коду
    ошибки бэкенда или fallback экрана (см. «Ошибки бэкенда»);
  - `UiText.Raw(value)` — готовый текст, который уже пришёл переведённым.

  Composable разрешает текст через `UiText.asString()`. Компоненты `:core:presentation`
  по-прежнему принимают `String`.
- **StringProvider** (`suspend`, Koin `single` в `appModule`) применяется только там, где
  готовая строка нужна вне Compose:
  - payload события, который уходит за пределы экрана или приложения (календарь, колбэк
    навигации);
  - текст, который VM использует в логике (поиск, сравнение);
  - названия для форматтеров дат в репозиториях и VM (`dateNames()`).
- **Даты.** Месяцы в родительном падеже, короткие и полные дни недели лежат в
  `:core:presentation` как `<string-array>` (`common_date_*`), «Сегодня» / «Вчера» — как `<string>`.
  Форматтеры остаются чистыми и синхронными и принимают `DateNames`. Вызывающий код получает
  его через `StringProvider.dateNames()` (suspend) или `rememberDateNames()` в Composable.
  Фразы с числами («День %1$d · %2$d %3$s», «%1$s. %2$d %3$s») — шаблоны в `strings.xml` фич.
  В тестах используется фикстура `ruDateNames` и `FakeStringProvider` из `:core:test-utils`.
- **Rich text со ссылками.** Один шаблон с позиционными плейсхолдерами, тексты ссылок — отдельные
  строки. Хелпер `buildLinkedText(template, links, baseStyle, linkStyle)` собирает
  `AnnotatedString`. Шаблон берётся через `stringResource(res)` без аргументов, тогда
  плейсхолдеры остаются в строке.
- **Ошибки бэкенда.** Бэкенд отвечает `{"error": "...", "code": "PHONE_ALREADY_USED"}`;
  `code` — стабильный UPPER_SNAKE_CASE из `ErrorCode` OpenAPI, `error` — английский текст для
  отладки, пользователю он не показывается.
  - `safeApiCall` кладёт `code` в `NetworkException.ClientError` / `ServerError`, расширение
    `Throwable.apiErrorCode` ищет его в исключении и цепочке `cause`.
  - Тексты лежат в `:core:presentation` в `values/api_errors.xml` с ключом
    `api_error_<code в нижнем регистре>`; `ApiErrorStrings.forCode(code)` находит строку через
    сгенерированный `Res.allStringResources`. Новый код — одна строка в xml.
  - `toUiText(fallback)` возвращает строку кода, если она есть, иначе fallback экрана.
    `toUiTextOrNull()` — для событий, где экран сам подставляет свой текст.
  - Для общих кодов (`BAD_REQUEST`, `CONFLICT`, `NOT_FOUND`, `INTERNAL_ERROR`,
    `VALIDATION_FAILED` …), технических (`*_INVALID_CURSOR`, `CHAT_PROTOCOL_ERROR` …) и `ADMIN_*`
    строк нет намеренно: контекстный текст экрана («Не удалось загрузить новости») понятнее.
  - Экран может переопределить текст для своего кода через `when (error.apiErrorCode)`
    (например, ввод кода саммита, занятый телефон в профиле саммита).
  - Мост живёт в `:core:data`, потому что только он видит и `:data-source:network`, и `UiText`.
- **Не выносим в ресурсы:**
  - тела `@Preview`, моки и sample-данные;
  - литералы-ключи для сопоставления с бэкендом;
  - KDoc;
  - тестовые фейки.

## Consequences

- Reducer остаётся чистым и синхронным, конструкторы VM не меняются, а тесты сравнивают
  `UiText` (равенство ресурсов по id) вместо локализованных строк.
- Смена языка подхватывается при рекомпозиции, перезапускать VM не нужно.
- Состояния, где раньше был `String`, теперь имеют тип `UiText`. Composable должен вызывать
  `.asString()`.
- Тексты ответов бэкенда (`error`) больше не показываются: пользователь видит строку по `code`
  или текст экрана, поэтому они переводятся вместе с остальными ресурсами.
- Лейблы дат, сохранённые в Room (дни программы, история саммитов), остаются на языке момента
  загрузки до следующего refresh.
- Follow-up:
  - сообщения data-слоя (`NO_SUMMIT_MESSAGE` и др.) — перевести на типизированные исключения
    (в UI они уже не попадают, вместо них показывается fallback экрана);
  - подсветка полей по `ValidationError.fields`, показ `CHAT_*` ошибок WebSocket,
    отдельный текст «нет интернета» для `NetworkException.UnknownError`;
  - `values-en` и `CFBundleLocalizations` для iOS;
  - порядок слов и пунктуация в датах пока заданы в коде форматтеров — вынести в шаблоны
    вместе с `values-en`.
