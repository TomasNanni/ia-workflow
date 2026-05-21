# PRD-001: AI-Powered Database Analysis Chatbot — Story Board

**PRD**: [PRD.md](./PRD.md)
**Epic Branch**: `epic/PRD-001-db-analysis-chatbot` (base: `main`)
**Status**: 🟡 active

## Progress

1/13 stories done — 7%

## Stories

All stories commit on the epic branch `epic/PRD-001-db-analysis-chatbot`. No per-story branches.

| ID | Title | Type | Status | Complexity | Plan | Commit |
|----|-------|------|--------|------------|------|--------|
| STORY-001 | Session Persistence & Dual DB Infrastructure | technical | 🟡 in-progress | medium | [.plan](../../plans/PRD-001/STORY-001-infrastructure-sessions-db.plan.md) | — |
| STORY-008 | Analytics DB Seeding (PostgreSQL) | technical | ✅ done | small | — | `82031a8` |
| STORY-006 | User Authentication (Login & Register) | feature | 🟡 in-progress | medium | [.plan](../../plans/PRD-001/STORY-006-user-authentication-auth.plan.md) | — |
| STORY-009 | "Obsidian Deep" Theming & Responsive | enhancement | 🟡 in-progress | medium | [.plan](../../plans/PRD-001/STORY-009-obsidian-deep-theming.plan.md) | — |
| STORY-002 | AI Agent Core & Schema Discovery | feature | 🟡 in-progress | medium | [.plan](../../plans/PRD-001/STORY-002-ai-agent-core-discovery.plan.md) | — |
| STORY-003 | Navigation & Session List UI | feature | 🟡 in-progress | small | [.plan](../../plans/PRD-001/STORY-003-core-navigation-sidebar.plan.md) | — |
| STORY-007 | AI Agent Query Execution & Chat API | feature | 🟡 in-progress | medium | [.plan](../../plans/PRD-001/STORY-007-ai-agent-chat-execution.plan.md) | — |
| STORY-004 | Chat Interface UI | feature | 🟡 in-progress | medium | [.plan](../../plans/PRD-001/STORY-004-chat-interface-interaction.plan.md) | — |
| STORY-005 | Schema Map Visualizer | feature | 🟡 in-progress | medium | [.plan](../../plans/PRD-001/STORY-005-schema-map-visualizer.plan.md) | — |
| STORY-010 | Automated Session Title Generation | enhancement | 🟡 in-progress | small | [.plan](../../plans/PRD-001/STORY-010-session-title-generation.plan.md) | — |
| STORY-011 | Query Validation & Timeout Security | enhancement | ⬜ todo | medium | — | — |
| STORY-012 | Session Lifecycle Management (Deletion) | feature | ⬜ todo | small | — | — |
| STORY-013 | Agent Accuracy Testing (Evaluation) | technical | ⬜ todo | medium | — | — |

## Status Icons
- ⬜ todo
- 🟡 in-progress
- ✅ done
- 🔴 blocked

## Dependencies

- STORY-008 blocked by STORY-001
- STORY-006 blocked by STORY-001
- STORY-002 blocked by STORY-001, STORY-008
- STORY-003 blocked by STORY-001, STORY-006, STORY-009
- STORY-007 blocked by STORY-002
- STORY-004 blocked by STORY-007, STORY-003, STORY-009
- STORY-005 blocked by STORY-004, STORY-002
- STORY-010 blocked by STORY-007
- STORY-011 blocked by STORY-007
- STORY-012 blocked by STORY-001, STORY-003
- STORY-013 blocked by STORY-007
