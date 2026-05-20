---
id: STORY-005
prd: PRD-001
slug: schema-map-hardening
title: Schema Map & Security Hardening
type: enhancement
priority: medium
complexity: medium
phase: 3
status: todo
labels: [frontend, backend, security]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: null
report: null
commit: null
depends_on: [STORY-004]
blocks: []
skills: [shadcn, fastapi-python]
created: 2026-05-20
updated: 2026-05-20
---

# STORY-005: Schema Map & Security Hardening

## Description

As a user, I want to see the database schema and be assured that my queries are safe and efficient, so that I can explore data confidently.

## Acceptance Criteria

- [ ] `SchemaMap` component is implemented as a 50/50 split on the right side of the chat.
- [ ] Schema map displays tables and columns from the analytics database.
- [ ] Backend validates that all generated queries are strictly `SELECT` statements.
- [ ] Backend enforces a 10-second timeout on all database analytics queries.
- [ ] UI displays a clear error message if a query times out or fails validation.

## Technical Notes

- Use `SchemaMap` to help the user (and AI) understand the structure.
- Implementation of 10s timeout using SQLAlchemy execution options or FastAPI background tasks if needed.
- Ensure "Obsidian Deep" theme consistency across the schema visualizer.
- Strict string check or SQL parser to ensure `SELECT` only.

## Dependencies

- **Blocked by**: STORY-004
- **Blocks**: None

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 6, 7, 9, 14
