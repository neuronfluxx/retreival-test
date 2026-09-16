"""Sample usage of the Multimodal RAG system"""

import requests
import json
from pathlib import Path


BASE_URL = "http://localhost:8003"


def health_check():
    """Check if service is healthy"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())
    return response.status_code == 200


def upload_document(file_path: str, collection_name: str = "default"):
    """Upload a document"""
    print(f"\nUploading document: {file_path}")

    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {
            "collection_name": collection_name,
            "extract_images": "true",
            "extract_tables": "true",
            "use_ocr": "true",
            "use_layout_detection": "true"
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/documents/upload",
            files=files,
            data=data
        )

    if response.status_code == 200:
        result = response.json()
        print(f"✓ Upload successful!")
        print(f"  Document ID: {result['document_id']}")
        print(f"  Chunks created: {result['num_chunks']}")
        print(f"  Processing time: {result['processing_time']:.2f}s")
        return result
    else:
        print(f"✗ Upload failed: {response.text}")
        return None


def query_documents(query: str, collection_name: str = "default", top_k: int = 5):
    """Query documents"""
    print(f"\nQuerying: {query}")

    payload = {
        "query": query,
        "collection_name": collection_name,
        "top_k": top_k,
        "include_images": True,
        "include_tables": True,
        "rerank": True,
        "temperature": 0.7,
        "max_tokens": 1500
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/query",
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Query successful!")
        print(f"\nAnswer:\n{result['answer']}")
        print(f"\nSources: {', '.join(result['sources'])}")
        print(f"Retrieved chunks: {len(result['retrieved_chunks'])}")
        print(f"Processing time: {result['processing_time']:.2f}s")

        # Show retrieved chunks
        print("\nRetrieved Chunks:")
        for i, chunk in enumerate(result['retrieved_chunks'], 1):
            print(f"\n  [{i}] Similarity: {chunk['similarity_score']:.3f}")
            print(f"      Type: {chunk['chunk_type']}")
            print(f"      Page: {chunk['page']}")
            print(f"      Content: {chunk['content'][:150]}...")

        return result
    else:
        print(f"✗ Query failed: {response.text}")
        return None


def search_documents(query: str, collection_name: str = "default", top_k: int = 5):
    """Search documents (no generation)"""
    print(f"\nSearching: {query}")

    payload = {
        "query": query,
        "collection_name": collection_name,
        "top_k": top_k
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/search",
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Search successful!")
        print(f"Total results: {result['total_results']}")

        for i, chunk in enumerate(result['results'], 1):
            print(f"\n  [{i}] Similarity: {chunk['similarity_score']:.3f}")
            print(f"      Content: {chunk['content'][:100]}...")

        return result
    else:
        print(f"✗ Search failed: {response.text}")
        return None


def list_collections():
    """List all collections"""
    print("\nListing collections...")

    response = requests.get(f"{BASE_URL}/api/v1/documents/collections")

    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Found {result['total']} collections:")

        for collection in result['collections']:
            print(f"\n  - {collection['name']}")
            print(f"    Documents: {collection.get('count', 0)}")

        return result
    else:
        print(f"✗ Failed to list collections: {response.text}")
        return None


def main():
    """Main demo function"""
    print("=" * 60)
    print("Multimodal RAG System - Sample Usage")
    print("=" * 60)

    # Health check
    if not health_check():
        print("Service is not healthy. Please start the service first.")
        return

    # Example 1: Upload a document
    # Replace with your actual document path
    doc_path = "sample_document.pdf"  # Update this path

    if Path(doc_path).exists():
        upload_result = upload_document(doc_path, "demo_collection")
    else:
        print(f"\nNote: Sample document '{doc_path}' not found.")
        print("Please provide a valid document path to test upload.")

    # Example 2: Query documents
    query_documents(
        query="What are the key findings in the document?",
        collection_name="demo_collection",
        top_k=5
    )

    # Example 3: Search documents
    search_documents(
        query="machine learning algorithms",
        collection_name="demo_collection",
        top_k=3
    )

    # Example 4: List collections
    list_collections()


if __name__ == "__main__":
    main()
