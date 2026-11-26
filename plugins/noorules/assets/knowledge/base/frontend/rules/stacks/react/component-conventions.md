# React Component Conventions

## Purpose

Keep React components cohesive and prevent local interactivity from widening
runtime or state boundaries unnecessarily.

## Applies when

Apply to React components, hooks and JSX.

## Does not apply when

Do not create wrappers or component splits that preserve no independent
responsibility. Framework runtime boundaries belong to the applicable
framework preset.

## Rules

- Keep rendering branches readable; avoid nested ternary expressions in JSX.
- Accept component input through one props parameter and follow the repository's
  documented destructuring convention.
- Keep state as close as possible to the UI or interaction that owns it.
- Extract a component when it creates a meaningful ownership, runtime,
  performance or reuse boundary.
- Avoid speculative generic components and prop surfaces.
- Forward rest props only when the underlying contract intentionally supports
  them.
- Handle applicable loading, empty, error, disabled and validation states.
- Preserve semantic HTML, accessible names, keyboard behavior and focus states.

## Checklist

- [ ] The component has one clear responsibility.
- [ ] Conditional rendering is readable.
- [ ] State and effects live with their owner.
- [ ] Extraction is justified by a real boundary.
- [ ] Applicable UI and accessibility states are present.

