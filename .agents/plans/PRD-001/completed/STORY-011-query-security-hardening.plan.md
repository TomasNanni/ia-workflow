---
story: STORY-011
prd: PRD-001
slug: query-security-hardening
title: Query Validation & Timeout Security
type: ENHANCEMENT
complexity: MEDIUM
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-21
---

# Plan: Query Validation & Timeout Security

## Summary

This plan addresses the security and stability requirements for database analytics. We will implement strict validation to ensure only `SELECT` statements are executed and enforce a 10-second timeout on all queries. This prevents unauthorized data modification and ensures the application doesn't hang on complex queries.

## User Story

As an administrator,
I want to ensure that all AI-generated queries are safe and don't overwhelm the database,
So that the system remains stable and secure.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-011-query-security-hardening.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | ENHANCEMENT |
| Complexity | MEDIUM |
| Systems Affected | backend, database |
| Story | STORY-011 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| fastapi-python | Implementing security logic and error handling. | All tasks |

---

## Patterns to Follow

### Query Validation
```python
if not query.strip().upper().startswith("SELECT"):
    raise ValueError("Only SELECT queries are allowed")
```

### Timeout
```python
# Using SQLAlchemy execution_options
session.execute(text(query).execution_options(timeout=10))
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/services/agent.py` | UPDATE | Implement query validation and timeout in `execute_read_query` tool |

---

## Tasks

### Task 1: Strict SELECT Validation

- **File**: `backend/app/services/agent.py`
- **Action**: UPDATE
- **Implement**: In `execute_read_query`, add a check to ensure the query (after stripping whitespace) starts with `SELECT`. Block any other commands like `INSERT`, `UPDATE`, `DELETE`, `DROP`, etc.
- **Validate**: Call the tool with `"DELETE FROM customers"` and verify it returns a clear security error message.

### Task 2: Execution Timeout

- **File**: `backend/app/services/agent.py`
- **Action**: UPDATE
- **Implement**: Update the SQLAlchemy execution call to include `execution_options(timeout=10)`. Handle the timeout exception and return a user-friendly error.
- **Validate**: Try to run a query that would take too long (e.g., a cross join if possible, or simulate it) and check for the timeout error.

### Task 3: SQL Injection Pattern Check

- **File**: `backend/app/services/agent.py`
- **Action**: UPDATE
- **Implement**: Add basic checks for multiple statements (e.g., `;`) or other common injection patterns that might bypass the simple `startswith("SELECT")` check.
- **Validate**: Test with `"SELECT * FROM customers; DROP TABLE sales"`.

---

## End-to-End Tests

- [ ] Ask the agent: "Delete all customers" -> Agent should refuse or the tool should block it.
- [ ] Ask the agent: "Drop the sales table" -> Tool should block it.
- [ ] Run a heavy query -> System should return a timeout error after 10 seconds.
- [ ] Run a valid SELECT -> System should return data as usual.

---

## Validation

```bash
cd backend
# Manual test script for the agent tool
python -m app.services.agent_test_security
```

---

## Acceptance Criteria

- [ ] Backend validates that every query starts with `SELECT`.
- [ ] A strict 10-second timeout is enforced on all analytics queries.
- [ ] Any non-SELECT query attempt is logged and blocked with a clear error message to the user.
- [ ] Application-level check prevents common SQL injection patterns in generated SQL.
