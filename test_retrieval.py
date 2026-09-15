#!/usr/bin/env python3
"""
Retrieval testing script for RAG quality evaluation.
Query Pinecone with questions and evaluate retrieved chunks.
"""

import os
import sys
from typing import Optional

from pinecone import Pinecone
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
AZURE_CHAT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
EMBED_DIM = 3072

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)


def embed_query(query: str) -> list[float]:
    """Generate embedding for a query."""
    url = f"{AZURE_ENDPOINT.rstrip('/')}/openai/deployments/{AZURE_DEPLOYMENT}/embeddings?api-version={AZURE_API_VERSION}"
    headers = {"Content-Type": "application/json", "api-key": AZURE_API_KEY}
    resp = requests.post(url, headers=headers, json={"input": query}, timeout=30)
    resp.raise_for_status()
    return resp.json()["data"][0]["embedding"]


def retrieve(
    query: str,
    top_k: int = 5,
    namespace: str = "",
    filter_metadata: Optional[dict] = None
) -> list[dict]:
    """
    Retrieve relevant chunks from Pinecone.
    
    Args:
        query: The search query
        top_k: Number of results to return
        namespace: Pinecone namespace
        filter_metadata: Optional metadata filter (e.g., {"source": "document_name"})
    
    Returns:
        List of retrieved chunks with metadata and scores
    """
    # Generate query embedding
    query_embedding = embed_query(query)
    
    # Query Pinecone
    query_params = {
        "vector": query_embedding,
        "top_k": top_k,
        "namespace": namespace,
        "include_metadata": True,
    }
    if filter_metadata:
        query_params["filter"] = filter_metadata
    
    results = index.query(**query_params)
    
    return [
        {
            "id": match["id"],
            "score": match["score"],
            "text": match["metadata"].get("text", ""),
            "source": match["metadata"].get("source", "unknown"),
            "filename": match["metadata"].get("filename", "unknown"),
            "chunk_index": match["metadata"].get("chunk_index", -1)
        }
        for match in results["matches"]
    ]


def generate_answer(query: str, context: str) -> str:
    """Generate an answer using Azure OpenAI chat completion."""
    url = f"{AZURE_ENDPOINT.rstrip('/')}/openai/deployments/{AZURE_CHAT_DEPLOYMENT}/chat/completions?api-version={AZURE_API_VERSION}"
    headers = {"Content-Type": "application/json", "api-key": AZURE_API_KEY}
    
    system_prompt = """You are a helpful assistant that answers questions based on the provided context.
Instructions:
- Answer the question using ONLY the information from the context
- If the context doesn't contain enough information, say so clearly
- Be concise but thorough
- Cite specific parts of the context when relevant"""
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def print_retrieval_results(query: str, results: list[dict], show_text: bool = True):
    """Pretty print retrieval results."""
    print(f"\n{'='*80}")
    print(f"🔍 Query: {query}")
    print(f"{'='*80}")
    print(f"\n📊 Found {len(results)} results:\n")
    
    for i, result in enumerate(results, 1):
        print(f"--- Result {i} (Score: {result['score']:.4f}) ---")
        print(f"Source: {result['filename']} (chunk #{result['chunk_index']})")
        if show_text:
            print(f"\nText:\n{result['text'][:500]}{'...' if len(result['text']) > 500 else ''}")
        print()


