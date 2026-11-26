# Тестирование

Jest-конфиг и первые тесты в проекте раньше отсутствовали полностью (`test:e2e` был заглушкой-`echo`, `npm run test` не запускался — не было ни секции `"jest"` в `package.json`, ни `test/jest-e2e.json`). Ниже — паттерн, установленный первыми тестами; донора с готовым паттерном в других проектах не нашлось, паттерн выбран по официальным NestJS/Prisma testing conventions.

## Unit-тесты

`*.spec.ts` рядом с тестируемым файлом (`rootDir: "src"` в jest-секции `package.json`, `testRegex: ".*\\.spec\\.ts$"`). Пример — `src/common/dto/get-query.dto.spec.ts`: тестирует реальный расшаренный DTO (`plainToInstance` + `validate` из `class-transformer`/`class-validator`, без обращения к сети/БД).

Сервисный unit-тест (когда появится первый доменный модуль — см. skill `new-module`) мокает `PrismaService` через `Test.createTestingModule({ providers: [ItemService, { provide: PrismaService, useValue: mockPrismaService }] })`, не поднимая реальную БД — стандартный NestJS DI-подход, а не ручной `jest.mock`.

## E2E-тесты

`test/*.e2e-spec.ts`, отдельный jest-конфиг `test/jest-e2e.json` (`npm run test:e2e`). Поднимают **весь модульный граф приложения** (`Test.createTestingModule({ imports: [AppModule] })`) плюс ту же сквозную конфигурацию Fastify, что и прод — через `configureApp(app)` из `src/configure-app.ts` (helmet, ValidationPipe, Swagger, versioning, CORS, multipart, basic-auth на `/admin/queues`). Без вызова `configureApp` e2e-тест проверял бы только чистый Nest-граф и не заметил бы регрессию в security-настройках, которые в проекте живут в бутстрапе, а не в модулях.

Пример — `test/app.e2e-spec.ts`: проверяет реальные сквозные поведения (`/swagger`, `/admin/queues`, `/health` — не доменные роуты, а инфраструктурные, поэтому не требуют Prisma-моков, `/health` реально стучится в Postgres/Redis из docker-compose):
- `GET /swagger` отдаёт 200 с security-заголовками от helmet;
- `GET /admin/queues` без Basic Auth — 401;
- `GET /admin/queues` с корректными credentials — не 401;
- `GET /health` отдаёт `status: "ok"` с `up` по базе и Redis.

Этот же e2e-прогон вскрыл реальный баг: `app.close()` не закрывал соединение Prisma (jest висел с предупреждением об открытых handle) — `PrismaService` не реализовывал `OnModuleDestroy`. Исправлено (`this.$disconnect()` в `onModuleDestroy`), заодно это и есть настоящий graceful shutdown для БД, а не только `app.enableShutdownHooks()` в `main.ts`.

Тестовая БД/testcontainers для e2e пока не заведены — как только появится первый доменный e2e-тест, читающий/пишущий через Prisma, эту часть нужно решить отдельно (реальная тестовая Postgres-база через `docker-compose` профиль или моки на уровне `PrismaService`, аналогично unit-тестам).

## Запуск

```
docker/dctl.sh run npm run test       # unit
docker/dctl.sh run npm run test:e2e   # e2e
docker/dctl.sh run npm run test:cov   # unit + coverage
docker/dctl.sh run npx jest path/to/x.spec.ts       # один unit-файл
docker/dctl.sh run npx jest --config ./test/jest-e2e.json path/to/x.e2e-spec.ts  # один e2e-файл
```
