"""
Hugging Face Spaces Entry Point
RAG Chatbot Backend for Physical AI & Humanoid Robotics Book
"""
import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Import and run the main server
if __name__ == "__main__":
    # Import here to ensure proper path setup
    from chatkit_server import app
    import uvicorn

    # Get port from environment (HF Spaces uses PORT env variable)
    port = int(os.getenv("PORT", os.getenv("CHATKIT_BACKEND_PORT", 7860)))

    print(f"🚀 Starting RAG Chatbot Backend on port {port}")
    print(f"📚 Book: Physical AI & Humanoid Robotics")
    print(f"🤖 Powered by: OpenAI ChatKit + Google Gemini + Qdrant + Neon Postgres")

    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
