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
- Supports content search functionality
- Includes book metadata access (chapters, parts, summaries)
- Implements incremental indexing for new content
- Includes performance monitoring and error handling

## Architecture

The system follows a hybrid approach with:

- `index_content.py`: Single script for the complete indexing pipeline (extraction, chunking, embedding, storage)
- `rag_agent.py`: RAG agent with Qdrant retrieval tool
- `main.py`: Entry point to orchestrate indexing or agent functionality
- `src/utils/`: Shared utilities for configuration and logging

## Setup

1. Install dependencies: `poetry install` or `pip install -r requirements.txt`
2. Configure environment variables in `.env` file (see `.env.example`)
3. Run initial indexing: `python main.py index`
4. Start the agent: `python main.py agent`

## Environment Variables

- `QDRANT_API_KEY`: API key for Qdrant vector database
- `QDRANT_URL`: URL endpoint for Qdrant database
- `COHERE_API_KEY`: API key for Cohere embedding service
- `GEMINI_API_KEY`: API key for Gemini model (used via OpenAI Chat Completions API)
- `CHUNK_SIZE`: Size of text chunks (default: 512)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)
- `TOP_K_RETRIEVAL`: Number of results to retrieve (default: 5)

## Usage

### Complete Workflow

To run indexing followed by the agent:

```bash
python main.py both
```

### Indexing Content

To extract, chunk, embed, and store book content:

```bash
python main.py index
```

For incremental indexing (only process new/updated documents):

```bash
python main.py index --incremental
```

### Running the Agent

To start the RAG agent for Q&A:

```bash
python main.py agent
```

### Running Search Mode

To search for specific content in the book:

```bash
python main.py search
```

### Usage Examples

#### Question Answering
```
> Your question: What is the primary purpose of the nervous system in humanoid robots?
> Answer: The nervous system in humanoid robots serves as the communication network that connects sensors, actuators, and processing units, enabling coordinated movement and response to environmental stimuli. It mimics biological nervous systems by transmitting signals between different components of the robot.
```

#### Content Search
```
> Search query: neural networks
> Found 3 relevant sections:

1. Neural Network Fundamentals - docs/part1-basics/neural_networks.md
   Relevance: 0.87
   Preview: Neural networks form the basis of machine learning in humanoid robotics...

2. Implementing Neural Control - docs/part2-advanced/neural_control.md
   Relevance: 0.79
   Preview: In humanoid robotics, neural networks are used to control complex movements...

3. Deep Learning Applications - docs/part3-applications/deep_learning.md
   Relevance: 0.72
   Preview: Deep learning neural networks have revolutionized how humanoid robots process...
```

#### Metadata Queries
```
> Your question: What chapters are in this book?
> Answer: The book contains the following chapters:
> 1. Introduction to Humanoid Robotics
> 2. Basic Components and Design
> 3. Sensor Integration
> 4. Actuator Systems
> 5. Control Systems
> 6. Advanced Topics
>
> You can find more detailed information about each chapter by asking specific questions.
```

## Dependencies

- Python 3.13+
- Qdrant vector database
- Cohere API for embeddings
- Gemini model via OpenAI API
- openai-agents SDK
- python-dotenv for environment management

## Development

This project follows functional programming principles with no OOP, clean, readable code, and beginner-friendly responses.

## Error Handling

The system includes comprehensive error handling for:
- Qdrant connection issues
- Invalid configuration values
- Performance monitoring (responses under 5 seconds)
- API key validation

## Performance

- Response times are monitored and logged
- Target response time: <5 seconds
- Performance warnings are logged if thresholds are exceeded