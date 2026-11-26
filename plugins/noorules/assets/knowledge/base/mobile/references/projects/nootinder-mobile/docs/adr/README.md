# Architecture Decision Records (ADR)

ADRs capture decisions that should outlive a single PR or chat session.

## When to add an ADR

- Choosing or changing navigation, DI, networking, storage, or module boundaries.
- Accepting a pattern that other features should copy.
- Deprecating an existing approach.

While architecture is still evolving, prefer status **Proposed** or **In progress** until the team explicitly accepts the decision.

## How to add

1. Copy `0000-template.md` to `NNNN-short-title.md` (next free number).
2. Fill Context / Decision / Consequences.
3. Link from [architecture.md](../architecture.md) if it changes the current picture.
4. Do not invent “Accepted” status for decisions that are only observed in code.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-modular-feature-api-impl.md) | Modular feature api/impl split | In progress |
| [0002](0002-feature-layered-architecture.md) | Feature layered architecture (Presentation / Domain / Data) | Proposed |
| [0003](0003-offline-first.md) | Offline-First data strategy | Proposed |
| [0004](0004-multi-tenant-theming.md) | Multi-tenant theming and feature flags | Proposed |
| [0006](0006-localization-strings.md) | Localization: string resources, UiText and StringProvider | Proposed |
| [0007](0007-summit-chat-socket.md) | Summit-level chat WebSocket and unread badge | Proposed |
| [0008](0008-call-sign-in.md) | Вход звонком через /api/auth/otp | Proposed |

Living overview + diagrams: [architecture.md](../architecture.md).
