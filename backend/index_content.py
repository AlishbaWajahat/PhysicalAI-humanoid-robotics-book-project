"""
Content indexing script for the RAG Chatbot Backend.
Extracts content from MDX files, chunks it, creates embeddings, and stores in Qdrant.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

from markdown import markdown
import frontmatter
import cohere

# Add backend path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.utils.config import (
    get_cohere_config,
    get_indexing_config,
    get_retrieval_config,
)
from src.utils.qdrant_client import (
    create_qdrant_client,
    get_or_create_collection,
    upsert_vectors,
)
from src.utils.logger import get_logger, log_info, log_error, log_debug
from src.utils.models import BookContent, TextChunk, Embedding

from qdrant_client.http import models

logger = get_logger(__name__)

# -------------------------------------------------------------------
# CONTENT EXTRACTION
# -------------------------------------------------------------------

def extract_content(docs_path: str = "docs/") -> List[BookContent]:
    log_info(f"Extracting content from {docs_path}")
    docs_dir = Path(docs_path)
    contents = []

    md_files = list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx"))

    for file_path in md_files:
        try:
            raw = file_path.read_text(encoding="utf-8")
            post = frontmatter.loads(raw)

            plain_text = extract_plain_text(post.content)
            rel_path = f"docs/{file_path.relative_to(docs_dir).as_posix()}"

            contents.append(
                BookContent(
                    source_path=rel_path,
                    content=plain_text,
                    title=post.metadata.get("title", ""),
                    metadata={
                        **post.metadata,
                        "file_mtime": file_path.stat().st_mtime,
                    },
                )
            )
        except Exception as e:
            log_error(f"Failed to process {file_path}: {e}")

    return contents


def extract_plain_text(mdx: str) -> str:
    mdx = re.sub(r"<[^>]+>", "", mdx)
    try:
        html = markdown(mdx)
        return re.sub(r"<[^>]+>", "", html)
    except Exception:
        return mdx


# -------------------------------------------------------------------
# CHUNKING
# -------------------------------------------------------------------

def chunk_text(
    contents: List[BookContent],
    chunk_size: int,
    overlap: int,
) -> List[TextChunk]:
    chunks = []
    idx = 0

    for content in contents:
        sentences = re.split(r"[.!?]\s+", content.content)
        buf = ""

        for s in sentences:
            if len(buf) + len(s) > chunk_size:
                chunks.append(
                    TextChunk(
                        content_id=content.id,
                        text=buf.strip(),
                        chunk_index=idx,
                        metadata={
                            "source_path": content.source_path,
                            "title": content.title,
                            "file_mtime": content.metadata["file_mtime"],
                        },
                    )
                )
                idx += 1
                buf = buf[-overlap:] + " " + s
            else:
                buf += " " + s

        if buf.strip():
            chunks.append(
                TextChunk(
                    content_id=content.id,
                    text=buf.strip(),
                    chunk_index=idx,
                    metadata={
                        "source_path": content.source_path,
                        "title": content.title,
                        "file_mtime": content.metadata["file_mtime"],
                    },
                )
            )
            idx += 1

    return chunks


# -------------------------------------------------------------------
# EMBEDDINGS
# -------------------------------------------------------------------

def generate_embeddings(chunks: List[TextChunk]) -> List[Embedding]:
    cfg = get_cohere_config()
    co = cohere.Client(cfg["api_key"])

    embeddings = []
    batch = 96

    for i in range(0, len(chunks), batch):
        texts = [c.text for c in chunks[i:i + batch]]
        res = co.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document",
        )

        for j, vec in enumerate(res.embeddings):
            embeddings.append(
                Embedding(
                    chunk_id=chunks[i + j].id,
                    vector=vec,
                    model_name="embed-english-v3.0",
                    model_version="3.0",
                )
            )

    return embeddings


# -------------------------------------------------------------------
# STORAGE
# -------------------------------------------------------------------

def store_in_qdrant(embeddings: List[Embedding], chunks: List[TextChunk]) -> bool:
    client = create_qdrant_client()
    collection = get_or_create_collection(client)

    chunk_map = {c.id: c for c in chunks}

    points = []
    for e in embeddings:
        c = chunk_map[e.chunk_id]
        points.append(
            models.PointStruct(
                id=e.chunk_id,
                vector=e.vector,
                payload={
                    "text": c.text,
                    "source_path": c.metadata["source_path"],
                    "title": c.metadata["title"],
                    "file_mtime": c.metadata["file_mtime"],
                    "chunk_index": c.chunk_index,
                },
            )
        )

    return upsert_vectors(client, collection, points)


# -------------------------------------------------------------------
# 🔥 CLEAN INCREMENTAL INDEXING (REWRITTEN)
# -------------------------------------------------------------------

def get_existing_docs(client, collection: str) -> Dict[str, float]:
    """
    Returns:
        { source_path: last_indexed_mtime }
    """
    records, _ = client.scroll(
        collection_name=collection,
        limit=10000,
        with_payload=True,
        with_vectors=False,
    )

    docs = {}
    for r in records:
        sp = r.payload.get("source_path")
        mt = r.payload.get("file_mtime")
        if sp and mt:
            docs[sp] = max(docs.get(sp, 0), mt)

    return docs


def incremental_indexing(docs_path: str = "docs/") -> bool:
    log_info("Running incremental indexing")

    client = create_qdrant_client()
    cfg = get_retrieval_config()
    collection = cfg["collection_name"]

    existing = get_existing_docs(client, collection)
    contents = extract_content(docs_path)

    to_index = []
    to_delete = []

    for c in contents:
        old_mtime = existing.get(c.source_path)
        new_mtime = c.metadata["file_mtime"]

        if not old_mtime:
            to_index.append(c)
        elif new_mtime > old_mtime:
            to_index.append(c)
            to_delete.append(c.source_path)

    if not to_index:
        log_info("No new or updated docs found")
        return True

    # delete outdated chunks
    for sp in to_delete:
        client.delete(
            collection_name=collection,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key="source_path",
                        match=models.MatchValue(value=sp),
                    )
                ]
            ),
        )

    idx_cfg = get_indexing_config()
    chunks = chunk_text(
        to_index,
        idx_cfg["chunk_size"],
        idx_cfg["chunk_overlap"],
    )
    embeddings = generate_embeddings(chunks)

    return store_in_qdrant(embeddings, chunks)


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

def main_indexing_pipeline(docs_path: str = "docs/", incremental: bool = False) -> bool:
    if incremental:
        return incremental_indexing(docs_path)

    cfg = get_indexing_config()
    contents = extract_content(docs_path)
    chunks = chunk_text(contents, cfg["chunk_size"], cfg["chunk_overlap"])
    embeddings = generate_embeddings(chunks)
    return store_in_qdrant(embeddings, chunks)


if __name__ == "__main__":
    ok = main_indexing_pipeline(incremental=True)
    print("Indexing completed" if ok else "Indexing failed")
