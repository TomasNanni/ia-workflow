---
id: STORY-005
prd: PRD-001
slug: schema-map-visualizer
title: Schema Map Visualizer
type: feature
priority: medium
complexity: medium
phase: 3
status: in-progress
labels: [frontend, ui]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: .agents/plans/PRD-001/STORY-005-schema-map-visualizer.plan.md
report: null
commit: null
depends_on: [STORY-004, STORY-002]
blocks: []
skills: [shadcn]
created: 2026-05-20
updated: 2026-05-20
---

# STORY-005: Schema Map Visualizer

## Description

As a user, I want to see the database schema on the side of the chat, so that I know what data is available for analysis.

## Acceptance Criteria

- [ ] `SchemaMap` component is implemented as a 50/50 split on the right side of the chat.
- [ ] Schema map displays tables and columns fetched from the analytics database.
- [ ] Users can toggle column details for each table.
- [ ] Layout is responsive, collapsing the schema map on small screens.

## Technical Notes

- Fetch schema information using a dedicated endpoint (e.g., `GET /api/v1/analytics/schema`).
- Use `shadcn` Accordion or similar for table/column list.

## Dependencies

- **Blocked by**: STORY-004, STORY-002
- **Blocks**: None

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 6, 7
