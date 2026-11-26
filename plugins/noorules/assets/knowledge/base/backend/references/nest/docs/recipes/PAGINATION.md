# Пагинация и общие DTO

Повторяющиеся куски выносятся в `src/common/dto/` при появлении второго домена, которому они нужны:

- `GetQueryDto` (`src/common/dto/get-query.dto.ts`) — базовый класс с `page`/`perPage` (дефолты, `@Min`/`@Max`, `@Transform` из query-строки в число) — все `FindMany*QueryDto` от него наследуются. Уже реализован в этом стартере, наследовать напрямую.
- `PaginatedResponse<T>(DataDto)` — generic-функция, возвращающая класс с `data: T[]`, `total`, `page`, `lastPage`, `nextPage`, используется как `type` в `@ApiOkResponse`.
- `IdResponseDto` — простой ответ `{ id: number }` для эндпоинтов, которые создают сущность и не должны возвращать её целиком.

**Паттерн на будущее**: в отличие от `GetQueryDto` (уже реализован), `PaginatedResponse`/`IdResponseDto` как файлы в `src/common/dto/` пока не заведены — добавляются вместе с первым модулем, которому реально нужен пагинированный/id-ответ, а не заранее.

```ts
// common/dto/paginated-response.dto.ts
export function PaginatedResponse<T>(DataDto: Type<T>)
{
    abstract class PaginatedResponseClass
    {
        @ApiProperty({ type: [DataDto] })
        data: T[];

        total: number;
        page: number;
        lastPage: number;
        nextPage: number | null;
    }

    Object.defineProperty(PaginatedResponseClass, "name", {
        value: `Paginated${DataDto.name}`,
        writable: false,
    });

    return PaginatedResponseClass as Type<any>;
}
```

Naming DTO, которые используют эти общие классы (`FindMany*QueryDto`, `FindMany*ResponseDto`) — см. `docs/conventions/NAMING.md`.
