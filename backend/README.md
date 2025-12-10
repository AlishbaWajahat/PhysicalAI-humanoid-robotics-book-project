# RAG Chatbot Backend

This backend implements a Retrieval-Augmented Generation (RAG) chatbot that answers user questions based only on the content from the Physical AI & Humanoid Robotics book.

## Overview

The system extracts book content from the `docs/` directory, chunks and embeds it into a Qdrant vector database, then uses an AI agent to answer user questions based only on the book content.

## Features

- Extracts content from MDX files in the docs/ directory
- Chunks and embeds content using Cohere embeddings
- Stores vectors in Qdrant vector database with metadata
- Implements an agent that retrieves relevant content and generates responses
- Ensures responses are based only on book content, not external knowledge
- Provides concise, beginner-friendly answers by default

## Architecture

The system follows a hybrid approach with:

- `index_content.py`: Single script for the complete indexing pipeline (extraction, chunking, embedding, storage)
- `rag_agent.py`: RAG agent with Qdrant retrieval tool
- `main.py`: Entry point to orchestrate indexing or agent functionality
- `src/utils/`: Shared utilities for configuration and logging

## Setup

1. Install dependencies: `poetry install` or `pip install -r requirements.txt`
2. Configure environment variables in `.env` file (see `.env.example`)
3. Run initial indexing: `python index_content.py`
4. Start the agent: `python rag_agent.py`

## Environment Variables

- `QDRANT_API_KEY`: API key for Qdrant vector database
- `QDRANT_URL`: URL endpoint for Qdrant database
- `COHERE_API_KEY`: API key for Cohere embedding service
- `GEMINI_API_KEY`: API key for Gemini model (used via OpenAI Chat Completions API)

## Usage

### Indexing Content

To extract, chunk, embed, and store book content:

```bash
python index_content.py
```

### Running the Agent

To start the RAG agent:

```bash
python rag_agent.py
```

## Dependencies

- Python 3.13+
- Qdrant vector database
- Cohere API for embeddings
- Gemini model via OpenAI API
- openai-agents SDK

## Development

This project follows functional programming principles with no OOP, clean, readable code, and beginner-friendly responses.