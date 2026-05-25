---
story: STORY-007
prd: PRD-001
slug: ai-agent-chat-execution
title: AI Agent Query Execution & Chat API
type: NEW_CAPABILITY
complexity: MEDIUM
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-21
---

# Plan: AI Agent Query Execution & Chat API

## Summary

This plan covers the implementation of the chat interaction logic. We will define the `Session` model for persistence, implement the `execute_read_query` tool for the Pydantic AI agent, and create a chat endpoint that processes user messages, updates the session's JSON history, and returns the agent's response (including the SQL query used).

## User Story

As a user,
I want the AI agent to execute SQL queries and provide answers,
So that I can get insights from the database.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-007-ai-agent-chat-execution.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | backend, ai, database |
| Story | STORY-007 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| building-pydantic-ai-agents | Defining the agent, tools, and handling LLM interaction. | Tasks 4-5 |
| fastapi-python | Implementing routers and session management. | Tasks 1-3, 6 |

---

## Patterns to Follow

### Naming
```python
// SOURCE: backend/AGENTS.md
// Repositories: Raw DB queries, returns None on not found
def get_session(db: Session, session_id: int):
    return db.query(Session).filter(Session.id == session_id).first()
```

### AI Agent Tools
```python
// SOURCE: backend/.agents/skills/building-pydantic-ai-agents/SKILL.md
@agent.tool
def execute_read_query(ctx: RunContext[Deps], query: str) -> str:
    """Execute a read-only SQL query."""
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/core/config.py` | UPDATE | Add `ANALYTICS_DB_URL` and `OPENROUTER_API_KEY` |
| `backend/app/models/session.py` | CREATE | SQLAlchemy Session model |
| `backend/app/schemas/session.py` | CREATE | Pydantic Session schemas |
| `backend/app/repositories/session.py` | CREATE | CRUD for Session |
| `backend/app/services/agent.py` | CREATE | Pydantic AI agent and tools |
| `backend/app/routers/session.py` | CREATE | Chat endpoint |
| `backend/app/main.py` | UPDATE | Register session router |

---

## Tasks

### Task 1: Database & API Keys Config

- **File**: `backend/app/core/config.py`
- **Action**: UPDATE
- **Implement**: Add `analytics_db_url` and `openrouter_api_key`. Ensure `analytics_db_url` starts with `postgresql`.
- **Validate**: `python -c "from app.core.config import settings; print(settings.analytics_db_url)"`

### Task 2: Session Model

- **File**: `backend/app/models/session.py`
- **Action**: CREATE
- **Implement**: Fields: `id`, `user_id` (FK), `title` (default "New Chat"), `created_at`, `messages` (JSONB or JSON depending on engine).
- **Validate**: Server restart auto-creates table.

### Task 3: Session Repository

- **File**: `backend/app/repositories/session.py`
- **Action**: CREATE
- **Implement**: `get_session`, `create_session`, `update_session_messages`.
- **Validate**: Test message storage/retrieval with JSON list.

### Task 4: AI Agent & Read Tool

- **File**: `backend/app/services/agent.py`
- **Action**: CREATE
- **Implement**: Define Pydantic AI `Agent`. 
    - **System Prompt**: Must be in Spanish, instructing the agent to respond in Spanish.
    - **Tools**: Implement `execute_read_query` tool using a separate engine for `ANALYTICS_DB_URL`. Enforce `SELECT` only.
- **Validate**: Script to run agent with a simple prompt like "Listar todos los clientes".

### Task 5: Chat Logic Service

- **File**: `backend/app/services/chat.py`
- **Action**: CREATE
- **Implement**: Logic to load session history, run agent, and update session record.
- **Validate**: Unit test with `TestModel`.

### Task 6: Chat Router

- **File**: `backend/app/routers/session.py`
- **Action**: CREATE
- **Implement**: `POST /sessions/{id}/chat`. Should be a protected route (Task 10 of STORY-006).
- **Validate**: `curl -H "Authorization: Bearer <token>" -X POST ...`

---

## End-to-End Tests

- [ ] Create a new session → returns session object.
- [ ] Post a message "How many products do we have?" → returns natural language answer + SQL.
- [ ] Verify message history is updated in SQLite.
- [ ] Attempt a `DELETE` query → agent should fail or return error.

## Acceptance Criteria

- [ ] Agent has `execute_read_query` tool to run SELECT statements against PostgreSQL.
- [ ] `POST /api/v1/sessions/{id}/chat` endpoint processes user messages.
- [ ] The entire conversation (user/agent) is stored in the session's `messages` JSON field.
- [ ] Agent response includes both the natural language answer and the SQL query used.
