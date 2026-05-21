---
id: STORY-001
prd: PRD-001
slug: infrastructure-sessions-db
title: Session Persistence & Dual DB Infrastructure
type: technical
priority: high
complexity: medium
phase: 1
status: done
labels: [backend, api, database]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: .agents/plans/PRD-001/completed/STORY-001-infrastructure-sessions-db.plan.md
report: .agents/reports/PRD-001/STORY-001-infrastructure-sessions-db.report.md
commit: 0de0df4
depends_on: []
blocks: [STORY-002, STORY-003, STORY-006, STORY-008]
skills: [fastapi-python]
created: 2026-05-20
updated: 2026-05-21
---

# STORY-001: Infrastructure, Models & Data Seeding (SQLite)

## Description

As a developer, I want to set up the dual database infrastructure, the User/Session models, and a seeding script for SQLite, so that the application has a solid foundation for personalized data analysis.

## Acceptance Criteria

- [x] SQLite database `sessions.db` is configured with `users` and `sessions` tables.
- [x] PostgreSQL connection to Supabase is configured for read-only analytics.
- [x] SQLAlchemy models for `User` and `Session` (with `created_at` timestamps) are implemented.
- [x] A seeding script `scripts/seed_sqlite.py` is created to populate the DB with 5 users and sample chat sessions with historical dates.
- [x] `GET /api/v1/sessions` returns a list of sessions for the authenticated user, including their `created_at` dates.
- [x] `POST /api/v1/sessions` creates a new session linked to the current user.

## Technical Notes

- Follow the `pais` pattern for both `User` and `Session` entities.
- The `Session` model must have a `user_id` foreign key.
- Seeding script should use `passlib` for hashing passwords of the 5 initial users.
- Sessions in the database must include a variety of creation dates to test the sidebar display.
- Reference `backend/AGENTS.md` for naming conventions.

## Dependencies

- **Blocked by**: None
- **Blocks**: STORY-002, STORY-003, STORY-006, STORY-008

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 8, 10, 12, 15
