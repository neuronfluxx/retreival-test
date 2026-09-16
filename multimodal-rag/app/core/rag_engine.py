"""RAG (Retrieval-Augmented Generation) engine for multimodal queries"""

import time
from typing import List, Optional, Dict, Any
from openai import AzureOpenAI

from app.config import get_settings
from app.utils.logger import app_logger
from app.utils.metrics import queries_total, query_duration_seconds, retrieval_results_count
from app.core.vector_store import get_vector_store
from app.core.embeddings import get_embedding_generator
from app.schemas.query import QueryRequest, QueryResponse, RetrievedChunk


class RAGEngine:
    """RAG engine for multimodal document querying"""

    def __init__(self):
        """Initialize RAG engine"""
        self.settings = get_settings()
        self.vector_store = get_vector_store()
        self.embedding_generator = get_embedding_generator()

        # Initialize Azure OpenAI for generation
        self.azure_client = AzureOpenAI(
            api_key=self.settings.azure_openai_api_key,
            api_version=self.settings.azure_openai_api_version,
            azure_endpoint=self.settings.azure_openai_endpoint
        )

        app_logger.info("RAG engine initialized")

    def query(self, request: QueryRequest) -> QueryResponse:
        """
        Process query and generate answer

        Args:
            request: Query request

        Returns:
            Query response with answer and sources
        """
        start_time = time.time()

        try:
            app_logger.info(f"Processing query: {request.query[:100]}...")

            # Step 1: Generate query embedding
            query_embedding = self.embedding_generator.generate_text_embedding(
                request.query
            )

            # Step 2: Retrieve relevant chunks
            ids, documents, metadatas, similarities = self.vector_store.query(
                collection_name=request.collection_name,
                query_embedding=query_embedding,
                top_k=request.top_k,
                filters=request.filters
            )

            # Step 3: Create retrieved chunks
            retrieved_chunks = []
            for i in range(len(ids)):
                chunk = RetrievedChunk(
                    chunk_id=ids[i],
                    document_id=metadatas[i].get("document_id", ""),
                    content=documents[i],
                    chunk_type=metadatas[i].get("type", "text"),
                    similarity_score=similarities[i],
                    page=metadatas[i].get("page", 0),
                    image_path=metadatas[i].get("image_path"),
                    metadata=metadatas[i]
                )
                retrieved_chunks.append(chunk)

            # Step 4: Rerank if requested
            if request.rerank and len(retrieved_chunks) > request.top_k:
                retrieved_chunks = self._rerank_chunks(
                    request.query,
                    retrieved_chunks
                )[:request.top_k]

            # Step 5: Generate answer
            answer = self._generate_answer(
                query=request.query,
                chunks=retrieved_chunks,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )

            # Step 6: Extract sources
            sources = list(set([
                chunk.metadata.get("filename", chunk.document_id)
                for chunk in retrieved_chunks
            ]))

            # Calculate processing time
            processing_time = time.time() - start_time

            # Update metrics
            queries_total.labels(query_type="text").inc()
            query_duration_seconds.labels(query_type="text").observe(processing_time)
            retrieval_results_count.observe(len(retrieved_chunks))

            app_logger.info(
                f"Query processed in {processing_time:.2f}s, "
                f"retrieved {len(retrieved_chunks)} chunks"
            )

            return QueryResponse(
                query=request.query,
                answer=answer,
                retrieved_chunks=retrieved_chunks,
                sources=sources,
                processing_time=processing_time,
                metadata={
                    "model": self.settings.azure_openai_deployment,
                    "collection": request.collection_name
                }
            )

        except Exception as e:
            app_logger.error(f"Query processing failed: {e}")
            raise

    def _generate_answer(
        self,
        query: str,
        chunks: List[RetrievedChunk],
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> str:
        """
        Generate answer using LLM with retrieved context

        Args:
            query: User query
            chunks: Retrieved chunks
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated answer
        """
        try:
            # Build context from retrieved chunks
            context_parts = []
            for i, chunk in enumerate(chunks, 1):
                chunk_context = f"[Source {i}]"
                if chunk.chunk_type == "table":
                    chunk_context += f" Table from page {chunk.page}:\n{chunk.content}"
                elif chunk.chunk_type == "image":
                    chunk_context += f" Image description: {chunk.content}"
                else:
                    chunk_context += f" {chunk.content}"

                context_parts.append(chunk_context)

            context = "\n\n".join(context_parts)

            # Create system prompt
            system_prompt = """You are a helpful assistant that answers questions based on the provided document context.

Instructions:
- Answer the question using only the information from the provided context
- If the context contains tables, interpret them accurately
- If the context refers to images, acknowledge them in your answer
- Cite sources using [Source X] notation
- If the answer is not in the context, say so clearly
- Be concise and accurate"""

            # Create user prompt
            user_prompt = f"""Context from documents:
{context}

Question: {query}

Please provide a comprehensive answer based on the context above."""

            # Generate response
            response = self.azure_client.chat.completions.create(
                model=self.settings.azure_openai_deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            answer = response.choices[0].message.content

            app_logger.debug(f"Generated answer: {answer[:100]}...")

            return answer

        except Exception as e:
            app_logger.error(f"Answer generation failed: {e}")
            raise

    def _rerank_chunks(
        self,
        query: str,
        chunks: List[RetrievedChunk]
    ) -> List[RetrievedChunk]:
        """
        Rerank chunks based on relevance

        Args:
            query: Query text
            chunks: Retrieved chunks

        Returns:
            Reranked chunks
        """
        # For now, just sort by similarity score
        # In production, you'd use a reranking model like Cohere rerank
        return sorted(chunks, key=lambda x: x.similarity_score, reverse=True)

    def multimodal_query(
        self,
        query_text: Optional[str] = None,
        query_image_path: Optional[str] = None,
        collection_name: str = "default",
        top_k: int = 5,
        weight_text: float = 0.5,
        weight_image: float = 0.5
    ) -> QueryResponse:
        """
        Perform multimodal query with text and/or image

        Args:
            query_text: Text query
            query_image_path: Image query path
            collection_name: Collection name
            top_k: Number of results
            weight_text: Weight for text similarity
            weight_image: Weight for image similarity

        Returns:
            Query response
        """
        start_time = time.time()

        try:
            # Generate embeddings
            text_embedding = None
            if query_text:
                text_embedding = self.embedding_generator.generate_text_embedding(
                    query_text
                )

            image_embedding = None
            if query_image_path:
                image_embedding = self.embedding_generator.generate_image_embedding(
                    query_image_path
                )

            # Hybrid search
            ids, documents, metadatas, scores = self.vector_store.hybrid_query(
                collection_name=collection_name,
                text_embedding=text_embedding,
                image_embedding=image_embedding,
                weight_text=weight_text,
                weight_image=weight_image,
                top_k=top_k
            )

            # Create retrieved chunks
            retrieved_chunks = []
            for i in range(len(ids)):
                chunk = RetrievedChunk(
                    chunk_id=ids[i],
                    document_id=metadatas[i].get("document_id", ""),
                    content=documents[i],
                    chunk_type=metadatas[i].get("type", "text"),
                    similarity_score=scores[i],
                    page=metadatas[i].get("page", 0),
                    image_path=metadatas[i].get("image_path"),
                    metadata=metadatas[i]
                )
                retrieved_chunks.append(chunk)

            # Generate answer
            query_str = query_text or "Multimodal query"
            answer = self._generate_answer(
                query=query_str,
                chunks=retrieved_chunks
            )

            # Extract sources
            sources = list(set([
                chunk.metadata.get("filename", chunk.document_id)
                for chunk in retrieved_chunks
            ]))

            processing_time = time.time() - start_time

            # Update metrics
            queries_total.labels(query_type="multimodal").inc()
            query_duration_seconds.labels(query_type="multimodal").observe(processing_time)

            app_logger.info(f"Multimodal query processed in {processing_time:.2f}s")

            return QueryResponse(
                query=query_str,
                answer=answer,
                retrieved_chunks=retrieved_chunks,
                sources=sources,
                processing_time=processing_time
            )

        except Exception as e:
            app_logger.error(f"Multimodal query failed: {e}")
            raise


# Global instance
_rag_engine: Optional[RAGEngine] = None


def get_rag_engine() -> RAGEngine:
    """Get or create global RAG engine instance"""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine
