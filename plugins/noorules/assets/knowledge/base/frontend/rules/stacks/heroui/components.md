# HeroUI Components

## Purpose

Use HeroUI consistently in projects that explicitly install HeroUI and its
required styling integration.

## Applies when

Apply when the project has installed HeroUI and selected this preset.

## Does not apply when

Do not assume HeroUI, its variants, or a class-composition helper in projects
that did not select this preset.

## Rules

- Check the official HeroUI documentation for the installed major version
  before changing component APIs.
- For HeroUI React v3, first use the official [documentation
  index](https://heroui.com/react/llms.txt) to discover the relevant component
  or topic.
- Then use the official [component
  documentation](https://heroui.com/react/llms-components.txt) for component
  APIs, slots, states and examples.
- Use the official [patterns
  documentation](https://heroui.com/react/llms-patterns.txt) for composition,
  styling, theming, animation and framework integration.
- Load the official [full
  documentation](https://heroui.com/react/llms-full.txt) only when a task
  crosses component and pattern boundaries.
- Do not infer an installed v2 or later-major API from the v3 sources. Prefer
  installed package types and documentation for the exact installed version
  when they disagree.
- Apply the selected component UI library rule for wrappers, states, tokens and
  accessibility; it is the canonical owner of those invariants.
- Use HeroUI primitives for applicable interactive and feedback states.
- Keep HeroUI providers, slots, variants and theme integration aligned with the
  installed version and existing project adapter.
- Keep vendor-specific notification, modal-registry and class-helper choices in
  project documentation.

## Checklist

- [ ] HeroUI is installed and selected.
- [ ] The generic component UI checklist was applied.
- [ ] Provider, slots, variants and theme usage match the installed version.
- [ ] No project-specific component contract was added here.
