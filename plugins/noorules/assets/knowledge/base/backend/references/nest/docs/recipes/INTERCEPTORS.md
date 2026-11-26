# Глобальные interceptor'ы

**Паттерн на будущее**: `CoreModule`/`TransformInterceptor`/`LoggingInterceptor` ниже в коде пока не существуют (нет `src/core/`) — заводить вместе с первым реальным эндпоинтом, которому это нужно, а не заранее (см. `docs/principles/GENERAL.md`).

Ответ каждого эндпоинта оборачивается в единый конверт `{ data: T }` через `TransformInterceptor`. Рядом с ним, тем же способом, подключён `LoggingInterceptor` — логирует время выполнения запроса. Оба зарегистрированы глобально (`APP_INTERCEPTOR`) в отдельном модуле (`CoreModule`), а не напрямую в `AppModule`, и оба относятся к сквозным механизмам, а не к конкретному домену.

```ts
// core/interceptors/transform.interceptor.ts
export interface Response<T>
{
    data: T;
}

@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, Response<T>>
{
    intercept(context: ExecutionContext, next: CallHandler<T>): Observable<Response<T>>
    {
        return next.handle().pipe(map(data => ({ data })));
    }
}

// core/interceptors/logging.interceptor.ts
@Injectable()
export class LoggingInterceptor implements NestInterceptor
{
    intercept(context: ExecutionContext, next: CallHandler): Observable<unknown>
    {
        const now = Date.now();
        return next.handle().pipe(tap(() => console.log(`Запрос обработан за ${Date.now() - now}мс`)));
    }
}

// core.module.ts
@Module({
    providers: [
        { provide: APP_INTERCEPTOR, useClass: TransformInterceptor },
        { provide: APP_INTERCEPTOR, useClass: LoggingInterceptor },
    ],
})
export class CoreModule {}
```

Именно поэтому методы контроллера возвращают сырые данные без ручной обёртки (`Promise<unknown>`, см. `docs/conventions/TYPESCRIPT.md`) — обёртка не забота контроллера, это отдельный сквозной слой.
