---
id: STORY-004
prd: PRD-001
slug: chat-interface-interaction
title: Chat Interface & Agent Interaction
type: feature
priority: high
complexity: medium
phase: 3
status: todo
labels: [frontend, ui, chat]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: null
report: null
commit: null
depends_on: [STORY-002, STORY-003]
blocks: [STORY-005]
skills: [shadcn, vercel-react-best-practices]
created: 2026-05-20
updated: 2026-05-20
---

# STORY-004: Chat Interface & Agent Interaction

## Description

As a user, I want a clean and distraction-free chat interface, so that I can focus on my data analysis.

## Acceptance Criteria

- [ ] `ChatInterface` component is implemented with Emerald Green accents for agent messages.
- [ ] User can type a message and send it (via Enter or Send button).
- [ ] Messages are displayed in a scrollable thread with distinct styles for User and Agent.
- [ ] Agent responses include the answer and, if applicable, the SQL query used (styled with JetBrains Mono).
- [ ] Loading state (skeleton or spinner) is shown while waiting for the agent.

## Technical Notes

- Use `shadcn/ui` components for buttons, inputs, and cards.
- Follow `vercel-react-best-practices` for efficient rendering and state management.
- Handle chat interaction using the `POST /api/v1/sessions/{id}/chat` endpoint.
- Use `lucide-react` for icons.

## Dependencies

- **Blocked by**: STORY-002, STORY-003
- **Blocks**: STORY-005

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 6, 7
