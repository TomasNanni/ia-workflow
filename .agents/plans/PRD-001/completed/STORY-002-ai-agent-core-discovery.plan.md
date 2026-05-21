---
story: STORY-002
prd: PRD-001
slug: ai-agent-core-discovery
title: AI Agent Core & Schema Discovery
type: feature
complexity: medium
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-20
---

# Plan: AI Agent Core & Schema Discovery

## Summary

This plan covers the implementation of the core AI agent using the `pydantic-ai` framework. The agent will be configured to use OpenRouter (DeepSeek model) and will be equipped with introspection tools to explore the read-only PostgreSQL analytics database. These tools (`list_tables` and `describe_table`) are essential for the agent to understand the schema before generating SQL queries.

## User Story

As a developer, I want to implement the core Pydantic AI agent and its schema discovery tools, so that the agent can understand the database structure it needs to query.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-002-ai-agent-pydantic-ai.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | feature |
| Complexity | MEDIUM |
| Systems Affected | backend |
| Story | STORY-002 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| building-pydantic-ai-agents | Provides patterns for agent construction, tool definition, and dependency injection. | All agent-related tasks |
| fastapi-python | Follows service-layer patterns for backend logic. | Task 1, Task 2 |

---

## Patterns to Follow

### Agent Definition
```python
# SOURCE: backend/.agents/skills/building-pydantic-ai-agents/SKILL.md
from pydantic_ai import Agent, RunContext

agent = Agent(
    'openai:gpt-4o', # Will use openrouter:deepseek/deepseek-chat:free
    deps_type=Engine,
    instructions='...'
)
```

### Tool with Context
```python
# SOURCE: backend/.agents/skills/building-pydantic-ai-agents/SKILL.md
@agent.tool
def my_tool(ctx: RunContext[Engine], ...) -> str:
    # use ctx.deps to access database engine
    pass
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/services/agent.py` | CREATE | Core agent definition, system instructions, and discovery tools. |
| `backend/app/core/config.py` | UPDATE | Ensure `OPENROUTER_API_KEY` and `AI_MODEL` are available. |
| `backend/scripts/test_agent_discovery.py` | CREATE | Script to verify the agent can discover tables and columns. |

---

## Tasks

### Task 1: Update Configuration for AI

- **File**: `backend/app/core/config.py`
- **Action**: UPDATE
- **Implement**: Add `openrouter_api_key: str` and `ai_model: str = "deepseek/deepseek-chat:free"`.
- **Validate**: `python -c "from app.core.config import settings; print(settings.ai_model)"`

### Task 2: Implement AI Agent & Tools

- **File**: `backend/app/services/agent.py`
- **Action**: CREATE
- **Implement**: 
    - Initialize `pydantic_ai.Agent`.
    - Set `deps_type` to SQLAlchemy `Engine` (for the analytics DB).
    - Tool `list_tables(ctx: RunContext[Engine])`: Query `information_schema.tables` or use SQLAlchemy inspector.
    - Tool `describe_table(ctx: RunContext[Engine], table_name: str)`: Query `information_schema.columns` or use SQLAlchemy inspector.
- **Validate**: `python -c "from app.services.agent import agent; print(agent.name)"`

### Task 3: Create Discovery Test Script

- **File**: `backend/scripts/test_agent_discovery.py`
- **Action**: CREATE
- **Implement**: A script that runs the agent with a prompt like "What tables are available in the database?" and "What columns does the 'sales' table have?". Use `TestModel` or a real run if an API key is provided.
- **Validate**: Run the script and observe the agent calling the tools and returning correct schema info.

---

## End-to-End Tests

- [ ] Run `python scripts/test_agent_discovery.py`.
- [ ] Verify `list_tables` returns the tables seeded in the Postgres DB (e.g., `paises` or whatever `seed_analytics.py` created).
- [ ] Verify `describe_table` returns the correct columns and types for a given table.

---

## Validation

```bash
cd backend
python scripts/test_agent_discovery.py
```

---

## Acceptance Criteria

- [x] Pydantic AI agent is initialized using `deepseek/deepseek-chat:free` via OpenRouter.
- [x] Agent has `list_tables` tool implemented to explore the analytics database.
- [x] Agent has `describe_table` tool implemented to get schema details (columns, types).
- [x] Unit tests (or a test script) verify the agent can correctly identify tables and columns when prompted.
