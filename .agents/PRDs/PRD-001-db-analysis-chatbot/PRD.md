---
id: PRD-001
slug: db-analysis-chatbot
title: AI-Powered Database Analysis Chatbot
status: draft
base_branch: main
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-17
updated: 2026-05-21
---

# PRD-001: AI-Powered Database Analysis Chatbot

## 1. Executive Summary
The AI-Powered Database Analysis Chatbot is a specialized tool that allows non-technical users to interact with a PostgreSQL database using natural language. The system leverages `pydantic-ai` to translate user queries into read-only SQL, executes them against a Supabase-hosted database, and presents the findings in a simple chat interface. 

The primary value proposition is to remove the SQL barrier for data analysis, providing immediate insights through a conversational experience. The application maintains session history using a local SQLite database, ensuring users can return to their previous analyses.

**MVP Goal**: A functional, minimal chat interface where users can ask questions about a fixed PostgreSQL schema and receive accurate, data-backed responses. All UI text and agent interactions will be in Spanish.

## 2. Mission
To make data analysis accessible to everyone, regardless of their coding skills.
- **Accessibility**: Design for non-coders first.
- **Spanish First**: The application is intended for Spanish-speaking users. All interface elements, error messages, and agent responses must be in Spanish.
- **Safety**: Strict read-only access to prevent data modification.- **Persistence**: Reliable conversation tracking for long-term utility.

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
    - **SQLite**: Local persistence for chat sessions, message history, and user accounts.
- [x] **User Authentication**: Simple Login/Register (email and password) to manage personalized session history.
- [x] **Data Seeding**: Initial population of SQLite with 5 users and sample chat sessions (including historical dates).
- [x] **Session Management**: Domain-driven architecture (similar to `pais` domain) for sessions. History is for user reference only; the AI agent operates in a stateless manner (no history context per query).
- [x] **JSON History**: Storing messages as a JSON field within the session record.
- [x] **Security**: Read-only DB user and application-level query timeouts.

### Out of Scope
- [ ] Multi-database configuration by the user (fixed schema).
- [ ] Advanced data visualizations (charts/graphs).
- [ ] SSO (Single Sign-On).
- [ ] Exporting results to CSV/PDF.

## 5. User Stories
1. **As a** non-technical user, **I want to** type a question like "How many sales did we have last month?", **so that** I don't have to learn SQL to get the answer.
2. **As a** user, **I want to** see my previous conversations in a list with their creation dates, **so that** I can easily identify and resume an analysis from a specific day.
3. **As a** user, **I want a clean and simple interface**, **so that** I can focus on the data without being overwhelmed by technical jargon.
4. **As an** administrator, **I want the chatbot to have read-only access**, **so that** there is no risk of accidental data deletion or modification.
5. **As a** user, **I want the chatbot to tell me if a query is taking too long**, **so that** I'm not left waiting indefinitely.
6. **As a** new user, **I want to create an account**, **so that** I can start saving my database analysis sessions.
7. **As a** returning user, **I want to log in with my email and password**, **so that** I can access my saved conversations and their history.

