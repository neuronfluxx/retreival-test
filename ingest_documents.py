#!/usr/bin/env python3
"""
Local document ingestion script for testing retrieval quality.
Ingests PDFs from a local directory into Pinecone without S3.
"""

import os
import sys
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from pypdf import PdfReader
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "rag-test-index")

AZURE_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AZURE_DEPLOYMENT = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
AZURE_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
EMBED_DIM = 3072

# Initialize clients
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Text splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


def embed(texts: list[str]) -> list[list[float]]:
    """Generate embeddings using Azure OpenAI."""
    url = f"{AZURE_ENDPOINT.rstrip('/')}/openai/deployments/{AZURE_DEPLOYMENT}/embeddings?api-version={AZURE_API_VERSION}"
    headers = {"Content-Type": "application/json", "api-key": AZURE_API_KEY}
    
    # Batch in groups of 16 to avoid rate limits
    all_embeddings = []
    batch_size = 16
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        resp = requests.post(url, headers=headers, json={"input": batch}, timeout=60)
        resp.raise_for_status()
        batch_embeddings = [d["embedding"] for d in resp.json()["data"]]
        all_embeddings.extend(batch_embeddings)
        print(f"  Embedded {len(all_embeddings)}/{len(texts)} chunks...")
    
    return all_embeddings


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(str(pdf_path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text


def ingest_document(pdf_path: Path, namespace: str = "") -> int:
    """
    Ingest a single PDF document into Pinecone.
    
    Args:
        pdf_path: Path to the PDF file
        namespace: Optional Pinecone namespace for isolation
    
    Returns:
        Number of chunks ingested
    """
    print(f"\n📄 Processing: {pdf_path.name}")
    
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print(f"  ⚠️  No extractable text in {pdf_path.name}")
        return 0
    
    # Split into chunks
    chunks = splitter.split_text(text)
    print(f"  ✂️  Split into {len(chunks)} chunks")
    
    # Generate embeddings
    print(f"  🔢 Generating embeddings...")
    embeddings = embed(chunks)
    
    # Prepare vectors with metadata
    source_id = pdf_path.stem  # filename without extension
    vectors = [
        {
            "id": f"{source_id}#{i}",
            "values": emb,
            "metadata": {
                "source": source_id,
                "filename": pdf_path.name,
                "chunk_index": i,
                "text": chunk
            }
        }
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings))
    ]
    
    # Upsert to Pinecone
    print(f"  ⬆️  Upserting to Pinecone...")
    index.upsert(vectors=vectors, namespace=namespace)
    print(f"  ✅ Upserted {len(vectors)} vectors")
    
    return len(vectors)


def ingest_directory(directory: str, namespace: str = "") -> dict:
    """
    Ingest all PDFs from a directory.
    
    Args:
        directory: Path to directory containing PDFs
        namespace: Optional Pinecone namespace
    
    Returns:
        Summary of ingestion results
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        raise ValueError(f"Directory not found: {directory}")
    
    pdf_files = list(dir_path.glob("*.pdf"))
    if not pdf_files:
        raise ValueError(f"No PDF files found in: {directory}")
    
    print(f"\n📚 Found {len(pdf_files)} PDF files in {directory}")
    print(f"🏷️  Namespace: {namespace or '(default)'}")
    
    results = {
        "total_files": len(pdf_files),
        "successful": 0,
        "failed": 0,
        "total_chunks": 0
    }
    
    for pdf_path in pdf_files:
        try:
            chunks_count = ingest_document(pdf_path, namespace)
            results["successful"] += 1
            results["total_chunks"] += chunks_count
        except Exception as e:
            print(f"  ❌ Error processing {pdf_path.name}: {e}")
            results["failed"] += 1
    
    return results


def clear_namespace(namespace: str = "") -> int:
    """Delete all vectors in a namespace."""
    print(f"\n🗑️  Clearing namespace: {namespace or '(default)'}")
    
    # Query all vectors with dummy vector
    results = index.query(
        vector=[0.0] * EMBED_DIM,
        top_k=10000,
        namespace=namespace,
        include_values=False,
        include_metadata=False,
    )
    
    ids = [match["id"] for match in results["matches"]]
    if ids:
        index.delete(ids=ids, namespace=namespace)
        print(f"  ✅ Deleted {len(ids)} vectors")
    else:
        print(f"  ℹ️  No vectors to delete")
    
    return len(ids)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest PDFs into Pinecone for RAG testing")
    parser.add_argument("path", help="Path to PDF file or directory")
    parser.add_argument("--namespace", "-n", default="", help="Pinecone namespace (optional)")
    parser.add_argument("--clear", action="store_true", help="Clear namespace before ingesting")
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    # Clear namespace if requested
    if args.clear:
        clear_namespace(args.namespace)
    
    # Ingest
    if path.is_file() and path.suffix.lower() == ".pdf":
        chunks = ingest_document(path, args.namespace)
        print(f"\n✅ Done! Ingested {chunks} chunks from {path.name}")
    elif path.is_dir():
        results = ingest_directory(str(path), args.namespace)
        print(f"\n✅ Done!")
        print(f"   Files processed: {results['successful']}/{results['total_files']}")
        print(f"   Total chunks: {results['total_chunks']}")
        if results['failed'] > 0:
            print(f"   ⚠️  Failed: {results['failed']}")
    else:
        print(f"❌ Invalid path: {path}")
        print("   Provide a PDF file or directory containing PDFs")
        sys.exit(1)


if __name__ == "__main__":
    main()
