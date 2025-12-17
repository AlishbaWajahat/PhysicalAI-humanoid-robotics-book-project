"""
Database models and operations for conversation history.
Uses Neon Serverless Postgres to store chat sessions and messages.
"""
import os
from datetime import datetime
from typing import List, Optional
import logging
from sqlalchemy import create_engine, Column, String, DateTime, Text, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import NullPool
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Database URL from environment
DATABASE_URL = os.getenv("NEON_DATABASE_URL")

# Create SQLAlchemy engine with connection pooling disabled for serverless
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Disable pooling for serverless Postgres
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class ChatSession(Base):
    """
    Represents a conversation session.
    Each user gets a unique session identified by session_id stored in localStorage.
    """
    __tablename__ = "chat_sessions"

    session_id = Column(String(255), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to messages
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ChatSession(session_id={self.session_id}, created_at={self.created_at})>"


class ChatMessage(Base):
    """
    Represents a single message in a conversation.
    Stores both user questions and assistant responses.
    """
    __tablename__ = "chat_messages"

    id = Column(String(255), primary_key=True)
    session_id = Column(String(255), ForeignKey("chat_sessions.session_id"), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)  # Optional highlighted text context
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to session
    session = relationship("ChatSession", back_populates="messages")

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, role={self.role}, session_id={self.session_id})>"


# Database operations
def init_database():
    """
    Initialize database tables.
    Creates tables if they don't exist.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def get_or_create_session(session_id: str) -> ChatSession:
    """
    Get existing session or create a new one.

    Args:
        session_id: Unique session identifier

    Returns:
        ChatSession object
    """
    db = SessionLocal()
    try:
        session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()

        if not session:
            session = ChatSession(session_id=session_id)
            db.add(session)
            db.commit()
            db.refresh(session)
            logger.info(f"Created new session: {session_id}")
        else:
            # Update last activity
            session.last_activity = datetime.utcnow()
            db.commit()

        return session
    except Exception as e:
        logger.error(f"Error in get_or_create_session: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def save_message(session_id: str, message_id: str, role: str, content: str, selected_text: Optional[str] = None):
    """
    Save a message to the database.

    Args:
        session_id: Session identifier
        message_id: Unique message identifier
        role: 'user' or 'assistant'
        content: Message content
        selected_text: Optional highlighted text context
    """
    db = SessionLocal()
    try:
        message = ChatMessage(
            id=message_id,
            session_id=session_id,
            role=role,
            content=content,
            selected_text=selected_text
        )
        db.add(message)
        db.commit()
        logger.info(f"Saved {role} message to session {session_id}")
    except Exception as e:
        logger.error(f"Error saving message: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_conversation_history(session_id: str, limit: int = 50) -> List[dict]:
    """
    Retrieve conversation history for a session.

    Args:
        session_id: Session identifier
        limit: Maximum number of messages to retrieve (default 50)

    Returns:
        List of message dictionaries with role, content, and timestamp
    """
    db = SessionLocal()
    try:
        messages = db.query(ChatMessage)\
            .filter(ChatMessage.session_id == session_id)\
            .order_by(ChatMessage.timestamp.asc())\
            .limit(limit)\
            .all()

        history = [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "selected_text": msg.selected_text,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]

        logger.info(f"Retrieved {len(history)} messages for session {session_id}")
        return history
    except Exception as e:
        logger.error(f"Error retrieving conversation history: {e}")
        return []
    finally:
        db.close()


def delete_session(session_id: str):
    """
    Delete a session and all its messages.

    Args:
        session_id: Session identifier
    """
    db = SessionLocal()
    try:
        session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if session:
            db.delete(session)
            db.commit()
            logger.info(f"Deleted session {session_id}")
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        db.rollback()
        raise
    finally:
        db.close()


# Health check function
def check_database_connection() -> bool:
    """
    Check if database connection is working.

    Returns:
        True if connection successful, False otherwise
    """
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False
