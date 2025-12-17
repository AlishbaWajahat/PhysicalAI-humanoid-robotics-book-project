# Research: ChatKit Frontend Integration

**Date**: 2025-12-13
**Feature**: 006-chatkit-frontend-integration
**Purpose**: Resolve technical unknowns for integrating ChatKit-Python and ChatKit-JS

## Research Questions

### Q1: How to integrate ChatKit-Python with an existing openai-agents SDK agent?

**Decision**: Use ChatKit-Python's `ChatKitServer` class with a custom `respond` method that calls the existing RAG agent

**Rationale**:
- ChatKit-Python provides a server abstraction that handles the protocol with Chat Kit-JS
- The `respond` method receives messages and can delegate to any backend logic
- Supports streaming via async generator pattern
- Does not require rebuilding the agent - can reuse existing implementation

**Implementation Notes**:
- Install `openai-chatkit` package (latest version from PyPI as of Nov 2025)
- Create ChatKitServer instance with custom respond handler
- Mount on FastAPI app using `app.mount("/chatkit", chatkit_server.app())`
- The respond method signature: `async def respond(thread: Thread, message: UserMessage) -> AsyncGenerator[StreamEvent, None]`
- Stream responses by yielding `TextDelta` events

**Sources**:
- https://openai.github.io/chatkit-python/ (Official ChatKit-Python docs)
- https://pypi.org/project/openai-chatkit/ (Package repository)
- https://github.com/openai/chatkit-python (Source code and examples)

**Alternatives Considered**:
- Building custom WebSocket/SSE server: Rejected - reinvents ChatKit protocol, more complexity
- Using ChatKit's built-in agent builder: Rejected - requires rewriting existing agent logic

---

### Q2: How to integrate ChatKit-JS into a Docusaurus React 19 application?

**Decision**: Use `@openai/chatkit-react` npm package with `useChatKit` hook and `ChatKit` component

**Rationale**:
- Official React bindings for ChatKit
- Provides `useChatKit` hook for state management
- `ChatKit` component handles UI, streaming, and backend communication
- Compatible with React 19 (verified from npm package page)
- Can be embedded in any React application including Docusaurus

**Implementation Notes**:
- Install: `npm install @openai/chatkit-react`
- Configure backend URL via `api.url` prop in `useChatKit`
- Component auto-handles streaming responses
- Customize UI via className and CSS modules
- Create wrapper component for floating icon + panel pattern

**Sources**:
- https://openai.github.io/chatkit-js/ (Official ChatKit.js docs)
- https://www.npmjs.com/package/@openai/chatkit-react (npm package)

**Alternatives Considered**:
- Custom chat UI with fetch/SSE: Rejected - requires implementing ChatKit protocol
- Third-party chat libraries: Rejected - not designed for ChatKit backend

---

### Q3: How does streaming work between ChatKit-Python and ChatKit-JS?

**Decision**: ChatKit uses Server-Sent Events (SSE) with a specific event protocol

**Rationale**:
- ChatKit-Python yields stream events (TextDelta, ToolUse, etc.)
- Events are automatically serialized to SSE format
- ChatKit-JS subscribes to SSE endpoint and reconstructs messages
- Built-in protocol handling - no manual SSE implementation needed

**Implementation Notes**:
- Backend yields events: `yield TextDelta(delta="word by word")`
- Frontend automatically receives and displays incremental text
- No manual SSE setup required - handled by ChatKit libraries
- Stream completes when generator finishes

**Sources**:
- https://openai.github.io/chatkit-python/api/chatkit/server/ (Server streaming docs)

**Alternatives Considered**:
- WebSocket streaming: Rejected - ChatKit uses SSE by default
- Polling: Rejected - doesn't support real-time streaming

---

### Q4: What are the error handling patterns for ChatKit?

**Decision**: Use try-except blocks in respond method + ChatKit error events for user-facing errors

**Rationale**:
- ChatKit-Python provides error event types for graceful error display
- Frontend automatically shows error messages to user
- Supports retry logic and error recovery
- Clean separation of internal errors vs user-facing errors

