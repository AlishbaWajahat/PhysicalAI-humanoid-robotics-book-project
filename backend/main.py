#!/usr/bin/env python3
import sys
import os
import argparse
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__)))

from index_content import main_indexing_pipeline
from rag_agent import main_agent


def run_indexing(docs_path: str = "../docs/"):
    print(f"Starting content indexing from {docs_path}...")
    success = main_indexing_pipeline(docs_path)
    if success:
        print("Content indexing completed successfully!")
    else:
        print("Content indexing failed!")
        sys.exit(1)


def run_agent():
    print("Starting RAG agent...")
    asyncio.run(main_agent())   # ✅ FIXED


def main():
    parser = argparse.ArgumentParser(description="RAG Chatbot Backend")
    parser.add_argument(
        "command",
        choices=["index", "agent", "both"],
        help="Choose what to run"
    )
    parser.add_argument(
        "--docs-path",
        type=str,
        default="../docs/",
        help="Path to docs directory"
    )

    args = parser.parse_args()

    if args.command == "index":
        run_indexing(args.docs_path)

    elif args.command == "agent":
        run_agent()

    elif args.command == "both":
        print("Running indexing first...")
        run_indexing(args.docs_path)
        print("\nIndexing completed. Starting agent...")
        run_agent()


if __name__ == "__main__":
    main()
