# Конфигурация

Единственная точка доступа к переменным окружения — `src/config/configuration.ts` (camelCase-ключи). Нигде в коде не читаем `process.env` или `configService.get('SOME_ENV_NAME')` напрямую — только через ключи из `configuration.ts`. Обязательность и формат переменных описываются в `src/config/validation.schema.ts` (Joi) — приложение не стартует, если `.env` не соответствует схеме.

**Исключение** — конфигурация `XModule.forRootAsync(...)` для внешних интеграций (почта, S3 и т.п.): `useFactory` в таком модуле читает `configService.get("MAIL_HOST")` напрямую сырым UPPER_CASE-именем переменной, без прохода через `configuration.ts`. Переменная всё равно обязана быть в `.env.example` и `src/config/validation.schema.ts` — не заводится только camelCase-ключ в `configuration.ts`. Подробности и пример — `docs/recipes/EXTERNAL-INTEGRATIONS.md`.
