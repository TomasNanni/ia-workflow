---
story: STORY-005
prd: PRD-001
slug: schema-map-visualizer
title: Schema Map Visualizer
type: feature
complexity: medium
epic_branch: epic/PRD-001-db-analysis-chatbot
created: 2026-05-20
---

# Plan: Schema Map Visualizer

## Summary

This plan covers the implementation of the `SchemaMap` component, providing users with a visual reference of the database structure. This component will fetch the schema (tables and columns) from the analytics database and display it in a clean, hierarchical list using `shadcn`'s Accordion. It will be integrated into the `ChatPage` in a 50/50 split layout.

## User Story

As a user, I want to see the database schema on the side of the chat, so that I know what data is available for analysis.

## Story Reference

- Story file: `.agents/stories/PRD-001-db-analysis-chatbot/STORY-005-schema-map-visualizer.md`
- PRD: `.agents/PRDs/PRD-001-db-analysis-chatbot/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | feature |
| Complexity | MEDIUM |
| Systems Affected | frontend, backend |
| Story | STORY-005 |
| PRD | PRD-001 |
| Epic Branch | `epic/PRD-001-db-analysis-chatbot` |

---

## Skills In Use

| Skill | Why it applies | Tasks affected |
|-------|---------------|----------------|
| shadcn | Used for the Accordion and layout components. | Task 2, Task 3 |

---

## Patterns to Follow

### Accordion for Schema
```jsx
// SOURCE: shadcn accordion documentation
<Accordion type="single" collapsible>
  {tables.map(table => (
    <AccordionItem value={table.name}>
      <AccordionTrigger>{table.name}</AccordionTrigger>
      <AccordionContent>
        <ul className="list-disc pl-4 text-sm text-muted-foreground">
          {table.columns.map(col => (
            <li key={col.name}>{col.name} ({col.type})</li>
          ))}
        </ul>
      </AccordionContent>
    </AccordionItem>
  ))}
</Accordion>
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/routers/analytics.py` | CREATE | Endpoint to fetch the analytics database schema. |
| `backend/app/main.py` | UPDATE | Register the analytics router. |
| `frontend/src/components/SchemaMap.jsx` | CREATE | Component to visualize the schema. |
| `frontend/src/pages/dashboard/ChatPage.jsx` | UPDATE | Split the layout to include the SchemaMap. |

---

## Tasks

### Task 1: Implement Backend Schema Endpoint

- **File**: `backend/app/routers/analytics.py`
- **Action**: CREATE
- **Implement**: 
    - `GET /api/v1/analytics/schema`
    - Use SQLAlchemy inspector on the `analytics_engine` to get table and column info.
    - Return a list of tables with their columns and types.
- **Validate**: `curl http://localhost:8000/api/v1/analytics/schema` returns the expected JSON.

### Task 2: Install Accordion Component

- **Action**: EXECUTE
- **Implement**: `npx shadcn@latest add accordion`
- **Validate**: Check `src/components/ui/accordion.jsx`.

### Task 3: Implement SchemaMap Component

- **File**: `frontend/src/components/SchemaMap.jsx`
- **Action**: CREATE
- **Implement**: 
    - Fetch schema data from the new backend endpoint.
    - Render a list of tables using `Accordion`.
    - Apply "Obsidian Deep" styling (dark backgrounds, subtle borders).
- **Validate**: `npm run dev` and verify the component renders data correctly.

### Task 4: Update ChatPage Layout

- **File**: `frontend/src/pages/dashboard/ChatPage.jsx`
- **Action**: UPDATE
- **Implement**: 
    - Use a `flex` container or `Resizable` panel to split the screen.
    - Render `ChatInterface` on the left and `SchemaMap` on the right.
    - Add responsive classes to hide `SchemaMap` or switch to tabs on small screens.
- **Validate**: Check the layout on different screen sizes.

---

## End-to-End Tests

- [ ] Open a chat session -> Schema map is visible on the right.
- [ ] Tables are listed and can be expanded to show columns.
- [ ] Column types are correctly displayed.
- [ ] Resizing the window behaves according to the responsive design.

---

## Validation

```bash
cd backend && uvicorn app.main:app --reload
cd frontend && npm run lint
```

---

## Acceptance Criteria

- [x] `SchemaMap` component is implemented as a 50/50 split on the right side of the chat.
- [x] Schema map displays tables and columns fetched from the analytics database.
- [x] Users can toggle column details for each table.
- [x] Layout is responsive, collapsing the schema map on small screens.
