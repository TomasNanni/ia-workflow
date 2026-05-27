---
story: STORY-012
prd: PRD-001
slug: session-deletion
title: Session Lifecycle Management (Deletion)
type: FEATURE
complexity: LOW
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-21
---

# Plan: Session Lifecycle Management (Deletion)

## Summary

This plan covers the implementation of session deletion. We will add a `DELETE` endpoint to the sessions API, implement the necessary logic in the repository and service layers to safely remove sessions (ensuring they belong to the requesting user), and update the frontend sidebar to include a deletion UI with a confirmation dialog.

## User Story

As a user,
I want to delete my previous chat sessions,
So that I can keep my history clean and remove irrelevant analyses.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-012-session-deletion.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | FEATURE |
| Complexity | LOW |
| Systems Affected | frontend, backend, api |
| Story | STORY-012 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| fastapi-python | Implementing the DELETE endpoint and ownership logic. | Tasks 1-3 |
| shadcn | Using AlertDialog for deletion confirmation. | Task 4 |
| react-router-declarative-mode | Redirecting user after deleting an active session. | Task 5 |

---

## Patterns to Follow

### Naming
```python
# SOURCE: backend/AGENTS.md
# Repositories: returns None on not found, pure DB functions
def delete(db: Session, id: int):
    # ...
```

### Error Handling
```python
# SOURCE: backend/AGENTS.md
# 403 for ownership violations
if session.user_id != current_user.id:
    raise HTTPException(status_code=403, detail="Prohibido")
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/repositories/session.py` | UPDATE | Add `delete` method |
| `backend/app/services/session.py` | UPDATE | Add `delete_session` with ownership check |
| `backend/app/routers/session.py` | UPDATE | Add `DELETE /{id}` endpoint |
| `frontend/src/components/AppSidebar.jsx` | UPDATE | Add delete button next to session titles |

---

## Tasks

### Task 1: Repository Delete Method

- **File**: `backend/app/repositories/session.py`
- **Action**: UPDATE
- **Implement**: Add `delete(db: Session, id: int) -> bool`. Return `True` if deleted, `False` if not found.
- **Mirror**: Basic SQLAlchemy deletion pattern.
- **Validate**: Test with a script that creates then deletes a session.

### Task 2: Service Delete Logic

- **File**: `backend/app/services/session.py`
- **Action**: UPDATE
- **Implement**: Add `delete_session(db: Session, id: int, user_id: int)`. First get the session, check if it belongs to `user_id`, then call repo. Raise 404 if not found, 403 if ownership mismatch.
- **Validate**: Unit test with mocked repo.

### Task 3: API Delete Endpoint

- **File**: `backend/app/routers/session.py`
- **Action**: UPDATE
- **Implement**: `DELETE /{id}`. Requires authentication. Calls the service layer.
- **Validate**: `curl -X DELETE ...` and check DB.

### Task 4: Frontend Sidebar Deletion UI

- **File**: `frontend/src/components/AppSidebar.jsx`
- **Action**: UPDATE
- **Implement**: Add a "Trash" icon button to each session in the list. On click, show a `shadcn` `AlertDialog` confirming deletion.
- **Mirror**: `shadcn` documentation for `AlertDialog`.
- **Validate**: Click button, verify dialog appears.

### Task 5: Deletion Flow & Redirection

- **File**: `frontend/src/components/AppSidebar.jsx`
- **Action**: UPDATE
- **Implement**: On confirmed deletion, call the API. If successful, remove from local state. If the deleted session is the currently active one (check `useParams`), redirect to `/dashboard` (New Chat).
- **Validate**: Delete current session, verify redirection.

---

## End-to-End Tests

- [ ] Create a session.
- [ ] Click delete icon in sidebar.
- [ ] Cancel deletion -> session stays.
- [ ] Confirm deletion -> session disappears from list.
- [ ] Check DB -> session is gone.
- [ ] Attempt to delete another user's session via API -> returns 403.

---

## Validation

```bash
cd frontend && npm run lint
curl -X DELETE http://localhost:8000/api/v1/sessions/1
```

---

## Acceptance Criteria

- [ ] Given an existing session, when the user clicks the delete button in the sidebar, then the session is removed from the list.
- [ ] Given a session ID, when a `DELETE /api/v1/sessions/{id}` request is made, then the session is permanently removed from the SQLite database.
- [ ] Given a delete request, when the session does not belong to the authenticated user, then the system returns a 403 Forbidden error.
- [ ] Given a successful deletion, when the user is currently viewing the deleted session, then they are redirected to the "New Chat" page.
