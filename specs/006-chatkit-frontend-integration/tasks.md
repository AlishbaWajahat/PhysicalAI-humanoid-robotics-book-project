# Tasks: ChatKit Frontend Integration

**Input**: Design documents from `/specs/006-chatkit-frontend-integration/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec - focusing on implementation and manual verification

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` (Python FastAPI server)
- **Frontend**: `src/components/` (Docusaurus React components)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [X] T001 Add ChatKit dependencies to backend/requirements.txt (openai-chatkit>=1.4.0, fastapi>=0.115.0, uvicorn[standard]>=0.34.0)
- [X] T002 [P] Install backend dependencies with `uv pip install -r backend/requirements.txt`
- [X] T003 [P] Add ChatKit-JS to package.json (@openai/chatkit-react)
- [X] T004 [P] Install frontend dependencies with `npm install`
- [X] T005 Add CHATKIT_BACKEND_PORT=8001 to backend/.env
- [X] T006 [P] Add CHATKIT_BACKEND_URL=http://localhost:8001/chatkit to docusaurus.config.js customFields
- [X] T006.1 Add SQLAlchemy and psycopg2-binary to backend/requirements.txt for Neon Postgres
- [X] T006.2 [P] Create Neon Serverless Postgres database instance
- [X] T006.3 Add NEON_DATABASE_URL to backend/.env with connection string
- [X] T006.4 [P] Install additional dependencies with `uv pip install -r backend/requirements.txt`

**Checkpoint**: Dependencies installed, environment configured, database provisioned

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Verify existing RAG agent is accessible and set up database schema

**⚠️ CRITICAL**: Ensure existing RAG agent can be imported before ChatKit integration

- [X] T007 Verify backend/agent/rag_agent.py exists and is importable
- [X] T008 Test existing RAG agent (book_rag_agent) responds correctly to sample queries
- [X] T009 Confirm Qdrant vector database is running and accessible
- [X] T009.1 [P] Create backend/database.py with SQLAlchemy setup
- [X] T009.2 Define Session model (id, created_at, last_activity) in backend/database.py
- [X] T009.3 Define Message model (id, session_id, role, content, selected_text, timestamp) in backend/database.py
- [X] T009.4 Create database tables using SQLAlchemy create_all()
- [X] T009.5 Test database connection and verify tables created successfully

**Checkpoint**: Foundation ready - RAG agent verified, database schema created

---

## Phase 3: User Story 1 - Ask Questions and Get Answers (Priority: P1) 🎯 MVP

**Goal**: Enable readers to ask questions about book content through a floating chatbot and receive streaming answers from the RAG backend.

**Independent Test**: Open any Docusaurus page, click chatbot icon, type "What is inverse kinematics?", verify streaming answer appears word-by-word.

### Backend Implementation for User Story 1

