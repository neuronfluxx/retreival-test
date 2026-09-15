#!/usr/bin/env python3
"""
Local document ingestion script for testing retrieval quality.
Ingests PDFs from a local directory into ChromaDB without S3.
"""

import os
import sys
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from pypdf import PdfReader
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CHROMA_DB_PATH = os.environ.get("CHROMA_DB_PATH", "./chroma_db")
CHROMA_COLLECTION_NAME = os.environ.get("CHROMA_COLLECTION_NAME", "rag-test-collection")

AZURE_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AZURE_DEPLOYMENT = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
AZURE_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
EMBED_DIM = 3072

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

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
    Ingest a single PDF document into ChromaDB.
    
    Args:
        pdf_path: Path to the PDF file
        namespace: Optional namespace for filtering (ChromaDB uses metadata instead)
    
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
    
    # Prepare documents for ChromaDB
    source_id = pdf_path.stem  # filename without extension
    ids = []
    documents = []
    metadatas = []
    
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        ids.append(f"{source_id}#{i}")
        documents.append(chunk)
        metadata = {
            "source": source_id,
            "filename": pdf_path.name,
            "chunk_index": str(i),
        }
        if namespace:
            metadata["namespace"] = namespace
        metadatas.append(metadata)
    
    # Add to ChromaDB
    print(f"  ⬆️  Adding to ChromaDB...")
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    print(f"  ✅ Added {len(ids)} vectors")
    
    return len(ids)


def ingest_directory(directory: str, namespace: str = "") -> dict:
    """
    Ingest all PDFs from a directory.
    
    Args:
        directory: Path to directory containing PDFs
        namespace: Optional namespace for filtering
    
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
    """Delete all vectors with a specific namespace."""
    print(f"\n🗑️  Clearing namespace: {namespace or '(default)'}")
    
    # Query all documents with namespace filter
    try:
        if namespace:
            results = collection.get(where={"namespace": namespace})
        else:
            results = collection.get()
        
        ids = results["ids"]
        if ids:
            collection.delete(ids=ids)
            print(f"  ✅ Deleted {len(ids)} vectors")
        else:
            print(f"  ℹ️  No vectors to delete")
        
        return len(ids)
    except Exception as e:
        print(f"  ❌ Error deleting: {e}")
        return 0


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest PDFs into ChromaDB for RAG testing")
    parser.add_argument("path", help="Path to PDF file or directory")
    parser.add_argument("--namespace", "-n", default="", help="Namespace for filtering (optional)")
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
