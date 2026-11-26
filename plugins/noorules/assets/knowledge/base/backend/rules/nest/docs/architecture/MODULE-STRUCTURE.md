# Структура доменного модуля

Папка модуля — множественное число, файлы внутри — единственное (см. `docs/conventions/NAMING.md`):

```
items/
    item.controller.ts
    item.service.ts
    item.module.ts
    dto/
        create-item.dto.ts
        update-item.dto.ts
        find-many-items-query.dto.ts
        response/
            find-many-items-response.dto.ts
```

`dto/response/` появляется только когда ответных DTO у домена много (от нескольких штук) — для одного-двух response-DTO достаточно `dto/`.

Та же логика — для любого дополнительного механизма модуля, которых может быть несколько (event-листенеры, BullMQ-процессоры и т.п.): свой поддиректорий во множественном числе, а не вперемешку с `*.controller.ts`/`*.service.ts` на одном уровне — иначе плоский список файлов модуля быстро становится нечитаемым:

```
orders/
    order.controller.ts
    order.service.ts
    order.module.ts
    dto/
        ...
    listeners/
        order.listener.ts
    processors/
        order.processor.ts
```

Для одного файла в категории поддиректорий заводится по той же причине, что и `dto/` — по единообразию, а не потому что файлов уже несколько.

Контроллер зависит только от сервиса и никогда не импортирует `PrismaService`/Prisma-типы напрямую (см. `docs/recipes/PRISMA.md`). Написание самого контроллера (Swagger-декораторы, path-параметры, guard'ы на эндпоинте) — см. `docs/recipes/CONTROLLERS.md`.
