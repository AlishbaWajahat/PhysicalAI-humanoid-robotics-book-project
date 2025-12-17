# 🚀 RAG Chatbot Quick Start Guide

Your RAG chatbot is now properly implemented using **OpenAI ChatKit**! Follow these steps to get it running.

## ✅ What's Been Fixed

- ✓ Proper ChatKit Python SDK implementation with `Store` class
- ✓ RAG agent integration with streaming responses
- ✓ Neon Postgres conversation history persistence
- ✓ Selected-text questioning support
- ✓ FastAPI backend with `/chatkit` endpoint
- ✓ React frontend with ChatKit-JS components

## 🏃 Quick Start (3 Steps)

### Step 1: Start the Backend

```bash
cd backend
python chatkit_server.py
```

You should see:
```
🚀 RAG Chatbot Backend with OpenAI ChatKit
📍 Server port: 8001
💾 Database: ✓ Connected
🏥 Health check: http://localhost:8001/health
💬 ChatKit endpoint: http://localhost:8001/chatkit
```

### Step 2: Start the Frontend

In a new terminal:

```bash
npm install  # If not already done
npm start
```

Docusaurus will start at: `http://localhost:3000`

### Step 3: Test the Chatbot!

1. Open `http://localhost:3000` in your browser
2. Click the 💬 floating chatbot icon (bottom-right)
3. Ask: **"What is inverse kinematics?"**
4. Try selected-text: Highlight any text on the page → Click "Ask about this"

## 🔧 Troubleshooting

### Backend won't start?

**Check dependencies:**
```bash
cd backend
pip list | grep -E "(chatkit|fastapi|sqlalchemy|agents)"
```

**Should see:**
- `openai-chatkit` (1.4.0+)
- `fastapi` (0.124.4+)
- `sqlalchemy` (2.0+)
- `openai-agents` (0.1.0+)

**Missing packages?**
```bash
pip install fastapi uvicorn openai-chatkit sqlalchemy psycopg2-binary
```

### Frontend issues?

**Check ChatKit React package:**
```bash
npm list @openai/chatkit-react
```

**Should see:**
- `@openai/chatkit-react@1.3.0` (or higher)

**Not installed?**
```bash
npm install @openai/chatkit-react
```

### Database connection failed?

The chatbot will still work in "fallback mode" (in-memory sessions only). Check your `.env` file:

```bash
cat backend/.env | grep NEON_DATABASE_URL
```

Make sure the connection string is valid.

### Test endpoints manually:

**Health check:**
```bash
curl http://localhost:8001/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "RAG Chatbot with ChatKit",
  "database": "connected",
  "timestamp": "2025-12-16T..."
}
```

## 📚 Architecture Overview

```
┌─────────────────────────────────────────┐
│  Frontend (Docusaurus + React)          │
│  - src/components/Chatkit-chatbot/      │
│  - src/theme/Root.js                    │
└────────────┬────────────────────────────┘
             │ HTTP/SSE
             ↓
┌─────────────────────────────────────────┐
│  Backend (FastAPI + ChatKit Server)     │
│  - backend/chatkit_server.py            │
│    ├── RAGChatStore (persistence)       │
│    └── RAGChatKitServer (respond)       │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┐
    ↓                 ↓
┌─────────┐    ┌──────────────┐
│  RAG    │    │ Neon Postgres│
│  Agent  │    │ (history)    │
│ (Qdrant │    └──────────────┘
│ +Cohere)│
└─────────┘
```

## 🎯 Features

### 1. Intelligent Q&A
Ask questions about your documentation and get contextual answers from the indexed content.

**Example:**
```
User: "What is forward kinematics?"
Bot: [Retrieves relevant content from Qdrant and generates answer]
```

### 2. Selected-Text Questioning 🔥
Highlight any text on the documentation page and ask questions about it!

**How it works:**
1. Highlight text on any page
2. Click "💡 Ask about this" button
3. Chatbot opens with the text as context
4. Ask your question

### 3. Conversation History
All conversations are persisted to Neon Postgres and available across sessions.

### 4. Streaming Responses
Responses stream in real-time for better UX.

## 🔑 Environment Variables

Your `backend/.env` should have:

```env
# Vector Database
QDRANT_URL="https://your-cluster.qdrant.cloud"
QDRANT_API_KEY="your-key"

# Embeddings
COHERE_API_KEY="your-key"

# LLM
GEMINI_API_KEY="your-key"

# Database
NEON_DATABASE_URL="postgresql://user:pass@host/db?sslmode=require"

# Server
CHATKIT_BACKEND_PORT=8001
```

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with DB status |
| `/chatkit` | POST | Main ChatKit endpoint (handles all chat) |
| `/api/history/{session_id}` | GET | Retrieve conversation history |

## 🎨 Customization

### Change Chatbot Colors

Edit `src/components/Chatkit-chatbot/styles.module.css`:

```css
.floatingIcon {
  background: linear-gradient(135deg, #YOUR_COLOR_1, #YOUR_COLOR_2);
}
```

### Modify Welcome Message

Edit the agent instructions in `backend/agent/rag_agent.py`:

```python
book_rag_agent = Agent(
    name='Book RAG Assistant',
    instructions="""Your custom instructions here...""",
    tools=[retrieve_book_content]
)
```

## 🐛 Common Issues

### "TypeError: Can't instantiate abstract class ChatKitServer"
**Fixed!** This was the main issue. The new implementation properly extends `ChatKitServer` with the `respond` method.

### "ImportError: cannot import name 'Attachment'"
**Fixed!** `Attachment` is imported from `chatkit.store`, not `chatkit.server`.

### Chatbot icon doesn't appear
1. Check browser console for errors
2. Verify `src/theme/Root.js` includes `ChatkitChatbot`
3. Clear browser cache

### Backend returns 500 errors
Check the logs:
```bash
tail -f backend/chatkit_server.log
```

## 🎉 You're All Set!

Your RAG chatbot is production-ready with:
- ✅ OpenAI ChatKit integration
- ✅ RAG-powered responses
- ✅ Conversation history persistence
- ✅ Selected-text questioning
- ✅ Beautiful, responsive UI

**Questions?** Check the logs or refer to:
- [ChatKit Python Docs](https://openai.github.io/chatkit-python/)
- [ChatKit JS Docs](https://openai.github.io/chatkit-js/)
- `CHATBOT_README.md` for detailed setup

**Happy chatting! 💬✨**
