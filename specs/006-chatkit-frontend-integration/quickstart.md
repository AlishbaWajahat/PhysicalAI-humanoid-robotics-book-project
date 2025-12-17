# Quickstart: ChatKit Frontend Integration

**Feature**: 006-chatkit-frontend-integration
**Date**: 2025-12-13
**Estimated Time**: 30-45 minutes

## Prerequisites

Before starting, ensure you have:

1. **Existing RAG Backend** (from feature 005-rag-chatbot-backend):
   - ✅ `backend/rag_agent.py` with working RAG agent
   - ✅ `backend/index_content.py` with indexed book content in Qdrant
   - ✅ `.env` file with `OPENAI_API_KEY`, `QDRANT_URL`, `COHERE_API_KEY`

2. **Development Environment**:
   - ✅ Python 3.13+ installed
   - ✅ Node.js 18+ and npm installed
   - ✅ Docusaurus site running (from features 001-003)

3. **Tool Access**:
   - ✅ Terminal/command line
   - ✅ Code editor
   - ✅ Web browser

---

## Phase 1: Backend Setup (15 minutes)

### Step 1.1: Install Dependencies

```bash
cd backend
pip install openai-chatkit>=1.4.0 fastapi>=0.115.0 uvicorn[standard]>=0.34.0
```

**Verify installation**:
```bash
python -c "import chatkit; print(chatkit.__version__)"
```

Expected output: `1.4.0` (or higher)

---

### Step 1.2: Create ChatKit Server

Create `backend/chatkit_server.py`:

```python
"""
ChatKit server that bridges frontend to existing RAG agent.
Implements streaming responses via ChatKit protocol.
"""

import os
import asyncio
from typing import AsyncGenerator
from chatkit import ChatKitServer, TextDelta, ErrorEvent
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import existing RAG agent
from rag_agent import get_agent, run_agent_query

# Initialize FastAPI
app = FastAPI(title="ChatKit RAG Server")

# CORS for Docusaurus dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ChatKit respond handler
async def respond(thread, message) -> AsyncGenerator:
    """
    Handle incoming chat messages and stream responses.

    Args:
        thread: ChatKit Thread object
        message: User message from frontend

    Yields:
        TextDelta events for streaming response
    """
    try:
        # Get RAG agent (existing implementation)
        agent = get_agent()

        # Query agent with user message
        response = await run_agent_query(agent, message.content)

        # Stream response word-by-word
        words = response.split()
        for word in words:
            yield TextDelta(delta=word + " ")
            await asyncio.sleep(0.05)  # Small delay for smooth streaming

    except Exception as e:
        # Log error and yield error event to frontend
        print(f"Error processing message: {e}")
        yield ErrorEvent(
            message="Sorry, I encountered an error processing your question.",
            code="server_error"
        )

# Create ChatKit server
chatkit_server = ChatKitServer(respond=respond)

# Mount ChatKit endpoint
app.mount("/chatkit", chatkit_server.app())

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("CHATKIT_BACKEND_PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**Note**: Adjust imports based on your actual `rag_agent.py` structure.

---

### Step 1.3: Update Environment Variables

Add to `backend/.env`:

```bash
# ChatKit Backend
CHATKIT_BACKEND_PORT=8001
CHATKIT_MAX_MESSAGE_LENGTH=10000
```

---

### Step 1.4: Test Backend

Start the ChatKit server:

```bash
python chatkit_server.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

Test health check in browser: http://localhost:8001/health

Expected: `{"status":"healthy"}`

**Keep this terminal running** - the backend server must stay active.

---

## Phase 2: Frontend Setup (15 minutes)

### Step 2.1: Install Dependencies

Open a new terminal:

```bash
cd <project-root>  # Where package.json is
npm install @openai/chatkit-react
```

**Verify installation**:
```bash
npm list @openai/chatkit-react
```

---

### Step 2.2: Create Chatbot Component

Create `src/components/Chatbot/index.jsx`:

```jsx
/**
 * ChatKit-based chatbot component for RAG Q&A.
 * Floating icon + expandable panel.
 */

import React, { useState } from 'react';
import { useChatKit, ChatKit } from '@openai/chatkit-react';
import styles from './styles.module.css';

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);

  // Initialize ChatKit with backend URL
  const { control } = useChatKit({
    api: {
      url: process.env.CHATKIT_BACKEND_URL || 'http://localhost:8001/chatkit'
    }
  });

  return (
    <div className={styles.chatbotContainer}>
      {/* Floating chatbot icon */}
      {!isOpen && (
        <button
          className={styles.floatingIcon}
          onClick={() => setIsOpen(true)}
          aria-label="Open chatbot"
        >
          💬
        </button>
      )}

      {/* Chatbot panel */}
      {isOpen && (
        <div className={styles.chatPanel}>
          <div className={styles.chatHeader}>
            <h3>Ask about the book</h3>
            <button
              className={styles.closeButton}
              onClick={() => setIsOpen(false)}
              aria-label="Close chatbot"
            >
              ×
            </button>
          </div>
          <ChatKit
            control={control}
            className={styles.chatKit}
          />
        </div>
      )}
    </div>
  );
}
```