**Implementation Notes**:
- Backend: Wrap agent calls in try-except, yield error events on failure
- Frontend: ChatKit component shows error messages automatically
- Use appropriate error types: connection errors, timeout errors, agent errors
- Log internal errors server-side, show friendly messages client-side

**Edge Case Handling**:

| Edge Case | Default Behavior | Recommended Handling |
|-----------|------------------|---------------------|
| Backend unreachable | ChatKit-JS connection error | Show "Cannot connect to server" message |
| Extremely long response | Streams continuously | No special handling - streaming works for any length |
| Empty message | Client validation prevents | Add frontend validation to disable submit on empty input |
| Navigate during stream | Stream interrupted | ChatKit-JS handles cleanup automatically |
| Tab closed mid-stream | Connection dropped | No action needed - server cleans up |

**Sources**:
- https://openai.github.io/chatkit-python/api/chatkit/errors/ (Error handling docs)

---

### Q5: What are the exact version requirements?

**Decision**: Use latest stable versions of all dependencies

**Versions to Specify**:
- Backend:
  - `openai-chatkit>=1.4.0` (latest as of Nov 2025)
  - `fastapi>=0.115.0`
  - `uvicorn>=0.34.0`
  - Python 3.13+
- Frontend:
  - `@openai/chatkit-react` (verify latest from npm at implementation time)
  - React 19 (already in use)
  - Node.js 18+ (for development)

**Rationale**:
- Latest versions include bug fixes and performance improvements
- ChatKit is actively developed - newer is better for streaming
- All versions confirmed compatible via official docs and package metadata

**Sources**:
- https://pypi.org/project/openai-chatkit/ (Python package versions)
- https://www.npmjs.com/package/@openai/chatkit-react (JS package versions)

---

## Configuration Requirements

### Environment Variables

```bash
# Backend .env
CHATKIT_BACKEND_PORT=8001
OPENAI_API_KEY=<existing>
QDRANT_URL=<existing>
COHERE_API_KEY=<existing>

# Frontend .env (or docusaurus.config.js)
CHATKIT_BACKEND_URL=http://localhost:8001/chatkit
```

### Dependencies

**backend/requirements.txt additions**:
```
openai-chatkit>=1.4.0
fastapi>=0.115.0
uvicorn[standard]>=0.34.0
```

**package.json additions**:
```json
{
  "dependencies": {
    "@openai/chatkit-react": "latest"
  }
}
```

---

## Integration Architecture

### Request/Response Flow

1. **User Action**: User clicks floating chatbot icon
2. **Frontend**: ChatKit-JS opens panel, initializes connection to `CHATKIT_BACKEND_URL`
3. **User Input**: User types message, ChatKit-JS sends to backend `/chatkit` endpoint
4. **Backend Reception**: ChatKitServer.respond() receives message
5. **Agent Processing**: respond() calls existing RAG agent with user question
6. **Agent Retrieval**: Agent queries Qdrant for relevant book chunks
7. **Agent Response**: Agent generates answer (may be non-streaming internally)
8. **Stream Conversion**: respond() yields TextDelta events for agent's response
9. **SSE Transmission**: ChatKit-Python streams events to frontend
10. **Frontend Display**: ChatKit-JS receives events, displays text word-by-word

### Backend Bridge Pattern

```python
# Conceptual structure (not final code)
from chatkit import ChatKitServer, TextDelta
from existing_agent import get_agent_response

async def respond(thread, message):
    # Call existing agent
    answer = await get_agent_response(message.content)

    # Stream response word-by-word
    for word in answer.split():
        yield TextDelta(delta=word + " ")
```

### Frontend Component Pattern

```jsx
// Conceptual structure (not final code)
import { useChatKit, ChatKit } from '@openai/chatkit-react';

function Chatbot() {
  const { control } = useChatKit({
    api: { url: process.env.CHATKIT_BACKEND_URL }
  });

  return <ChatKit control={control} />;
}
```

---

## Open Questions Resolved

All technical unknowns from the specification have been resolved through research. The implementation can proceed to Phase 1 (Design & Contracts).
