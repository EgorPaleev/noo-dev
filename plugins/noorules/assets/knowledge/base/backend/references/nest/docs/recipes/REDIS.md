# Redis

`RedisService` — тонкая обёртка над `cache-manager`/`@keyv/redis` (не `ioredis` напрямую), три метода:

```ts
@Injectable()
export class RedisService
{
    constructor(@Inject(CACHE_MANAGER) private cacheManager: Cache) {}

    async get<T>(key: string): Promise<T | undefined>
    {
        return this.cacheManager.get<T>(key);
    }

    async set<T>(key: string, value: any, ttl: number): Promise<T | undefined>
    {
        return this.cacheManager.set<T>(key, value, ttl);
    }

    async del(key: string): Promise<boolean>
    {
        return this.cacheManager.del(key);
    }
}
```

`RedisModule` — глобальный (`@Global()`), других модулей его импортировать не нужно (см. `docs/architecture/MODULE-BOUNDARIES.md`).

Используется как read-through cache: сначала `get`, если пусто — берём данные из Prisma/внешнего API и кладём через `set`. Ключи — вручную собранные template-строки (например, `` `station:budget:${stationId}` ``); единого реестра ключей нет, ключ живёт рядом с местом использования (как `private readonly`-константа на классе, если шаблон ключа нужен нескольким методам одного сервиса — см. `docs/conventions/CONSTANTS.md`).
