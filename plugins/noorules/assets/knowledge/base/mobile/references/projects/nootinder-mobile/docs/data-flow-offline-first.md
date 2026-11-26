# Offline-First: сеть → Room → UI

Практическое описание того, как сейчас устроены загрузка и кэш данных (не целевая ADR-визия, а **текущий код**).

Связанные документы: [architecture.md](architecture.md), [ADR 0003](adr/0003-offline-first.md).

---

## Кратко

Для data-heavy фич (саммиты, профиль, история) работает:

1. UI подписывается на `Flow` из Repository через UseCase / ViewModel.
2. Repository вызывает `CachedRemoteRepository.execute(fromRemote, fromCache, saveToCache)`.
3. Сразу эмитятся данные из **Room** (если есть).
4. Параллельно идёт **Ktor**-запрос; ответ мапится DTO → Entity → DBO и пишется в Room.
5. Room Flow эмитит снова → merge → `UiState` → экран обновляется.

Auth — исключение: remote-only + secure token storage, без Room.

---

## Стек

| Слой | Технология | Модуль |
|---|---|---|
| HTTP | Ktor (+ Bearer refresh) | `:data-source:network` |
| Local DB | Room KMP (`sovpa.db`) | `:data-source:local` |
| Offline engine | `CachedRemoteRepository` | `:core:data` |
| DI | Koin | `:shared` + feature modules |
| UI state | ViewModel + StateFlow / MVI | `features/*-impl` |

Токены **не** в Room: `TokenStorage` / `SecureTokenStorage`.

---

## Движок: `CachedRemoteRepository`

Файл: `core/data/.../CachedRemoteRepositoryImpl.kt`

```text
cacheFlow  = fromCache()     → RequestState.Success(cache)
remoteFlow = Loading → fromRemote() → saveToCache() → Success | Error

combine(cache, remote) → MergeStrategy → RequestState → toUiState() → UiState
```

Поведение merge (`MergeStrategyImpl`):

| Cache | Remote | Итог для UI |
|---|---|---|
| Success(data) | Loading | InProgress(data) — старые данные + лоадер |
| Success(data) | Success(new) | Success (предпочтение cache/remote по merge) |
| Success(data) | Error | Error(data, throwable) — данные не пропадают |
| пусто / нет | Loading → Success | InProgress → Success после сети |

Маппинг состояния: `RequestState.toUiState()` в `core/data/.../RequestState.kt`.

---

## Пример end-to-end: «Мои саммиты»

Экран: `MySummitScreen` → `MySummitViewModel` → `GetMySummitsUseCase` → `SummitRepository.observeMySummits()`.

### Полная цепочка

```text
MySummitScreen
  collectAsStateWithLifecycle(viewModel.state)
       ▲
MySummitViewModel
  LoadData → ObserveSummits → getMySummitsUseCase.execute().collect
       ▲
GetMySummitsUseCaseImpl
  summitRepository.observeMySummits()
       ▲
SummitRepositoryImpl + CachedRemoteRepositoryImpl
  ┌─────────────────────────────┬──────────────────────────────┐
  │ fromCache                   │ fromRemote                   │
  │ MySummitsCacheStorage       │ ProfileApi.listMySummits()   │
  │   → MySummitCacheDao        │   GET /api/profile/summits   │
  │   → Flow<List<MySummitDbo>> │   → List<SummitSummaryDto>   │
  │   → .toSummit()             │   → .toSummit()              │
  └──────────────┬──────────────┴──────────────┬───────────────┘
                 │                             │
                 │         saveToCache         │
                 │    .toDbo() → replaceAll    │
                 └──────────────┬──────────────┘
                                ▼
                         Room: my_summits_cache
                                │
                 merge → RequestState → UiState
                                ▼
MySummitReducer: List<Summit> → currentSummit + pastSummits
                                ▼
MySummitScreenContent (карточки)
```

### Типы по слоям

```text
SummitSummaryDto  →  Summit (domain)  →  MySummitDbo (Room)
                                      →  SummitListItem (UI VO)
```

Мапперы: `features/feature-summit-impl/.../data/Mapper.kt`.

### Ключевые файлы

