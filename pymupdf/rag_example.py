#!/usr/bin/env python3
"""
Simple RAG Example using Extracted PDF Data

This demonstrates a basic retrieval-augmented generation pattern using
the extracted PDF content.
"""

import os
import json
from pathlib import Path
from collections import defaultdict


class SimpleRAG:
    """Simple retrieval system for extracted PDF data."""
    
    def __init__(self, json_dir):
        self.json_dir = json_dir
        self.documents = []
        self.load_documents()
    
    def load_documents(self):
        """Load all JSON documents into memory."""
        print("Loading documents...")
        for json_file in Path(self.json_dir).glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract page-level chunks
            for page in data.get('pages', []):
                self.documents.append({
                    'source': data.get('source', 'unknown'),
                    'page': page.get('page_number', 'unknown'),
                    'text': page.get('text', ''),
                    'metadata': page.get('metadata', {})
                })
        
        print(f"Loaded {len(self.documents)} page chunks from {len(list(Path(self.json_dir).glob('*.json')))} documents\n")
    
    def simple_search(self, query, top_k=5):
        """
        Simple keyword-based search (in production, use semantic embeddings).
        Returns top_k most relevant chunks.
        """
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        
        results = []
        for doc in self.documents:
            text_lower = doc['text'].lower()
            
            # Simple scoring: count matching terms
            score = sum(1 for term in query_terms if term in text_lower)
            
            # Boost if exact phrase match
            if query_lower in text_lower:
                score += 10
            
            if score > 0:
                results.append({
                    'score': score,
                    'document': doc
                })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def format_context(self, results):
        """Format retrieved results as context."""
        context_parts = []
        for i, result in enumerate(results, 1):
            doc = result['document']
            context_parts.append(
                f"[Source {i}: {doc['source']}, Page {doc['page']}]\n"
                f"{doc['text'][:500]}...\n"  # First 500 chars
            )
        return "\n---\n".join(context_parts)
    
    def query(self, question, top_k=3):
        """
        RAG-style query: retrieve relevant context and format for LLM.
        """
        print(f"Query: {question}")
        print("=" * 80)
        
        # Retrieve relevant documents
        results = self.simple_search(question, top_k=top_k)
        
        if not results:
            print("No relevant documents found.\n")
            return None
        
        print(f"\nFound {len(results)} relevant chunks:\n")
        
        # Format context
        context = self.format_context(results)
        
        # Create RAG prompt
        rag_prompt = f"""Based on the following context from extracted PDF documents, answer the question.

Context:
{context}

Question: {question}

Answer: [This is where you would send to an LLM. For now, showing context only.]
"""
        
        print(rag_prompt)
        
        # Show detailed results
        print("\n" + "=" * 80)
        print("Detailed Results:")
        print("=" * 80)
        for i, result in enumerate(results, 1):
            doc = result['document']
            print(f"\n{i}. Source: {doc['source']}")
            print(f"   Page: {doc['page']}")
            print(f"   Relevance Score: {result['score']}")
            print(f"   Text Preview: {doc['text'][:200]}...")
            print()
        
        return rag_prompt


def main():
    """Demo RAG queries."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_dir = os.path.join(script_dir, "extracted_data", "json")
    
    if not os.path.exists(json_dir):
        print(f"Error: JSON directory not found: {json_dir}")
        print("Please run 'python3 extract_pdfs.py' first.")
        return
    
    # Initialize RAG system
    rag = SimpleRAG(json_dir)
    
    # Demo queries
    queries = [
        "What is the transformer architecture?",
        "How do you install solar panels?",
        "What is attention mechanism?",
    ]
    
    print("=" * 80)
    print("Simple RAG Demo - Extracted PDF Content")
    print("=" * 80)
    print()
    
    for query in queries:
        rag.query(query, top_k=2)
        print("\n" + "=" * 80 + "\n")
    
    print("\n💡 Note: This is a simple keyword-based retrieval.")
    print("   For production RAG systems, use:")
    print("   - Semantic embeddings (OpenAI, Cohere, sentence-transformers)")
    print("   - Vector databases (Pinecone, Weaviate, Chroma, FAISS)")
    print("   - LLM integration (OpenAI, Anthropic, local models)")


if __name__ == "__main__":
    main()
