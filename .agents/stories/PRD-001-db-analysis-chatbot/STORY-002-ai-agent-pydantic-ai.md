---
id: STORY-002
prd: PRD-001
slug: ai-agent-core-discovery
title: AI Agent Core & Schema Discovery
type: feature
priority: high
complexity: medium
phase: 2
status: in-progress
labels: [backend, ai, pydantic-ai]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: .agents/plans/PRD-001/STORY-002-ai-agent-core-discovery.plan.md
report: null
commit: null
depends_on: [STORY-001, STORY-008]
blocks: [STORY-007, STORY-005]
skills: [building-pydantic-ai-agents, fastapi-python]
created: 2026-05-20
updated: 2026-05-20
---

# STORY-002: AI Agent Core & Schema Discovery

## Description

As a developer, I want to implement the core Pydantic AI agent and its schema discovery tools, so that the agent can understand the database structure it needs to query.

## Acceptance Criteria

- [ ] Pydantic AI agent is initialized using `deepseek/deepseek-chat:free` via OpenRouter.
- [ ] Agent has `list_tables` tool implemented to explore the analytics database.
- [ ] Agent has `describe_table` tool implemented to get schema details (columns, types).
- [ ] Unit tests (or a test script) verify the agent can correctly identify tables and columns when prompted.

## Technical Notes

- Use `pydantic-ai` for agent and tool definition.
- Implement tools with `@agent.tool` as per `building-pydantic-ai-agents` skill.
- The agent should use the `ANALYTICS_DB_URL` engine for introspection.
- Reference `backend/AGENTS.md` for tool naming and service structure.

## Dependencies

- **Blocked by**: STORY-001, STORY-008
- **Blocks**: STORY-007, STORY-005

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 7, 8
