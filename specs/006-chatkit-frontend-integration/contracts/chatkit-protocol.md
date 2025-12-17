# ChatKit Protocol Contract

**Feature**: 006-chatkit-frontend-integration
**Date**: 2025-12-13
**Protocol**: ChatKit (OpenAI)

## Overview

This document specifies the API contract between ChatKit-JS (frontend) and ChatKit-Python (backend). The protocol is defined by OpenAI's ChatKit libraries and is documented here for reference.

**Note**: This is NOT a custom API design. We are implementing the ChatKit standard protocol.

---

## Base Configuration

### Backend Endpoint

```
POST /chatkit
```

**Purpose**: Entry point for ChatKit protocol
**Implementation**: Mounted via `app.mount("/chatkit", chatkit_server.app())`
**Protocol**: Server-Sent Events (SSE) for streaming

### Frontend Configuration

```javascript
useChatKit({
  api: {
    url: process.env.CHATKIT_BACKEND_URL  // e.g., "http://localhost:8001/chatkit"
  }
})
```

---

## Request Format

### User Message Request

**Method**: POST (via ChatKit protocol)
**Content-Type**: application/json

**Request Body** (simplified representation):
```json
{
  "thread_id": "string",
  "message": {
    "id": "string",
    "role": "user",
    "content": "What is inverse kinematics?",
    "timestamp": "2025-12-13T10:30:00Z"
  }
}
```

**Fields**:
- `thread_id`: Session/conversation identifier (managed by ChatKit)
- `message.id`: Unique message ID
- `message.role`: Always "user" for user messages
- `message.content`: The actual question text
- `message.timestamp`: ISO 8601 timestamp

**Note**: ChatKit-JS automatically constructs these requests. Backend receives via ChatKitServer.respond() method.

---

## Response Format

### Streaming Response (SSE)

**Content-Type**: text/event-stream
**Transfer-Encoding**: chunked

### Event Types

#### 1. TextDelta Event

**Purpose**: Stream response text word-by-word

**Format**:
```
event: text.delta
data: {"delta": "word "}
```

**Python Backend**:
```python
yield TextDelta(delta="word ")
```

**Frontend Handling**: ChatKit-JS automatically appends to message

---

#### 2. Text Complete Event

**Purpose**: Signal end of text streaming

**Format**:
```
event: text.complete
data: {"text": "complete response text"}
```

**Python Backend**:
```python
# Automatically sent when generator completes
return
```

**Frontend Handling**: ChatKit-JS marks message as complete

---

#### 3. Error Event

**Purpose**: Report errors to user

**Format**:
```
event: error
data: {"message": "An error occurred", "code": "server_error"}
```

**Python Backend**:
```python
yield ErrorEvent(message="Cannot process request", code="server_error")
```

**Frontend Handling**: ChatKit-JS displays error message in UI

---

### Response Lifecycle

1. **Stream Start**: Connection established
2. **Text Deltas**: Multiple `text.delta` events streamed
3. **Stream End**: Generator completes, `text.complete` sent
4. **Connection Close**: SSE connection closed

**Example Stream**:
```
event: text.delta
data: {"delta": "Inverse "}

event: text.delta
data: {"delta": "kinematics "}

event: text.delta
data: {"delta": "is "}

event: text.delta
data: {"delta": "the "}

event: text.delta
data: {"delta": "process..."}

event: text.complete
data: {"text": "Inverse kinematics is the process..."}
```

---

## Error Handling

### Client Errors (400-499)

| Status Code | Error Type | User Message |
|-------------|-----------|--------------|
| 400 | Invalid Request | "Invalid message format" |
| 413 | Payload Too Large | "Message too long (max 10,000 characters)" |
| 429 | Rate Limit | "Too many requests. Please wait." |

**Backend Handling**:
```python
if len(message.content) > 10000:
    yield ErrorEvent(message="Message too long", code="invalid_request")
    return
```

---

### Server Errors (500-599)

| Status Code | Error Type | User Message |
|-------------|-----------|--------------|
| 500 | Internal Server Error | "Something went wrong. Please try again." |
| 502 | Bad Gateway | "Cannot connect to backend service" |
| 503 | Service Unavailable | "Service temporarily unavailable" |
| 504 | Gateway Timeout | "Request timed out. Please try again." |

