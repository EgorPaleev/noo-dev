# Request context через AsyncLocalStorage

**Паттерн на будущее**: `RequestContextService`/`RequestContextMiddleware` ниже в коде пока не существуют — заводить, когда появится реальная сквозная задача (аудит-лог, request-id в логах и т.п.), а не заранее.

Middleware, подключённый на `'*'` в `AppModule.configure()`, кладёт метаданные запроса (`userId`, `ipAddress`, `userAgent`, `method`) в `AsyncLocalStorage`; сервис-обёртка отдаёт текущий контекст геттером. Благодаря этому любой код ниже по стеку (например, Prisma-extension, который пишет audit-log) может прочитать «кто сейчас делает запрос», не получая эти данные явным параметром через десять слоёв вызовов. Механизм общий — не только для авторизации, годится для любых сквозных технических данных запроса (request-id для логов, tenant-id и т.п.).

```ts
// request-context.service.ts
export interface AuditContextInfo
{
    userId?: string;
    ipAddress?: string;
    userAgent?: string;
    method: string;
}

@Injectable()
export class RequestContextService
{
    private static readonly storage = new AsyncLocalStorage<AuditContextInfo>();

    get storage()
    {
        return RequestContextService.storage;
    }

    get currentContext(): AuditContextInfo | undefined
    {
        return RequestContextService.storage.getStore();
    }
}

// request-context.middleware.ts
@Injectable()
export class RequestContextMiddleware implements NestMiddleware
{
    constructor(private readonly contextService: RequestContextService) {}

    use(req: FastifyRequest["raw"], res: FastifyReply["raw"], next: () => void)
    {
        const context: AuditContextInfo = {
            userId: (req as any).user?.id ?? undefined,
            ipAddress: req.socket.remoteAddress,
            userAgent: req.headers["user-agent"],
            method: req.method ?? "GET",
        };

        this.contextService.storage.run(context, () => { next(); });
    }
}
```

Хранилище (`storage`) — `static`, а сам `RequestContextService` — обычный `@Injectable()`, инжектится конструктором как любой другой сервис. Благодаря `static` разные инстансы сервиса (в middleware, в guard'е, в Prisma-extension) видят один и тот же `AsyncLocalStorage`, хотя каждый получил свой собственный инстанс через DI — `.run(...)` вызывается снаружи, на объекте, который вернул геттер `storage`, а не статическим методом на классе.

Если контекст пополняется данными, доступными только позже в цепочке запроса (например, `userId` после того, как guard аутентифицировал пользователя — middleware выполняется раньше guard'ов) — это делается прямой мутацией объекта из `currentContext`: `this.contextService.currentContext.userId = user.id`.
