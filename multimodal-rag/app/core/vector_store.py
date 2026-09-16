"""Vector store using ChromaDB"""

import time
import chromadb
from chromadb.config import Settings
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path

from app.config import get_settings
from app.utils.logger import app_logger
from app.utils.metrics import (
    vector_store_operations_total,
    vector_store_size
)
from app.schemas.document import DocumentChunk


class ChromaVectorStore:
    """ChromaDB vector store for multimodal embeddings"""

    def __init__(self):
        """Initialize ChromaDB client"""
        self.settings = get_settings()
        self.persist_dir = Path(self.settings.chroma_persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        app_logger.info(f"Initializing ChromaDB at {self.persist_dir}")

        try:
            # Initialize persistent client
            self.client = chromadb.PersistentClient(
                path=str(self.persist_dir),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )

            app_logger.info("ChromaDB initialized successfully")

        except Exception as e:
            app_logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def get_or_create_collection(
        self,
        collection_name: str,
        embedding_function: Optional[Any] = None
    ):
        """
        Get or create a collection

        Args:
            collection_name: Name of the collection
            embedding_function: Custom embedding function (optional)

        Returns:
            ChromaDB collection
        """
        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )

            app_logger.debug(f"Collection '{collection_name}' ready")

            return collection

        except Exception as e:
            app_logger.error(f"Failed to get/create collection: {e}")
            raise

    def add_documents(
        self,
        collection_name: str,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]]
    ) -> bool:
        """
        Add document chunks to vector store

        Args:
            collection_name: Name of collection
            chunks: List of document chunks
            embeddings: List of embedding vectors

        Returns:
            Success status
        """
        start_time = time.time()

        try:
            if not chunks or not embeddings:
                app_logger.warning("No chunks or embeddings provided")
                return False

            if len(chunks) != len(embeddings):
                raise ValueError("Number of chunks and embeddings must match")

            # Get collection
            collection = self.get_or_create_collection(collection_name)

            # Prepare data for ChromaDB
            ids = [chunk.chunk_id for chunk in chunks]
            documents = [chunk.content for chunk in chunks]
            metadatas = [
                {
                    "document_id": chunk.document_id,
                    "type": chunk.type,
                    "page": chunk.page,
                    "image_path": chunk.image_path or "",
                    **chunk.metadata
                }
                for chunk in chunks
            ]

            # Add to collection
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )

            # Update metrics
            duration = time.time() - start_time
            vector_store_operations_total.labels(
                operation="add",
                status="success"
            ).inc()
            vector_store_size.labels(collection=collection_name).set(
                collection.count()
            )

            app_logger.info(
                f"Added {len(chunks)} documents to '{collection_name}' "
                f"in {duration:.3f}s"
            )

            return True

        except Exception as e:
            app_logger.error(f"Failed to add documents: {e}")
            vector_store_operations_total.labels(
                operation="add",
                status="error"
            ).inc()
            raise

    def query(
        self,
        collection_name: str,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[str], List[str], List[Dict], List[float]]:
        """
        Query vector store for similar documents

        Args:
            collection_name: Name of collection
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filters: Metadata filters

        Returns:
            Tuple of (ids, documents, metadatas, distances)
        """
        start_time = time.time()

        try:
            # Get collection
            collection = self.get_or_create_collection(collection_name)

            # Query
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filters
            )

            # Extract results
            ids = results['ids'][0] if results['ids'] else []
            documents = results['documents'][0] if results['documents'] else []
            metadatas = results['metadatas'][0] if results['metadatas'] else []
            distances = results['distances'][0] if results['distances'] else []

            # Convert distances to similarities (cosine distance -> similarity)
            similarities = [1 - d for d in distances]

            # Update metrics
            duration = time.time() - start_time
            vector_store_operations_total.labels(
                operation="query",
                status="success"
            ).inc()

            app_logger.debug(
                f"Retrieved {len(ids)} results from '{collection_name}' "
                f"in {duration:.3f}s"
            )

            return ids, documents, metadatas, similarities

        except Exception as e:
            app_logger.error(f"Failed to query vector store: {e}")
            vector_store_operations_total.labels(
                operation="query",
                status="error"
            ).inc()
            raise

    def hybrid_query(
        self,
        collection_name: str,
        text_embedding: Optional[List[float]] = None,
        image_embedding: Optional[List[float]] = None,
        weight_text: float = 0.5,
        weight_image: float = 0.5,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[str], List[str], List[Dict], List[float]]:
        """
        Perform hybrid search with text and image embeddings

        Args:
            collection_name: Name of collection
            text_embedding: Text query embedding
            image_embedding: Image query embedding
            weight_text: Weight for text similarity
            weight_image: Weight for image similarity
            top_k: Number of results
            filters: Metadata filters

        Returns:
            Tuple of (ids, documents, metadatas, scores)
        """
        try:
            if text_embedding is None and image_embedding is None:
                raise ValueError("At least one embedding must be provided")

            # Get all relevant documents first
            collection = self.get_or_create_collection(collection_name)

            results_dict = {}

            # Query with text embedding
            if text_embedding is not None:
                ids_t, docs_t, meta_t, sims_t = self.query(
                    collection_name,
                    text_embedding,
                    top_k=top_k * 2,  # Get more for fusion
                    filters=filters
                )

                for i, doc_id in enumerate(ids_t):
                    results_dict[doc_id] = {
                        "document": docs_t[i],
                        "metadata": meta_t[i],
                        "text_score": sims_t[i],
                        "image_score": 0.0
                    }

            # Query with image embedding
            if image_embedding is not None:
                ids_i, docs_i, meta_i, sims_i = self.query(
                    collection_name,
                    image_embedding,
                    top_k=top_k * 2,
                    filters=filters
                )

                for i, doc_id in enumerate(ids_i):
                    if doc_id in results_dict:
                        results_dict[doc_id]["image_score"] = sims_i[i]
                    else:
                        results_dict[doc_id] = {
                            "document": docs_i[i],
                            "metadata": meta_i[i],
                            "text_score": 0.0,
                            "image_score": sims_i[i]
                        }

            # Compute hybrid scores
            for doc_id, data in results_dict.items():
                data["hybrid_score"] = (
                    weight_text * data["text_score"] +
                    weight_image * data["image_score"]
                )

            # Sort by hybrid score
            sorted_results = sorted(
                results_dict.items(),
                key=lambda x: x[1]["hybrid_score"],
                reverse=True
            )[:top_k]

            # Extract results
            ids = [doc_id for doc_id, _ in sorted_results]
            documents = [data["document"] for _, data in sorted_results]
            metadatas = [data["metadata"] for _, data in sorted_results]
            scores = [data["hybrid_score"] for _, data in sorted_results]

            app_logger.debug(f"Hybrid query returned {len(ids)} results")

            return ids, documents, metadatas, scores

        except Exception as e:
            app_logger.error(f"Hybrid query failed: {e}")
            raise

    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection

        Args:
            collection_name: Name of collection

        Returns:
            Success status
        """
        try:
            self.client.delete_collection(name=collection_name)
            app_logger.info(f"Deleted collection '{collection_name}'")
            return True

        except Exception as e:
            app_logger.error(f"Failed to delete collection: {e}")
            return False

    def list_collections(self) -> List[str]:
        """
        List all collections

        Returns:
            List of collection names
        """
        try:
            collections = self.client.list_collections()
            names = [c.name for c in collections]
            app_logger.debug(f"Found {len(names)} collections")
            return names

        except Exception as e:
            app_logger.error(f"Failed to list collections: {e}")
            return []

    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """
        Get collection statistics

        Args:
            collection_name: Name of collection

        Returns:
            Collection statistics
        """
        try:
            collection = self.get_or_create_collection(collection_name)
            count = collection.count()

            stats = {
                "name": collection_name,
                "count": count,
                "metadata": collection.metadata
            }

            return stats

        except Exception as e:
            app_logger.error(f"Failed to get collection stats: {e}")
            return {}


# Global instance
_vector_store: Optional[ChromaVectorStore] = None


def get_vector_store() -> ChromaVectorStore:
    """Get or create global vector store instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = ChromaVectorStore()
    return _vector_store
