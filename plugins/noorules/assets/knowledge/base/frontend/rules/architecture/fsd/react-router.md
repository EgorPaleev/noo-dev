# FSD with React Router

## Purpose

Integrate React Router route configuration with Feature-Sliced Design page
ownership and public APIs.

## Applies when

Apply when a React project explicitly uses Feature-Sliced Design and the
installed `react-router` package for browser routing.

## Does not apply when

Do not apply to framework-owned file routing, non-FSD projects or projects that
document another routing composition boundary.

## Rules

- Keep application bootstrap, router creation, providers, error boundaries and
  guarded layout composition in the FSD app layer.
- When using a data router such as `createBrowserRouter`, create the router once
  outside the React component tree and pass it to the application provider.
- Keep route-level UI and page-local behavior in page slices; expose each route
  component through its slice public API.
- Import pages, layouts and guards into app routing only through their public
  APIs.
- Centralize typed path builders when the project already uses a route-helper
  contract; do not duplicate literal paths across navigation and route config.
- Keep authentication guards and reusable application layouts above their
  child routes rather than repeating them in page components.
- Keep navigation-menu registration separate from route existence. Add a menu
  item only when the route is intended to be discoverable there.
- Keep loaders, actions and error elements with the owner selected by project
  architecture. Do not move page-specific behavior into shared routing merely
  because React Router can register it globally.
- Configure TypeScript and the bundler with matching aliases for every actual
  FSD layer; do not create aliases or empty layers speculatively.
- Keep browser-router version-specific APIs aligned with the installed package.

## Checklist

- [ ] Router creation and guarded layouts belong to app initialization.
- [ ] Route components come from page public APIs.
- [ ] Path helpers and route registration agree.
- [ ] Menu visibility is an explicit separate decision.
- [ ] Page-specific behavior remains in the page owner.
- [ ] TypeScript and bundler aliases resolve the same real layers.
