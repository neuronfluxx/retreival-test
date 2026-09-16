"""Embedding generation for multimodal content"""

import time
import numpy as np
from typing import List, Optional, Dict, Any, Union
from openai import AzureOpenAI
from PIL import Image

from app.config import get_settings
from app.utils.logger import app_logger
from app.utils.metrics import (
    embeddings_generated_total,
    embedding_generation_duration_seconds
)
from app.models.clip_model import get_clip_embedder


class EmbeddingGenerator:
    """Generate embeddings for text and images"""

    def __init__(self):
        """Initialize embedding generators"""
        self.settings = get_settings()

        # Initialize Azure OpenAI for text embeddings
        self.azure_client = AzureOpenAI(
            api_key=self.settings.azure_openai_api_key,
            api_version=self.settings.azure_openai_api_version,
            azure_endpoint=self.settings.azure_openai_endpoint
        )

        # Initialize CLIP for image embeddings
        self.clip_embedder = get_clip_embedder()

        app_logger.info("Embedding generator initialized")

    def generate_text_embedding(
        self,
        text: str,
        model: Optional[str] = None
    ) -> List[float]:
        """
        Generate text embedding using Azure OpenAI

        Args:
            text: Input text
            model: Model name (defaults to config)

        Returns:
            Embedding vector
        """
        start_time = time.time()

        try:
            if not text or text.strip() == "":
                app_logger.warning("Empty text provided for embedding")
                return []

            model_name = model or self.settings.azure_openai_embedding_deployment

            response = self.azure_client.embeddings.create(
                input=text,
                model=model_name
            )

            embedding = response.data[0].embedding

            # Record metrics
            duration = time.time() - start_time
            embeddings_generated_total.labels(embedding_type="text").inc()
            embedding_generation_duration_seconds.labels(
                embedding_type="text"
            ).observe(duration)

            app_logger.debug(f"Generated text embedding in {duration:.3f}s")

            return embedding

        except Exception as e:
            app_logger.error(f"Failed to generate text embedding: {e}")
            raise

    def generate_text_embeddings_batch(
        self,
        texts: List[str],
        model: Optional[str] = None
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of input texts
            model: Model name

        Returns:
            List of embedding vectors
        """
        start_time = time.time()

        try:
            # Filter empty texts
            valid_texts = [t for t in texts if t and t.strip()]
            if not valid_texts:
                return []

            model_name = model or self.settings.azure_openai_embedding_deployment

            # Batch API call
            response = self.azure_client.embeddings.create(
                input=valid_texts,
                model=model_name
            )

            embeddings = [item.embedding for item in response.data]

            # Record metrics
            duration = time.time() - start_time
            embeddings_generated_total.labels(embedding_type="text").inc(len(embeddings))
            embedding_generation_duration_seconds.labels(
                embedding_type="text"
            ).observe(duration)

            app_logger.debug(
                f"Generated {len(embeddings)} text embeddings in {duration:.3f}s"
            )

            return embeddings

        except Exception as e:
            app_logger.error(f"Failed to generate text embeddings: {e}")
            raise

    def generate_image_embedding(
        self,
        image: Union[Image.Image, str]
    ) -> List[float]:
        """
        Generate image embedding using CLIP

        Args:
            image: PIL Image or file path

        Returns:
            Embedding vector
        """
        start_time = time.time()

        try:
            # Generate embedding using CLIP
            embedding = self.clip_embedder.encode_image(image, normalize=True)

            # Convert to list
            embedding_list = embedding[0].tolist()

            # Record metrics
            duration = time.time() - start_time
            embeddings_generated_total.labels(embedding_type="image").inc()
            embedding_generation_duration_seconds.labels(
                embedding_type="image"
            ).observe(duration)

            app_logger.debug(f"Generated image embedding in {duration:.3f}s")

            return embedding_list

        except Exception as e:
            app_logger.error(f"Failed to generate image embedding: {e}")
            raise

    def generate_image_embeddings_batch(
        self,
        images: List[Union[Image.Image, str]]
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple images

        Args:
            images: List of PIL Images or file paths

        Returns:
            List of embedding vectors
        """
        start_time = time.time()

        try:
            # Generate embeddings using CLIP
            embeddings = self.clip_embedder.encode_image(images, normalize=True)

            # Convert to list of lists
            embeddings_list = [emb.tolist() for emb in embeddings]

            # Record metrics
            duration = time.time() - start_time
            embeddings_generated_total.labels(
                embedding_type="image"
            ).inc(len(embeddings_list))
            embedding_generation_duration_seconds.labels(
                embedding_type="image"
            ).observe(duration)

            app_logger.debug(
                f"Generated {len(embeddings_list)} image embeddings in {duration:.3f}s"
            )

            return embeddings_list

        except Exception as e:
            app_logger.error(f"Failed to generate image embeddings: {e}")
            raise

    def compute_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Compute cosine similarity between two embeddings

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Similarity score (0-1)
        """
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Normalize
        vec1 = vec1 / np.linalg.norm(vec1)
        vec2 = vec2 / np.linalg.norm(vec2)

        # Compute cosine similarity
        similarity = np.dot(vec1, vec2)

        return float(similarity)

    def get_embedding_dimensions(self) -> Dict[str, int]:
        """Get embedding dimensions for text and image"""
        return {
            "text": 3072,  # Azure text-embedding-3-large
            "image": self.clip_embedder.get_embedding_dimension()  # CLIP
        }


# Global instance
_embedding_generator: Optional[EmbeddingGenerator] = None


def get_embedding_generator() -> EmbeddingGenerator:
    """Get or create global embedding generator instance"""
    global _embedding_generator
    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator()
    return _embedding_generator
