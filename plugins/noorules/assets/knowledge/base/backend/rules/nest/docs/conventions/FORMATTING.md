# Форматирование

Форматирование полностью на ESLint (`eslint.config.mjs`, `@stylistic/eslint-plugin`) — отдельного `prettier`/`npm run format` в проекте нет, всё ловится и автофиксится через `npm run lint`.

Ключевые правила:

- отступ — 4 пробела;
- **Allman-стиль скобок** для блоков (тело класса, функции, `if`/`else`, `try`/`catch`, стрелочные функции с телом-блоком) — открывающая `{` на новой строке;
- объектные литералы (аргументы вызова, конфиг модуля/декоратора) — открывающая `{` на той же строке, это не блок;
- двойные кавычки, точка с запятой обязательна, висячая запятая на многострочных списках/объектах.

```ts
@Injectable()
export class StationService
{
    constructor(private readonly prismaService: PrismaService) {}

    async findById(stationId: number): Promise<Station>
    {
        if (!stationId)
        {
            throw new BadRequestException("Не указан идентификатор вокзала");
        }

        return this.prismaService.station.findUnique({
            where: { id: stationId },
        });
    }
}
```

Не нужно вручную подгонять отступы/скобки — `npm run lint` делает это сам (`eslint --fix`).
