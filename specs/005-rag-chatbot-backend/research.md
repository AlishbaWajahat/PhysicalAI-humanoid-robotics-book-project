# Research: RAG Chatbot Backend

## Overview
This document captures research findings for the RAG Chatbot Backend implementation, addressing unknowns identified in the Technical Context and exploring best practices for the technologies involved.

## Technology Research

### 1. OpenAI Agents SDK
- **Status**: Need to verify if OpenAI Agents SDK exists and is appropriate for this use case
- **Research Required**: Check official OpenAI documentation for 2025 agents framework
- **Alternative Considered**: LangChain, LlamaIndex, or custom implementation using OpenAI API directly
- **Decision**: Based on spec requirement, will use OpenAI Agents SDK if available, otherwise implement with OpenAI API directly

### 2. Qdrant Vector Database Integration
- **Library**: qdrant-client
- **Version**: Latest stable (as of 2025) - need to verify exact version
- **Usage**: For storing and retrieving vector embeddings of book content
- **Best Practices**:
  - Use batch operations for efficient embedding storage
  - Implement proper metadata schema for book content tracking
  - Use sparse and dense vector combinations if needed
  - Implement proper collection management for incremental updates

### 3. Cohere Embedding Model
- **Library**: cohere
- **Version**: Latest stable (as of 2025) - need to verify exact version
- **Model**: Recommended embedding model for text content (likely embed-multilingual-v3.0 or newer)
- **Best Practices**:
  - Batch requests for efficiency
  - Handle rate limiting appropriately
  - Cache embeddings to avoid reprocessing

### 4. MDX/Markdown Content Extraction
- **Library**: pydantic, pathlib, and built-in Python libraries for file operations
- **Approach**: Read MDX files from docs/ directory and extract text content
- **Consideration**: Need to handle JSX components in MDX appropriately while extracting text content
- **Decision**: Use simple text extraction focusing on content between JSX components

### 5. Functional Programming Approach
- **Implementation**: All modules will be implemented with pure functions
- **No OOP**: Avoid classes and objects as per specification
- **State Management**: Use explicit parameters and return values
- **Best Practices**: Immutable data structures, function composition

## Architecture Decisions

### 1. Two-Phase Implementation (As Specified)
- **Phase 1**: Data pipeline for content extraction, chunking, embedding, and vector storage
- **Phase 2**: Agent implementation that retrieves content and generates responses
- **Rationale**: Separates data concerns from AI interaction concerns

### 2. Environment Configuration
- **Library**: python-dotenv
- **Purpose**: Load API keys and configuration from .env file
- **Security**: Never commit .env files to version control

### 3. Error Handling Strategy
- **Approach**: Explicit error handling with appropriate fallbacks
- **Logging**: Use structured logging for debugging and monitoring
- **User Experience**: Graceful degradation when services are unavailable

## Dependencies and Versions

Based on the existing pyproject.toml and requirements:

- Python: 3.13 (from backend/.python-version)
- Required packages to research and add to pyproject.toml:
  - openai-agents SDK or openai
  - qdrant-client
  - cohere
  - python-dotenv
  - pydantic (for data validation)
  - pytest (for testing)
  - black (for formatting)
  - ruff (for linting)
  - mypy (for type checking)

## Data Flow Design

### Content Processing Pipeline
1. Extract text content from MDX files in docs/ folder
2. Chunk text into manageable segments (e.g., 512-1024 tokens)
3. Create embeddings using Cohere
4. Store embeddings in Qdrant with metadata
5. Enable incremental updates for new content

### Query Processing Pipeline
1. Receive user query
2. Generate embedding for query using Cohere
3. Retrieve top 5 most relevant chunks from Qdrant
4. Pass chunks to agent for response generation
5. Return response to user

## Risks and Mitigations

### 1. API Availability
- **Risk**: OpenAI Agents SDK may not exist as specified
- **Mitigation**: Prepare alternative implementation using OpenAI API directly

### 2. Rate Limiting
- **Risk**: Cohere and Qdrant APIs may have rate limits
- **Mitigation**: Implement proper retry logic and caching

### 3. Content Freshness
- **Risk**: Book content updates not reflected in vector store
- **Mitigation**: Implement incremental indexing with content hash checking

## Next Steps

1. Verify OpenAI Agents SDK availability and documentation
2. Set up proper dependency versions in pyproject.toml
3. Implement content extraction from docs/ folder
4. Create vector storage and retrieval functions
5. Build the RAG agent with Qdrant integration