- [X] T010 [P] [US1] Create backend/chatkit_server.py file with FastAPI app initialization
- [X] T011 [US1] Import existing RAG agent (book_rag_agent, Runner) from backend/agent/rag_agent.py
- [X] T011.5 [US1] Load environment variables (GEMINI_API_KEY, QDRANT_URL, CHATKIT_BACKEND_PORT, NEON_DATABASE_URL) from backend/.env using dotenv
- [X] T012 [US1] Implement async respond(thread, message) handler that calls RAG agent
- [X] T012.1 [US1] Extract session_id from thread metadata
- [X] T012.2 [US1] Retrieve conversation history from database for session_id
- [X] T012.3 [US1] Include conversation history in RAG agent context
- [X] T013 [US1] Add streaming logic: yield TextDelta events word-by-word from agent response
- [X] T013.1 [US1] Save user message to database before processing
- [X] T013.2 [US1] Save assistant response to database after streaming completes
- [X] T014 [US1] Add try-except error handling with ErrorEvent for agent failures
- [X] T014.1 [US1] Add database fallback: if DB fails, continue with in-memory session only
- [X] T015 [US1] Create ChatKitServer instance with respond handler
- [X] T016 [US1] Mount ChatKit server on FastAPI app at /chatkit endpoint
- [X] T017 [US1] Add CORS middleware to allow Docusaurus frontend (http://localhost:3000)
- [X] T018 [US1] Add health check endpoint at /health
- [X] T019 [US1] Add uvicorn server startup in __main__ block using CHATKIT_BACKEND_PORT

### Frontend Implementation for User Story 1

- [X] T020 [P] [US1] Create src/components/Chatkit-chatbot/ directory
- [X] T021 [P] [US1] Create src/components/Chatkit-chatbot/index.jsx with React component skeleton
- [X] T022 [US1] Import useChatKit and ChatKit from @openai/chatkit-react
- [X] T023 [US1] Initialize useChatKit hook with api.url from docusaurus.config.js customFields
- [X] T023.1 [US1] Generate or retrieve session_id from localStorage
- [X] T023.2 [US1] Pass session_id in thread metadata to backend
- [X] T024 [US1] Add useState for isOpen (chat panel visibility)
- [X] T025 [US1] Render floating chatbot icon (💬) when isOpen is false
- [X] T026 [US1] Render chat panel with ChatKit component when isOpen is true
- [X] T027 [US1] Add onClick handler to floating icon to set isOpen=true

### Styling for User Story 1

- [X] T028 [P] [US1] Create src/components/Chatkit-chatbot/styles.module.css
- [X] T029 [P] [US1] Style floating icon (position: fixed, bottom-right, circular button)
- [X] T030 [P] [US1] Style chat panel (fixed position, 380px width, 600px height, white background)
- [X] T031 [P] [US1] Style chat header with title "Ask about the book"
- [X] T032 [P] [US1] Add hover effect to floating icon (scale transform)
- [X] T033 [P] [US1] Add box shadow to chat panel for depth

### Integration for User Story 1

- [X] T034 [US1] Create src/theme/Root.js if it doesn't exist (Docusaurus theme swizzle)
- [X] T035 [US1] Import Chatkit-chatbot component in src/theme/Root.js
- [X] T036 [US1] Render Chatkit-chatbot component in Root layout (appears on all pages)
- [X] T037 [US1] Start backend server with `python backend/chatkit_server.py`
- [X] T038 [US1] Start Docusaurus dev server with `npm start`
- [X] T039 [US1] Manually test: Click icon, ask question, verify streaming response

**Checkpoint**: User Story 1 complete - users can ask questions and get streaming answers. This is the MVP.

---

## Phase 4: User Story 2 - Minimize and Restore Chatbot (Priority: P2)

**Goal**: Allow readers to close the chat panel while preserving conversation history, then reopen to see previous messages.

**Independent Test**: Open chatbot, ask a question, close panel via close button, reopen panel, verify conversation history is visible.

### Implementation for User Story 2

- [X] T040 [P] [US2] Add close button to chat panel header in src/components/Chatkit-chatbot/index.jsx
- [X] T041 [US2] Add onClick handler to close button that sets isOpen=false
- [X] T042 [US2] Verify ChatKit-JS maintains conversation state when panel is closed
- [X] T043 [US2] Test reopening panel shows full conversation history

### Styling for User Story 2

- [X] T044 [P] [US2] Style close button (× symbol, top-right of header, white color)
- [X] T045 [P] [US2] Add hover effect to close button (opacity change)

### Verification for User Story 2

- [X] T046 [US2] Manually test: Ask question, close panel, reopen panel, verify history persists
- [X] T047 [US2] Verify closing panel only hides UI (does not destroy state)
- [X] T048 [US2] Verify multiple open/close cycles maintain conversation

**Checkpoint**: User Story 2 complete - users can minimize and restore chatbot while keeping conversation history.

---

## Phase 5: User Story 3 - Selected Text Questioning (Priority: P2)

**Goal**: Allow readers to highlight text on documentation pages and ask questions about it, providing context to the chatbot.

**Independent Test**: Highlight text on any page, click "Ask about this" button that appears, verify chatbot receives selected text as context.

### Backend Implementation for User Story 3

- [X] T048.1 [US3] Modify respond handler in chatkit_server.py to accept selected_text field from message metadata
- [X] T048.2 [US3] Extract selected_text from message if present
- [X] T048.3 [US3] Prepend selected_text to user question with context marker (e.g., "Selected text: {text}\n\nQuestion: {question}")
- [X] T048.4 [US3] Store selected_text in Message model when saving to database
- [X] T048.5 [US3] Test with sample selected text to verify context is used in RAG retrieval

### Frontend Implementation for User Story 3

- [X] T048.6 [P] [US3] Add text selection detection in src/components/Chatkit-chatbot/index.jsx
- [X] T048.7 [US3] Add useEffect hook to listen for text selection events on document
- [X] T048.8 [US3] Add useState for selectedText and showAskButton
- [X] T048.9 [US3] When text selected, show floating "Ask about this" button near selection
- [X] T048.10 [US3] When "Ask about this" clicked, open chatbot with selectedText pre-loaded
- [X] T048.11 [US3] Pass selectedText in message metadata to backend
- [X] T048.12 [US3] Display selected text in chat as context (e.g., quoted block above input)
- [X] T048.13 [US3] Add clear button to remove selected text context

### Styling for User Story 3

- [X] T048.14 [P] [US3] Style "Ask about this" button (floating, follows cursor, distinctive color)
- [X] T048.15 [P] [US3] Style selected text display in chat panel (quoted block, gray background)
- [X] T048.16 [P] [US3] Add animation for button appearance/disappearance

### Verification for User Story 3

- [X] T048.17 [US3] Test highlighting text and clicking "Ask about this" button
- [X] T048.18 [US3] Verify selected text appears in chat as context
- [X] T048.19 [US3] Verify backend receives and uses selected text in RAG query
- [X] T048.20 [US3] Test clearing selected text context
- [X] T048.21 [US3] Test with long selected text (>500 characters)

**Checkpoint**: User Story 3 complete - users can ask questions about selected text.

---

## Phase 6: User Story 4 - Conversation History Persistence (Priority: P2)

**Goal**: Persist conversation history to Neon Postgres so users can continue conversations across browser sessions.

**Independent Test**: Ask questions, close browser, reopen site, verify conversation history is restored from database.

### Backend Implementation for User Story 4

- [X] T048.22 [US4] Verify database.py Session and Message models support persistence (already created in Phase 2)
- [X] T048.23 [US4] In chatkit_server.py, add get_or_create_session(session_id) function
- [X] T048.24 [US4] Add get_conversation_history(session_id, limit=50) function
- [X] T048.25 [US4] Add save_message(session_id, role, content, selected_text) function
- [X] T048.26 [US4] In respond handler, call get_conversation_history at start
- [X] T048.27 [US4] Format history as messages for RAG agent context
- [X] T048.28 [US4] Update session.last_activity after each message
- [X] T048.29 [US4] Add database connection pooling for performance
- [X] T048.30 [US4] Test database operations with multiple sessions

### Frontend Implementation for User Story 4

- [X] T048.31 [P] [US4] Verify session_id persists in localStorage (already implemented in Phase 3)
- [X] T048.32 [US4] Add GET /chatkit/history/{session_id} endpoint in backend
- [X] T048.33 [US4] On component mount, fetch conversation history from backend
- [X] T048.34 [US4] Load history into ChatKit component state
- [X] T048.35 [US4] Test closing and reopening browser to verify history persists
- [X] T048.36 [US4] Add "Clear history" button to chatbot UI (optional feature)

### Error Handling for User Story 4

- [X] T048.37 [P] [US4] Add try-catch around all database operations
- [X] T048.38 [US4] If database unavailable, log warning and continue with in-memory session
- [X] T048.39 [US4] Add reconnection logic for transient database failures
- [X] T048.40 [US4] Test behavior when Neon Postgres is unreachable

### Verification for User Story 4

- [X] T048.41 [US4] Test conversation persistence: ask questions, close browser, reopen, verify history
- [X] T048.42 [US4] Test with multiple sessions (different browser/incognito)
- [X] T048.43 [US4] Verify conversations don't mix between sessions
- [X] T048.44 [US4] Test large conversation history (>50 messages)
- [X] T048.45 [US4] Test database failure fallback to in-memory

**Checkpoint**: User Story 4 complete - conversation history persists across sessions.

---

## Phase 7: User Story 5 - Visual Feedback During Processing (Priority: P3)

**Goal**: Show users a typing indicator or loading state while the backend processes their question before streaming begins.

**Independent Test**: Ask a question, observe loading indicator appears immediately, verify indicator disappears when streaming starts.

### Implementation for User Story 3

- [X] T049 [P] [US3] Check if ChatKit-JS provides built-in loading state indicators
- [X] T050 [US3] If built-in: Enable loading indicator in ChatKit component props
- [X] T051 [US3] If custom needed: Add isLoading state to Chatkit-chatbot component
- [X] T052 [US3] Set isLoading=true when message sent, false when streaming starts
- [X] T053 [US3] Render loading indicator (typing dots animation) in chat panel

### Styling for User Story 3

- [X] T054 [P] [US3] Create typing indicator animation in styles.module.css
- [X] T055 [P] [US3] Style loading state with pulsing dots or spinner

### Verification for User Story 3

- [X] T056 [US3] Manually test: Ask question, verify loading indicator appears
- [X] T057 [US3] Verify loading indicator disappears when text starts streaming
- [X] T058 [US3] Test with slow network (throttle) to ensure indicator is visible

**Checkpoint**: User Story 5 complete - users see visual feedback during processing.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements, error handling, and production readiness

### Error Handling

- [X] T059 [P] Add error message display in frontend for connection failures
- [X] T060 [P] Add error message for empty message submission (if not handled by ChatKit)
- [X] T061 Add backend logging for all errors with proper log levels
- [X] T062 Test backend unreachable scenario: Stop server, verify frontend shows error

### Edge Cases

- [X] T063 [P] Test extremely long response (>1000 words) - verify streaming works
- [X] T064 [P] Test navigation during streaming - verify ChatKit cleans up properly
- [X] T065 Test 10-message conversation - verify no performance degradation
- [X] T066 Test rapid consecutive messages - verify all are answered correctly
- [X] T066.1 [P] Test extremely long selected text (>1000 characters) - verify handling
- [X] T066.2 [P] Test database connection failure during chat - verify fallback works
- [X] T066.3 Test highlighting text while response is streaming
- [X] T066.4 Test corrupted session_id in localStorage
- [X] T066.5 Test very large conversation history (>100 messages) - verify performance

### Documentation

- [X] T067 [P] Add inline code comments to backend/chatkit_server.py
- [X] T067.1 [P] Add inline code comments to backend/database.py
- [X] T068 [P] Add inline code comments to src/components/Chatkit-chatbot/index.jsx
- [X] T069 Create README section explaining how to run the chatbot feature
- [X] T069.1 [P] Document Neon Postgres setup instructions
- [X] T069.2 [P] Document environment variables in README

### Code Quality

- [X] T070 [P] Run Black formatter on backend/chatkit_server.py and backend/database.py
- [X] T071 [P] Run Ruff linter on backend/chatkit_server.py and backend/database.py - fix issues
- [X] T072 [P] Run ESLint on src/components/Chatkit-chatbot/ and fix issues
- [X] T073 [P] Run Prettier on src/components/Chatkit-chatbot/ for formatting

### Verification

- [X] T074 Verify all acceptance scenarios from spec.md are satisfied
- [X] T075 Verify all success criteria from spec.md are met
- [X] T076 Final end-to-end test: Full user journey from opening site to multi-turn conversation

**Checkpoint**: Feature complete and production-ready

---

## Dependency Graph

### Story Completion Order

```
Setup (Phase 1)
  ↓
Foundational (Phase 2)
  ↓
User Story 1 (Phase 3) ← MUST complete first (MVP)
  ↓
User Story 2 (Phase 4) ← Can start after US1 complete
  ↓
User Story 3 (Phase 5) ← Can start after US1 complete
  ↓
Polish (Phase 6)
```

### Independent Stories

- **User Story 2** and **User Story 3** can be implemented in parallel after User Story 1 is complete
- Each story builds on User Story 1 but is otherwise independent

---

## Parallel Execution Opportunities

### Phase 1 (Setup)
- Tasks T002, T003, T004, T006 can run in parallel

### Phase 3 (User Story 1)
- Backend tasks T010-T019 independent from frontend tasks T020-T033
- Can assign backend to one developer, frontend to another
- Styling tasks T028-T033 can run in parallel with implementation

### Phase 4 (User Story 2)
- Styling tasks T044-T045 can run in parallel with implementation

### Phase 5 (User Story 3)
- Styling tasks T054-T055 can run in parallel with implementation

### Phase 6 (Polish)
- Most tasks can run in parallel (different files, independent concerns)

---

## Implementation Strategy

### MVP Approach

**Minimum Viable Product**: User Story 1 only
- Delivers core value: Ask questions, get streaming answers
- Estimated effort: 30-45 minutes
- Provides immediate user value

### Incremental Delivery

1. **Release 1 (MVP)**: User Story 1
   - Users can ask questions and get answers
   - Basic functionality working

2. **Release 2**: User Story 1 + User Story 2
   - Added minimize/restore capability
   - Improved usability

3. **Release 3**: All user stories
   - Added loading indicators
   - Complete feature set

4. **Release 4**: All stories + Polish
   - Production-ready
   - Error handling complete
   - Code quality verified

---

## Task Summary

- **Total Tasks**: 77
- **Phase 1 (Setup)**: 6 tasks
- **Phase 2 (Foundational)**: 3 tasks
- **Phase 3 (User Story 1 - MVP)**: 31 tasks
- **Phase 4 (User Story 2)**: 9 tasks
- **Phase 5 (User Story 3)**: 10 tasks
- **Phase 6 (Polish)**: 18 tasks

**Parallel Opportunities**: ~30 tasks marked [P] can run in parallel with others

**Independent Test Criteria**:
- **US1**: Open page → Click icon → Ask question → Verify streaming answer
- **US2**: Ask question → Close panel → Reopen → Verify history persists
- **US3**: Ask question → Observe loading indicator → Verify it disappears when streaming starts

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only)

---

## Validation Checklist

Before marking this feature complete:

- [X] All User Story 1 acceptance scenarios pass
- [X] All User Story 2 acceptance scenarios pass
- [X] All User Story 3 acceptance scenarios pass
- [X] All edge cases from spec.md handled
- [X] All success criteria from spec.md met (< 5s response, < 2s streaming start, etc.)
- [X] Constitution Rule 4: Code passes Black, Ruff, ESLint
- [X] Constitution Rule 5: All versions explicitly specified
- [X] Constitution Rule 14: No modifications to existing agent/indexing
- [X] Manual testing completed on Docusaurus site
- [X] Documentation updated with usage instructions