| Файл | Роль |
|---|---|
| `.../presentation/MySummitScreen.kt` | Compose, collect state |
| `.../vm/MySummitViewModel.kt` | Intent → commands → collect use case |
| `.../vm/mvi/MySummitReducer.kt` | `UiState<List<Summit>>` → `MySummitState` |
| `.../usecase/GetMySummitsUseCaseImpl.kt` | Прокси в repository |
| `.../data/SummitRepositoryImpl.kt` | `CachedRemoteRepository.execute(...)` |
| `core/data/.../CachedRemoteRepositoryImpl.kt` | Cache + remote combine |
| `core/data/.../strategy/MergeStrategyImpl.kt` | Merge состояний |
| `data-source/network/.../ProfileApiImpl.kt` | `GET /api/profile/summits` |
| `data-source/local/.../mysummit/MySummitsCacheStorage.kt` | Обёртка над DAO |
| `data-source/local/.../mysummit/MySummitCacheDao.kt` | Room Flow / replaceAll |
| `data-source/local/.../db/AppDatabase.kt` | Schema, `sovpa.db` |

### Хронология

**Первый заход (кэш пуст):**

1. `cacheFlow` → пустой список.
2. `remoteFlow` → `Loading` → UI: спиннер / `InProgress`.
3. Ktor → ответ → `saveToCache` → Room `replaceAll`.
4. Room Flow эмитит → UI: список саммитов.

**Повторный заход (кэш есть):**

1. Сразу Success из Room — карточки на экране.
2. Параллельно сеть; при успехе Room обновляется → UI обновляется.
3. При ошибке сети — список из кэша + error state (данные не стираются).

Покрыто тестами: `SummitRepositoryImplTest` (`observeMySummits maps remote...`, `returns cached list when remote fails`).

---

## Mutations (запись)

Чтения идут через `CachedRemoteRepository`. Мутации обычно **network-first**, потом запись в кэш:

| Действие | Пример | Паттерн |
|---|---|---|
| Обновить профиль | `ProfileRepository.updateProfile` | API → `saveProfile` |
| Redeem invite | `SummitRepository.redeemInvitation` | API → `listMySummits` → `saveAll` |
| Logout | `LogoutRepositoryImpl` | `POST /api/auth/logout` (best-effort) → clear tokens → clear всех cache tables |
| Выход из саммита | `LeaveSummitRepositoryImpl` | clear current summit id → clear cache tables с `summitId` |

---

## Другие фичи с тем же паттерном

| Repository | Remote | Cache table(s) |
|---|---|---|
| `SummitRepositoryImpl.observeMySummits` | `GET /api/profile/summits` | `my_summits_cache` |
| `SummitRepositoryImpl.observeSummit` | `GET /api/summits/{id}` | `my_summits_cache` |
| `SummitRepositoryImpl.observeMembers` | members API | `summit_members_cache` |
| `SummitRepositoryImpl.observeMemberProfile` | member profile API | `summit_member_profile_cache` |
| `ProfileRepositoryImpl.getProfile` | `GET /api/profile` | `profile_cache` |
| `ProfileRepositoryImpl.getCurrentSummit` | `GET /api/profile/current-summit` | `summit_cache` |
| Events history | history API | `summit_history_cache` / events |
| `SpeakersRepositoryImpl.observeSpeakers` | `GET /api/summits/{id}/speakers` | `summit_speakers_cache` |
| `SpeakerProfileRepositoryImpl.observeSpeaker` | `GET /api/summits/{id}/speakers/{profileId}` | `summit_speaker_profile_cache` |

---

## Auth (не offline-first)

```text
SmsCode / Splash → UseCase → AuthRepository → AuthApi
                                      ↓
                         TokenRefreshStorage (secure)
```

Room не участвует. См. `AuthRepositoryImpl`.

---

## Как добавить новый offline-first список

1. DTO в `:data-source:network`, метод API.
2. Entity (+ DBO / DAO / CacheStorage) в `:data-source:local`, зарегистрировать в `AppDatabase` + `localModule`.
3. В feature repository: `cachedRemoteRepository.execute(fromRemote, fromCache, saveToCache)`.
4. UseCase → ViewModel collect `Flow<UiState<T>>` → screen state.
5. Мапперы DTO ↔ Entity ↔ DBO рядом с repository.
6. Тест на «remote → cache» и «remote fail → cache remains» по образцу `SummitRepositoryImplTest`.

