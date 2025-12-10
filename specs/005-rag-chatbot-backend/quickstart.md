# Quickstart Guide: RAG Chatbot Backend

**Feature**: 005-rag-chatbot-backend
**Date**: 2025-12-10
**Input**: Feature specification from `/specs/005-rag-chatbot-backend/spec.md`

## Overview

This guide provides instructions for setting up and running the RAG Chatbot Backend that extracts book content from docs/, stores it in Qdrant vector database, and enables question-answering based on the book content.

## Prerequisites

- Python 3.13 (as specified in `.python-version`)
- pip package manager
- Access to Cohere API for embeddings
- Access to Qdrant vector database (cloud or local)
- Access to OpenAI API for the agent functionality

## Setup Instructions

### 1. Clone and Navigate to Backend Directory

```bash
cd backend/
```

### 2. Install Dependencies

```bash
pip install poetry
poetry install
```

Or if using pip directly:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Ensure the `.env` file exists in the backend directory with the following variables:

```env
QDRANT_API_KEY="your-qdrant-api-key"
QDRANT_URL="your-qdrant-url"
COHERE_API_KEY="your-cohere-api-key"
GEMINI_API_KEY="your-gemini-api-key"  # for the agent using Gemini via OpenAI Chat Completions API
```

Note: The .env file should already exist in the backend directory.

### 4. Run Initial Content Indexing

To extract content from docs/ directory and store it in Qdrant:

```bash
python index_content.py
```

This will:
1. Extract text content from all MDX files in docs/
2. Chunk the content into appropriate segments
3. Generate embeddings using Cohere
4. Store the vectors in Qdrant with proper metadata

### 5. Start the RAG Agent

To start the chatbot agent that can answer questions from the indexed content:

```bash
python rag_agent.py
```

## Usage Examples

### Indexing Content

```bash
# Index all content from docs/ directory
python index_content.py

# Index with specific options (if implemented)
python index_content.py --docs-path /path/to/docs --collection-name my_collection
```

### Running the Agent

```bash
# Start the RAG agent
python rag_agent.py

# The agent will prompt for questions and respond based only on book content
```

## Key Components

### 1. Content Indexing (`index_content.py`)
- `extract_content()`: Extracts text from MDX files in docs/
- `chunk_text()`: Segments content into appropriate chunks
- `generate_embeddings()`: Creates vector embeddings using Cohere
- `store_in_qdrant()`: Stores vectors with metadata in Qdrant

### 2. RAG Agent (`rag_agent.py`)
- Implements the agent using OpenAI agents SDK
- Uses Qdrant retrieval tool to access vector database
- Responds to questions based only on book content
- Provides concise answers by default

### 3. Configuration (`src/utils/config.py`)
- Loads environment variables securely
- Provides configuration for API endpoints and keys

## Environment Configuration

The system uses the following environment variables:

- `QDRANT_API_KEY`: API key for Qdrant vector database
- `QDRANT_URL`: URL endpoint for Qdrant database
- `COHERE_API_KEY`: API key for Cohere embedding service
- `GEMINI_API_KEY`: API key for Gemini model (used via OpenAI Chat Completions API)

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all required API keys are properly set in `.env`
2. **Qdrant Connection**: Verify QDRANT_URL and QDRANT_API_KEY are correct
3. **Embedding Issues**: Check COHERE_API_KEY is valid and has sufficient quota

### Verification Steps

1. Verify environment variables are loaded:
   ```bash
   python -c "from src.utils.config import get_config; print(get_config())"
   ```

2. Test Qdrant connection:
   ```bash
   python -c "from backend.src.utils.config import *; # test connection"
   ```

## Next Steps

After successful setup:
1. Verify content has been indexed by checking your Qdrant collection
2. Test the RAG agent with sample questions about your book content
3. Review and adjust chunking parameters for optimal retrieval
4. Monitor API usage for Cohere and Qdrant services