# Feature Specification: RAG Chatbot Backend

**Feature Branch**: `005-rag-chatbot-backend`
**Created**: 2025-12-10
**Status**: Draft
**Input**: User description: "Write a full spec.md for my backend project with the following requirements:

🎯 Project Goal

Build the backend of an Integrated RAG Chatbot that answers user questions only from my book's content.
The system will:

Extract book content from the docs/ folder

Chunk → embed → store into Qdrant vector database

Build an agent that retrieves the most relevant chunks and generates responses

Support questions about the book, selected text, and metadata (parts, chapters, summaries)

Use openai-agents SDK for the backend

Frontend later will be built with chatkit-js, backend uses chatkit-python, so no FastAPI is needed.

🧱 Tech Stack

Backend: openai-agents SDK

Vector DB: Qdrant

Embedding model: Cohere

LLM model: Gemini model (via OpenAI Chat Completions API → use best free Gemini model)

Context7 MCP server: must be used to fetch latest documentation when needed

Environment: load all secrets from .env

No OOP — use simple, clean, functional code

📦 Data Workflow Requirements

Include detailed steps for:

Extracting book text from docs/

Chunking text

Creating embeddings using Cohere embeddings

Storing vectors in Qdrant

Supporting incremental indexing for future new book files

Querying Qdrant to retrieve top 5 most relevant chunks

Passing retrieved chunks into the agent for answering

🤖 Agent Requirements

Specify that the agent must:

Use Gemini model via OpenAI

Use a retrieve tool built around Qdrant search

Be strictly instructed to answer only from book content

Provide short, concise answers by default, unless user asks for details

Be beginner-friendly and helpful

Be able to answer:

factual questions from the book

search queries

metadata questions (parts list, chapters, chapter count, URLs, summaries)

📘 Additional Constraints

Code must be simple, readable, and breathable

Avoid OOP entirely

Use context7 MCP server to fetch latest docs instead of relying on internal knowledge

Ask clarifying questions whenever something is missing

✏️ What the output should be

Ge"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Book Question Answering (Priority: P1)

As a reader of the book, I want to ask questions about the book content and receive accurate answers based only on the book material, so that I can quickly find information without having to search through the entire book manually.

**Why this priority**: This is the core functionality that delivers the primary value of the RAG chatbot - enabling users to get answers from book content efficiently.

**Independent Test**: Can be fully tested by asking various questions about book content and verifying that responses are accurate and sourced from the book material.

**Acceptance Scenarios**:

1. **Given** the RAG chatbot is initialized with book content, **When** a user asks a factual question about the book, **Then** the system returns an accurate answer based only on the book content
2. **Given** the user asks a question not covered in the book, **When** the system processes the query, **Then** the system responds that the information is not available in the book content
3. **Given** the user asks a complex question requiring multiple book sections, **When** the system processes the query, **Then** the system synthesizes information from multiple relevant book sections to form a coherent response

---

### User Story 2 - Book Content Search (Priority: P2)

As a reader, I want to search for specific content or topics within the book, so that I can locate relevant sections quickly.

**Why this priority**: This enhances the user experience by providing search capabilities beyond simple Q&A.

**Independent Test**: Can be tested by entering search queries and verifying that the system returns relevant book sections or chapters.

**Acceptance Scenarios**:

1. **Given** the user enters a search query, **When** the system processes the query against book content, **Then** the system returns the most relevant book sections matching the query
2. **Given** the user searches for a specific term, **When** the system searches the book content, **Then** the system returns all relevant mentions of that term with context

---

### User Story 3 - Book Metadata Access (Priority: P3)

As a user, I want to ask about the book's structure (chapters, parts, summaries) to understand the organization and navigate the content better.

**Why this priority**: This provides auxiliary functionality that helps users understand the book structure and find content more effectively.

**Independent Test**: Can be tested by asking metadata questions and verifying that the system provides accurate information about book structure.

**Acceptance Scenarios**:

1. **Given** the user asks about book chapters or parts, **When** the system processes the query, **Then** the system returns the correct list of chapters/parts from the book
2. **Given** the user asks for a summary of a specific chapter, **When** the system processes the request, **Then** the system returns the appropriate chapter summary if available

---

### Edge Cases

- What happens when the book content is updated or new chapters are added?
- How does the system handle ambiguous questions that could refer to multiple parts of the book?
- What happens when the vector database is temporarily unavailable?
- How does the system handle extremely long or complex questions?
- What happens when the user asks for information that might be sensitive or copyrighted beyond the book content?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST extract text content from MDX files in the docs/ folder
- **FR-002**: System MUST chunk extracted text into manageable segments for embedding
- **FR-003**: System MUST create vector embeddings of text chunks using Cohere embedding model
- **FR-004**: System MUST store vector embeddings in Qdrant vector database with appropriate metadata
- **FR-005**: System MUST support incremental indexing to handle new book content without reprocessing everything
- **FR-006**: System MUST use openai-agents SDK to create an intelligent agent for response generation
- **FR-007**: System MUST ensure responses are based only on book content and not external knowledge
- **FR-008**: System MUST provide concise answers by default, with option for more detail when requested
- **FR-009**: System MUST retrieve top 5 most relevant text chunks from Qdrant when processing user queries
- **FR-010**: System MUST provide beginner-friendly responses that are easy to understand
- **FR-011**: System MUST handle metadata queries about book structure (chapters, parts, summaries)
- **FR-012**: System MUST load all required configuration from environment variables (.env file)

### Key Entities *(include if feature involves data)*

- **Book Content**: Represents the text content extracted from MDX files in docs/, including chapters, sections, and metadata
- **Text Chunks**: Segments of book content that have been processed and prepared for embedding
- **Vector Embeddings**: Numerical representations of text chunks stored in Qdrant for semantic search
- **User Query**: Questions or search requests submitted by users to the chatbot
- **Response**: Answers generated by the agent based on retrieved book content

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can ask factual questions about the book content and receive accurate answers within 5 seconds
- **SC-002**: The system successfully retrieves relevant book content for 90% of user queries
- **SC-003**: Users report 80% satisfaction with the accuracy and helpfulness of responses in post-interaction surveys
- **SC-004**: The system processes new book content updates within 10 minutes of changes to the docs/ folder
- **SC-005**: Response accuracy (measured by human evaluation) exceeds 85% for factual questions