**Backend Handling**:
```python
try:
    response = await agent.get_response(message.content)
except Exception as e:
    logger.error(f"Agent error: {e}")
    yield ErrorEvent(message="Error processing request", code="server_error")
    return
```

---

### Network Errors

| Error Type | Detection | Recovery |
|------------|-----------|----------|
| Connection Lost | SSE connection drops | ChatKit-JS shows "Connection lost" |
| Timeout | No data for 30 seconds | Frontend shows timeout message |
| Aborted | User closes chat/tab | Backend cleans up automatically |

---

## Streaming Protocol Details

### SSE Event Format

```
event: <event_type>
data: <json_payload>
id: <optional_event_id>

```

**Key Points**:
- Events separated by double newline (`\n\n`)
- Data must be JSON-encoded
- Event type determines how frontend processes data
- No custom headers needed (handled by ChatKit)

### Chunk Size

- **Recommended**: 1-10 words per TextDelta
- **Min**: 1 character
- **Max**: No hard limit (but smaller chunks = smoother UX)

### Latency Targets

- **First Byte**: < 2 seconds (time to first TextDelta)
- **Inter-Chunk**: < 200ms (time between deltas)
- **Total Timeout**: 30 seconds (max time for complete response)

---

## Configuration Options

### Backend Configuration

**Environment Variables**:
```bash
# FastAPI server
CHATKIT_BACKEND_PORT=8001
CHATKIT_MAX_MESSAGE_LENGTH=10000
CHATKIT_TIMEOUT_SECONDS=30

# Existing services
OPENAI_API_KEY=<key>
QDRANT_URL=<url>
COHERE_API_KEY=<key>
```

**ChatKitServer Options**:
```python
server = ChatKitServer(
    respond=respond_handler,
    # Additional options can be configured here
)
```

---

### Frontend Configuration

**ChatKit-JS Options**:
```javascript
useChatKit({
  api: {
    url: process.env.CHATKIT_BACKEND_URL,
    // Optional: timeout, retry, headers
  }
})
```

---

## Security Considerations

### CORS Configuration

**Backend** (FastAPI middleware):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Docusaurus dev server
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Content Security

- **Input Sanitization**: Handled by ChatKit libraries
- **Output Escaping**: Frontend auto-escapes all text
- **XSS Prevention**: Built into ChatKit-JS
- **CSRF**: Not applicable (no authentication/sessions)

---

## Testing Contract

### Manual Testing

**Test Case 1: Basic Message**
1. Send: "What is forward kinematics?"
2. Expect: Streaming response with relevant answer
3. Verify: Text appears word-by-word

**Test Case 2: Long Response**
1. Send: "Explain all types of kinematics"
2. Expect: Long streaming response (many TextDelta events)
3. Verify: UI remains responsive during streaming

**Test Case 3: Error Handling**
1. Stop backend server
2. Send: "Test message"
3. Expect: Connection error shown in UI

**Test Case 4: Empty Message**
1. Try to send empty message
2. Expect: Submit button disabled (frontend validation)

---

### Automated Testing

**Backend Contract Tests**:
```python
# Test respond method yields correct event types
async def test_respond_yields_text_deltas():
    events = []
    async for event in respond(mock_thread, mock_message):
        events.append(event)

    assert any(isinstance(e, TextDelta) for e in events)
```

**Frontend Integration Tests**:
```javascript
// Test ChatKit component receives streamed responses
test('displays streaming response', async () => {
  render(<Chatbot />);
  // Send message
  // Assert text appears incrementally
});
```

---

## Protocol Compliance

This implementation adheres to the ChatKit protocol specification as defined by OpenAI:
- https://openai.github.io/chatkit-python/ (Backend protocol)
- https://openai.github.io/chatkit-js/ (Frontend protocol)

**Version**: ChatKit Python SDK >= 1.4.0, ChatKit React >= latest

**Deviations**: None - full protocol compliance

---

## References

- [ChatKit Python Documentation](https://openai.github.io/chatkit-python/)
- [ChatKit JS Documentation](https://openai.github.io/chatkit-js/)
- [Server-Sent Events Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [OpenAI Platform ChatKit Guide](https://platform.openai.com/docs/guides/chatkit)
