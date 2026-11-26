---
name: review-conventions
description: Чек-лист конвенций этого стартер-пака для код-ревью — используй вместе с /code-review (или отдельно) для diff'ов, которые трогают доменные модули, DTO, guards или конфигурацию. Ловит нарушения, специфичные именно для этого репозитория, которые общий /code-review не знает.
---

# Чек-лист конвенций стартер-пака

Общий `/code-review` ловит корректность/simplification/efficiency в целом — этот чек-лист специфичен для конвенций именно этого репозитория и дополняет его при ревью diff'а, а не заменяет.

## Язык (`docs/principles/LANGUAGE.md`)

- Идентификаторы — английский, всё видимое человеком (`throw new XException(...)`, `message` у `class-validator`, `@ApiProperty({ description })`) — русский.
- `message` присутствует на **каждом** `class-validator`-декораторе, включая `@IsOptional`/`@IsNotEmpty`.
- Нет комментариев, пересказывающих код; нет ссылок на задачу/issue/PR в коде.

## Naming и DTO (`docs/conventions/NAMING.md`)

- kebab-case файлы, единственное число внутри доменной папки.
- `Update*Dto` — все поля `@IsOptional()`, без `PartialType`.
- Порядок декораторов на поле: `@ApiProperty`/`@ApiPropertyOptional` → `@Transform` (если нужен) → `@IsOptional` → `@IsNotEmpty` → декоратор типа → декораторы диапазона/формата.

## Prisma (`docs/recipes/PRISMA.md`)

- Сервис инжектит `PrismaService` напрямую — нет отдельного repository-класса.
- Контроллер не импортирует `PrismaService`/Prisma-типы.

## Типизация (`docs/conventions/TYPESCRIPT.md`)

- CRUD-примитивы — строго Prisma-типами.
- Композиционные методы (пагинация, join) — `Promise<unknown>`, не самодельный `interface`/`type`.
- `request`/event payload/JWT payload — `any`, не типизируются.
- Enum'ы — только импорт из `@prisma/client`, не продублированы вручную.

## Guards (`docs/recipes/GUARDS.md`)

- Marker-декораторы экспортируют `*_KEY`-константу, не строковый литерал, продублированный в guard'е.
- Ролевой guard — точечно через `@UseGuards` на методе/контроллере, не глобально через `APP_GUARD`.

## Общее (`docs/principles/GENERAL.md`, `docs/conventions/CONSTANTS.md`, `docs/recipes/CONFIGURATION.md`)

- Нет кода "про запас", нет неиспользуемого boilerplate от `nest generate`.
- Константа, используемая одним файлом — `private readonly` на классе, не отдельный `constants.ts`.
- `process.env`/сырой `configService.get('UPPER_CASE')` — только внутри `XModule.forRootAsync` (см. `docs/recipes/EXTERNAL-INTEGRATIONS.md`), нигде больше в коде.

## Форматирование (`docs/conventions/FORMATTING.md`)

- Не проверять руками — `npm run lint` (`eslint --fix`) ловит и чинит сам; в ревью важно, что линт реально прогнан, а не что отступы на глаз верные.
