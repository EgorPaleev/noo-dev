# Guards и декораторы доступа

**Паттерн на будущее**: `RolesGuard`, `@Public()`/`@Roles()` и параметр-декоратор `@User()` ниже в коде пока не существуют — заводить вместе с первой реальной авторизацией/ролевой моделью, а не заранее.

## Guards

- Guard, который выполняется на каждом запросе (например проверка токена) — подключается глобально через `APP_GUARD`, кладёт результат в `request.user`, пропускает без проверки маршруты, помеченные соответствующим marker-декоратором (`@Public()` и т.п. — см. ниже).
- Guard, который проверяет роль/право — навешивается точечно через `@UseGuards(RolesGuard)` на конкретном контроллере/методе (не глобально), сравнивает `request.user.role` со списком, переданным в `@Roles(...)`.
- Доменный вариант того же паттерна (например, гвард на роль внутри конкретного модуля, а не общая роль пользователя) — своя metadata-key, своя бизнес-логика, но структура identична общему `RolesGuard`. Не пытаться притянуть доменную роль в общий guard — это логически разные вещи, разные guard-классы это отражают.

## Marker-декораторы для guard'ов

Каждый marker-декоратор экспортирует **свою metadata-key константой** — не полагаемся на строковый литерал, продублированный отдельно в декораторе и в guard'е (магическая строка в двух местах — источник рассинхрона при рефакторинге).

```ts
// public.decorator.ts
export const IS_PUBLIC_KEY = "isPublic";
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);

// auth.guard.ts
const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
    context.getHandler(),
    context.getClass(),
]);
```

Тот же паттерн — для `@Roles(...roles: UserRole[])` и любых доменных ролевых декораторов: экспортируемая `*_KEY`-константа (`ROLES_KEY`, `EMPLOYEE_ROLES_KEY` и т.п.), `SetMetadata` в декораторе, чтение через `Reflector.getAllAndOverride` в соответствующем guard'е — константа импортируется из файла декоратора, а не передекларируется заново внутри `canActivate`.

## Параметр-декоратор: текущий пользователь

Для задачи «достать текущего пользователя из request» (который guard выше уже положил в `request.user`) — `createParamDecorator`:

```ts
export const User = createParamDecorator((data: string | undefined, ctx: ExecutionContext) =>
{
    const request = ctx.switchToHttp().getRequest();
    if (!request?.user) return null;
    if (data) return request.user[data];
    return request.user;
});

// controller
async findMe(@User() user: any) { ... }
async findMe(@User("id") userId: number) { ... }
```

Тип `request`/payload — `any`, см. `docs/conventions/TYPESCRIPT.md`.
