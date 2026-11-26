# Типизация

Главный принцип: типизировать строго там, где тип уже есть бесплатно или где это публичный контракт API — и не тратить силы на типы, которые нужны только компилятору, а не читателю. Ниже — по слоям, от «всегда строго» до «всегда `any`».

## Слой 1 — Prisma CRUD-примитивы сервиса: строго, бесплатно

Каждый сервис держит «сырые» CRUD-методы, которые 1:1 принимают/возвращают типы, уже сгенерированные Prisma. Выписывать их вручную не нужно — они уже есть, грех не взять.

```ts
async findUnique(args: Prisma.StationFindUniqueArgs): Promise<Station>
{
    return this.prismaService.station.findUnique(args);
}

async count(args: Prisma.StationCountArgs): Promise<number>
{
    return this.prismaService.station.count(args);
}
```

Исключение — `create`/`update`: если для действия уже есть DTO (`CreateXDto`/`UpdateXDto`, приходит из контроллера) — метод сервиса принимает его напрямую, а не заворачивает в `Prisma.XCreateArgs`/`Prisma.XUpdateArgs`, раз DTO и так под рукой и однозначно подходит:

```ts
async create(dto: CreateStationDto): Promise<Station>
{
    return this.prismaService.station.create({ data: dto });
}
```

Заводить DTO там, где под него нет очевидного повода (просто обернуть `id`/фильтр для `findUnique`/`count`/`delete`) — не нужно, `Prisma.XArgs` тут проще и не требует поддержки лишнего класса.

## Слой 2 — бизнес/композиционные методы: `Promise<unknown>`

Как только метод строит свою форму ответа (пагинация, join нескольких сервисов, произвольный `select`, для которого нет готового именованного типа) — не пишем под неё `interface`/`type`, возвращаемый тип метода сервиса и метода контроллера, который просто транслирует результат — `Promise<unknown>`.

```ts
async findMany(dto: FindManyStationsQueryDto): Promise<unknown>
{
    const { page, perPage, search } = dto;
    const filter: Prisma.StationWhereInput = {
        name: search ? { contains: search, mode: "insensitive" } : undefined,
    };

    const [total, data] = await Promise.all([
        this.prismaService.station.count({ where: filter }),
        this.prismaService.station.findMany({ skip: (page - 1) * perPage, take: perPage, where: filter }),
    ]);

    return { data, total, page, lastPage: Math.ceil(total / perPage) };
}
```

Response DTO (`FindXxxResponseDto`, обёртка `PaginatedResponse<T>` — см. `docs/recipes/PAGINATION.md`) пишется не ради внутренней строгости, а только когда форма — часть публичного Swagger-контракта, который должен быть виден потребителю API.

## Слой 3 — узкий `select` при широком типе метода: локальный `any`

Когда `select`/`include` возвращает урезанный объект, а метод-обёртка объявлен с полным типом модели, TypeScript не даст читать вложенные поля напрямую. Не переписываем сигнатуру через `Prisma.XGetPayload<{ select: ... }>` — просто кастуем локальную переменную в `any` в точке использования:

```ts
const employee: any = await this.employeeService.create({
    data: { name, organizationId },
    select: { id: true, role: true, organization: { select: { id: true, name: true } } },
});

return employee.organization.name;
```

## Мелкие самодельные формы — inline object-тип, если легко выписать

Если форма не из Prisma-`select`, а просто маленькая собственная структура — выписать её прямо в сигнатуре дёшево, это не тот случай, где стоит экономить:

```ts
async parseBase64String(base64String: string): Promise<{ mimeType: string; cleanBase64: string } | undefined>
```

## Request / event / JWT payload — всегда `any`

Динамические структуры, форму которых наш код не контролирует напрямую (HTTP request после ручного `request.user = ...`, payload `@OnEvent`, payload JWT) — не типизируются вообще:

```ts
const request = context.switchToHttp().getRequest<any>();

@OnEvent("station.created", { async: true })
async handleStationCreated(event: any): Promise<boolean> { ... }
```

## Enum'ы — только из `@prisma/client`

Никогда не дублировать enum вручную string-literal union'ом или собственным `enum`. Если значения уже объявлены в `schema.prisma` — импортировать и использовать как есть, в том числе в guard'ах и DTO:

```ts
import { UserRole } from "@prisma/client";

@Roles(UserRole.ADMIN)
```

## Что НЕ нужно делать

- Не писать `interface`/`type` под форму, которую строит один метод и использует только он сам — возвращайте `unknown`.
- Не писать `Prisma.XGetPayload<...>` под каждый `select` — локальный `any` в точке использования не хуже по факту (TypeScript всё равно не проверяет форму объекта в рантайме) и не требует поддержки при изменении `select`.
- Не заводить response DTO, если форма не всплывает в Swagger как публичный контракт.
- Не типизировать `request`/event payload/JWT payload — это динамические структуры вне контроля нашего кода.
- Не оборачивать `create`/`update` в `Prisma.XCreateArgs`/`Prisma.XUpdateArgs`, если под рукой уже готовый DTO — лишний слой ради лишнего слоя (см. Слой 1 выше).
- Не заводить DTO под чистый CRUD-примитив без DTO по смыслу (`findUnique`/`count`/`delete` по `id`/фильтру) — `Prisma.XArgs` там проще.