---

### Step 2.3: Create Styles

Create `src/components/Chatbot/styles.module.css`:

```css
.chatbotContainer {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.floatingIcon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #0066cc;
  color: white;
  font-size: 24px;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s;
}

.floatingIcon:hover {
  transform: scale(1.1);
}

.chatPanel {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 380px;
  height: 600px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chatHeader {
  padding: 16px;
  background: #0066cc;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chatHeader h3 {
  margin: 0;
  font-size: 18px;
}

.closeButton {
  background: none;
  border: none;
  color: white;
  font-size: 32px;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  line-height: 1;
}

.chatKit {
  flex: 1;
  overflow: hidden;
}
```

---

### Step 2.4: Integrate into Docusaurus

Edit `docusaurus.config.js` to add the backend URL:

```javascript
// Add to customFields section
module.exports = {
  // ... other config
  customFields: {
    CHATKIT_BACKEND_URL: process.env.CHATKIT_BACKEND_URL || 'http://localhost:8001/chatkit',
  },
  // ... rest of config
};
```

Edit your theme or root component to include the Chatbot. For example, in `src/theme/Root.js`:

```jsx
import React from 'react';
import Chatbot from '@site/src/components/Chatbot';

export default function Root({children}) {
  return (
    <>
      {children}
      <Chatbot />
    </>
  );
}
```

**Note**: Create `src/theme/Root.js` if it doesn't exist (this is a Docusaurus theme swizzle point).

---

### Step 2.5: Test Frontend

Start Docusaurus dev server (new terminal if needed):

```bash
npm start
```

Expected: Browser opens to `http://localhost:3000`

1. **Verify chatbot icon** appears in bottom-right corner
2. **Click icon** - chat panel should open
3. **Type a question** - e.g., "What is inverse kinematics?"
4. **Observe streaming response** - text should appear word-by-word

---

## Phase 3: Verification (10 minutes)

### Test Cases

#### Test 1: Basic Q&A
- **Action**: Ask "What is forward kinematics?"
- **Expected**: Relevant answer from book content, streaming display
- **Pass Criteria**: Response appears within 5 seconds, no errors

#### Test 2: Session Persistence
- **Action**: Ask question, close panel, reopen panel
- **Expected**: Previous conversation still visible
- **Pass Criteria**: Chat history persists in current session

#### Test 3: Error Handling
- **Action**: Stop backend server, try to send message
- **Expected**: Error message in UI
- **Pass Criteria**: "Cannot connect" or similar message shown

#### Test 4: Multiple Messages
- **Action**: Send 5 different questions in sequence
- **Expected**: All answered correctly, conversation flows naturally
- **Pass Criteria**: No performance degradation or UI glitches

---

### Troubleshooting

**Issue**: "Cannot connect to chat server"
- **Solution**: Verify backend is running on http://localhost:8001
- **Check**: `curl http://localhost:8001/health` returns `{"status":"healthy"}`

**Issue**: Chatbot icon not visible
- **Solution**: Check browser console for errors
- **Solution**: Verify `src/theme/Root.js` imports Chatbot component

**Issue**: Responses not streaming
- **Solution**: Check `chatkit_server.py` yields `TextDelta` events
- **Solution**: Verify `asyncio.sleep()` is present between deltas

**Issue**: Empty responses
- **Solution**: Verify RAG agent is working: `python -c "from rag_agent import get_agent, run_agent_query; ...""`
- **Solution**: Check Qdrant has indexed content

---

## Next Steps

After successful quickstart:

1. **Production Deployment** (`/sp.tasks` will cover):
   - Configure production CORS origins
   - Add error monitoring and logging
   - Set up proper environment variable management
   - Deploy backend and frontend

2. **Optional Enhancements** (beyond current scope):
   - Add authentication
   - Persist conversation history (database)
   - Add typing indicators
   - Customize ChatKit UI theme

3. **Monitoring**:
   - Monitor backend logs for errors
   - Track response times (target < 5 seconds)
   - Monitor Qdrant query performance

---

## Summary

You now have:
- ✅ ChatKit-Python server bridging frontend to RAG agent
- ✅ ChatKit-JS component embedded in Docusaurus
- ✅ Streaming responses from book content
- ✅ Floating chatbot UI with clean design

**Time invested**: ~30-45 minutes
**Lines of code**: ~150 (backend + frontend)
**Dependencies added**: 4 (chatkit libs + fastapi + uvicorn)

Proceed to `/sp.tasks` for detailed implementation tasks and testing.
