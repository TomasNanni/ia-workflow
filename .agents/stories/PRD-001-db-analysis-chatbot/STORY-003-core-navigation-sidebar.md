---
id: STORY-003
prd: PRD-001
slug: core-navigation-sidebar
title: Navigation & Session List UI
type: feature
priority: medium
complexity: small
phase: 3
status: todo
labels: [frontend, ui, react-router]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: null
report: null
commit: null
depends_on: [STORY-001]
blocks: [STORY-004]
skills: [react-router-declarative-mode, shadcn, vercel-react-best-practices]
created: 2026-05-20
updated: 2026-05-20
---

# STORY-003: Navigation & Session List UI (with Dates)

## Description

As a user, I want to see my previous conversations in a sidebar with their creation dates, so that I can easily identify and switch between analyses.

## Acceptance Criteria

- [ ] `AppSidebar` component (shadcn/ui) displays a list of recent chat sessions for the logged-in user.
- [ ] Each session entry in the sidebar shows the `title` and its `created_at` date (formatted).
- [ ] Sessions are ordered by date (newest first).
- [ ] Clicking a session navigates to `/chat/:sessionId`.
- [ ] "Obsidian Deep" theme (Black/Charcoal/Emerald) is applied app-wide via `index.css`.
- [ ] "New Chat" button starts a fresh analysis.

## Technical Notes

- Use `date-fns` or similar for formatting timestamps in the sidebar.
- Implement CSS variables for the "Obsidian Deep" palette in `index.css`.
- The sidebar should reflect the active route state.
- Ensure the sidebar collapses/expands correctly as per `shadcn/ui` Sidebar component.

## Dependencies

- **Blocked by**: STORY-001, STORY-006
- **Blocks**: STORY-004

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 6, 7
