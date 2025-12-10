"""
RAG Agent for the Chatbot Backend (OpenAI AgentSDK Approach).
Implements an agent that retrieves relevant content and generates responses using openai-agents SDK.
"""
import os
import sys
import dotenv
from typing import Dict, List, Any, Optional
import asyncio

# Add the backend directory to the path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.utils.config import get_gemini_config, get_retrieval_config, get_cohere_config
from src.utils.qdrant_client import create_qdrant_client, search_vectors
from src.utils.logger import get_logger, log_info, log_error, log_debug
from src.utils.models import UserQuery, RetrievedChunk, AgentResponse, AgentConfig

# Import OpenAI AgentSDK
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

# Initialize logger
logger = get_logger(__name__)

# Disable tracing for cleaner output
set_tracing_disabled(disabled=True)
dotenv.load_dotenv()

# Set up environment variables for API keys
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
model = 'gemini/gemini-2.5-flash'


@function_tool
def retrieve_book_content(query: str, top_k: Optional[int] = 5) -> List[Dict[str, Any]]:
    """
    Retrieve relevant book content from Qdrant vector database based on the query.

    Args:
        query: The user's query to search for in the book content
        top_k: Number of relevant chunks to retrieve (default: 5)

    Returns:
        List of dictionaries containing relevant content chunks with their metadata
    """
    log_info(f"Retrieving book content for query: {query[:50]}...")

    try:
        # Create Qdrant client and get configuration
        client = create_qdrant_client()
        retrieval_config = get_retrieval_config()

        # Generate embedding for the query using Cohere (since we used Cohere for indexing)
        import cohere
        cohere_config = get_cohere_config()
        co = cohere.Client(cohere_config['api_key'])

        # Generate embedding for the query
        response = co.embed(
            texts=[query],
            model='embed-english-v3.0',
            input_type="search_query"  # Specify this is for search queries
        )
        query_embedding = response.embeddings[0]

        # Search in Qdrant for similar vectors
        results = search_vectors(
            client=client,
            collection_name=retrieval_config['collection_name'],
            query_vector=query_embedding,
            top_k=top_k
        )

        retrieved_chunks = []
        for result in results:
            chunk_data = {
                'id': result['id'],
                'text': result['payload'].get('text', ''),
                'relevance_score': result['score'],
                'source_path': result['payload'].get('source_path', ''),
                'title': result['payload'].get('title', ''),
                'metadata': result['payload']
            }
            retrieved_chunks.append(chunk_data)

        log_info(f"Retrieved {len(retrieved_chunks)} relevant chunks")
        return retrieved_chunks

    except Exception as e:
        log_error(f"Error retrieving book content: {str(e)}")
        return []


# Define the RAG Agent using OpenAI AgentSDK
book_rag_agent = Agent(
    name='Book RAG Assistant',
    model=LitellmModel(model=model),
    instructions="""You are a helpful assistant for the PhysicalAI humanoid robotics book.
    Use the retrieve_book_content tool to find relevant information from the book content.
    Only answer questions based on the retrieved content. If the information is not available
    in the retrieved content, clearly state that the information is not in the book.
    Provide concise and accurate answers based on the book content.""",
    tools=[retrieve_book_content]
)


async def main_agent():
    """
    Main function to run the RAG agent in interactive mode using AgentSDK.
    """
    log_info("Starting RAG Agent with AgentSDK...")

    print("Book RAG Agent is ready! Ask questions about the PhysicalAI humanoid robotics book content.")
    print("Type 'quit' or 'exit' to stop.\n")

    # Create a runner for the agent
    runner = Runner()

    while True:
        try:
            user_input = input("Your question: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                print("Please ask a question.\n")
                continue

            # Process the query using the AgentSDK - await the coroutine
            run_result = await runner.run(starting_agent=book_rag_agent, input=user_input)
            # Extract the actual response from the RunResult
            if hasattr(run_result, 'output') and run_result.output:
                response = run_result.output
            elif isinstance(run_result, str):
                response = run_result
            else:
                response = str(run_result)
            print(f"Answer: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            log_error(f"Error in main agent loop: {str(e)}")
            print("An error occurred. Please try again.\n")


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main_agent())

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main_agent())
    except KeyboardInterrupt:
        print("Agent stopped.")