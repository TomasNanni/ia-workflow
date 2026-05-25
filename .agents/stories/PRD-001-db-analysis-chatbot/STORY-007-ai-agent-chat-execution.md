---
id: STORY-007
prd: PRD-001
slug: ai-agent-chat-execution
title: AI Agent Query Execution & Chat API
type: feature
priority: high
complexity: medium
phase: 3
status: done
labels: [backend, ai, api]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: .agents/plans/PRD-001/completed/STORY-007-ai-agent-chat-execution.plan.md
report: .agents/reports/PRD-001/STORY-007-ai-agent-chat-execution.report.md
commit: 0c93cca
depends_on: [STORY-002]
blocks: [STORY-004, STORY-010, STORY-011]
skills: [building-pydantic-ai-agents, fastapi-python]
created: 2026-05-20
updated: 2026-05-25
---

# STORY-007: AI Agent Query Execution & Chat API

## Description

As a user, I want the AI agent to execute SQL queries and provide answers, so that I can get insights from the database.

## Acceptance Criteria

- [x] Agent has `execute_read_query` tool to run SELECT statements against PostgreSQL.
- [x] `POST /api/v1/sessions/{id}/chat` endpoint processes user messages.
- [x] The entire conversation (user/agent) is stored in the session's `messages` JSON field.
- [x] Agent response includes both the natural language answer and the SQL query used.

## Technical Notes

- Use SQLAlchemy's `text()` for executing the generated SQL.
- Ensure the agent remains stateless (history is for display only).
- Store messages as a list of objects in the JSON field.

## Dependencies

- **Blocked by**: STORY-002
- **Blocks**: STORY-004, STORY-010, STORY-011

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 7, 8, 10
