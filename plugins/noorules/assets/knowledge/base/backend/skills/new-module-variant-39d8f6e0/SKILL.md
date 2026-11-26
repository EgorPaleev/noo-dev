---
name: new-module
description: Создать новый доменный модуль NestJS (controller/service/module/dto) по конвенциям этого стартер-пака. Используй, когда нужно завести новый домен целиком — контроллер, сервис, DTO, модуль — а не точечно поправить существующий файл.
---

# Новый доменный модуль

Скаффолдинг доменного NestJS-модуля по паттерну этого репозитория (Fastify + Prisma напрямую, без repository-слоя).

## Перед тем как писать код

Прочитать (если ещё не читалось в этой сессии):

- `docs/MODULE-STRUCTURE.md` — структура папки
- `docs/NAMING.md` — имена файлов/классов, naming DTO, порядок декораторов на поле DTO
- `docs/PRISMA.md` — сервис работает с `PrismaService` напрямую
- `docs/TYPESCRIPT.md` — где типизировать строго, где `unknown`/`any`
- `docs/PAGINATION.md` — `GetQueryDto`/`PaginatedResponse`/`IdResponseDto`
- `docs/CONTROLLERS.md` — Swagger-декораторы, `ParseIntPipe`, guards на конкретном эндпоинте
- `docs/CONSTANTS.md` — куда класть константы
- `docs/MODULE-BOUNDARIES.md` — что экспортировать
- `docs/LANGUAGE.md` — русский для сообщений/Swagger, английский для идентификаторов

Проверить `prisma/schema.prisma` — Prisma-модель домена должна уже существовать (миграция — отдельная задача, не часть скаффолдинга модуля).

## Порядок действий

1. Создать папку `src/<domains>/` (множественное число, см. `docs/MODULE-STRUCTURE.md`).
2. `dto/create-<entity>.dto.ts`, `dto/update-<entity>.dto.ts` (все поля через `@IsOptional()`, без `PartialType`), `dto/find-many-<entity>-query.dto.ts extends GetQueryDto` — naming и порядок декораторов строго по `docs/NAMING.md`. `dto/response/` заводить только когда response-DTO у домена несколько.
3. `<entity>.service.ts` — инжект `PrismaService` в конструктор, без repository-слоя. CRUD-примитивы типизированы Prisma-типами (`Prisma.<Entity>FindUniqueArgs` и т.п.), композиционные методы (пагинация, join) — `Promise<unknown>` (см. `docs/TYPESCRIPT.md`).
4. `<entity>.controller.ts` — зависит только от сервиса, никогда не импортирует `PrismaService`/Prisma-типы напрямую. Swagger-декораторы и их порядок — `docs/CONTROLLERS.md`; числовой `:id` — через встроенный `ParseIntPipe`.
5. `<entity>.module.ts` — импортировать `PrismaModule` явно (несмотря на `@Global()` — так делает этот репозиторий, см. `docs/MODULE-BOUNDARIES.md`), экспортировать только то, что реально нужно другим модулям (обычно сервис).
6. Подключить `<Entity>Module` в `imports` корневого `app.module.ts`.
7. Прогнать `docker/dctl.sh run npm run lint`.

## Не делать

- Не заводить repository-слой поверх `PrismaService`.
- Не писать `interface`/`type` под форму composed-ответа — `Promise<unknown>`, см. `docs/TYPESCRIPT.md`.
- Не оставлять boilerplate от `nest generate` (неиспользуемые pipes/interceptors и т.п.) — см. `docs/GENERAL.md`.
