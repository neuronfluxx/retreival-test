"""Query schemas"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Query request for RAG system"""
    query: str = Field(..., min_length=1, description="Query text")
    collection_name: str = "default"
    top_k: int = Field(5, ge=1, le=20, description="Number of results to retrieve")
    include_images: bool = True
    include_tables: bool = True
    filters: Optional[Dict[str, Any]] = None
    rerank: bool = True
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(1500, ge=100, le=4000)


class MultimodalQueryRequest(BaseModel):
    """Multimodal query with text and/or image"""
    query_text: Optional[str] = None
    query_image_base64: Optional[str] = None
    collection_name: str = "default"
    top_k: int = Field(5, ge=1, le=20)
    similarity_threshold: float = Field(0.7, ge=0.0, le=1.0)
    weight_text: float = Field(0.5, ge=0.0, le=1.0)
    weight_image: float = Field(0.5, ge=0.0, le=1.0)


class RetrievedChunk(BaseModel):
    """Retrieved chunk with similarity score"""
    chunk_id: str
    document_id: str
    content: str
    chunk_type: str
    similarity_score: float
    page: int = 0
    image_path: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    """Query response with generated answer"""
    query: str
    answer: str
    retrieved_chunks: List[RetrievedChunk] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    processing_time: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    """Search response for similarity search"""
    query: str
    results: List[RetrievedChunk] = Field(default_factory=list)
    total_results: int = 0
    processing_time: float = 0.0
