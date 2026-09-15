# Pinecone to ChromaDB Migration Guide

## Summary of Changes

All three files have been successfully migrated from Pinecone to ChromaDB:

- ✅ `ingest_documents.py` - Local document ingestion
- ✅ `lambda_function_all.py` - AWS Lambda function for S3 integration
- ✅ `test_retrieval.py` - Retrieval testing and evaluation

## Key Differences

### 1. **Database Initialization**

**Before (Pinecone):**
```python
from pinecone import Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
```

**After (ChromaDB):**
```python
import chromadb
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)
```

### 2. **Upserting Documents**

**Before (Pinecone):**
```python
vectors = [
    {
        "id": f"{source_id}#{i}",
        "values": emb,  # embedding
        "metadata": {"text": chunk, "source": source_id}
    }
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings))
]
index.upsert(vectors=vectors, namespace=namespace)
```

**After (ChromaDB):**
```python
collection.add(
    ids=[f"{source_id}#{i}" for i, _ in enumerate(chunks)],
    embeddings=embeddings,
    documents=documents,  # chunks are stored as documents
    metadatas=[{"source": source_id} for _ in chunks]
)
```

### 3. **Querying**

**Before (Pinecone):**
```python
results = index.query(
    vector=query_embedding,
    top_k=5,
    namespace=namespace,
    include_metadata=True
)
```

**After (ChromaDB):**
```python
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    where=where_filter,  # optional metadata filter
    include=["documents", "metadatas", "distances"]
)
```

### 4. **Deletion**

**Before (Pinecone):**
```python
results = index.query(vector=[0.0]*DIM, top_k=10000, filter={"source": key})
ids = [match["id"] for match in results["matches"]]
index.delete(ids=ids)
```

**After (ChromaDB):**
```python
results = collection.get(where={"source": key})
ids = results["ids"]
collection.delete(ids=ids)
```

## Environment Variables

Update your `.env` file:

```bash
# Remove Pinecone variables
# PINECONE_API_KEY=...
# PINECONE_INDEX_NAME=...

# Add ChromaDB variables (optional, defaults are sensible)
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=rag-test-collection

# Keep Azure OpenAI variables unchanged
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=...
```

## Installation

Install ChromaDB:

```bash
pip install chromadb
```

Remove Pinecone if no longer needed:

```bash
pip uninstall pinecone
```

## Features Comparison

| Feature | Pinecone | ChromaDB |
|---------|----------|----------|
| **Setup** | Requires API key | Local/embedded |
| **Cost** | Paid (serverless pricing) | Free |
| **Persistence** | Cloud-based | Local files |
| **Scaling** | Server-side | Client-side |
| **Namespaces** | Native support | Simulated via metadata |
| **Metadata filtering** | Supported | Supported |
| **Backup** | Built-in | Manual file backup |

## Migration Steps

1. **Update dependencies:**
   ```bash
   pip install chromadb
   pip uninstall pinecone
   ```

2. **Update environment variables** - Remove Pinecone API key, add ChromaDB path

3. **Re-ingest documents:**
   ```bash
   python ingest_documents.py /path/to/pdfs --clear
   ```

4. **Test retrieval:**
   ```bash
   python test_retrieval.py --question "Your test question"
   ```

## Data Location

ChromaDB stores data locally in the `CHROMA_DB_PATH` directory (default: `./chroma_db`). To backup your data, copy this directory.

## Advantages of ChromaDB

- ✅ No API keys or credentials needed
- ✅ Faster for development/testing
- ✅ Data stays local
- ✅ Zero cost
- ✅ Easy to reset data (just delete the directory)
- ✅ Better debugging capabilities

## Notes

- Similarity scores are converted from ChromaDB distances (1 - distance)
- Namespace functionality is simulated using metadata filters
- All existing functionality is preserved
- The Azure OpenAI embedding service is still used for generating embeddings