def interactive_mode(namespace: str = "", top_k: int = 5, generate: bool = False):
    """
    Interactive Q&A mode for testing retrieval.
    
    Args:
        namespace: Pinecone namespace to query
        top_k: Number of results to retrieve
        generate: Whether to generate answers with LLM
    """
    print("\n🤖 RAG Retrieval Testing")
    print("=" * 40)
    print(f"Namespace: {namespace or '(default)'}")
    print(f"Top K: {top_k}")
    print(f"Generate answers: {'Yes' if generate else 'No'}")
    print("\nCommands:")
    print("  - Type your question and press Enter")
    print("  - Type 'quit' or 'exit' to stop")
    print("  - Type 'filter:source=filename' to filter by source")
    print("-" * 40)
    
    current_filter = None
    
    while True:
        try:
            user_input = input("\n❓ Question: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Handle filter commands
            if user_input.startswith('filter:'):
                try:
                    filter_parts = user_input[7:].split('=')
                    if len(filter_parts) == 2:
                        key, value = filter_parts
                        current_filter = {key.strip(): value.strip()}
                        print(f"✅ Filter set: {current_filter}")
                    else:
                        print("❌ Invalid filter format. Use: filter:key=value")
                except Exception as e:
                    print(f"❌ Error setting filter: {e}")
                continue
            
            if user_input == 'clear':
                current_filter = None
                print("✅ Filter cleared")
                continue
            
            # Retrieve
            results = retrieve(user_input, top_k=top_k, namespace=namespace, filter_metadata=current_filter)
            print_retrieval_results(user_input, results)
            
            # Generate answer if enabled
            if generate and results:
                context = "\n\n---\n\n".join([r['text'] for r in results])
                print("🤖 Generating answer...\n")
                try:
                    answer = generate_answer(user_input, context)
                    print(f"{'='*80}")
                    print("💡 Answer:")
                    print(f"{'='*80}")
                    print(answer)
                    print(f"{'='*80}\n")
                except Exception as e:
                    print(f"❌ Error generating answer: {e}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def batch_test(questions: list[str], namespace: str = "", top_k: int = 5) -> list[dict]:
    """
    Test retrieval on multiple questions.
    
    Args:
        questions: List of questions to test
        namespace: Pinecone namespace
        top_k: Number of results per question
    
    Returns:
        Test results for all questions
    """
    results = []
    
    for question in questions:
        print(f"\n🔍 Testing: {question}")
        retrieved = retrieve(question, top_k=top_k, namespace=namespace)
        
        results.append({
            "question": question,
            "num_results": len(retrieved),
            "avg_score": sum(r['score'] for r in retrieved) / len(retrieved) if retrieved else 0,
            "sources": list(set(r['source'] for r in retrieved)),
            "top_result": retrieved[0] if retrieved else None
        })
    
    return results


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test RAG retrieval quality")
    parser.add_argument("--namespace", "-n", default="", help="Pinecone namespace")
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Number of results to retrieve")
    parser.add_argument("--generate", "-g", action="store_true", help="Generate answers with LLM")
    parser.add_argument("--question", "-q", help="Single question (non-interactive)")
    parser.add_argument("--batch", "-b", help="Path to file with questions (one per line)")
    parser.add_argument("--no-text", action="store_true", help="Hide chunk text in output")
    
    args = parser.parse_args()
    
    if args.question:
        # Single question mode
        results = retrieve(args.question, top_k=args.top_k, namespace=args.namespace)
        print_retrieval_results(args.question, results, show_text=not args.no_text)
        
        if args.generate and results:
            context = "\n\n---\n\n".join([r['text'] for r in results])
            answer = generate_answer(args.question, context)
            print(f"\n💡 Answer:\n{answer}")
    
    elif args.batch:
        # Batch test mode
        with open(args.batch, 'r') as f:
            questions = [line.strip() for line in f if line.strip()]
        
        results = batch_test(questions, namespace=args.namespace, top_k=args.top_k)
        
        print("\n" + "="*80)
        print("📊 BATCH TEST SUMMARY")
        print("="*80)
        for r in results:
            print(f"\nQ: {r['question']}")
            print(f"   Results: {r['num_results']}, Avg Score: {r['avg_score']:.4f}")
            print(f"   Sources: {', '.join(r['sources'])}")
    
    else:
        # Interactive mode
        interactive_mode(namespace=args.namespace, top_k=args.top_k, generate=args.generate)


if __name__ == "__main__":
    main()
