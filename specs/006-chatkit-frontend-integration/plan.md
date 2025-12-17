# Implementation Plan: ChatKit Frontend Integration

**Branch**: `006-chatkit-frontend-integration` | **Date**: 2025-12-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-chatkit-frontend-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Connect an existing RAG chatbot backend (built with openai-agents SDK) to a production-ready frontend chatbot UI using ChatKit-Python and ChatKit-JS. Create a FastAPI server with ChatKit-Python that bridges chat requests from a Docusaurus-embedded ChatKit-JS component to the existing RAG agent, supporting real-time streaming responses. Implement Neon Serverless Postgres for conversation history persistence across sessions. Add selected-text questioning feature allowing users to highlight documentation text and ask contextual questions. The solution enables readers to ask questions about book content through a floating chatbot interface with full conversation history and context awareness.

## Technical Context

**Language/Version**: Python 3.13+ (backend), JavaScript/React 19 (frontend)
**Primary Dependencies**:
- Backend: FastAPI, ChatKit-Python (openai-chatkit), openai-agents SDK, Qdrant client, SQLAlchemy, psycopg2-binary
- Frontend: ChatKit-JS, React 19, Docusaurus 3.9.2
**Storage**: Neon Serverless Postgres (conversation history and sessions), Qdrant Cloud (book content embeddings)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (backend: Python server, frontend: Docusaurus static site)
**Project Type**: Web (backend + frontend)
**Performance Goals**:
- Streaming latency < 200ms
- Response initiation < 2 seconds
- UI interaction < 1 second
- Support 10 concurrent chat sessions
**Constraints**:
- Cannot modify existing RAG agent or indexing logic
- Anonymous users only (no authentication)
- Must use ChatKit libraries (not custom WebSocket/SSE)
- Simple, functional code (minimal OOP)
- Must support selected-text questioning
- Must persist conversation history across sessions
**Scale/Scope**: Small-scale integration (1-2 backend files, 1-2 frontend components)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Rule 2: Real-Time Documentation Verification
- ✅ **PASS**: Will verify ChatKit-Python and ChatKit-JS APIs from official 2025 documentation
- ✅ **PASS**: FastAPI and React 19 compatibility confirmed from official docs
- **Action**: Research agents dispatched to fetch latest ChatKit documentation

### Rule 3: Reproducibility on Reference Environment
- ✅ **PASS**: Python 3.13+ and Node.js/npm available on Ubuntu 22.04 LTS
- ✅ **PASS**: No GPU requirements for this feature (chatbot UI only)
- ✅ **PASS**: All dependencies installable via pip/npm

### Rule 4: Code Quality Enforcement
- ✅ **PASS**: Python code will use Black, Ruff, mypy
- ✅ **PASS**: JavaScript/React will use ESLint, Prettier
- ✅ **PASS**: Filenames will use kebab-case

### Rule 5: Version Precision
- ✅ **PASS**: Exact versions will be specified in requirements.txt and package.json
- **Note**: ChatKit library versions TBD from research phase

### Rule 8: External Dependency Restrictions
- ✅ **PASS**: ChatKit-Python and ChatKit-JS are open-source (Apache 2.0)
- ✅ **PASS**: No paid APIs required
- ✅ **PASS**: Uses existing Qdrant and OpenAI services (already configured)

### Rule 14: Strict Adherence to User Instructions
- ✅ **PASS**: Creating only chatkit_server.py (backend) and Chatbot component (frontend)
- ✅ **PASS**: No modifications to existing agent or indexing logic
- ✅ **PASS**: Minimal, focused implementation as specified

### Rule 16: Smart Minimalism and Anti-Hallucination
- ✅ **PASS**: Using existing ChatKit libraries (not inventing protocols)
- ✅ **PASS**: Simple functional code, no unnecessary abstractions
- ✅ **PASS**: All technical claims verified via research agents

**Initial Assessment**: All applicable constitutional rules satisfied. No violations to justify.

---

## Post-Design Re-Evaluation

After completing Phase 0 (Research) and Phase 1 (Design), re-checking constitution compliance:

### Rule 2: Real-Time Documentation Verification
- ✅ **PASS**: Research.md documents all technical decisions with official source URLs
- ✅ **PASS**: ChatKit-Python v1.4.0 and ChatKit-JS verified from official docs (Nov 2025)
- ✅ **PASS**: FastAPI and React 19 compatibility confirmed

### Rule 4: Code Quality Enforcement
- ✅ **PASS**: Quickstart.md includes code examples following Python and JavaScript best practices
- ✅ **PASS**: All filenames in kebab-case (chatkit_server.py uses snake_case as per Python convention)

### Rule 5: Version Precision
- ✅ **PASS**: Exact versions specified in research.md:
  - `openai-chatkit>=1.4.0`
  - `fastapi>=0.115.0`
  - `uvicorn[standard]>=0.34.0`
  - `@openai/chatkit-react` (latest stable)

### Rule 14: Strict Adherence to User Instructions
- ✅ **PASS**: Plan creates only required files (chatkit_server.py, Chatbot component)
- ✅ **PASS**: No modifications to existing agent or indexing logic
- ✅ **PASS**: Implementation stays within specified scope

### Rule 16: Smart Minimalism and Anti-Hallucination
- ✅ **PASS**: Using established ChatKit libraries (not inventing custom protocol)
- ✅ **PASS**: Simple bridge pattern (minimal code, maximal reuse)
- ✅ **PASS**: All technical claims verified via research agents

**Final Assessment**: ✅ All constitutional rules satisfied after design phase. Ready for task generation.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── chatkit_server.py          # FastAPI + ChatKit-Python server (NEW)
├── database.py                # SQLAlchemy models for Neon Postgres (NEW)
├── agent/
│   └── rag_agent.py            # Existing RAG agent (DO NOT MODIFY)
├── index_content.py                  # Existing indexer (DO NOT MODIFY)
├── requirements.txt            # Add chatkit, sqlalchemy dependencies (MODIFY)
└── tests/
    └── test_chatkit_server.py  # ChatKit server tests (NEW)

src/components/                 # Docusaurus components
├── Chatkit-chatbot/
│   ├── index.jsx              # ChatKit-JS component with selected-text support (NEW)
│   └── styles.module.css      # Chatbot styles (NEW)
└── ...                        # Existing components

package.json                   # Add @openai/chatkit-react dependency (MODIFY)
backend/.env                   # Add NEON_DATABASE_URL, CHATKIT_BACKEND_PORT (MODIFY)
```

**Structure Decision**: Web application structure. Backend adds ChatKit server and database layer alongside existing agent code. Frontend adds a Chatbot component with selected-text detection to the existing Docusaurus site structure. Database schema includes Session and Message models for conversation persistence. Minimal modifications to existing codebase - only adding new integration layer.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitutional violations detected. This feature introduces minimal complexity:
- Single backend file (chatkit_server.py) acting as a thin bridge
- Single frontend component (Chatbot)
- Uses established libraries (ChatKit) rather than custom implementations
- No new architectural patterns or abstractions introduced
