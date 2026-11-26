# Event listeners

**Паттерн на будущее**: `@nestjs/event-emitter` пока не установлен, пример `StationListener` ниже — иллюстративный, такого файла в коде нет — заводить вместе с первым реальным доменным событием, а не заранее.

`@nestjs/event-emitter`: сервис эмитит событие после завершения бизнес-операции, слушатель — отдельный `@Injectable()`-класс с методами `@OnEvent`. На каждый связанный набор событий одного домена — один listener-класс, а не по listener-классу на каждое событие. Расположение файла внутри модуля — поддиректорий `listeners/` (см. `docs/architecture/MODULE-STRUCTURE.md`).

```ts
// station.service.ts
this.eventEmitter.emit("station.created", { stationId: station.id });

// listeners/station.listener.ts
@Injectable()
export class StationListener
{
    constructor(private readonly mailService: MailService) {}

    @OnEvent("station.created", { async: true })
    async handleStationCreated(event: any): Promise<boolean>
    {
        await this.mailService.sendStationCreatedNotification(event.stationId);
        return true;
    }
}
```

Имя события — `<домен>.<действие>` через точку (`station.created`, `order.published`); на практике встречаются и смешанные варианты через точку и дефис (`organization.order.carrier-picked`) — единообразие не строгое. Payload события не типизируется (`any`, см. `docs/conventions/TYPESCRIPT.md`) — это динамическая шина, а не прямой вызов метода.
