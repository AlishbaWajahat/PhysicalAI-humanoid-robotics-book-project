"""
Data validation models for the RAG Chatbot Backend.
Defines the data structures used throughout the system based on data-model.md.
"""
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Union
from datetime import datetime
import uuid


class BookContent(BaseModel):
    """
    Represents extracted content from MDX files in the docs/ directory.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_path: str = Field(..., description="File path relative to docs/ directory")
    content: str = Field(..., description="The extracted text content")
    title: str = Field(default="", description="Title or heading from the document")
    metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Additional document metadata")

    @validator('source_path')
    def validate_source_path(cls, v):
        if not v.startswith('docs/'):
            raise ValueError('source_path must start with "docs/"')
        return v

    @validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError('content cannot be empty')
        return v


class TextChunk(BaseModel):
    """
    Represents a segmented portion of book content suitable for embedding.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_id: str = Field(..., description="Reference to the original BookContent.id")
    text: str = Field(..., description="The chunked text content")
    chunk_index: int = Field(..., ge=0, description="Position of this chunk within the original content")
    metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Chunk-specific metadata")

    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('text cannot be empty')
        return v

    @validator('chunk_index')
    def validate_chunk_index(cls, v):
        if v < 0:
            raise ValueError('chunk_index must be non-negative')
        return v


class Embedding(BaseModel):
    """
    Represents the vector embedding of a text chunk.
    """
    chunk_id: str = Field(..., description="Reference to TextChunk.id")
    vector: List[float] = Field(..., description="The embedding vector from Cohere")
    model_name: str = Field(..., description="Name of the embedding model used")
    model_version: str = Field(default="", description="Version of the embedding model")

    @validator('vector')
    def validate_vector(cls, v):
        if not v:
            raise ValueError('vector cannot be empty')
        if not all(isinstance(x, (int, float)) for x in v):
            raise ValueError('vector must contain only numeric values')
        return v


class VectorRecord(BaseModel):
    """
    Represents data stored in Qdrant vector database.
    """
    id: str = Field(..., description="Unique identifier (same as chunk_id)")
    vector: List[float] = Field(..., description="The embedding vector")
    payload: Dict[str, Union[str, int, float, bool, Dict]] = Field(default_factory=dict, description="Metadata including source_path, content, and additional context")
    collection_name: str = Field(default="humanoid_ai_book", description="Name of the Qdrant collection")

    @validator('id')
    def validate_id(cls, v):
        if not v:
            raise ValueError('id cannot be empty')
        return v

    @validator('vector')
    def validate_record_vector(cls, v):
        if not v:
            raise ValueError('vector cannot be empty')
        if not all(isinstance(x, (int, float)) for x in v):
            raise ValueError('vector must contain only numeric values')
        return v


class UserQuery(BaseModel):
    """
    Represents a query from the user to the RAG system.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str = Field(..., description="The user's question or query text")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the query was received")
    user_context: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Optional user-specific context")

    @validator('text')
    def validate_query_text(cls, v):
        if not v.strip():
            raise ValueError('query text cannot be empty')
        return v


class RetrievedChunk(BaseModel):
    """
    Represents relevant chunks retrieved from Qdrant for a query.
    """
    chunk_id: str = Field(..., description="ID of the retrieved chunk")
    text: str = Field(..., description="The content of the chunk")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Score indicating relevance to the query")
    source_path: str = Field(..., description="Path to the original document")
    metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Additional metadata from the vector record")

    @validator('relevance_score')
    def validate_relevance_score(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('relevance_score must be between 0 and 1')
        return v


class AgentResponse(BaseModel):
    """
    Represents the final response generated by the agent.
    """
    query_id: str = Field(..., description="Reference to the original UserQuery.id")
    response_text: str = Field(..., description="The agent's response to the user")
    source_chunks: List[str] = Field(default_factory=list, description="IDs of chunks used to generate the response")
    confidence: float = Field(ge=0.0, le=1.0, description="Agent's confidence in the response")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the response was generated")

    @validator('response_text')
    def validate_response_text(cls, v):
        if not v.strip():
            raise ValueError('response_text cannot be empty')
        return v

    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('confidence must be between 0 and 1')
        return v


class IndexingResult(BaseModel):
    """
    Represents the result of an indexing operation.
    """
    success: bool = Field(..., description="Whether the indexing operation was successful")
    indexed_count: int = Field(..., ge=0, description="Number of items successfully indexed")
    error_count: int = Field(..., ge=0, description="Number of items that failed to index")
    errors: List[str] = Field(default_factory=list, description="List of error messages for failed items")
    duration: float = Field(..., ge=0, description="Duration of the operation in seconds")


class AgentConfig(BaseModel):
    """
    Configuration for the RAG agent.
    """
    model_name: str = Field(default="gemini", description="Name of the LLM model to use")
    max_tokens: int = Field(default=1024, ge=1, le=4096, description="Maximum tokens for the response")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperature for response generation")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p sampling parameter")
    retrieve_top_k: int = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve for context")