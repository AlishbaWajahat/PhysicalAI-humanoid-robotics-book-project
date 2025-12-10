# Implementation Plan: RAG Chatbot Backend

**Branch**: `005-rag-chatbot-backend` | **Date**: 2025-12-10 | **Spec**: [specs/005-rag-chatbot-backend/spec.md](specs/005-rag-chatbot-backend/spec.md)
**Input**: Feature specification from `/specs/005-rag-chatbot-backend/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a RAG (Retrieval Augmented Generation) chatbot backend that extracts book content from docs/, chunks and embeds it into Qdrant vector database, then uses an agent to answer user questions based only on book content. The implementation will be in two phases: (1) data pipeline for content extraction, chunking, and vector storage; (2) agent implementation that retrieves relevant content and generates responses.

## Technical Context

**Language/Version**: Python 3.13 (as evidenced by existing backend/.python-version and pyproject.toml)
**Primary Dependencies**: openai-agents SDK, Qdrant client, Cohere, python-dotenv, PyMDX (for docs/ parsing)
**Storage**: Qdrant vector database (cloud-based) with local .env configuration
**Testing**: pytest (to be added)
**Target Platform**: Linux server (Ubuntu 22.04 LTS per constitution)
**Project Type**: Backend service for RAG functionality
**Performance Goals**: <5 seconds response time for user queries, 90% content retrieval accuracy
**Constraints**: Must use functional programming (no OOP), responses only from book content, beginner-friendly
**Scale/Scope**: Single-user book content access system

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Rule 1 (Spec-Driven Dev)**: ✅ Validated - proceeding from approved spec.md
- **Rule 2 (Real-Time Documentation)**: ✅ Will verify all API references and library usage against 2025 documentation
- **Rule 3 (Reproducibility)**: ✅ Targeting Ubuntu 22.04 LTS environment
- **Rule 4 (Code Quality)**: ✅ Will enforce Black formatting, Ruff linting, mypy type checking
- **Rule 5 (Version Precision)**: ✅ Will specify exact versions for all dependencies
- **Rule 8 (External Dependencies)**: ✅ Using Qdrant cloud, Cohere API, and free-tier services as specified
- **Rule 10 (Docusaurus + MDX)**: N/A - backend implementation
- **Rule 14 (Strict Adherence)**: ✅ Implementing exactly as specified in feature requirements
- **Rule 16 (Smart Minimalism)**: ✅ Functional approach as requested, avoiding unnecessary complexity

## Project Structure

### Documentation (this feature)

```text
specs/005-rag-chatbot-backend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── index_content.py          # Single script with functions: extract_content(), chunk_text(), generate_embeddings(), store_in_qdrant()
├── rag_agent.py              # RAG agent with separate retrieve tool for Qdrant interaction
├── main.py                   # Main entry point to orchestrate indexing or agent
├── pyproject.toml            # Project dependencies and configuration
├── .env                      # Environment variables
├── .python-version           # Python version specification
├── README.md                 # Project documentation
└── src/
    └── utils/                # Helper functions
        ├── config.py         # Configuration loading from .env
        └── logger.py         # Logging utilities
```

**Structure Decision**: Single backend project following hybrid approach that balances functional programming principles with simplicity. The indexing functionality is consolidated in a single script with well-defined functions, while the agent functionality remains separate for clear separation of concerns between data ingestion and query processing.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
