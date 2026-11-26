# Диплинки

Приложение открывает экраны саммита по ссылкам двух видов с одинаковым путём:

- `sovpa://summits/{summitId}/...` — своя схема, работает без настроек на сервере;
- `https://sovpa.ru/summits/{summitId}/...` (и `www.sovpa.ru`) — App Links (Android) / Universal Links (iOS), требуют файлов верификации на домене (см. ниже).

## Пути

| Путь | Экран | Id |
|---|---|---|
| `/summits/{summitId}/participants/{profileId}` | Профиль участника | summit-profile UUID |
| `/summits/{summitId}/speakers/{speakerId}` | Профиль спикера | id спикера |
| `/summits/{summitId}/chats/{profileId}` | Чат с участником | summit-profile UUID собеседника (не chat_id) |
| `/summits/{summitId}/meetings/{meetingId}` | Карточка встречи | id встречи |
| `/summits/{summitId}/sessions/{eventId}` | Сессия программы | id элемента программы |
| `/summits/{summitId}/faq` | FAQ | — |
| `/summits/{summitId}/faq/{itemId}` | FAQ с раскрытым вопросом | id вопроса |
| `/summits/{summitId}/navigation/{pointId}` | Карта площадки с выбранной точкой | id точки навигации |

Query-параметры и `#fragment` игнорируются, завершающий `/` допустим. Неизвестный путь игнорируется.

## Поведение

- Пользователь не авторизован: ссылка запоминается и открывается после входа.
- `summitId` совпадает с текущим саммитом: экран открывается поверх текущего стека.
- Другой саммит, в котором пользователь состоит: саммит становится текущим, стек — «главная саммита → экран».
- Саммит, в котором пользователь не состоит: показывается тост «Саммит из ссылки недоступен», навигация не меняется.

## Что нужно разместить на sovpa.ru

Оба файла отдаются по HTTPS без редиректов, `Content-Type: application/json`.

### `https://sovpa.ru/.well-known/assetlinks.json`

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "ru.sovpa",
      "sha256_cert_fingerprints": ["<SHA-256 release-ключа подписи>"]
    }
  }
]
```

Если приложение подписывается в Google Play (Play App Signing), нужен SHA-256 ключа из Play Console → «Целостность приложения». Для отладочных сборок можно добавить отпечаток debug-ключа вторым элементом массива.

### `https://sovpa.ru/.well-known/apple-app-site-association`

Файл без расширения.

```json
{
  "applinks": {
    "details": [
      {
        "appIDs": ["M5FALJYS77.ru.sovpa"],
        "components": [
          { "/": "/summits/*" }
        ]
      }
    ]
  }
}
```

То же содержимое нужно на `www.sovpa.ru`, если ссылки будут с `www`.

## Проверка

Android:

```bash
adb shell am start -W -a android.intent.action.VIEW -d "sovpa://summits/<summitId>/sessions/<eventId>" ru.sovpa
```

До размещения `assetlinks.json` https-ссылки можно включить вручную:

```bash
adb shell pm set-app-links-user-selection --user cur --package ru.sovpa true sovpa.ru
```

iOS (симулятор):

```bash
xcrun simctl openurl booted "sovpa://summits/<summitId>/sessions/<eventId>"
```
