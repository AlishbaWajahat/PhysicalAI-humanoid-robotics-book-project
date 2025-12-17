#!/usr/bin/env python3
import sys
import os
import argparse
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__)))

from index_content import main_indexing_pipeline
from agent.rag_agent import main_agent
from tools.agent_tools import search_book_content, retrieve_book_content
from src.utils.logger import get_logger, log_info


def run_indexing(docs_path: str = "../docs/", incremental: bool = False):
    print(f"Starting content indexing from {docs_path} (incremental: {incremental})...")
    success = main_indexing_pipeline(docs_path, incremental=incremental)
    if success:
        print("Content indexing completed successfully!")
    else:
        print("Content indexing failed!")
        sys.exit(1)


def run_agent():
    print("Starting RAG agent...")
    asyncio.run(main_agent())   # ✅ FIXED


def run_search():
    """Run the search functionality interactively."""
    print("Book Content Search is ready! Enter search queries to find specific content in the PhysicalAI humanoid robotics book.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            user_input = input("Search query: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                print("Please enter a search query.\n")
                continue

            # Perform search
            results = search_book_content(query=user_input, top_k=5)

            if results:
                print(f"\nFound {len(results)} relevant sections:\n")
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result.get('title', 'Untitled')} - {result.get('source_path', 'Unknown path')}")
                    print(f"   Relevance: {result.get('relevance_score', 0):.2f}")
                    print(f"   Preview: {result.get('text', '')[:200]}{'...' if len(result.get('text', '')) > 200 else ''}\n")
            else:
                print("No relevant content found for your search query.\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred during search: {str(e)}\n")


def main():
    parser = argparse.ArgumentParser(description="RAG Chatbot Backend")
    parser.add_argument(
        "command",
        choices=["index", "agent", "search", "both"],
        help="Choose what to run: 'index' to index content, 'agent' to run the Q&A agent, 'search' to run search mode, 'both' to do indexing then run agent"
    )
    parser.add_argument(
        "--docs-path",
        type=str,
        default="../docs/",
        help="Path to docs directory"
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Perform incremental indexing (only process new/updated documents)"
    )

    args = parser.parse_args()

    if args.command == "index":
        run_indexing(args.docs_path, incremental=args.incremental)

    elif args.command == "agent":
        run_agent()

    elif args.command == "search":
        run_search()

    elif args.command == "both":
        print("Running indexing first...")
        run_indexing(args.docs_path, incremental=args.incremental)
        print("\nIndexing completed. Starting agent...")
        run_agent()


if __name__ == "__main__":
    main()
