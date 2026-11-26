---
name: noo-git
description: "Объясняет Conventional Commits или готовит состав и сообщение Git-коммита по правилам текущего проекта."
---

# Правила Git

Для нового запроса используй [порядок входа рабочего навыка](../noo-rules/references/project-context.md#вызов-рабочего-навыка).

Для вопроса о формате открой только нужный модуль из [правил Git](../../assets/knowledge/base/git/rules/conventional-header.md). Дополнительные модули описывают [несовместимые изменения](../../assets/knowledge/base/git/rules/breaking-change.md) и [тело с подвалом](../../assets/knowledge/base/git/rules/body-and-trailers.md). Сверь требования с принятыми в проекте типами сообщений, областью и языком.

Если требуется подготовить коммит, используй [выбор состава](../../assets/knowledge/base/git/workflows/select-commit-changes.md) и [чек-лист](../../assets/knowledge/base/git/checklists/commit-ready.md). Изменяй индекс и создавай коммит только в рамках порученного пользователем действия. В пайплайне этап `git-commit` по умолчанию готовит файл `commit-ready` с предлагаемым составом и сообщением.
