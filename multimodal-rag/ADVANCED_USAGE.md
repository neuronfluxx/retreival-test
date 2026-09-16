# Advanced Usage Guide

Advanced use cases and examples for the Multimodal RAG system.

## Table of Contents

1. [Batch Document Processing](#batch-document-processing)
2. [Multimodal Queries](#multimodal-queries)
3. [Custom Metadata Filtering](#custom-metadata-filtering)
4. [Table-Specific Queries](#table-specific-queries)
5. [Image-Based Retrieval](#image-based-retrieval)
6. [Collection Management](#collection-management)
7. [Integration Examples](#integration-examples)
8. [Performance Optimization](#performance-optimization)

## Batch Document Processing

### Upload Multiple Documents

```python
import asyncio
import aiohttp
from pathlib import Path

async def upload_document(session, file_path, collection_name):
    """Upload a single document"""
    url = "http://localhost:8003/api/v1/documents/upload"
    
    data = aiohttp.FormData()
    data.add_field('file', 
                   open(file_path, 'rb'),
                   filename=file_path.name)
    data.add_field('collection_name', collection_name)
    data.add_field('extract_images', 'true')
    data.add_field('extract_tables', 'true')
    
    async with session.post(url, data=data) as response:
        result = await response.json()
        print(f"Uploaded {file_path.name}: {result['document_id']}")
        return result

async def batch_upload(directory, collection_name):
    """Upload all PDFs from a directory"""
    pdf_files = list(Path(directory).glob("*.pdf"))
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            upload_document(session, file_path, collection_name)
            for file_path in pdf_files
        ]
        results = await asyncio.gather(*tasks)
    
    print(f"\nUploaded {len(results)} documents")
    return results

# Usage
asyncio.run(batch_upload("./documents", "research_papers"))
```

## Multimodal Queries

### Text + Image Query

```python
import base64
import requests

def multimodal_query(query_text, query_image_path, collection_name="default"):
    """Query with both text and image"""
    
    # Read and encode image
    with open(query_image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()
    
    payload = {
        "query_text": query_text,
        "query_image_base64": image_base64,
        "collection_name": collection_name,
        "top_k": 5,
        "weight_text": 0.6,
        "weight_image": 0.4
    }
    
    response = requests.post(
        "http://localhost:8003/api/v1/search/multimodal",
        json=payload
    )
    
    return response.json()

# Example: Find similar charts
result = multimodal_query(
    query_text="revenue growth chart",
    query_image_path="sample_chart.png",
    collection_name="financial_reports"
)
```

### Image-Only Search

```python
def find_similar_images(query_image_path, collection_name="default"):
    """Find visually similar images"""
    
    with open(query_image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()
    
    payload = {
        "query_image_base64": image_base64,
        "collection_name": collection_name,
        "top_k": 10,
        "weight_image": 1.0,
        "weight_text": 0.0
    }
    
    response = requests.post(
        "http://localhost:8003/api/v1/search/multimodal",
        json=payload
    )
    
    results = response.json()
    
    # Extract image paths
    image_results = [
        r for r in results['results']
        if r['chunk_type'] == 'image' and r['image_path']
    ]
    
    return image_results
```

## Custom Metadata Filtering

### Filter by Document Type

```python
def query_with_filters(query, filters=None, collection_name="default"):
    """Query with metadata filters"""
    
    payload = {
        "query": query,
        "collection_name": collection_name,
        "top_k": 5,
        "filters": filters or {}
    }
    
    response = requests.post(
        "http://localhost:8003/api/v1/query",
        json=payload
    )
    
    return response.json()

# Example 1: Only tables
result = query_with_filters(
    query="quarterly revenue breakdown",
    filters={"type": "table"}
)

# Example 2: Specific page range
result = query_with_filters(
    query="methodology section",
    filters={"page": {"$gte": 10, "$lte": 20}}
)

# Example 3: Specific document
result = query_with_filters(
    query="key findings",
    filters={"document_id": "doc_abc123"}
)
```

## Table-Specific Queries

### Extract and Query Tables

```python
def query_tables(query, collection_name="default"):
    """Query specifically for table content"""
    
    # First, search for tables
    payload = {
        "query": query,
        "collection_name": collection_name,
        "top_k": 10,
        "filters": {"type": "table"}
    }
    
    response = requests.post(
        "http://localhost:8003/api/v1/search",
        json=payload
    )
    
    tables = response.json()['results']
    
    # Display tables in markdown
    for i, table in enumerate(tables, 1):
        print(f"\n{'='*60}")
        print(f"Table {i} (Page {table['page']})")
        print(f"Similarity: {table['similarity_score']:.3f}")
        print(f"{'='*60}")
        print(table['content'])
    
    return tables

# Example
tables = query_tables(
    query="financial performance metrics",
    collection_name="annual_reports"
)
```

### Compare Tables Across Documents

```python
def compare_tables(query, year_1, year_2):
    """Compare similar tables from different years"""
    
    results = {}
    
    for year in [year_1, year_2]:
        payload = {
            "query": query,
            "collection_name": f"reports_{year}",
            "top_k": 3,
            "filters": {"type": "table"}
        }
        
        response = requests.post(
            "http://localhost:8003/api/v1/search",
            json=payload
        )
        
        results[year] = response.json()['results']
    
    # Display comparison
    print(f"\n{query}")
    print("="*60)
    print(f"\n{year_1}:")
    print(results[year_1][0]['content'] if results[year_1] else "No data")
    print(f"\n{year_2}:")
    print(results[year_2][0]['content'] if results[year_2] else "No data")
    
    return results

# Example
compare_tables("revenue by region", "2022", "2023")
```

## Image-Based Retrieval

### Find All Charts in Documents

```python
def extract_all_images(collection_name="default", image_type="chart"):
    """Extract all images of specific type"""
    
    payload = {
        "query": f"{image_type} diagram illustration",
        "collection_name": collection_name,
        "top_k": 100,
        "filters": {"type": "image"}
    }
    
    response = requests.post(
        "http://localhost:8003/api/v1/search",
        json=payload
    )
    
    images = response.json()['results']
    
    # Download and organize images
    from pathlib import Path
    import shutil
    
    output_dir = Path(f"extracted_{image_type}s")
    output_dir.mkdir(exist_ok=True)
    
    for i, img in enumerate(images):
        if img['image_path']:
            src = Path(img['image_path'])
            if src.exists():
                dst = output_dir / f"{image_type}_{i}_{src.name}"
                shutil.copy(src, dst)
                print(f"Extracted: {dst}")
    
    return images
```

## Collection Management

### Create Specialized Collections

```python
class CollectionManager:
    """Manage document collections"""
    
    def __init__(self, base_url="http://localhost:8003"):
        self.base_url = base_url
    
    def create_collection_from_directory(self, 
                                        directory, 
                                        collection_name,
                                        file_pattern="*.pdf"):
        """Create collection from directory"""
        from pathlib import Path
        
        files = list(Path(directory).glob(file_pattern))
        print(f"Found {len(files)} files")
        
        for file_path in files:
            self.upload_document(file_path, collection_name)
        
        stats = self.get_collection_stats(collection_name)
        print(f"\nCollection '{collection_name}' created:")
        print(f"  Documents: {stats['count']}")
    
    def upload_document(self, file_path, collection_name):
        """Upload single document"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'collection_name': collection_name}
            
            response = requests.post(
                f"{self.base_url}/api/v1/documents/upload",
                files=files,
                data=data
            )
            
            return response.json()
    
    def get_collection_stats(self, collection_name):
        """Get collection statistics"""
        response = requests.get(
            f"{self.base_url}/api/v1/documents/collections"
        )
        
        collections = response.json()['collections']
        
        for coll in collections:
            if coll['name'] == collection_name:
                return coll
        
        return {}
    
    def merge_collections(self, source_collections, target_collection):
        """Merge multiple collections into one"""
        # This would require backend support
        # For now, re-upload documents to new collection
        pass

# Usage
manager = CollectionManager()
manager.create_collection_from_directory(
    directory="./research_papers",
    collection_name="ml_research"
)
```

## Integration Examples

### Streamlit UI

```python
import streamlit as st
import requests

st.title("Multimodal RAG Interface")

# File upload
uploaded_file = st.file_uploader("Upload Document", type=['pdf', 'jpg', 'png'])

if uploaded_file:
    with st.spinner("Processing document..."):
        files = {'file': uploaded_file}
        data = {'collection_name': 'streamlit_docs'}
        
        response = requests.post(
            "http://localhost:8003/api/v1/documents/upload",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            st.success("Document uploaded successfully!")
            result = response.json()
            st.json(result)

# Query interface
query = st.text_input("Ask a question:")

if query:
    with st.spinner("Searching..."):
        payload = {
            "query": query,
            "collection_name": "streamlit_docs",
            "top_k": 5
        }
        
        response = requests.post(
            "http://localhost:8003/api/v1/query",
            json=payload
        )
        
        result = response.json()
        
        st.subheader("Answer")
        st.write(result['answer'])
        
        st.subheader("Sources")
        for chunk in result['retrieved_chunks']:
            with st.expander(f"Source {chunk['chunk_id']}"):
                st.write(f"Type: {chunk['chunk_type']}")
                st.write(f"Page: {chunk['page']}")
                st.write(f"Similarity: {chunk['similarity_score']:.3f}")
                st.write(chunk['content'])
```

### FastAPI Client Library

```python
from typing import List, Optional
import httpx

class MultimodalRAGClient:
    """Client library for Multimodal RAG API"""
    
    def __init__(self, base_url: str = "http://localhost:8003"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=300.0)
    
    def upload_document(self, 
                       file_path: str,
                       collection_name: str = "default",
                       **kwargs) -> dict:
        """Upload document"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'collection_name': collection_name,
                **kwargs
            }
            
            response = self.client.post(
                f"{self.base_url}/api/v1/documents/upload",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
    
    def query(self,
             query: str,
             collection_name: str = "default",
             top_k: int = 5,
             **kwargs) -> dict:
        """Query documents"""
        payload = {
            "query": query,
            "collection_name": collection_name,
            "top_k": top_k,
            **kwargs
        }
        
        response = self.client.post(
            f"{self.base_url}/api/v1/query",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def search(self, query: str, **kwargs) -> List[dict]:
        """Search without generation"""
        payload = {"query": query, **kwargs}
        
        response = self.client.post(
            f"{self.base_url}/api/v1/search",
            json=payload
        )
        response.raise_for_status()
        return response.json()['results']
    
    def list_collections(self) -> List[dict]:
        """List all collections"""
        response = self.client.get(
            f"{self.base_url}/api/v1/documents/collections"
        )
        response.raise_for_status()
        return response.json()['collections']

# Usage
client = MultimodalRAGClient()

# Upload
result = client.upload_document(
    "document.pdf",
    collection_name="my_docs"
)

# Query
answer = client.query(
    "What are the key findings?",
    collection_name="my_docs",
    top_k=5
)

print(answer['answer'])
```

## Performance Optimization

### Batch Embedding Generation

```python
# Instead of processing one by one
for text in texts:
    embedding = generate_embedding(text)

# Use batch processing
embeddings = generate_embeddings_batch(texts)
```

### Caching Strategy

```python
import hashlib
import json

class EmbeddingCache:
    """Cache embeddings to avoid regeneration"""
    
    def __init__(self, cache_file="embedding_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    def _load_cache(self):
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    def get_embedding(self, text, generator):
        """Get cached or generate new embedding"""
        cache_key = hashlib.md5(text.encode()).hexdigest()
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        embedding = generator.generate_text_embedding(text)
        self.cache[cache_key] = embedding
        self._save_cache()
        
        return embedding
```

### Async Query Processing

```python
import asyncio
import aiohttp

async def query_multiple(queries, collection_name="default"):
    """Process multiple queries in parallel"""
    
    async def single_query(session, query):
        payload = {
            "query": query,
            "collection_name": collection_name,
            "top_k": 3
        }
        
        async with session.post(
            "http://localhost:8003/api/v1/query",
            json=payload
        ) as response:
            return await response.json()
    
    async with aiohttp.ClientSession() as session:
        tasks = [single_query(session, q) for q in queries]
        results = await asyncio.gather(*tasks)
    
    return results

# Usage
queries = [
    "What is the methodology?",
    "What are the results?",
    "What are the conclusions?"
]

results = asyncio.run(query_multiple(queries))
```

## Monitoring and Debugging

### Check System Health

```python
def system_health_check():
    """Comprehensive health check"""
    
    checks = {
        "api": False,
        "embeddings": False,
        "vector_store": False
    }
    
    # API health
    try:
        response = requests.get("http://localhost:8003/health")
        checks["api"] = response.status_code == 200
    except:
        pass
    
    # Test embedding generation
    try:
        payload = {
            "query": "test",
            "collection_name": "test",
            "top_k": 1
        }
        response = requests.post(
            "http://localhost:8003/api/v1/search",
            json=payload
        )
        checks["embeddings"] = response.status_code in [200, 404]
    except:
        pass
    
    # Check collections
    try:
        response = requests.get(
            "http://localhost:8003/api/v1/documents/collections"
        )
        checks["vector_store"] = response.status_code == 200
    except:
        pass
    
    print("System Health Check:")
    for component, status in checks.items():
        icon = "✓" if status else "✗"
        print(f"  {icon} {component}: {'OK' if status else 'FAIL'}")
    
    return all(checks.values())
```

## Conclusion

These advanced examples demonstrate the full capabilities of the multimodal RAG system. Combine these patterns to build sophisticated document understanding applications.
