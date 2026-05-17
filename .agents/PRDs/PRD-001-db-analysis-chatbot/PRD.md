---
id: PRD-001
slug: db-analysis-chatbot
title: AI-Powered Database Analysis Chatbot
status: draft
base_branch: main
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-17
updated: 2026-05-17
---

# PRD-001: AI-Powered Database Analysis Chatbot

## 1. Executive Summary
The AI-Powered Database Analysis Chatbot is a specialized tool that allows non-technical users to interact with a PostgreSQL database using natural language. The system leverages `pydantic-ai` to translate user queries into read-only SQL, executes them against a Supabase-hosted database, and presents the findings in a simple chat interface. 

The primary value proposition is to remove the SQL barrier for data analysis, providing immediate insights through a conversational experience. The application maintains session history using a local SQLite database, ensuring users can return to their previous analyses.

**MVP Goal**: A functional, minimal chat interface where users can ask questions about a fixed PostgreSQL schema and receive accurate, data-backed responses.

## 2. Mission
To make data analysis accessible to everyone, regardless of their coding skills.
- **Accessibility**: Design for non-coders first.
- **Safety**: Strict read-only access to prevent data modification.
- **Persistence**: Reliable conversation tracking for long-term utility.

## 3. Target Users
- **Non-Technical Managers**: Need quick stats without bothering the dev team.
- **Business Analysts**: Want to explore data patterns through conversation.
- **Operations Staff**: Require real-time data lookups for daily tasks.

## 4. MVP Scope
### In Scope
- [x] **New Chat Section**: A dedicated, minimal UI for database interactions.
- [x] **Natural Language to SQL**: AI agent using `pydantic-ai`.
- [x] **Dual Database System**:
    - **PostgreSQL (Supabase)**: Read-only source for analytics data.
    - **SQLite**: Local persistence for chat sessions and message history.
- [x] **Session Management**: Domain-driven architecture (similar to `pais` domain) for sessions.
- [x] **JSON History**: Storing messages as a JSON field within the session record.
- [x] **Security**: Read-only DB user and application-level query timeouts.

### Out of Scope
- [ ] Multi-database configuration by the user (fixed schema).
- [ ] Advanced data visualizations (charts/graphs).
- [ ] User authentication/SSO.
- [ ] Exporting results to CSV/PDF.

## 5. User Stories
1. **As a** non-technical user, **I want to** type a question like "How many sales did we have last month?", **so that** I don't have to learn SQL to get the answer.
2. **As a** user, **I want to** see my previous conversations in a list, **so that** I can resume an analysis I started earlier.
3. **As a** user, **I want a clean and simple interface**, **so that** I can focus on the data without being overwhelmed by technical jargon.
4. **As an** administrator, **I want the chatbot to have read-only access**, **so that** there is no risk of accidental data deletion or modification.
5. **As a** user, **I want the chatbot to tell me if a query is taking too long**, **so that** I'm not left waiting indefinitely.

## 6. Core Architecture & Patterns
- **Backend (FastAPI)**:
    - Follows the established layered pattern: `router` → `service` → `repository` → `model`.
    - **Dependency Injection**: Separate dependencies for `get_sessions_db` (SQLite) and `get_analytics_db` (Postgres).
    - **Pydantic AI**: Agent defined with structured tools for schema exploration and query execution.
- **Frontend (React 19)**:
    - **Declarative Routing**: New route `/chat` for the analytics interface.
    - **Minimal Design**: Utilizing shadcn/ui components with a focus on whitespace and readability.
    - **JSON State**: Handling the JSON message history from the backend.

## 7. Tools/Features
- **Agent Tools**:
    - `list_tables`: List available tables in the analytics DB.
    - `describe_table`: Get column names and types for a specific table.
    - `execute_read_query`: Execute the generated SELECT statement.
- **UI Components**:
    - `ChatWindow`: Minimalist message thread.
    - `SessionSidebar`: List of recent analytics sessions.

## 8. Technology Stack
- **Backend**: Python 3.10+, FastAPI, `pydantic-ai`, SQLAlchemy 2.0 (Dual Engine), `psycopg2` (Postgres), `sqlite3`.
- **Frontend**: React 19, React Router 7, Tailwind CSS v4, shadcn/ui.
- **Skills referenced**: `building-pydantic-ai-agents`, `fastapi-python`, `react-router-declarative-mode`, `shadcn`, `vercel-react-best-practices`.

## 9. Security & Configuration
- **Permissions**: The `ANALYTICS_DB_URL` must point to a user with `SELECT` permissions only.
- **Validation**: Application-level check to ensure queries start with `SELECT`.
- **Timeout**: Enforced 10-second timeout on all database analytics queries.
- **Configuration**: `DATABASE_URL` (Postgres), `SESSIONS_DB_URL` (SQLite), `OPENROUTER_API_KEY`.

## 10. API Specification
- `GET /api/v1/sessions`: List all chat sessions.
- `POST /api/v1/sessions`: Create a new session.
- `GET /api/v1/sessions/{id}`: Get session details including JSON message history.
- `POST /api/v1/sessions/{id}/chat`: Post a user message and receive the agent response.

## 11. Success Criteria
- [ ] Agent correctly identifies the schema of the Supabase DB.
- [ ] User can complete a full cycle: Ask question -> View data result -> History saved.
- [ ] System prevents any non-SELECT query execution.
- [ ] UI remains responsive and clear for non-technical users.

## 12. Implementation Phases
- **Phase 0: Data Seeding**: Populate Supabase with sample tables (products, customers, sales).
- **Phase 1: Dual DB Infrastructure**: Setting up SQLite for sessions and connecting to the read-only Postgres.
- **Phase 2: Chat Backend**: ImplementinBuilding the new Chat section with shadcn/ui.
- **Phase 4: Hardening**: Adding timeouts, read-only validation, and error handling.

## 13. Future Considerations
- Supporting natural language to chart (e.g., "Show me sales by month as a bar chart").
- Allowing users to upload CSVs to be analyzed by the same agent.

## 14. Risks & Mitigations
- **Risk**: AI Hallucination in SQL. **Mitigation**: The agent must always call `describe_table` before writing complex joins.
- **Risk**: Performance Bottlenecks. **Mitigation**: Automated `LIMIT` on all queries and strict timeouts.
- **Risk**: UI Complexity. **Mitigation**: User-centric design reviews focused on non-coders.

## 15. Appendix
- **Database Schema**: Fixed PostgreSQL schema (Supabase).
- **Session Schema**: SQLite table `sessions` with `id`, `title`, `created_at`, and `messages` (JSON).
a**: SQLite table `sessions` with `id`, `title`, `created_at`, and `messages` (JSON).
at`, and `messages` (JSON).
