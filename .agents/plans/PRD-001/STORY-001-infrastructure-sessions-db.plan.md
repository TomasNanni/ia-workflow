---
story: STORY-001
prd: PRD-001
slug: infrastructure-sessions-db
title: Session Persistence & Dual DB Infrastructure
type: technical
complexity: medium
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-20
---

# Plan: Session Persistence & Dual DB Infrastructure

## Summary

This plan establishes the core infrastructure for the dual-database system. We will configure SQLite for session management and User accounts, and Postgres for read-only analytics. We will implement the `User` and `Session` entities following the layered architecture (Model -> Schema -> Repository -> Service -> Router) and provide a seeding script to populate the system with initial data.

## User Story

As a developer, I want to set up the dual database infrastructure, the User/Session models, and a seeding script for SQLite, so that the application has a solid foundation for personalized data analysis.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-001-infrastructure-sessions-db.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | technical |
| Complexity | MEDIUM |
| Systems Affected | backend |
| Story | STORY-001 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| fastapi-python | Follows FastAPI best practices, async operations, and layered structure. | All backend tasks |

---

## Patterns to Follow

### Naming
```python
# SOURCE: backend/AGENTS.md
# Files and variables: snake_case
# Classes (models, schemas): PascalCase
# Table names: snake_case, plural (e.g., users, sessions)
```

### Schemas
```python
# SOURCE: backend/AGENTS.md
class ResourceRead(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
```

### Models
```python
# SOURCE: backend/app/core/database.py
class Base(DeclarativeBase):
    pass
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/core/config.py` | UPDATE | Add `analytics_db_url` and `sessions_db_url` settings. |
| `backend/app/core/database.py` | UPDATE | Add secondary engine for Analytics (read-only). |
| `backend/app/models/user.py` | CREATE | SQLAlchemy model for User. |
| `backend/app/models/session.py` | CREATE | SQLAlchemy model for Session. |
| `backend/app/schemas/user.py` | CREATE | Pydantic schemas for User. |
| `backend/app/schemas/session.py` | CREATE | Pydantic schemas for Session. |
| `backend/app/repositories/user.py` | CREATE | Repository for User data access. |
| `backend/app/repositories/session.py` | CREATE | Repository for Session data access. |
| `backend/app/services/user.py` | CREATE | Service for User business logic. |
| `backend/app/services/session.py` | CREATE | Service for Session business logic. |
| `backend/app/routers/session.py` | CREATE | Router for session endpoints. |
| `backend/app/main.py` | UPDATE | Register the new session router. |
| `backend/scripts/seed_sqlite.py` | CREATE | Script to seed SQLite with 5 users and sample sessions. |
| `backend/.env.example` | UPDATE | Add `ANALYTICS_DB_URL`. |

---

## Tasks

### Task 1: Update Configuration

- **File**: `backend/app/core/config.py`
- **Action**: UPDATE
- **Implement**: Add `analytics_db_url: str` and rename `database_url` to `sessions_db_url` (or keep it as default for SQLite).
- **Validate**: `python -c "from app.core.config import settings; print(settings.database_url)"`

### Task 2: Configure Dual Engine

- **File**: `backend/app/core/database.py`
- **Action**: UPDATE
- **Implement**: Create a second engine `analytics_engine` using `settings.analytics_db_url`. Keep the primary `engine` for SQLite.
- **Validate**: Verify both engines can be imported without error.

### Task 3: Create User & Session Models

- **File**: `backend/app/models/user.py`, `backend/app/models/session.py`
- **Action**: CREATE
- **Implement**: 
    - `User`: `id`, `email`, `hashed_password`, `created_at`.
    - `Session`: `id`, `user_id` (FK), `title`, `created_at`, `messages` (JSON).
- **Mirror**: `backend/app/core/database.py:20` for `Base` inheritance.
- **Validate**: `python -c "from app.models.user import User; from app.models.session import Session"`

### Task 4: Implement User & Session Schemas

- **File**: `backend/app/schemas/user.py`, `backend/app/schemas/session.py`
- **Action**: CREATE
- **Implement**: Base, Create, Read schemas. For Session, include `messages` as `list[dict]`.
- **Mirror**: `backend/AGENTS.md` schema pattern.
- **Validate**: Instantiate a `SessionRead` model in a test script.

### Task 5: Implement Repositories

- **File**: `backend/app/repositories/user.py`, `backend/app/repositories/session.py`
- **Action**: CREATE
- **Implement**: Basic CRUD functions. `get_by_user_id` for sessions.
- **Validate**: Ensure they use `db: Session` from SQLAlchemy.

### Task 6: Implement Services

- **File**: `backend/app/services/user.py`, `backend/app/services/session.py`
- **Action**: CREATE
- **Implement**: Business logic, `_get_or_404` helpers.
- **Validate**: Check that they call repositories correctly.

### Task 7: Implement Session Router

- **File**: `backend/app/routers/session.py`
- **Action**: CREATE
- **Implement**: `GET /` (list), `POST /` (create).
- **Temporary**: For now, use a hardcoded `user_id=1` or a query param until Auth is ready.
- **Validate**: `uvicorn app.main:app --reload` and hit endpoints via Swagger.

### Task 8: Create Seeding Script

- **File**: `backend/scripts/seed_sqlite.py`
- **Action**: CREATE
- **Implement**: Use `passlib.context.CryptContext` for hashing. Create 5 users. Create multiple sessions with historical dates (e.g., 2 days ago, 1 week ago).
- **Validate**: Run `python scripts/seed_sqlite.py` and check `app.db` with a SQLite viewer or `sqlite3` CLI.

---

## End-to-End Tests

- [ ] Run `python scripts/seed_sqlite.py`.
- [ ] Start backend: `uvicorn app.main:app`.
- [ ] `GET /api/v1/sessions` -> returns seeded sessions for user 1.
- [ ] `POST /api/v1/sessions` -> creates a new session.

---

## Validation

```bash
cd backend
python -m scripts.seed_sqlite
curl http://localhost:8000/api/v1/sessions
```

---

## Acceptance Criteria

- [x] SQLite database `sessions.db` (or `app.db`) is configured with `users` and `sessions` tables.
- [x] PostgreSQL connection to Supabase is configured for read-only analytics.
- [x] SQLAlchemy models for `User` and `Session` (with `created_at` timestamps) are implemented.
- [x] A seeding script `scripts/seed_sqlite.py` is created to populate the DB with 5 users and sample chat sessions with historical dates.
- [x] `GET /api/v1/sessions` returns a list of sessions for the authenticated user (mocked for now), including their `created_at` dates.
- [x] `POST /api/v1/sessions` creates a new session linked to the current user (mocked for now).