---

## Deep dive: как устроен кэш и почему так

Ниже — разбор механизмов, которые сидят «под капотом». Это не отдельный CacheManager-класс, а **набор паттернов**, сложенных вместе.

### 1. Идея: stale-while-revalidate, не sync-engine

Это **не** полноценный offline sync (нет очереди мутаций, conflict resolution, background worker).

Это **cache-aside + stale-while-revalidate**:

1. UI всегда читает через Repository.
2. Repository показывает то, что уже есть в Room.
3. Параллельно ходит в сеть и **перезаписывает** кэш.
4. Room `Flow` сам пушит обновление подписчикам.

Мутации (update profile, redeem) — отдельно: сначала сеть, потом явная запись в кэш. Без сети мутация просто падает.

### 2. Разделение ролей (почему код «многослойный»)

| Слой | Ответственность | Не знает про |
|---|---|---|
| `CachedRemoteRepository` | Timing: cache Flow + remote one-shot + merge | Какой API, какая таблица, какие поля |
| Feature `*RepositoryImpl` | Что фетчить / куда писать / как мапить | Как merge-ить Loading/Error |
| `*CacheStorage` | Тонкая обёртка над DAO | Сеть, UI |
| `*CacheDao` + `*Dbo` | SQL / schema / реактивный observe | Domain Entity |
| `MergeStrategy` | Политика «что показать при паре состояний» | Откуда данные взялись |
| `RequestState` → `UiState` | Data-layer vs presentation vocabulary | Конкретный экран |

Смысл: один generic engine на все фичи. Добавляя новый список, не копируешь combine/loading/error — только три лямбды.

Интерфейс:

```kotlin
fun <T> execute(
    fromRemote: suspend () -> T,      // один запрос
    fromCache: () -> Flow<T>,         // реактивный источник (Room)
    saveToCache: suspend (T) -> Unit, // side-effect после успеха сети
    mergeStrategy: MergeStrategy<T> = MergeStrategyImpl()
): Flow<RequestState<T>>
```

`T` — domain entity (`Summit`, `Profile`, `List<SummitMember>`…), не DTO и не DBO. Маппинг снаружи, в feature repository.

### 3. Два Flow внутри `execute`

#### `cacheFlow` — «долгоживущий» источник правды

```kotlin
val cacheFlow = fromCache()
    .map { RequestState.Success(it) }
    .catch { e ->
        if (e is CancellationException) throw e
        emit(RequestState.Error(throwable = e))
    }
```

Важные решения:

- **Кэш никогда не эмитит Loading.** Room либо отдаёт строку/список (в т.ч. пустой), либо ошибку чтения. «Загрузка» — только про сеть.
- Любой эмит из Room оборачивается в `Success`. Пустой список саммитов = `Success(emptyList())`, не Error.
- `CancellationException` пробрасывается — иначе сломается отмена корутин (collect отменился → нельзя «проглотить» cancellation).

#### `remoteFlow` — одноразовый cold flow

```kotlin
val remoteFlow = flow {
    emit(RequestState.Loading())
    try {
        val data = fromRemote()
        saveToCache(data)          // сначала пишем в БД
        emit(RequestState.Success(data))
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        emit(RequestState.Error(throwable = e))
    }
}.flowOn(Dispatchers.IO)
```

Важные решения:

- Это **не** бесконечный poller. Один subscribe → один сетевой цикл.
- Порядок: **сначала `saveToCache`, потом `Success`.** После записи Room обычно эмитит новый `cacheFlow`, и combine сработает ещё раз — UI увидит данные уже как из кэша (SSOT).
- Сеть на `Dispatchers.IO`.
- Ошибка сети **не** чистит кэш — только `Error` в remote-ветке; merge сохранит cache data.

### 4. `combine` — ключевой механизм склейки

```kotlin
cacheFlow.combine(remoteFlow) { cacheState, remoteState ->
    mergeStrategy.merge(cacheState, remoteState)
}
```

Как работает `combine`:

1. Ждёт, пока **оба** Flow эмитнут хотя бы раз.
2. Дальше на **каждый** новый эмит любого из них пересчитывает пару `(последний cache, последний remote)`.

Отсюда хронология «повторный заход»:

