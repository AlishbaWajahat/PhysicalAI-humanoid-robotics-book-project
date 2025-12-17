# 🤖 RAG Chatbot - Complete Setup Guide

> **Production-ready RAG chatbot with OpenAI ChatKit, conversation history, and selected-text questioning**

Built with:
- ✅ **OpenAI ChatKit** - Beautiful, production-ready UI
- ✅ **Neon Serverless Postgres** - Conversation history persistence
- ✅ **Qdrant Cloud** - Vector database for book content
- ✅ **Cohere Embeddings** - Semantic search
- ✅ **Google Gemini** - LLM for responses
- ✅ **FastAPI** - High-performance backend
- ✅ **Selected-Text Support** - Ask questions about highlighted text

---

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.13+
- Node.js 20+
- Accounts on: Qdrant Cloud, Cohere, Google AI Studio, Neon

### Step 1: Get Your API Keys

1. **Qdrant Cloud**: https://cloud.qdrant.io/
   - Create a cluster → Copy URL and API key

2. **Cohere**: https://dashboard.cohere.com/api-keys
   - Sign up → Generate API key

3. **Google Gemini**: https://makersuite.google.com/app/apikey
   - Create project → Generate API key

4. **Neon Postgres**: https://console.neon.tech
   - Create project → Copy connection string

### Step 2: Configure Environment

```bash
# Navigate to backend directory
cd backend

# Copy example env file
cp .env.example .env

# Edit .env and fill in your API keys
# (Use your favorite editor)
```

### Step 3: Install Dependencies

```bash
# Backend dependencies (from project root)
cd backend
uv pip install -r requirements.txt
# Or: pip install sqlalchemy psycopg2-binary fastapi uvicorn openai-chatkit

# Frontend dependencies (from project root)
cd ..
npm install
```

### Step 4: Initialize Database

```bash
# Create database tables
cd backend
python -c "from database import init_database; init_database()"
```

### Step 5: Index Your Content (If not done already)

```bash
# Run the ingestion script to index your documentation
cd backend
python index_content.py
```

### Step 6: Start Servers

**Terminal 1 - Backend:**
```bash
cd backend
python chatkit_server.py
# Server running at: http://localhost:8001
```

**Terminal 2 - Frontend:**
```bash
npm start
# Docusaurus running at: http://localhost:3000
```

### Step 7: Test It Out! 🎉

1. Visit http://localhost:3000
2. Click the 💬 floating icon (bottom-right)
3. Ask: "What is inverse kinematics?"
4. **Try selected-text**: Highlight any text on the page → Click "Ask about this"

---

## ✨ Features

### 1. **Intelligent Q&A**
- Ask questions about your book content
- Answers are grounded in your documentation (no hallucinations)
- Streaming responses for better UX

### 2. **Selected-Text Questioning** 🔥
- Highlight any text on the page
- Click the "Ask about this" button
- The chatbot uses the selected text as context

### 3. **Conversation History**
- All conversations stored in Neon Postgres
- History persists across browser sessions
- Continue previous conversations anytime

### 4. **Beautiful UI**
- Modern, professional design
- Smooth animations
- Mobile-responsive
- Dark mode support

---

## 📁 Project Structure

```
backend/
├── chatkit_server.py       # Main ChatKit server with streaming
├── database.py             # SQLAlchemy models (sessions, messages)
├── agent/
│   └── rag_agent.py        # Existing RAG agent (DO NOT MODIFY)
├── tools/
│   └── agent_tools.py      # Qdrant retrieval tools
├── index_content.py        # Content ingestion script
├── .env                    # Your API keys (DO NOT COMMIT)
└── .env.example            # Template for environment variables

src/
├── components/
│   └── Chatkit-chatbot/
│       ├── index.jsx       # React component with selected-text
│       └── styles.module.css # Professional styling
└── theme/
    └── Root.js             # Docusaurus integration

docs/                       # Your documentation content (MDX files)
```

---

## 🗄️ Database Schema

**chat_sessions**
- `session_id` (PK) - Unique session identifier
- `created_at` - Session creation timestamp
- `last_activity` - Last message timestamp

**chat_messages**
- `id` (PK) - Message UUID
- `session_id` (FK) - References chat_sessions
- `role` - 'user' or 'assistant'
- `content` - Message text
- `selected_text` - Optional highlighted text context
- `timestamp` - Message creation time

---

## 🔧 Configuration

### Backend Environment Variables

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

### Frontend Configuration

The chatbot automatically connects to `http://localhost:8001/chatkit`.

To change the backend URL, edit `src/components/Chatkit-chatbot/index.jsx`:

```javascript
const chatkit = useChatKit({
  api: {
    url: 'https://your-production-backend.com/chatkit',
  },
  // ...
});
```

---

## 🚢 Deployment

### Option 1: Render (Recommended for Backend)

**Backend Deployment:**

1. Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: rag-chatbot-backend
    runtime: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && python chatkit_server.py
    envVars:
      - key: QDRANT_URL
        sync: false
      - key: QDRANT_API_KEY
        sync: false
      - key: COHERE_API_KEY
        sync: false
      - key: GEMINI_API_KEY
        sync: false
      - key: NEON_DATABASE_URL
        sync: false
      - key: CHATKIT_BACKEND_PORT
        value: 8001
