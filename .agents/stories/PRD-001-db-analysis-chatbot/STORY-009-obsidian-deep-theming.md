---
id: STORY-009
prd: PRD-001
slug: obsidian-deep-theming
title: "Obsidian Deep" Theming & Responsive Layout
type: enhancement
priority: medium
complexity: medium
phase: 3
status: todo
labels: [frontend, ui, css]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: null
report: null
commit: null
depends_on: []
blocks: [STORY-003, STORY-004]
skills: [shadcn]
created: 2026-05-20
updated: 2026-05-20
---

# STORY-009: "Obsidian Deep" Theming & Responsive Layout

## Description

As a user, I want a professional and immersive dark theme, so that the application feels modern and high-quality.

## Acceptance Criteria

- [ ] "Obsidian Deep" palette (Deep Black, Charcoal, Emerald Green) is implemented in `index.css`.
- [ ] Subtle linear gradients are applied to page backgrounds.
- [ ] Emerald Green glows are added to active/interactive elements.
- [ ] Geist (Sans) and JetBrains Mono (Code) fonts are correctly configured.
- [ ] The layout is fully responsive across mobile, tablet, and desktop.

## Technical Notes

- Use Tailwind v4 CSS variables for the palette.
- Implement gradients using `bg-linear-to-b`.
- Ensure shadcn components inherit these styles.

## Dependencies

- **Blocked by**: None
- **Blocks**: STORY-003, STORY-004

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 6
