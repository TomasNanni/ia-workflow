---
id: STORY-002
prd: PRD-001
slug: ai-agent-pydantic-ai
title: AI Agent for Natural Language to SQL
type: feature
priority: high
complexity: large
phase: 2
status: todo
labels: [backend, ai, pydantic-ai]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: null
report: null
commit: null
depends_on: [STORY-001]
blocks: [STORY-004, STORY-005]
skills: [building-pydantic-ai-agents, fastapi-python]
created: 2026-05-20
updated: 2026-05-20
---

# STORY-002: AI Agent for Natural Language to SQL

## Description

As a user, I want to ask questions in natural language, so that the AI agent can translate them into SQL and provide data-backed answers.

## Acceptance Criteria

- [ ] Pydantic AI agent is implemented using `deepseek/deepseek-chat:free` via OpenRouter.
- [ ] Agent has `list_tables` tool to explore the analytics database.
- [ ] Agent has `describe_table` tool to get schema details (columns, types).
- [ ] Agent has `execute_read_query` tool to run the generated SELECT query against PostgreSQL.
- [ ] `POST /api/v1/sessions/{id}/chat` endpoint processes user messages, updates the session's JSON history, and returns the agent's response.
- [ ] Agent is stateless (does not use history for query context) but the session history is updated.

## Technical Notes

- Use `pydantic-ai` for agent and tool definition.
- Implement tools with `@agent.tool` or `@agent.tool_plain` as per `building-pydantic-ai-agents` skill.
- Ensure the agent is strictly read-only by using the `ANALYTICS_DB_URL` engine.
- Store the entire conversation (user message and agent response) in the session's `messages` JSON field.

## Dependencies

- **Blocked by**: STORY-001
- **Blocks**: STORY-004, STORY-005

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 4, 7, 8
