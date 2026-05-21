---
story: STORY-003
prd: PRD-001
slug: core-navigation-sidebar
title: Navigation & Session List UI
type: feature
complexity: small
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-20
---

# Plan: Navigation & Session List UI

## Summary

This plan covers the implementation of the `AppSidebar` component using `shadcn/ui`. The sidebar will serve as the primary navigation for chat history, allowing users to view their previous sessions, see when they were created, and start new chats. It will use `NavLink` to highlight the active session and `date-fns` for human-readable timestamps.

## User Story

As a user, I want to see my previous conversations in a sidebar, so that I can easily identify and switch between analyses.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-003-core-navigation-sidebar.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | feature |
| Complexity | SMALL |
| Systems Affected | frontend |
| Story | STORY-003 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| shadcn | Used to install and configure the Sidebar component. | Task 1, Task 2 |
| react-router-declarative-mode | Used for navigation and active route highlighting. | Task 2 |
| vercel-react-best-practices | Ensures efficient rendering and proper effect usage. | Task 2 |

---

## Patterns to Follow

### Sidebar Implementation
```jsx
// SOURCE: shadcn sidebar documentation
import { Sidebar, SidebarContent, SidebarGroup, SidebarGroupLabel, SidebarMenu, SidebarMenuItem, SidebarMenuButton } from "@/components/ui/sidebar"
```

### NavLink
```jsx
// SOURCE: frontend/.agents/skills/react-router-declarative-mode/SKILL.md
<NavLink to={`/chat/${session.id}`} className={({ isActive }) => cn("...", isActive && "...")} />
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `frontend/src/components/AppSidebar.jsx` | CREATE | Main navigation sidebar component. |
| `frontend/src/layouts/RootLayout.jsx` | UPDATE | Integrate `SidebarProvider` and `AppSidebar`. |
| `frontend/src/App.jsx` | UPDATE | Add routes for chat sessions. |

---

## Tasks

### Task 1: Install Sidebar & date-fns

- **Action**: EXECUTE
- **Implement**: 
    - `npx shadcn@latest add sidebar`
    - `npm install date-fns`
- **Validate**: Check `package.json` and `src/components/ui/sidebar.jsx`.

### Task 2: Implement AppSidebar Component

- **File**: `frontend/src/components/AppSidebar.jsx`
- **Action**: CREATE
- **Implement**: 
    - Use `Sidebar` layout.
    - Fetch sessions from `GET /api/v1/sessions` (mocking auth for now).
    - Render a list of `NavLink` items.
    - Show session `title` and formatted `created_at` (e.g., "May 20, 2026").
    - Add a "New Chat" button that navigates to `/chat/new` or similar.
- **Mirror**: `frontend/src/components/PageHeader.jsx` for component structure.
- **Validate**: `npm run dev` and verify the sidebar appears.

### Task 3: Update Root Layout

- **File**: `frontend/src/layouts/RootLayout.jsx`
- **Action**: UPDATE
- **Implement**: Wrap the content with `SidebarProvider` and include `<AppSidebar />` and `<SidebarTrigger />`.
- **Validate**: Sidebar should be collapsible and functional.

### Task 4: Configure Routes

- **File**: `frontend/src/App.jsx`
- **Action**: UPDATE
- **Implement**: Add `<Route path="chat/:sessionId" element={<ChatPage />} />`. (Note: `ChatPage` will be implemented in STORY-004).
- **Validate**: Clicking a sidebar item updates the URL.

---

## End-to-End Tests

- [ ] Open the app -> Sidebar is visible.
- [ ] Sidebar shows the list of seeded sessions (from STORY-001).
- [ ] Clicking a session navigates to `/chat/:id`.
- [ ] The active session is highlighted in the sidebar.

---

## Validation

```bash
cd frontend
npm run lint
```

---

## Acceptance Criteria

- [x] `AppSidebar` component (shadcn/ui) displays a list of recent chat sessions for the logged-in user.
- [x] Each session entry in the sidebar shows the `title` and its `created_at` date (formatted).
- [x] Sessions are ordered by date (newest first).
- [x] Clicking a session navigates to `/chat/:sessionId`.
- [x] "New Chat" button starts a fresh analysis.
