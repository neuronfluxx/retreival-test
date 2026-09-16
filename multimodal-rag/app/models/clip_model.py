"""CLIP model for image embeddings"""

import torch
import numpy as np
from PIL import Image
from typing import List, Union, Optional
from transformers import CLIPProcessor, CLIPModel
from app.utils.logger import app_logger
from app.config import get_settings


class CLIPEmbedder:
    """CLIP model wrapper for generating image and text embeddings"""

    def __init__(self):
        """Initialize CLIP model"""
        self.settings = get_settings()
        self.model_name = self.settings.clip_model_name
        self.device = self.settings.clip_device

        app_logger.info(f"Loading CLIP model: {self.model_name}")

        try:
            # Load model and processor
            self.model = CLIPModel.from_pretrained(self.model_name)
            self.processor = CLIPProcessor.from_pretrained(self.model_name)

            # Move model to device
            self.model.to(self.device)
            self.model.eval()

            app_logger.info(f"CLIP model loaded successfully on {self.device}")

        except Exception as e:
            app_logger.error(f"Failed to load CLIP model: {e}")
            raise

    def encode_image(
        self,
        images: Union[Image.Image, List[Image.Image], str, List[str]],
        normalize: bool = True
    ) -> np.ndarray:
        """
        Encode images into embeddings

        Args:
            images: Single image or list of images (PIL Image or file paths)
            normalize: Whether to normalize embeddings

        Returns:
            Image embeddings as numpy array
        """
        try:
            # Convert to list if single image
            if not isinstance(images, list):
                images = [images]

            # Load images if paths provided
            loaded_images = []
            for img in images:
                if isinstance(img, str):
                    loaded_images.append(Image.open(img).convert("RGB"))
                else:
                    loaded_images.append(img.convert("RGB"))

            # Process images
            inputs = self.processor(
                images=loaded_images,
                return_tensors="pt",
                padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Generate embeddings
            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)

                if normalize:
                    # Normalize using torch.nn.functional
                    image_features = torch.nn.functional.normalize(
                        image_features, p=2, dim=-1
                    )

            embeddings = image_features.cpu().numpy()

            app_logger.debug(f"Generated embeddings for {len(loaded_images)} images")

            return embeddings

        except Exception as e:
            app_logger.error(f"Failed to encode images: {e}")
            raise

    def encode_text(
        self,
        texts: Union[str, List[str]],
        normalize: bool = True
    ) -> np.ndarray:
        """
        Encode text into embeddings

        Args:
            texts: Single text or list of texts
            normalize: Whether to normalize embeddings

        Returns:
            Text embeddings as numpy array
        """
        try:
            # Convert to list if single text
            if not isinstance(texts, list):
                texts = [texts]

            # Process texts
            inputs = self.processor(
                text=texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=77  # CLIP's max sequence length
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Generate embeddings
            with torch.no_grad():
                text_features = self.model.get_text_features(**inputs)

                if normalize:
                    # Normalize using torch.nn.functional
                    text_features = torch.nn.functional.normalize(
                        text_features, p=2, dim=-1
                    )

            embeddings = text_features.cpu().numpy()

            app_logger.debug(f"Generated embeddings for {len(texts)} texts")

            return embeddings

        except Exception as e:
            app_logger.error(f"Failed to encode texts: {e}")
            raise

    def compute_similarity(
        self,
        image_embeddings: np.ndarray,
        text_embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Compute cosine similarity between image and text embeddings

        Args:
            image_embeddings: Image embeddings (N x D)
            text_embeddings: Text embeddings (M x D)

        Returns:
            Similarity matrix (N x M)
        """
        # Normalize embeddings
        image_embeddings = image_embeddings / np.linalg.norm(
            image_embeddings, axis=1, keepdims=True
        )
        text_embeddings = text_embeddings / np.linalg.norm(
            text_embeddings, axis=1, keepdims=True
        )

        # Compute cosine similarity
        similarity = np.dot(image_embeddings, text_embeddings.T)

        return similarity

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings"""
        return self.model.config.projection_dim


# Global instance
_clip_embedder: Optional[CLIPEmbedder] = None


def get_clip_embedder() -> CLIPEmbedder:
    """Get or create global CLIP embedder instance"""
    global _clip_embedder
    if _clip_embedder is None:
        _clip_embedder = CLIPEmbedder()
    return _clip_embedder
