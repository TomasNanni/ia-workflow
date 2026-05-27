---
id: STORY-010
prd: PRD-001
slug: session-title-generation
title: Automated Session Title Generation
type: enhancement
priority: low
complexity: small
phase: 3
status: done
labels: [backend, ai]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: .agents/plans/PRD-001/completed/STORY-010-session-title-generation.plan.md
report: .agents/reports/PRD-001/STORY-010-session-title-generation.report.md
commit: a255e16
depends_on: [STORY-007]
blocks: []
skills: [building-pydantic-ai-agents]
created: 2026-05-20
updated: 2026-05-27
---

# STORY-010: Automated Session Title Generation

## Description

As a user, I want my chat sessions to have descriptive titles based on my first question, so that I can easily find them in the history.

## Acceptance Criteria

- [ ] After the first user message in a session, the AI agent generates a short (3-5 words) title.
- [ ] The session record in SQLite is updated with this generated title.
- [ ] The sidebar reflects the new title immediately.

## Technical Notes

- Use a separate, small prompt to the AI for title generation.
- Trigger this only if the session title is still the default (e.g., "New Chat").

## Dependencies

- **Blocked by**: STORY-007
- **Blocks**: None

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 4, 15
