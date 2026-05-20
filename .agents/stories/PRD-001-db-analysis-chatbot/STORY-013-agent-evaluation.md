---
id: STORY-013
prd: PRD-001
slug: agent-evaluation
title: Agent Accuracy Testing (Evaluation)
type: technical
priority: medium
complexity: medium
phase: 5
status: todo
labels: [backend, ai, testing]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: null
report: null
commit: null
depends_on: [STORY-007]
blocks: []
skills: [fastapi-python, building-pydantic-ai-agents]
created: 2026-05-20
updated: 2026-05-20
---

# STORY-013: Agent Accuracy Testing (Evaluation)

## Description

As a developer, I want to implement automated evaluation tests for the AI agent, so that I can ensure it generates valid SQL and accurate answers for common natural language queries.

## Acceptance Criteria

- [ ] A test suite `backend/tests/test_agent_accuracy.py` is implemented.
- [ ] Tests verify that the agent generates syntactically correct SQL for at least 5 standard queries (e.g., total sales, customer count by city).
- [ ] Tests verify that the agent correctly identifies when a table or column requested by the user does not exist in the schema.
- [ ] Tests run against the Supabase analytics database (or a local replica) to verify data results match expected values.

## Technical Notes

- Use `pytest` for running the evaluations.
- Since `pydantic-ai` agents are being used, leverage its testing/instrumentation features if available.
- Focus on "SQL correctness" and "Information retrieval accuracy".

## Dependencies

- **Blocked by**: STORY-007
- **Blocks**: None

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 11, 14