```

2. Connect GitHub repo to Render
3. Add environment variables in Render dashboard
4. Deploy!

**Backend URL**: `https://your-app.onrender.com`

### Option 2: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy backend
cd backend
railway up

# Set environment variables in Railway dashboard
```

### Option 3: Vercel (Frontend Only)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
vercel deploy

# Production deployment
vercel --prod
```

**Important**: Update the backend URL in `src/components/Chatkit-chatbot/index.jsx` to your deployed backend.

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Chatbot icon appears on every page
- [ ] Clicking icon opens chat panel
- [ ] Can send messages and receive streaming responses
- [ ] Highlight text → "Ask about this" button appears
- [ ] Click button → chatbot opens with selected text context
- [ ] Close and reopen chat → conversation history persists
- [ ] Close browser and reopen → history still persists
- [ ] Multiple questions in sequence work correctly
- [ ] Backend health check: http://localhost:8001/health

### API Testing

**Health Check:**
```bash
curl http://localhost:8001/health
```

**Get Conversation History:**
```bash
curl http://localhost:8001/api/history/your-session-id
```

---

## 🐛 Troubleshooting

### Backend Issues

**Database connection fails:**
```bash
# Test database connection
python -c "from backend.database import check_database_connection; print(check_database_connection())"

# Check Neon Postgres status: https://console.neon.tech
```

**Qdrant connection fails:**
```bash
# Verify Qdrant URL and API key
# Check if cluster is running: https://cloud.qdrant.io/
```

**Import errors:**
```bash
# Reinstall dependencies
cd backend
uv pip install --force-reinstall -r requirements.txt
```

### Frontend Issues

**Chatbot doesn't appear:**
- Check browser console for errors
- Verify Root.js includes ChatkitChatbot component
- Clear browser cache

**Selected-text button doesn't appear:**
- Make sure you're highlighting at least a few words
- Check if selection is within the main content area
- Try different browsers

**Backend connection fails:**
- Verify backend is running: http://localhost:8001/health
- Check CORS configuration in chatkit_server.py
- Update API URL in index.jsx if using different port

---

## 📊 Monitoring

### Check Server Logs

```bash
# Backend logs
tail -f backend/chatkit_server.log

# Check for errors
grep ERROR backend/chatkit_server.log
```

### Database Queries

```sql
-- Count total sessions
SELECT COUNT(*) FROM chat_sessions;

-- Count messages by role
SELECT role, COUNT(*) FROM chat_messages GROUP BY role;

-- Recent conversations
SELECT session_id, COUNT(*) as message_count, MAX(timestamp) as last_message
FROM chat_messages
GROUP BY session_id
ORDER BY last_message DESC
LIMIT 10;
```

---

## 🔒 Security Considerations

1. **Never commit `.env` files**
   - Add to `.gitignore`
   - Use `.env.example` template

2. **Use environment variables in production**
   - Set via hosting platform dashboard
   - Never hardcode API keys

3. **Enable HTTPS in production**
   - Most hosting platforms provide this automatically

4. **Rate limiting** (Optional enhancement)
   - Add rate limiting middleware in FastAPI
   - Prevent abuse

---

## 🎨 Customization

### Change Colors

Edit `src/components/Chatkit-chatbot/styles.module.css`:

```css
.floatingIcon {
  background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

### Modify Welcome Message

Edit the chatbot instructions in `backend/agent/rag_agent.py`:

```python
book_rag_agent = Agent(
    name='Book RAG Assistant',
    instructions="""Your custom instructions here...""",
    tools=[retrieve_book_content]
)
```

### Change Position

Edit `src/components/Chatkit-chatbot/styles.module.css`:

```css
.floatingIcon {
  bottom: 24px;  /* Adjust vertical position */
  right: 24px;   /* Adjust horizontal position */
}
```

---

## 📈 Performance Optimization

### Database

- Add indexes on frequently queried columns
- Use connection pooling (already configured)
- Archive old conversations

### Backend

- Enable response caching for common questions
- Use async/await throughout (already implemented)
- Add CDN for static assets

### Frontend

- Lazy load chatbot component (already using BrowserOnly)
- Minimize bundle size
- Use React.memo for expensive components

---

## 🆘 Support & Resources

- **Qdrant Docs**: https://qdrant.tech/documentation/
- **Cohere Docs**: https://docs.cohere.com/
- **Neon Docs**: https://neon.tech/docs/introduction
- **ChatKit Docs**: https://github.com/openai/chatkit
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

## 🎉 You're All Set!

Your RAG chatbot is now fully functional with:
✅ Intelligent Q&A from your documentation
✅ Selected-text questioning
✅ Persistent conversation history
✅ Beautiful, production-ready UI
✅ Ready for deployment

**Next Steps:**
1. Customize the styling to match your brand
2. Deploy to production
3. Monitor usage and iterate

---

## 📝 License

This chatbot implementation is part of the PhysicalAI Humanoid Robotics Book project.

---

**Built with ❤️ using OpenAI ChatKit, Neon Postgres, Qdrant Cloud, and Cohere**
