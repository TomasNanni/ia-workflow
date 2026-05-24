---
story: STORY-006
prd: PRD-001
slug: user-authentication-auth
title: User Authentication (Login & Register)
type: NEW_CAPABILITY
complexity: MEDIUM
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-21
---

# Plan: User Authentication (Login & Register)

## Summary

This plan covers the implementation of a full-stack authentication system using JWT for secure session management. We will implement registration and login endpoints on the backend with password hashing via `passlib`, and corresponding Login/Register pages on the frontend using `shadcn/ui`. Access to the chat application will be restricted via a `RequireAuth` wrapper.

## User Story

As a user,
I want to create an account and log in,
So that my chat history is securely saved and accessible only to me.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-006-user-authentication-auth.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | backend, frontend, database |
| Story | STORY-006 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| fastapi-python | Standards for routers, services, and Pydantic schemas. | Tasks 1-6 |
| shadcn | Using Form and Input components for Auth pages. | Tasks 8-9 |
| vercel-react-best-practices | Optimizing client-side auth state and routing. | Task 10 |

---

## Patterns to Follow

### Naming
```python
// SOURCE: backend/AGENTS.md
// Schemas: ResourceCreate, ResourceUpdate, ResourceRead
class UserCreate(UserBase):
    password: str
```

### Error Handling
```python
// SOURCE: backend/AGENTS.md
// Services raise HTTPException directly
raise HTTPException(status_code=401, detail="Incorrect email or password")
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/core/config.py` | UPDATE | Add JWT settings (SECRET_KEY, etc.) |
| `backend/app/models/user.py` | CREATE | SQLAlchemy User model |
| `backend/app/schemas/user.py` | CREATE | Pydantic User schemas |
| `backend/app/schemas/token.py` | CREATE | JWT Token schemas |
| `backend/app/repositories/user.py` | CREATE | CRUD for User |
| `backend/app/services/auth.py` | CREATE | JWT and Hashing logic |
| `backend/app/routers/auth.py` | CREATE | Register and Login routes |
| `backend/app/main.py` | UPDATE | Register auth router |
| `frontend/src/pages/auth/Login.jsx` | CREATE | Login page |
| `frontend/src/pages/auth/Register.jsx` | CREATE | Register page |
| `frontend/src/components/auth/RequireAuth.jsx` | CREATE | Auth guard component |
| `frontend/src/App.jsx` | UPDATE | Add auth routes and wrap protected routes |

---

## Tasks

### Task 1: Auth Configuration

- **File**: `backend/app/core/config.py`
- **Action**: UPDATE
- **Implement**: Add `SECRET_KEY`, `ALGORITHM` (default HS256), and `ACCESS_TOKEN_EXPIRE_MINUTES`.
- **Validate**: `cd backend && python -c "from app.core.config import settings; print(settings.SECRET_KEY)"`

### Task 2: User Model

- **File**: `backend/app/models/user.py`
- **Action**: CREATE
- **Implement**: Define `User` class extending `Base`. Fields: `id`, `email` (unique), `hashed_password`, `created_at`.
- **Validate**: Server restart auto-creates table in SQLite.

### Task 3: User & Token Schemas

- **File**: `backend/app/schemas/user.py`, `backend/app/schemas/token.py`
- **Action**: CREATE
- **Implement**: `UserCreate`, `UserRead`, `Token`, `TokenData`.
- **Validate**: Import in a test script to check Pydantic validation.

### Task 4: User Repository

- **File**: `backend/app/repositories/user.py`
- **Action**: CREATE
- **Implement**: `get_user_by_email`, `create_user`.
- **Validate**: Unit test with a temporary DB session.

### Task 5: Auth Service

- **File**: `backend/app/services/auth.py`
- **Action**: CREATE
- **Implement**: `get_password_hash`, `verify_password`, `create_access_token`, `authenticate_user`.
- **Validate**: Check hashing and verification in a script.

### Task 6: Auth Router

- **File**: `backend/app/routers/auth.py`
- **Action**: CREATE
- **Implement**: `POST /register`, `POST /login` (returns `Token`).
- **Validate**: `curl -X POST http://localhost:8000/api/v1/auth/register -d '{"email": "test@example.com", "password": "password"}'`

### Task 7: Register Router in Main

- **File**: `backend/app/main.py`
- **Action**: UPDATE
- **Implement**: `app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])`.

### Task 8: Frontend Login Page

- **File**: `frontend/src/pages/auth/Login.jsx`
- **Action**: CREATE
- **Implement**: Form with email/password using shadcn. Handle token storage in `localStorage`.
- **Validate**: Renders at `/login`.

### Task 9: Frontend Register Page

- **File**: `frontend/src/pages/auth/Register.jsx`
- **Action**: CREATE
- **Implement**: Form with email/password/confirm password.
- **Validate**: Renders at `/register`.

### Task 10: RequireAuth Guard & Routing

- **File**: `frontend/src/components/auth/RequireAuth.jsx`, `frontend/src/App.jsx`
- **Action**: CREATE/UPDATE
- **Implement**: `RequireAuth` wrapper checking for token. Wrap `/dashboard` and `/chat` routes.
- **Validate**: Navigating to dashboard without token redirects to `/login`.

---

## End-to-End Tests

- [ ] Register a new user via UI → success message + redirect to login.
- [ ] Log in with new user → redirect to dashboard.
- [ ] Check `localStorage` for `access_token`.
- [ ] Attempt to access `/dashboard` when logged out → redirect to `/login`.

## Acceptance Criteria

- [ ] Backend endpoints `POST /api/v1/auth/register` and `POST /api/v1/auth/login` are implemented.
- [ ] Passwords are securely hashed using `passlib`.
- [ ] Login returns a JWT token.
- [ ] Frontend `Login` and `Register` pages are implemented.
- [ ] Protected routes (using a `RequireAuth` wrapper) ensure session access is restricted.