## 6. Design & Aesthetics
- **Visual Style**: "Obsidian Deep" — A professional, high-contrast dark theme.
    - **Palette**: Deep Black (#09090b), Charcoal Gray (#27272a), and Emerald Green accents (#059669).
    - **Surface**: Use of subtle linear gradients (top-to-bottom, Black to Charcoal) for page backgrounds and dark green glows for interactive elements.
    - **Typography**: Clean sans-serif (Geist) for UI, with JetBrains Mono for SQL and data tables.
- **Layout Structure**:
    - **Login/Register Pages**: Minimalist centered forms with "Obsidian Deep" styling.
    - **Collapsible Sidebar (Left)**: Minimalist navigation for user profile, logout, and conversation history (ordered by date, newest first).
    - **Main Content (Responsive 50/50 Split)**:
        - **Left Side (Chat)**: Clean, distraction-free chat interface. Starts with a welcoming message and clear input area.
        - **Right Side (Schema Visualizer)**: A minimally interactive map of the database. Users can click on table names to see column details. 
        - **Responsive Behavior**: On mobile/small screens, the layout stacks vertically or uses a tabbed view to maintain usability, with the chat prioritized.

## 7. Tools/Features
- **Agent Tools**:
    - `list_tables`: List available tables in the analytics DB.
    - `describe_table`: Get column names and types for a specific table.
    - `execute_read_query`: Execute the generated SELECT statement.
- **UI Components**:
    - `AuthForms`: Simple login and registration forms.
    - `AppSidebar`: Collapsible shadcn Sidebar for history (with dates) and profile.
    - `ChatInterface`: Minimalist thread with dark green accents for the agent's messages.
    - `SchemaMap`: Interactive or list-based visualization of tables on the right side of the chat.

## 8. Technology Stack
- **Backend**: Python 3.10+, FastAPI, `pydantic-ai`, SQLAlchemy 2.0 (Dual Engine), `psycopg2` (Postgres), `sqlite3`, `passlib` (for password hashing).
- **AI Model**: `deepseek/deepseek-chat:free` via OpenRouter.
- **Frontend**: React 19, React Router 7, Tailwind CSS v4, shadcn/ui.
- **Skills referenced**: `building-pydantic-ai-agents`, `fastapi-python`, `react-router-declarative-mode`, `shadcn`, `vercel-react-best-practices`.

## 9. Security & Configuration
- **Permissions**: The `ANALYTICS_DB_URL` must point to a user with `SELECT` permissions only.
- **Validation**: Application-level check to ensure queries start with `SELECT`.
- **Timeout**: Enforced 10-second timeout on all database analytics queries.
- **Authentication**: JWT-based or simple session-based auth for SQLite database users.
- **Configuration**: 
    - `DATABASE_URL` (Postgres Admin)
    - `ANALYTICS_DB_URL` (Postgres Read-Only)
    - `SESSIONS_DB_URL` (SQLite)
    - `OPENROUTER_API_KEY` (User provided)
    - `AI_MODEL`: `deepseek/deepseek-chat:free`
    - `SECRET_KEY`: (For Auth tokens)

## 10. API Specification
- **Auth**:
    - `POST /api/v1/auth/register`: Create a new user.
    - `POST /api/v1/auth/login`: Authenticate and return a session token.
- **Sessions**:
    - `GET /api/v1/sessions`: List all chat sessions for the authenticated user (returns id, title, and created_at).
    - `POST /api/v1/sessions`: Create a new session.
    - `GET /api/v1/sessions/{id}`: Get session details including JSON message history.
    - `POST /api/v1/sessions/{id}/chat`: Post a user message and receive the agent response.

## 11. Success Criteria
- [ ] Agent correctly identifies the schema of the Supabase DB.
- [ ] User can register, log in, and see their own history (with dates) only.
- [ ] SQLite is seeded with 5 users and sample data on first run.
- [ ] System prevents any non-SELECT query execution.
- [ ] UI remains responsive and clear for non-technical users.

## 12. Implementation Phases
- **Phase 0: Data Seeding**: Populate Supabase with sample tables and SQLite with sample users/sessions (with varied dates).
- **Phase 1: Dual DB & Auth Infrastructure**: Setting up SQLite for users/sessions and connecting to read-only Postgres.
- **Phase 2: Auth UI**: Login and Register pages.
- **Phase 3: Chat Backend**: Building the Pydantic AI agent and chat endpoints.
- **Phase 4: Chat UI**: Building the new Chat section with shadcn/ui, including the history list with dates.
- **Phase 5: Hardening**: Adding timeouts, read-only validation, and error handling.

## 13. Future Considerations
- Supporting natural language to chart (e.g., "Show me sales by month as a bar chart").
- Allowing users to upload CSVs to be analyzed by the same agent.

## 14. Risks & Mitigations
- **Risk**: AI Hallucination in SQL. **Mitigation**: The agent must always call `describe_table` before writing complex joins.
- **Risk**: Performance Bottlenecks. **Mitigation**: Automated `LIMIT` on all queries and strict timeouts.
- **Risk**: UI Complexity. **Mitigation**: User-centric design reviews focused on non-coders.

## 15. Appendix
- **Database Schema**: Fixed PostgreSQL schema (Supabase).
- **User Schema**: SQLite table `users` with `id`, `email`, `hashed_password`, `created_at`.
- **Session Schema**: SQLite table `sessions` with `id`, `user_id` (FK), `title`, `created_at` (Timestamp), and `messages` (JSON).
