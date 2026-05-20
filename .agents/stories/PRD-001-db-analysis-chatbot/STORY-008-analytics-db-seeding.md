---
id: STORY-008
prd: PRD-001
slug: analytics-db-seeding
title: Analytics Database Seeding (PostgreSQL)
type: technical
priority: medium
complexity: small
phase: 0
status: done
labels: [backend, database]
epic_branch: epic/PRD-001-db-analysis-chatbot
plan: null
report: "PostgreSQL database in Supabase is already populated with tables: customers, products, sales via scripts/seed_analytics.py."
commit: 82031a8
depends_on: [STORY-001]
blocks: [STORY-002]
skills: [fastapi-python]
created: 2026-05-20
updated: 2026-05-20
---

# STORY-008: Analytics Database Seeding (PostgreSQL)

## Description

As a developer, I want to seed the Supabase PostgreSQL database with sample analytics data, so that I can test the AI agent's query capabilities.

## Acceptance Criteria

- [x] Script `scripts/seed_analytics.py` is created (or updated).
- [x] Sample tables (e.g., `sales`, `products`, `customers`) are created in the Supabase DB.
- [x] Tables are populated with at least 50 rows of varied data each.
- [x] Verification that a read-only user can query these tables.

## Technical Notes

- Use `psycopg2` or SQLAlchemy to connect to the Supabase instance.
- Ensure the schema is fixed as described in the PRD appendix.

## Dependencies

- **Blocked by**: STORY-001
- **Blocks**: STORY-002

## PRD Reference

Source: [`PRD-001/PRD.md`](../../PRDs/PRD-001-db-analysis-chatbot/PRD.md) — section 12, 15