```text
t0  cache: Success(old)     remote: ещё нет        → combine молчит
t1  cache: Success(old)     remote: Loading        → InProgress(old)   ← UI: данные + лоадер
t2  saveToCache(new)
t3  cache: Success(new)     remote: Loading        → InProgress(new)   ← Room уже обновился
t4  cache: Success(new)     remote: Success(new)   → Success(new)
```

При ошибке сети:

```text
cache: Success(old) + remote: Error → Error(old, throwable)
```

UI может показать toast/баннер, но список не обнуляется (`UiState.Error` тоже несёт `data`).

После combine:

- `distinctUntilChanged()` — не дёргать UI, если merge вернул то же состояние.
- `flowOn(Dispatchers.Main)` — downstream collect ближе к UI-потоку (подписка VM обычно всё равно на IO/Main через свой scope).

### 5. `RequestState` / `UiState`: состояние + данные вместе

```kotlin
// data-layer
Loading(data: T? = null)
Error(data: T? = null, throwable)
Success(data: T)

// presentation
InProgress(data: T? = null)
Error(data: T? = null, throwable)
Success(data: T)
```

Это не «либо данные, либо статус». Это **статус поверх опциональных данных** — классика progressive / optimistic UI:

- есть кэш + идёт сеть → `InProgress(cached)`
- есть кэш + сеть упала → `Error(cached, e)`
- нет кэша + сеть упала → `Error(null, e)` → экран показывает empty/error

Конвертация: `RequestState.toUiState()` — 1:1 map, без логики.

### 6. `MergeStrategy` — Strategy pattern

Интерфейс специально вынесен: теоретически можно подставить другую политику (например, всегда предпочитать remote).

Дефолт `MergeStrategyImpl` — таблица 3×3 (Loading/Error/Success × то же). Смысл ветвей:

| Ситуация | Результат | Зачем |
|---|---|---|
| Cache Success + Remote Loading | `Loading(cache)` | Stale-while-revalidate |
| Cache Success + Remote Error | `Error(cache, e)` | Offline UX |
| Cache Success + Remote Success | `Success(cache ?: remote)` | **Кэш — SSOT**; после `saveToCache` cache уже = remote |
| Cache Error + Remote Success | `Success(remote)` | Сеть спасает битый/пустой кэш-путь |
| Cache Loading + … | почти не бывает на практике | Room-ветка Loading не эмитит; ветки «на всякий» |

Почему при двух Success берут **cache**, а не remote:

- После успешного `saveToCache` актуальные данные уже в Room.
- UI концептуально «смотрит в БД», remote — только способ обновить БД.
- Если на мгновение remote Success пришёл раньше Room-эмита, на экране ещё старый cache; следующий эмит cache это поправит. Это сознательный trade-off в пользу SSOT = DB.

### 7. Слой Room: DBO → DAO → Storage

#### Schema

`AppDatabase` (`sovpa.db`, version 7) — набор **cache-таблиц** под фичи:

- `profile_cache`, `summit_cache`, `my_summits_cache`, …
- `summit_members_cache` с составным PK `(summitId, id)` — кэш **скоупирован** по саммиту
- `updatedAt` на многих DBO — для сортировки / свежести, не для TTL-expiry (автоматической протухаемости по времени нет)

Миграции: `fallbackToDestructiveMigration(dropAllTables = true)` — при смене version схема сбрасывается. Для кэша это ок (перезагрузится с сети); для «важных» локальных данных было бы плохо.

Сборка: `BundledSQLiteDriver` + expect/actual `Room.databaseBuilder` (Android Context / iOS path).

#### DAO-паттерны

**Singleton-кэш** (один профиль / один current summit):

```kotlin
@Query("SELECT * FROM profile_cache LIMIT 1")
fun observeProfile(): Flow<ProfileDbo?>

@Insert(onConflict = REPLACE)
suspend fun upsert(...)
```

**Список с полной заменой**:

```kotlin
@Transaction
suspend fun replaceAll(items) {
    clear()
    insertAll(items)
}
```

Полный replace, не diff/merge по id: проще, нет «зомби»-строк после удаления на бэке.

**Список, привязанный к родителю**:

```kotlin
@Transaction
suspend fun replaceForSummit(summitId, items) {
    clearBySummitId(summitId)
    insertAll(items)
}
```

