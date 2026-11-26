# Naming и DTO

- Файлы — kebab-case. Внутри доменной папки (множественное число) файлы называются в единственном числе: `stations/station.controller.ts`, `station.service.ts`, `station.module.ts` → классы `StationController`, `StationService`, `StationModule`.
- DTO лежат в `dto/` рядом с модулем. Когда у домена много ответных DTO — они выносятся в `dto/response/`, запросные и command-DTO остаются в `dto/`.
- Naming DTO по действию:
  - `create-<entity>.dto.ts` → `Create<Entity>Dto`
  - `update-<entity>.dto.ts` → `Update<Entity>Dto` (все поля через `@IsOptional()`, без `PartialType`)
  - `find-many-<entity>-query.dto.ts` → `FindMany<Entity>QueryDto`, наследуется от общего `GetQueryDto` (см. `docs/recipes/PAGINATION.md`)
  - `find-many-<entity>-response.dto.ts` или обёртка `PaginatedResponse(<Entity>Dto)` — см. `docs/recipes/PAGINATION.md`
- Порядок декораторов на поле DTO: `@ApiProperty`/`@ApiPropertyOptional` → (`@Transform`, если нужно привести тип из query-строки) → `@IsOptional({ message: '...' })` (если поле необязательное) → `@IsNotEmpty({ message: '...' })` → декоратор типа (`@IsString`, `@IsInt`, `@IsNumber` и т.д. с `message`) → декораторы диапазона/формата (`@Min`, `@Max` и т.д. с `message`). Русский `message` обязателен везде — см. `docs/principles/LANGUAGE.md`.

```ts
export class CreateStationDto
{
    @ApiProperty({ description: "Имя" })
    @IsNotEmpty({ message: "Имя обязательно" })
    @IsString({ message: "Имя должно быть строкой" })
    name: string;
}

export class FindManyStationsQueryDto extends GetQueryDto
{
    @ApiPropertyOptional({ description: "Идентификатор сотрудника" })
    @Transform(({ value }) => (value ? parseInt(value) : undefined))
    @IsOptional()
    @IsInt({ message: "Идентификатор сотрудника должен быть числом" })
    employeeId: number;
}
```
