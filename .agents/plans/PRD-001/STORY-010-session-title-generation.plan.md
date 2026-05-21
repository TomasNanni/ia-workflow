---
story: STORY-010
prd: PRD-001
slug: session-title-generation
title: Automated Session Title Generation
type: ENHANCEMENT
complexity: LOW
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-21
---

# Plan: Automated Session Title Generation

## Summary

This plan describes how to automatically generate descriptive titles for chat sessions. When the first message is processed in a session, we will call a small AI utility to summarize the user's intent into a 3-5 word title and update the session record in SQLite.

## User Story

As a user,
I want my chat sessions to have descriptive titles based on my first question,
So that I can easily find them in the history.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-010-session-title-generation.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | ENHANCEMENT |
| Complexity | LOW |
| Systems Affected | backend, ai |
| Story | STORY-010 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| building-pydantic-ai-agents | Using LLM for summarization task. | Task 1 |

---

## Patterns to Follow

### AI Prompting
```python
// Pattern for title generation
prompt = f"Generate a 3-5 word title for this question: {message}"
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/services/agent.py` | UPDATE | Add title generation function |
| `backend/app/services/chat.py` | UPDATE | Trigger title generation on first message |

---

## Tasks

### Task 1: Title Generation Utility

- **File**: `backend/app/services/agent.py`
- **Action**: UPDATE
- **Implement**: Create `async def generate_session_title(message: str) -> str`. Use a lightweight prompt.
- **Validate**: Test with various inputs: "How many sales in May?" -> "May Sales Analysis".

### Task 2: Integration in Chat Flow

- **File**: `backend/app/services/chat.py`
- **Action**: UPDATE
- **Implement**: In the chat processing logic, check if `session.title == "New Chat"`. If so, generate a title and update the session.
- **Validate**: Start a new chat, send a message, check if the title in the DB updates.

---

## End-to-End Tests

- [ ] Create new chat.
- [ ] Send message: "What are our top products?".
- [ ] Check sidebar or DB -> Title should be something like "Top Products Analysis".
- [ ] Send another message in the same chat -> Title should NOT change.

## Acceptance Criteria

- [ ] After the first user message in a session, the AI agent generates a short (3-5 words) title.
- [ ] The session record in SQLite is updated with this generated title.
- [ ] The sidebar reflects the new title immediately.
