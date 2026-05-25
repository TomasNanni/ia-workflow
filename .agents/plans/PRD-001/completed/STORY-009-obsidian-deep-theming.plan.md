---
story: STORY-009
prd: PRD-001
slug: obsidian-deep-theming
title: "Obsidian Deep" Theming & Responsive Layout
type: ENHANCEMENT
complexity: MEDIUM
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-21
---

# Plan: "Obsidian Deep" Theming & Responsive Layout

## Summary

This plan details the implementation of the "Obsidian Deep" visual theme. We will update the global CSS using Tailwind v4 variables to define the palette (Deep Black, Charcoal, Emerald Green), apply gradients to the background, and add interactive glows. We will also ensure that Geist and JetBrains Mono fonts are correctly integrated and that the layout is responsive.

## User Story

As a user,
I want a professional and immersive dark theme,
So that the application feels modern and high-quality.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-009-obsidian-deep-theming.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | ENHANCEMENT |
| Complexity | MEDIUM |
| Systems Affected | frontend, css |
| Story | STORY-009 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| shadcn | Styling components via semantic tokens and CSS variables. | Tasks 1-3 |

---

## Patterns to Follow

### Tailwind v4 Variables
```css
// SOURCE: frontend/src/index.css (pattern)
@theme {
  --color-background: #09090b;
  --color-primary: #059669;
}
```

### Gradients
```jsx
// SOURCE: PRD Section 6
<div className="bg-linear-to-b from-[#09090b] to-[#27272a]">
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `frontend/src/index.css` | UPDATE | Define Obsidian Deep palette and global styles |
| `frontend/src/layouts/RootLayout.jsx` | UPDATE | Apply global background and font classes |
| `frontend/src/main.jsx` | UPDATE | Ensure fonts are imported |

---

## Tasks

### Task 1: Define Obsidian Deep Palette

- **File**: `frontend/src/index.css`
- **Action**: UPDATE
- **Implement**: Define colors:
  - `background`: `#09090b` (Deep Black)
  - `card`: `#27272a` (Charcoal)
  - `primary`: `#059669` (Emerald Green)
  - `accent`: `#059669` with glow effect
- **Validate**: Inspect elements in browser to see color variables applied.

### Task 2: Configure Fonts

- **File**: `frontend/src/main.jsx`, `frontend/src/index.css`
- **Action**: UPDATE
- **Implement**: Import `@fontsource-variable/geist` and `@fontsource-variable/jetbrains-mono`. Set `font-sans` and `font-mono` in `@theme`.
- **Validate**: Check typography in browser.

### Task 3: Global Background & Gradients

- **File**: `frontend/src/layouts/RootLayout.jsx`
- **Action**: UPDATE
- **Implement**: Apply `bg-linear-to-b from-background to-card` to the main wrapper. Add emerald glow to interactive elements (buttons, active sidebar items).
- **Validate**: Visual check of the background gradient.

### Task 4: Responsive Layout Tweaks

- **File**: `frontend/src/layouts/RootLayout.jsx`, `frontend/src/pages/dashboard/Dashboard.jsx`
- **Action**: UPDATE
- **Implement**: Ensure sidebar collapses correctly and content area pads/stacks on mobile.
- **Validate**: Test with Chrome DevTools mobile emulator.

---

## End-to-End Tests

- [ ] Open app → Background is deep black to charcoal gradient.
- [ ] Active links/buttons have emerald green highlights.
- [ ] Code snippets use JetBrains Mono.
- [ ] UI is readable and usable on mobile (375px width).

## Acceptance Criteria

- [ ] "Obsidian Deep" palette (Deep Black, Charcoal, Emerald Green) is implemented in `index.css`.
- [ ] Subtle linear gradients are applied to page backgrounds.
- [ ] Emerald Green glows are added to active/interactive elements.
- [ ] Geist (Sans) and JetBrains Mono (Code) fonts are correctly configured.
- [ ] The layout is fully responsive across mobile, tablet, and desktop.
