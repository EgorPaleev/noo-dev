# 0004. Multi-tenant theming and feature flags

## Status

Proposed

## Context

The app should support multiple companies (tenants): brand colors, logo, company name, and feature toggles. Today theming lives mainly in `:core:presentation` as a shared design system without per-tenant runtime config.

## Decision

**Intended flow (after authorization):**

1. Backend returns tenant config (theme, features, branding).
2. `ThemeRepository` receives it and persists locally (candidate stores: **KVault** or **multiplatform-settings** — pick one when implementing; do not add both).
3. `ThemeManager` applies config into Compose Theme.
4. The whole app recolors; feature flags gate screens / entry points.

Example config shape:

```json
{
  "companyId": "Sber",
  "theme": {
    "primary": "#…",
    "secondary": "#…",
    "background": "#…",
    "error": "#…"
  },
  "features": {
    "chat": true,
    "meetings": true,
    "workshops": false
  },
  "branding": {
    "logo": "…",
    "companyName": "…"
  }
}
```

**Constraints:**

- Theme application stays in shared Compose (`:core:presentation` or a dedicated theme core), not duplicated per feature.
- Feature flags should gate navigation / module entry, not scatter `if (company)` deep in unrelated UI without a clear API.
- New dependencies (KVault, settings) need confirmation and catalog versions.
- Do not hardcode tenant secrets or API keys in the repo.

## Consequences

- One binary can serve multiple brands after login.
- Need clear fallback theme when config is missing or offline (ties to Offline-First for cached tenant config).
- Until implemented, keep using the existing static theme and do not invent parallel theme systems in features.
- Diagram: [../architecture/diagrams/03-stack-offline-multitenant.png](../../../../../assets/projects/nootinder-mobile/docs/architecture/diagrams/03-stack-offline-multitenant.png).
