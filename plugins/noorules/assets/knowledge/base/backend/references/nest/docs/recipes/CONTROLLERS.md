# Controllers

**Паттерн на будущее**: пример `StationController` ниже — иллюстративный, такого контроллера в репозитории нет — паттерн применяется к первому реальному контроллеру (см. skill `new-module`).

## Swagger-декораторы

Порядок декораторов на методе контроллера: `@ApiOperation` → `@ApiOkResponse`/`@ApiCreatedResponse` (с `type`, часто generic-обёртка вроде `PaginatedResponse(EntityDto)` — см. `docs/recipes/PAGINATION.md`) → `@ApiBearerAuth("access-token")` (если эндпоинт требует авторизации) → `@ApiQuery(...)` вручную на каждое поле query-DTO. Swagger не подхватывает `@ApiPropertyOptional` с полей унаследованного DTO автоматически на уровне `@Get()`, поэтому query-параметры пагинации/фильтров описываются вручную ещё раз в контроллере, даже если DTO их уже описывает.

```ts
@ApiTags("Станции")
@Controller("stations")
export class StationController
{
    constructor(private readonly stationService: StationService) {}

    @ApiOperation({ summary: "Получить станции" })
    @ApiOkResponse({ description: "Сущности станций", type: PaginatedResponse(StationDto) })
    @ApiBearerAuth("access-token")
    @ApiQuery({ type: "number", name: "page", description: "Номер страницы (default: 1)", required: false })
    @ApiQuery({ type: "number", name: "perPage", description: "Количество записей на страницу (default: 50)", required: false })
    @Get()
    async findMany(@Query() query: FindManyStationsQueryDto): Promise<unknown>
    {
        return this.stationService.findMany(query);
    }
}
```

## Path-параметры

Числовой `:id` в пути — через встроенный `ParseIntPipe` из `@nestjs/common`, не через кастомный pipe:

```ts
@Get(":id/budget")
async findStationBudget(@Param("id", ParseIntPipe) stationId: number): Promise<unknown> { ... }
```

## Guards на конкретном эндпоинте

`@UseGuards(RolesGuard)` + `@Roles(UserRole.ADMIN)` (см. `docs/recipes/GUARDS.md`) вешаются на конкретный метод, а не на весь контроллер — доступ ограничивается точечно, остальные методы контроллера остаются под общими правилами глобального guard'а:

```ts
@ApiBearerAuth("access-token")
@UseGuards(RolesGuard)
@Roles(UserRole.ADMIN)
@Post()
async create(@Body() dto: CreateStationDto): Promise<unknown> { ... }
```

Возвращаемый тип методов — см. `docs/conventions/TYPESCRIPT.md`.
