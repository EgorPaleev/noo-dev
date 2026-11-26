---
name: add-env-var
description: Добавить новую переменную окружения в проект. Используй, когда задача требует новой env-переменной (обычной или для внешней интеграции через XModule.forRootAsync) — гарантирует, что переменная не будет частично забыта в одном из мест.
---

# Добавление переменной окружения

Прочитать `docs/recipes/CONFIGURATION.md` перед началом — единственная точка доступа к env в коде: `src/config/configuration.ts`. Обязательность/формат — `src/config/validation.schema.ts` (Joi); приложение не стартует, если `.env` не соответствует схеме.

## Обычная переменная (читается через `configuration.ts`)

Обновить все три места:

1. `.env.example` (корень проекта) — добавить переменную с примером значения.
2. `src/config/configuration.ts` — добавить camelCase-ключ, читающий `process.env.VAR_NAME`.
3. `src/config/validation.schema.ts` — добавить Joi-правило (`.required()` для обязательных переменных).

## Переменная только для `XModule.forRootAsync` внешней интеграции (см. `docs/recipes/EXTERNAL-INTEGRATIONS.md`)

Читается сырым UPPER_CASE-именем прямо в `useFactory` модуля интеграции — `configuration.ts` не трогается:

1. `.env.example` — добавить переменную.
2. `src/config/validation.schema.ts` — добавить Joi-правило.
3. `configuration.ts` — **не менять**.

## `docker/.env.example`

Отдельный файл — переменные уровня `docker-compose.yml` (порты, `PROJECT_PREFIX`, учётные данные Postgres-контейнера), не app-level `configuration.ts`. Трогать только если переменная нужна самому `docker-compose.yml`/скриптам в `docker/`, а не только Nest-приложению.

## Проверка

После изменения — перезапустить контейнер (`docker/dctl.sh restart`) и убедиться по логам (`docker/dctl.sh logs web`), что старт прошёл без Joi-ошибки валидации.
