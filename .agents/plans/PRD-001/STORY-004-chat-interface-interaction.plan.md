---
story: STORY-004
prd: PRD-001
slug: chat-interface-interaction
title: Chat Interface UI
type: feature
complexity: medium
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-20
---

# Plan: Chat Interface UI

## Summary

This plan covers the implementation of the `ChatInterface` component, which is the heart of the user's interaction with the AI agent. The component will display a scrollable thread of messages, differentiate between user and agent roles, and handle message submission and loading states. Agent responses will specifically highlight SQL queries using a dedicated code block style.

## User Story

As a user, I want a clean and distraction-free chat interface, so that I can focus on my data analysis.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-004-chat-interface-interaction.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | feature |
| Complexity | MEDIUM |
| Systems Affected | frontend |
| Story | STORY-004 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| shadcn | Used for chat bubbles, input area, and scroll area components. | Task 1, Task 2 |
| vercel-react-best-practices | Ensures smooth scroll and efficient list rendering. | Task 2 |

---

## Patterns to Follow

### Chat Bubble
```jsx
// SOURCE: Suggested shadcn composition
<div className={cn("flex flex-col gap-2", isUser ? "items-end" : "items-start")}>
  <div className={cn("rounded-lg p-4", isUser ? "bg-primary text-primary-foreground" : "bg-muted")}>
    {content}
  </div>
</div>
```

### Auto-scroll
```jsx
// SOURCE: Common React pattern
useEffect(() => {
  scrollRef.current?.scrollIntoView({ behavior: "smooth" });
}, [messages]);
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `frontend/src/components/ChatInterface.jsx` | CREATE | Main chat thread and input component. |
| `frontend/src/pages/dashboard/ChatPage.jsx` | CREATE | Page wrapper for the chat session. |
| `frontend/src/App.jsx` | UPDATE | Ensure `ChatPage` is imported and used in the route. |

---

## Tasks

### Task 1: Create ChatPage component

- **File**: `frontend/src/pages/dashboard/ChatPage.jsx`
- **Action**: CREATE
- **Implement**: 
    - Use `useParams` to get `sessionId`.
    - Fetch initial session history from `GET /api/v1/sessions/{id}`.
    - Render `ChatInterface` and pass messages and session ID.
- **Validate**: Navigate to `/chat/1` and verify the page loads.

### Task 2: Implement ChatInterface Component

- **File**: `frontend/src/components/ChatInterface.jsx`
- **Action**: CREATE
- **Implement**: 
    - Message list using `ScrollArea`.
    - Distinct styling for roles (`user`, `agent`).
    - Handle `onSubmit` for the input field.
    - Call `POST /api/v1/sessions/{id}/chat` and update local state with the response.
    - Display a loading skeleton or spinner while waiting for the agent.
- **Validate**: Type a message and see it appear in the thread.

### Task 3: SQL Code Formatting

- **File**: `frontend/src/components/ChatInterface.jsx`
- **Action**: UPDATE
- **Implement**: Detect SQL code blocks in agent responses and apply `font-mono` and `bg-zinc-900` styling (Obsidian Deep theme).
- **Validate**: Verify SQL queries are readable and correctly styled.

### Task 4: Integration with App.jsx

- **File**: `frontend/src/App.jsx`
- **Action**: UPDATE
- **Implement**: Import `ChatPage` and add it to the routes under the dashboard layout.
- **Validate**: Full navigation flow from Sidebar to ChatPage.

---

## End-to-End Tests

- [ ] Select a session from the sidebar -> Chat history loads.
- [ ] Send a message -> Message appears, agent starts thinking.
- [ ] Agent replies -> Reply appears with SQL query formatted correctly.
- [ ] Chat automatically scrolls to the newest message.

---

## Validation

```bash
cd frontend
npm run lint
```

---

## Acceptance Criteria

- [x] `ChatInterface` component is implemented with distinct styles for User and Agent.
- [x] User can type a message and send it.
- [x] Messages are displayed in a scrollable thread.
- [x] Agent responses display SQL queries in a code block (JetBrains Mono).
- [x] Loading state is shown while waiting for the agent response.
