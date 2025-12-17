"""
Production ChatKit Server for RAG Chatbot.
Integrates existing RAG agent with ChatKit-Python, conversation history, and selected-text support.
Follows official OpenAI ChatKit patterns with Store implementation and streaming responses.
"""
import os
import sys
import logging
import uuid
from typing import AsyncIterator, Optional
from datetime import datetime
import dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response, JSONResponse

# Add backend directory to path
sys.path.append(os.path.dirname(__file__))

# Load environment variables
dotenv.load_dotenv()

# Import ChatKit server components
from chatkit.server import (
    ChatKitServer,
    ThreadMetadata,
    ThreadItem,
    Page,
    UserMessageItem,
    AssistantMessageItem,
    ThreadStreamEvent,
    AssistantMessageContent,
    StreamingResult,
)
from chatkit.store import (
    Store,
    StoreItemType,
    default_generate_id,
    Attachment,
)

# Import existing RAG agent
from agent.rag_agent import book_rag_agent, config
from agents import Runner


# Import database operations
from database import (
    init_database,
    get_or_create_session,
    save_message,
    get_conversation_history,
    check_database_connection
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('chatkit_server.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="RAG Chatbot ChatKit Server")

# Add CORS middleware for Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Common alternative port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
database_available = False
try:
    init_database()
    database_available = check_database_connection()
    if database_available:
        logger.info("Database initialized and connected")
    else:
        logger.warning("Database connection failed - using in-memory mode")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    logger.warning("Running in fallback mode")


class RAGChatStore(Store[dict]):
    """
    Custom Store implementation for RAG chatbot with Neon Postgres persistence.
    Handles thread metadata, thread items (messages), and conversation history.
    """

    def __init__(self):
        # In-memory storage for threads and items
        self.threads: dict[str, ThreadMetadata] = {}
        self.thread_items: dict[str, list[ThreadItem]] = {}
        self.attachments: dict[str, Attachment] = {}

    def generate_thread_id(self, context: dict) -> str:
        """Generate unique thread ID."""
        return default_generate_id("thread")

    def generate_item_id(
        self, item_type: StoreItemType, thread: ThreadMetadata, context: dict
    ) -> str:
        """Generate unique item ID."""
        return default_generate_id(item_type)

    async def load_thread(self, thread_id: str, context: dict) -> ThreadMetadata:
        """Load thread metadata from storage."""
        if thread_id not in self.threads:
            # Create new thread with metadata
            metadata_dict = context.get("metadata", {})
            thread = ThreadMetadata(
                id=thread_id,
                created_at=datetime.utcnow(),
                metadata=metadata_dict
            )
            self.threads[thread_id] = thread

            # Create session in database
            if database_available:
                try:
                    session_id = thread.metadata.get("session_id", thread_id)
                    get_or_create_session(session_id)
                except Exception as e:
                    logger.error(f"Error creating session: {e}")
        else:
            # Update existing thread metadata with new context
            existing_thread = self.threads[thread_id]
            new_metadata = context.get("metadata", {})

            # Merge metadata: keep existing session_id, update selected_text
            if "selected_text" in new_metadata:
                existing_thread.metadata["selected_text"] = new_metadata["selected_text"]

        return self.threads[thread_id]

    async def save_thread(self, thread: ThreadMetadata, context: dict) -> None:
        """Save thread metadata to storage."""
        self.threads[thread.id] = thread

        # Update session in database
        if database_available:
            try:
                session_id = thread.metadata.get("session_id", thread.id)
                get_or_create_session(session_id)
            except Exception as e:
                logger.error(f"Error saving thread: {e}")

    async def load_thread_items(
        self,
        thread_id: str,
        after: Optional[str],
        limit: int,
        order: str,
        context: dict,
    ) -> Page[ThreadItem]:
        """Load thread items (messages) from storage."""
        items = self.thread_items.get(thread_id, [])

        # Apply ordering
        if order == "desc":
            items = sorted(items, key=lambda x: x.created_at, reverse=True)
        else:
            items = sorted(items, key=lambda x: x.created_at)

        # Apply after filter
        if after:
            items = [item for item in items if item.id > after]

        # Apply limit
        items = items[:limit]

        return Page(
            data=items,
            has_more=len(items) >= limit,
            first_id=items[0].id if items else None,
            last_id=items[-1].id if items else None,
        )

    async def load_threads(
        self,
        limit: int,
        after: Optional[str],
        order: str,
        context: dict,
    ) -> Page[ThreadMetadata]:
        """Load threads from storage."""
        threads = list(self.threads.values())

        if order == "desc":
            threads = sorted(threads, key=lambda x: x.created_at, reverse=True)
        else:
            threads = sorted(threads, key=lambda x: x.created_at)

        if after:
            threads = [t for t in threads if t.id > after]

        threads = threads[:limit]

        return Page(
            data=threads,
            has_more=len(threads) >= limit,
            first_id=threads[0].id if threads else None,
            last_id=threads[-1].id if threads else None,
        )

    async def add_thread_item(
        self, thread_id: str, item: ThreadItem, context: dict
    ) -> None:
        """Add a new item to a thread."""
        if thread_id not in self.thread_items:
            self.thread_items[thread_id] = []

        self.thread_items[thread_id].append(item)

        # Save to database
        if database_available and isinstance(item, (UserMessageItem, AssistantMessageItem)):
            try:
                thread = self.threads.get(thread_id)
                session_id = thread.metadata.get("session_id", thread_id) if thread else thread_id

                if isinstance(item, UserMessageItem):
                    selected_text = thread.metadata.get("selected_text", "") if thread else ""
                    content_text = self._extract_text_from_user_content(item.content)
                    save_message(session_id, item.id, "user", content_text, selected_text)
                elif isinstance(item, AssistantMessageItem):
                    content_text = self._extract_text_from_content(item.content)
                    save_message(session_id, item.id, "assistant", content_text)
            except Exception as e:
                logger.error(f"Error saving message to database: {e}")

    async def save_item(
        self, thread_id: str, item: ThreadItem, context: dict
    ) -> None:
        """Update an existing item in a thread."""
        if thread_id in self.thread_items:
            items = self.thread_items[thread_id]
            for i, existing_item in enumerate(items):
                if existing_item.id == item.id:
                    items[i] = item
                    break

    async def load_item(
        self, thread_id: str, item_id: str, context: dict
    ) -> ThreadItem:
        """Load a specific item from a thread."""
        items = self.thread_items.get(thread_id, [])
        for item in items:
            if item.id == item_id:
                return item
        raise ValueError(f"Item {item_id} not found in thread {thread_id}")

    async def delete_thread(self, thread_id: str, context: dict) -> None:
        """Delete a thread and all its items."""
        if thread_id in self.threads:
            del self.threads[thread_id]
        if thread_id in self.thread_items:
            del self.thread_items[thread_id]

        # Delete from database
        if database_available:
            try:
                from database import delete_session
                thread = self.threads.get(thread_id)
                session_id = thread.metadata.get("session_id", thread_id) if thread else thread_id
                delete_session(session_id)
            except Exception as e:
                logger.error(f"Error deleting thread from database: {e}")

    async def delete_thread_item(
        self, thread_id: str, item_id: str, context: dict
    ) -> None:
        """Delete a specific item from a thread."""
        if thread_id in self.thread_items:
            self.thread_items[thread_id] = [
                item for item in self.thread_items[thread_id] if item.id != item_id
            ]

    async def save_attachment(self, attachment: Attachment, context: dict) -> None:
        """Save an attachment."""
        self.attachments[attachment.id] = attachment

    async def load_attachment(
        self, attachment_id: str, context: dict
    ) -> Attachment:
        """Load an attachment."""
        if attachment_id not in self.attachments:
            raise ValueError(f"Attachment {attachment_id} not found")
        return self.attachments[attachment_id]

    async def delete_attachment(self, attachment_id: str, context: dict) -> None:
        """Delete an attachment."""
        if attachment_id in self.attachments:
            del self.attachments[attachment_id]

    def _extract_text_from_content(self, content: list[AssistantMessageContent]) -> str:
        """Extract text from assistant message content."""
        text_parts = []
        for part in content:
            if hasattr(part, 'text'):
                text_parts.append(part.text)
            elif isinstance(part, dict) and 'text' in part:
                text_parts.append(part['text'])
        return ' '.join(text_parts)

    def _extract_text_from_user_content(self, content) -> str:
        """Extract text from user message content (handles both list and string)."""
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            text_parts = []
            for part in content:
                if hasattr(part, 'text'):
                    text_parts.append(part.text)
                elif isinstance(part, dict) and 'text' in part:
                    text_parts.append(part['text'])
                elif isinstance(part, str):
                    text_parts.append(part)
            return ' '.join(text_parts)
        else:
            return str(content)
        

class RAGChatKitServer(ChatKitServer[dict]):

    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: Optional[UserMessageItem],
        context: dict,
    ) -> AsyncIterator[ThreadStreamEvent]:

        if not input_user_message:
            return

        # Get selected_text and session_id
        selected_text = context.get("metadata", {}).get("selected_text", "") if context else ""
        session_id = thread.metadata.get("session_id", thread.id) or thread.id

        try:
            # Extract user text
            user_text = self.store._extract_text_from_user_content(input_user_message.content)

            # Retrieve conversation history
            conversation_history = []
            if database_available:
                try:
                    history = get_conversation_history(session_id, limit=10)
                    conversation_history = [f"{msg['role'].capitalize()}: {msg['content']}" for msg in history]
                except Exception as e:
                    logger.error(f"Error retrieving history: {e}")

            # Build query
            parts = []
            if conversation_history:
                parts.append("Previous conversation:\n" + "\n".join(conversation_history[-10:]))
            if selected_text:
                parts.append(f'Selected text:\n"{selected_text}"')
            parts.append(f"Current question:\n{user_text}")
            enhanced_query = "\n\n".join(parts)

            # Run agent
            runner = Runner()
            run_result = await runner.run(
                starting_agent=book_rag_agent,
                input=enhanced_query,
                run_config=config
            )

            # Extract response
            response_text = str(run_result.final_output or run_result.output or run_result)

            # Create and yield assistant message
            from chatkit.server import ThreadItemAddedEvent
            assistant_msg = AssistantMessageItem(
                id=str(uuid.uuid4()),
                thread_id=thread.id,
                created_at=datetime.utcnow(),
                content=[AssistantMessageContent(text=response_text)],
            )
            yield ThreadItemAddedEvent(item=assistant_msg)

        except Exception as e:
            logger.error(f"Error in respond: {type(e).__name__}: {e}", exc_info=True)
            # Re-raise to let ChatKit server handle it
            raise






# Create store and server instances
store = RAGChatStore()
chatkit_server = RAGChatKitServer(store=store)


# ChatKit endpoint
@app.post("/chatkit")
async def chatkit_endpoint(request: Request) -> Response:
    """
    Main ChatKit endpoint that processes all chat requests.
    Handles both streaming and non-streaming responses.
    Extracts session_id and selected_text from custom headers.
    """
    try:
        # Extract custom headers for session and selected text
        session_id = request.headers.get('X-Session-Id', '')
        selected_text = request.headers.get('X-Selected-Text', '')

        # Build context with metadata
        context = {
            "request": request,
            "metadata": {
                "session_id": session_id,
                "selected_text": selected_text,
            }
        }

        payload = await request.body()
        result = await chatkit_server.process(payload, context)

        if isinstance(result, StreamingResult):
            return StreamingResponse(result, media_type="text/event-stream")
        else:
            return Response(content=result.json, media_type="application/json")
    except Exception as e:
        logger.error(f"ChatKit error: {type(e).__name__}: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "type": type(e).__name__}
        )


@app.get("/health")
async def health_check():
    """Health check endpoint with database status."""
    db_status = "connected" if check_database_connection() else "disconnected"
    return {
        "status": "healthy",
        "service": "RAG Chatbot with ChatKit",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/history/{session_id}")
async def get_history(session_id: str, limit: int = 50):
    """
    Retrieve conversation history for a session.

    Args:
        session_id: Session identifier
        limit: Maximum number of messages to retrieve

    Returns:
        List of messages with role, content, and timestamp
    """
    if not database_available:
        return {"error": "Database unavailable", "messages": []}

    try:
        history = get_conversation_history(session_id, limit=limit)
        return {"session_id": session_id, "messages": history, "count": len(history)}
    except Exception as e:
        logger.error(f"Error retrieving history for {session_id}: {e}")
        return {"error": str(e), "messages": []}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("CHATKIT_BACKEND_PORT", "8001"))
    print("=" * 70)
    print("RAG Chatbot Backend with OpenAI ChatKit")
    print("=" * 70)
    print(f"Server port: {port}")
    print(f"Database: {'Connected' if database_available else 'Fallback mode'}")
    print(f"Health check: http://localhost:{port}/health")
    print(f"ChatKit endpoint: http://localhost:{port}/chatkit")
    print(f"History API: http://localhost:{port}/api/history/{{session_id}}")
    print("=" * 70)

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
