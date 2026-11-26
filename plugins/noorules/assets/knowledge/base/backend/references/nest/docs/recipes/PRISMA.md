# Работа с Prisma

Сервис инжектит `PrismaService` и обращается к моделям напрямую — отдельного repository-слоя нет.

## Naming в schema.prisma

- Модель — `PascalCase`, единственное число: `Item`, не `Items`/`item`.
- Поле — `camelCase`: `createdAt`, не `created_at`.
- Таблица в Postgres — `snake_case`, множественное число: `items`, не `Item`/`Items`. Это не подстройка под «другой стиль» БД, а обычная практика самой Prisma — у моделей и таблиц исторически разные принятые нейминги (`PascalCase`/singular для моделей, `snake_case`/plural для таблиц), поэтому `@@map` на модель ставится по умолчанию, а не только когда БД к этому вынуждает.
- Поля мапить через `@map` только когда конкретное поле называется в БД не так, как в camelCase-варианте (например колонка уже `created_at`) — заводить `@map` на каждое поле «на всякий случай» не нужно.

```prisma
model Item {
  id        Int      @id @default(autoincrement())
  name      String
  createdAt DateTime @default(now()) @map("created_at")

  @@map("items")
}
```

## Индексы и уникальность

- `@unique` — уникальность одного поля.
- `@@unique([...])` — составной уникальный индекс.
- `@@index([...])` — обычный индекс (в т.ч. составной).

```prisma
model Item {
  id   Int    @id @default(autoincrement())
  sku  String @unique
  name String

  @@index([name])
}

model OrderItem {
  orderId Int
  itemId  Int

  @@unique([orderId, itemId])
}
```

Заводить индекс/уникальность — только под реальный запрос (частый `WHERE`/`ORDER BY` или бизнес-ограничение уникальности), не заранее. Опции вроде `sort`, `length` (MySQL), `type: Hash/Gin/...` (PostgreSQL) — по конкретной необходимости, в базовых моделях не нужны.

`Item`/`ItemService` ниже — иллюстративный пример, такого модуля в репозитории нет; сам принцип (без repository-слоя) уже действует для реального `PrismaService` (`src/prisma/`).

```ts
// item.service.ts
@Injectable()
export class ItemService
{
    constructor(private readonly prismaService: PrismaService) {}

    findById(id: number): Promise<Item>
    {
        return this.prismaService.item.findUnique({ where: { id } });
    }

    findMany(dto: FindManyItemsQueryDto): Promise<unknown>
    {
        const { page, perPage, search } = dto;
        const filter: Prisma.ItemWhereInput = {
            name: search ? { contains: search, mode: "insensitive" } : undefined,
        };

        return Promise.all([
            this.prismaService.item.count({ where: filter }),
            this.prismaService.item.findMany({
                skip: (page - 1) * perPage,
                take: perPage,
                where: filter,
            }),
        ]);
    }
}
```

Типизация методов сервиса — см. `docs/conventions/TYPESCRIPT.md` (CRUD-примитивы строго типизированы Prisma-типами, кроме `create`/`update` — там сразу DTO; композиционные методы вроде `findMany` выше — `Promise<unknown>`).
