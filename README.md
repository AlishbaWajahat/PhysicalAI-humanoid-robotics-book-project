# Humanoid Robotics Book

Interactive textbook on humanoid robotics built with [Docusaurus](https://docusaurus.io/), featuring an AI-powered RAG chatbot for enhanced learning.

## Features

- **AI Chatbot**: Ask questions about the book content and get answers with source citations
- **Text Selection Help**: Select any text and ask the AI to explain it
- **Smart Search**: Semantic search through book content with vector embeddings
- **Book Navigation**: Query book structure (parts, chapters, topics)
- **Persistent History**: Your last 5 conversations are saved locally

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## RAG Chatbot Backend

The AI chatbot requires a separate backend service. See [backend/README.md](backend/README.md) for setup instructions.

**Quick Start:**

```bash
# 1. Set up backend
cd backend
pip install -r requirements.txt
cp .env.example .env  # Configure your API keys

# 2. Index the book
python -m src.vector_store.indexer

# 3. Start API server
uvicorn src.api.main:app --reload --port 8000

# 4. Start frontend (in another terminal)
cd ..
yarn start
```

The chatbot will appear as a floating icon in the bottom-right corner of all pages.

For detailed documentation, see [specs/005-rag-chatbot/](specs/005-rag-chatbot/).