Чужой саммит в кэше не трогаем.

#### Storage

`MySummitsCacheStorage` / `ProfileCacheStorage` — почти без логики: `observe` / `save` / `clear`. Зачем:

- Repository не зависит от Room-аннотаций напрямую (чуть проще тестировать с fake storage/dao).
- Единая точка, если позже добавят in-memory fallback / logging.

Room `Flow` из `@Query` — **hot относительно БД**: пока есть коллектор, любое изменение таблицы (в т.ч. из другого места: logout, redeem, edit profile) автоматически доезжает до UI **без нового сетевого вызова**, если подписка уже жива.

### 8. Как feature repository подключает движок

Типичный вызов (саммиты):

```kotlin
cachedRemoteRepository.execute(
    fromRemote = { profileApi.listMySummits().getOrThrow().map { it.toSummit() } },
    fromCache  = { mySummitsCacheStorage.observeAll().map { it.map(MySummitDbo::toSummit) } },
    saveToCache = { mySummitsCacheStorage.saveAll(it.map(Summit::toDbo)) },
).map { it.toUiState() }
```

Нюансы разных фич:

| Фича | Особенность |
|---|---|
| My summits | `T = List<Summit>`; пустой список валиден |
| Current summit | `T = Summit?`; `null` = «нет текущего», в cache `clearSummit()` |
| Profile | `fromCache` делает `checkNotNull(dbo)` — **пустой кэш роняет cacheFlow в Error**; дальше merge ждёт remote Success. Жёстче, чем empty list |
| observeSummit / member | `execute<T?>` + `toRequiredUiState()` — `Success(null)` трактуется как ещё InProgress, пока нет обязательной сущности |
| observeCachedProfile | **только** Room Flow, без `CachedRemoteRepository` — читать кэш без сетевого side-effect |

### 9. Жизненный цикл подписки

1. VM делает `useCase.execute().collect { ... }` (часто после Intent `LoadData`).
2. Collect стартует cold `remoteFlow` → один сетевой запрос.
3. Collect держит `cacheFlow` → Room observe.
4. Cancel collect (уход с экрана / `job.cancel()`) → отмена remote (если ещё бежал) + отписка от Room.
5. Повторный `LoadData` → **новый** `execute()` → снова сеть. Это не «вечный sync», а «обновить при подписке / retry».

Redeem после успеха сам делает `saveAll` и часто снова `ObserveSummits` — список обновляется и из явной записи, и из новой подписки.

### 10. Logout = граница сессии для кэша

`LogoutRepositoryImpl`:

1. `authApi.logout(refreshToken)` — `POST /api/auth/logout`, отзыв серверной сессии. Только если refresh-токен
   есть на устройстве; best-effort с таймаутом 5 c — ошибка или зависание не мешают локальному выходу
2. `profileApi.logout()` — сброс in-memory Bearer в Ktor
3. `clearTokens()`
4. `clear*` по всем cache storage

Иначе следующий пользователь на том же устройстве увидел бы чужой offline-кэш. Токены и Room намеренно разделены: токены — security, Room — UX-кэш.

Выход из саммита (`LeaveSummitRepositoryImpl`, кнопка на главном экране) — граница поменьше: сбрасывает
current summit id и все таблицы с `summitId` (участники, профили, контакты, программа, события, чаты,
сообщения, новости, встречи, спикеры и их профили, свой summit-профиль). Профиль пользователя, «Мои саммиты», `summit_cache`
и история остаются — они нужны на экране выбора саммита.

### 11. Чего в механизме нет (осознанно / пока)

- TTL / авто-invalidate по времени
- ETag / If-None-Match
- Очередь offline-мутаций
- Частичный merge списков (только full replace)
- Отдельный «cache hit metrics» слой (есть только Kermit-логи)
- Unit-тесты именно на `MergeStrategyImpl` / `CachedRemoteRepositoryImpl` (покрытие косвенно через feature repository tests)

### 12. Ментальная модель одной фразой

> Room — реактивный SSOT для UI; сеть — способ обновить Room; `CachedRemoteRepository` — шаблон, который показывает кэш сразу, грузит remote параллельно и аккуратно склеивает Loading/Error/Success так, чтобы данные не исчезали с экрана.
