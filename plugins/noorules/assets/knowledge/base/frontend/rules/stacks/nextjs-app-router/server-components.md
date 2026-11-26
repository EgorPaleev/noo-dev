# Next.js Server and Client Components

## Purpose

Keep client boundaries narrow while allowing fully interactive components to
remain cohesive.

## Applies when

Apply to Next.js App Router components that mix server-rendered composition and
client-only capabilities.

## Does not apply when

Do not split a component merely to reduce file size. A component that is
intrinsically interactive may be client-rendered as a whole.

## Rules

- Keep a component server-rendered when only an isolated fragment needs hooks,
  state, effects, events, browser APIs or a client-only library.
- Extract that fragment into an adjacent, domain-named Client Component.
- Place the client directive only at the intended client entry boundary.
- Keep fragment-owned queries, state and loading/error UI inside that fragment.
- Pass minimal serializable props across the server/client boundary.
- Do not import server-only modules through client-safe public entry points.
- Document a project exception when a wider client boundary is intentional.

## Checklist

- [ ] Client-only capability has the narrowest useful owner.
- [ ] The split does not create an empty wrapper.
- [ ] Props crossing the boundary are serializable.
- [ ] Server-only modules stay out of the client graph.
- [ ] Interactive state and UI states remain cohesive.

