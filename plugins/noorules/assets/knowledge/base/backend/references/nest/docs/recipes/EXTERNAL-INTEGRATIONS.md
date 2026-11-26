# Интеграции с внешними сервисами

## Сверяться с актуальной документацией, а не с памятью

Перед тем как писать интеграцию с новым SDK/библиотекой — и перед тем как вручную писать логику, которую библиотека, вероятно, уже реализует (парсинг, ретраи, форматирование, готовый health-индикатор и т.п.) — свериться с официальной документацией через `WebFetch`/`WebSearch`, а не полагаться на память: у библиотек меняются API между мажорными версиями, обучающие данные могут быть устаревшими или просто не про ту версию, что стоит в `package.json` этого проекта. Конкретно проверять:

- Есть ли у SDK официальный NestJS-модуль (см. правило ниже) — не предполагать по памяти, а посмотреть в официальном README/докe SDK на момент реализации.
- Актуальную сигнатуру `useFactory`/опций модуля для установленной в `package.json` версии — они меняются между мажорными релизами.
- Не реализует ли SDK нужную функциональность уже готовым методом/опцией, прежде чем писать её руками поверх клиента.

## Правило выбора паттерна

- **Есть официальный NestJS-модуль у SDK** (`XModule.forRootAsync({ useFactory, inject: [ConfigService] })`) — используем его, конфигурируя через `ConfigService`. Обёрточный сервис инжектит клиент через механизм, который предоставляет сам модуль (специфичный `@InjectXxx()`-декоратор либо сервис, который модуль сам зарегистрировал). Это основной вариант.
- **Официального Nest-модуля нет** — только тогда пишем свой factory provider со строковым токеном инъекции:

```ts
// providers/some-sdk.provider.ts
export const SOME_SDK = "SOME_SDK";

export const someSdkProvider: Provider = {
    provide: SOME_SDK,
    useFactory: (configService: ConfigService) => new SomeSdkClient({
        apiKey: configService.get("someSdkApiKey"),
    }),
    inject: [ConfigService],
};

// some.service.ts
constructor(@Inject(SOME_SDK) private readonly client: SomeSdkClient) {}
```

Так конфигурация клиента живёт в одном месте, а сервис зависит от токена, а не от конкретной реализации — её проще подменить в тестах или заменить провайдера. Это запасной вариант, применяется только когда официального модуля нет.

## Пример официального модуля

Почта (`MailerModule.forRootAsync`, шаблоны через handlebars), S3 (`S3Module.forRootAsync`, инъекция через `@InjectS3()`), HTTP-клиент для стороннего REST API (`@nestjs/axios` `HttpModule`, обёрточный сервис инжектит `HttpService`).

```ts
// mail.module.ts
@Module({
    imports: [
        MailerModule.forRootAsync({
            inject: [ConfigService],
            useFactory: (configService: ConfigService) => ({
                transport: {
                    host: configService.get<string>("MAIL_HOST"),
                    port: Number(configService.get("MAIL_PORT")),
                    secure: false,
                    auth: {
                        user: configService.get<string>("MAIL_USER"),
                        pass: configService.get<string>("MAIL_PASS"),
                    },
                },
                defaults: { from: configService.get<string>("MAIL_FROM") },
                template: {
                    dir: join(__dirname, "templates"),
                    adapter: new HandlebarsAdapter(),
                    options: { strict: true },
                },
            }),
        }),
    ],
    providers: [MailService],
    exports: [MailService],
})
export class MailModule {}
```

Здесь `configService.get("MAIL_HOST")` читает переменную окружения напрямую по сырому UPPER_CASE-имени — это осознанное исключение из общего правила «единственная точка доступа к env — `configuration.ts`» (см. `docs/recipes/CONFIGURATION.md`): конфиг сторонних `XModule.forRootAsync` собирается прямо в месте объявления модуля, а не проксируется через `configuration.ts`. Переменная всё равно описывается в `.env.example` и `src/config/validation.schema.ts`, как любая другая — только без camelCase-ключа в `configuration.ts`.

Обёрточный сервис (`MailService`, `FileService`, доменный HTTP-клиент к стороннему API) — тонкий слой поверх клиента: собирает и отправляет вызов с нужными данными, не тащит в себя бизнес-логику модуля, ради которого письмо/файл отправляются.

Redis (кэш) — уже готовая часть инфраструктуры этого стартера, а не пример интеграции, которую нужно с нуля добавлять — см. `docs/recipes/REDIS.md`.
