---
id: STORY-004
prd: PRD-001
slug: chat-interface-interaction
title: Chat Interface UI
type: feature
priority: high
complexity: medium
phase: 3
status: in-progress
labels: [frontend, ui, chat]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: .agents/plans/PRD-001/STORY-004-chat-interface-interaction.plan.md
report: null
commit: null
depends_on: [STORY-007, STORY-003, STORY-009]
blocks: [STORY-005]
skills: [shadcn, vercel-react-best-practices]
created: 2026-05-20
updated: 2026-05-20
---

# STORY-004: Chat Interface UI

## Description

As a user, I want a clean and distraction-free chat interface, so that I can focus on my data analysis.

## Acceptance Criteria

- [ ] `ChatInterface` component is implemented with distinct styles for User and Agent.
- [ ] User can type a message and send it.
- [ ] Messages are displayed in a scrollable thread.
- [ ] Agent responses display SQL queries in a code block (JetBrains Mono).
- [ ] Loading state is shown while waiting for the agent response.

## Technical Notes

- Use `shadcn/ui` components for chat bubbles and inputs.
- Handle chat interaction via the `POST /api/v1/sessions/{id}/chat` endpoint.
- Use `lucide-react` for icons.

## Dependencies

- **Blocked by**: STORY-007, STORY-003, STORY-009
- **Blocks**: STORY-005

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 6, 7
