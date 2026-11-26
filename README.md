# NooRules Dev

Разработка, ревью, тестирование и выпуск.

## Установка в Codex

```sh
codex plugin marketplace add git@github.com:EgorPaleev/noo-dev.git
codex plugin add noorules@noorules-dev
```

Откройте проект и один раз вызовите `$noo-setup`. Затем начните новый чат в этом проекте. Для обычной задачи сначала согласуйте план, посмотрите способ исполнения и напишите «запускай». Точечный запрос с понятным результатом можно выполнить сразу. Для явного входа используйте `$noo-task`.

## Установка в Claude Code

```sh
claude plugin marketplace add git@github.com:EgorPaleev/noo-dev.git
claude plugin install noorules@noorules-dev --scope project
```

В новой сессии вызовите `/noorules:noo-task`.

Навыки и материалы лежат в `plugins/noorules/` и готовы к установке из этого репозитория.
