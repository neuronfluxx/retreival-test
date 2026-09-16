"""Query endpoints for RAG"""

from fastapi import APIRouter, HTTPException
from app.utils.logger import app_logger
from app.schemas.query import QueryRequest, QueryResponse, SearchResponse, RetrievedChunk
from app.core.rag_engine import get_rag_engine
from app.core.vector_store import get_vector_store
from app.core.embeddings import get_embedding_generator

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Query documents and generate answer

    Args:
        request: Query request

    Returns:
        Query response with answer and sources
    """
    try:
        app_logger.info(f"Received query: {request.query[:100]}...")

        rag_engine = get_rag_engine()
        response = rag_engine.query(request)

        return response

    except Exception as e:
        app_logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=SearchResponse)
async def search_documents(request: QueryRequest):
    """
    Search documents without generation (similarity search only)

    Args:
        request: Query request

    Returns:
        Search response with retrieved chunks
    """
    try:
        app_logger.info(f"Received search query: {request.query[:100]}...")

        # Generate query embedding
        embedding_generator = get_embedding_generator()
        query_embedding = embedding_generator.generate_text_embedding(request.query)

        # Search vector store
        vector_store = get_vector_store()
        ids, documents, metadatas, similarities = vector_store.query(
            collection_name=request.collection_name,
            query_embedding=query_embedding,
            top_k=request.top_k,
            filters=request.filters
        )

        # Create retrieved chunks
        results = []
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
            results.append(chunk)

        return SearchResponse(
            query=request.query,
            results=results,
            total_results=len(results),
            processing_time=0.0
        )

    except Exception as e:
        app_logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
