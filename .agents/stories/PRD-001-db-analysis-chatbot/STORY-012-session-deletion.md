---
id: STORY-012
prd: PRD-001
slug: session-deletion
title: Session Lifecycle Management (Deletion)
type: feature
priority: medium
complexity: small
phase: 4
status: done
labels: [frontend, backend, api]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: .agents/plans/PRD-001/completed/STORY-012-session-deletion.plan.md
report: .agents/reports/PRD-001/STORY-012-session-deletion.report.md
commit: a9e6dff
depends_on: [STORY-001, STORY-003]
blocks: []
skills: [fastapi-python, shadcn, react-router-declarative-mode]
created: 2026-05-20
updated: 2026-05-21
---

# STORY-012: Session Lifecycle Management (Deletion)

## Description

As a user, I want to delete my previous chat sessions, so that I can keep my history clean and remove irrelevant analyses.

## Acceptance Criteria

- [ ] Given an existing session, when the user clicks the delete button in the sidebar, then the session is removed from the list.
- [ ] Given a session ID, when a `DELETE /api/v1/sessions/{id}` request is made, then the session is permanently removed from the SQLite database.
- [ ] Given a delete request, when the session does not belong to the authenticated user, then the system returns a 403 Forbidden error.
- [ ] Given a successful deletion, when the user is currently viewing the deleted session, then they are redirected to the "New Chat" page.

## Technical Notes

- Backend: Implement `DELETE` endpoint in `routers/sessions.py` calling the service and repository layers.
- Frontend: Add a "Trash" icon or "Delete" option in the `AppSidebar` next to each session title.
- Use a confirmation dialog (shadcn `AlertDialog`) before final deletion.

## Dependencies

- **Blocked by**: STORY-001, STORY-003
- **Blocks**: None

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 10
