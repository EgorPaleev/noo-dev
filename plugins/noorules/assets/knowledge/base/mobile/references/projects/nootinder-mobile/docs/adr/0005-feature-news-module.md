# 0005. Feature News module (лента новостей саммита)

## Status

Accepted

## Context

Появляется новый продуктовый раздел — **«Новости»**: лента официальных объявлений
организаторов саммита (кейс 9 «Чаты», экран 2 в `sovpa_design`). Канал только для
чтения — без поля ввода, реакций и экрана-деталки.

Первая итерация вышла на мок-данных (`NewsRepositoryImpl` отдавал статичный список).
Бэкенд новостей теперь готов (swagger tag **Summit News**), и раздел переводится на
реальные данные с оффлайн-кэшем.

## Decision

- Вертикальный слайс `feature-news-api` / `feature-news-impl` по образцу
  `feature-chats-list` (offline-first + курсорная пагинация), см.
  [ADR 0001](0001-modular-feature-api-impl.md),
  [ADR 0002](0002-feature-layered-architecture.md),
  [data-flow-offline-first](../data-flow-offline-first.md):
  - `feature-news-api`: `NewsArticle`, `NewsPage(articles, nextCursor)`,
    `NewsRepository` (`observeNews(): Flow<UiState<NewsPage>>` +
    `loadMoreNews(cursor): Result<NewsPage>`), `ObserveNewsUseCase` /
    `LoadMoreNewsUseCase`.
  - `feature-news-impl`: `NewsRepositoryImpl` на `CachedRemoteRepository` + `NewsApi` +
    `NewsCacheStorage`; `NewsViewModel` держит domain-`NewsState` (`isLoading` /
    `hasLoadError` / `articles` / `canLoadMore` / `isLoadingMore`) и `Channel<NewsEvent>`
    для ошибок дозагрузки; UI — кнопка «Загрузить ещё», обёртка `InternetStatus`.
  - `NewsArticle.dateLabel` формируется в `NewsDateFormatter` из `published_at`
    (`«Сегодня, HH:mm»` / `«Вчера, HH:mm»` / `«d MMMM, HH:mm»`).
- Сеть: `data-source:network/news` — `NewsApi.getNews(summitId, cursor, limit)` +
  `markNewsRead(summitId, newsId)` (эндпоинт `PUT .../news/{newsID}/read`).
- Прочитанное: `NewsRepository.markNewsRead(ids)` / `MarkNewsReadUseCase` шлют PUT по
  каждому id параллельно и пишут `isRead = 1` в `summit_news_cache` только для успешных
  (схема не меняется). `NewsViewModel` помечает непрочитанные при открытии экрана —
  на `UiState.Success` (сетевой ответ уже в кэше) и для страниц «Загрузить ещё»; тег
  «Новое» держится до выхода с экрана (`unreadThisVisit`), ошибки повторяются на
  следующем `Success`.
- Превью в списке чатов: `feature-chats-list-impl` зависит от `feature-news-api`;
  `ObserveNewsChannelUseCaseImpl` берёт первую (самую свежую) статью из
  `ObserveNewsUseCase` → `NewsChannelSummary(previewText = title, timeLabel = dateLabel,
  isUnread = any { isNew })`. Нет новостей / ошибка без кэша → `NewsChannelSummary.Empty`:
  строка «Новости» остаётся без превью, времени и точки. Ошибки новостей не влияют на
  `hasLoadError` списка чатов. Кэш общий, поэтому точка гаснет, как только экран новостей
  пометил прочитанное.
- Кэш: summit-scoped таблица `summit_news_cache` (PK `summitId, id`, `replaceForSummit`)
  в `:data-source:local`, по образцу `events_cache`. `AppDatabase` **16 → 17**,
  `fallbackToDestructiveMigration` (кэш пересобирается из сети). `NewsCacheStorage`
  очищается на logout в `LogoutRepositoryImpl`.
- Навигация: `NavigationDestination.News` + entry в `App.kt`; переход из строки
  «Новости» списка чатов (`ChatsListScreen.onNewsClick` → `navigation.openNews()`).
  Модули подключены в `settings.gradle.kts`, `shared/build.gradle.kts`, `InitKoin`.
- UI переиспользует `:core:presentation` (`NootinderTopBar`, `Modifier.shimmerEffect`,
  `UiState`, тема, `InternetStatus`, `NootinderToastHost`). Иконка канала — заглушка
  `NootinderIcons.bell` (мегафон придёт отдельной веткой).

## Consequences

- Контракт `feature-news-api` изменился (список → `NewsPage` + курсор), но слой Domain
  остаётся без Ktor/Room/Compose.
- Бамп версии БД деструктивный: кэши всех фич на устройстве очищаются при обновлении и
  перезагружаются из сети — приемлемо для кэша.
- Порядок первой страницы определяет сервер: в свагере «ordered by publication time»
  без направления. Превью верно, только если сервер отдаёт свежие новости первыми
  (`published_at DESC`) — нужно подтвердить у бэкенда.
- Follow-up: обработчик WS-событий `news.created` / `news.updated`; bulk-эндпоинт
  «прочитать всё» и `unread_count` на бэкенде (сейчас N параллельных PUT и загрузка целой
  страницы ради одной строки); заменить иконку-заглушку на мегафон.
