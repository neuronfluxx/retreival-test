"""OCR models for text extraction"""

import easyocr
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional, Dict, Any
from app.utils.logger import app_logger
from app.config import get_settings
from app.schemas.document import BoundingBox


class OCRResult:
    """OCR extraction result"""

    def __init__(
        self,
        text: str,
        bbox: BoundingBox,
        confidence: float,
        language: str = "en"
    ):
        self.text = text
        self.bbox = bbox
        self.confidence = confidence
        self.language = language


class EasyOCRExtractor:
    """EasyOCR wrapper for text extraction"""

    def __init__(self):
        """Initialize EasyOCR reader"""
        self.settings = get_settings()
        self.languages = self.settings.ocr_languages
        self.use_gpu = self.settings.use_gpu_ocr

        app_logger.info(f"Initializing EasyOCR with languages: {self.languages}")

        try:
            self.reader = easyocr.Reader(
                self.languages,
                gpu=self.use_gpu
            )
            app_logger.info("EasyOCR initialized successfully")

        except Exception as e:
            app_logger.error(f"Failed to initialize EasyOCR: {e}")
            raise

    def extract_text(
        self,
        image: Image.Image,
        detail_level: int = 1,
        paragraph: bool = False
    ) -> List[OCRResult]:
        """
        Extract text from image

        Args:
            image: PIL Image
            detail_level: 0=simple, 1=detailed (with confidence)
            paragraph: Combine text into paragraphs

        Returns:
            List of OCR results with bounding boxes
        """
        try:
            # Convert PIL Image to numpy array
            image_np = np.array(image)

            # Perform OCR
            results = self.reader.readtext(
                image_np,
                detail=detail_level,
                paragraph=paragraph
            )

            # Parse results
            ocr_results = []
            for result in results:
                if detail_level == 1:
                    bbox_coords, text, confidence = result

                    # Convert bbox format: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
                    x_coords = [point[0] for point in bbox_coords]
                    y_coords = [point[1] for point in bbox_coords]

                    bbox = BoundingBox(
                        x=min(x_coords),
                        y=min(y_coords),
                        width=max(x_coords) - min(x_coords),
                        height=max(y_coords) - min(y_coords),
                        page=0
                    )

                    ocr_results.append(
                        OCRResult(
                            text=text,
                            bbox=bbox,
                            confidence=confidence
                        )
                    )
                else:
                    bbox_coords, text = result
                    x_coords = [point[0] for point in bbox_coords]
                    y_coords = [point[1] for point in bbox_coords]

                    bbox = BoundingBox(
                        x=min(x_coords),
                        y=min(y_coords),
                        width=max(x_coords) - min(x_coords),
                        height=max(y_coords) - min(y_coords),
                        page=0
                    )

                    ocr_results.append(
                        OCRResult(
                            text=text,
                            bbox=bbox,
                            confidence=1.0
                        )
                    )

            app_logger.debug(f"Extracted {len(ocr_results)} text blocks")

            return ocr_results

        except Exception as e:
            app_logger.error(f"OCR extraction failed: {e}")
            raise

    def extract_text_simple(self, image: Image.Image) -> str:
        """
        Extract all text from image as single string

        Args:
            image: PIL Image

        Returns:
            Extracted text
        """
        results = self.extract_text(image, detail_level=0)
        return " ".join([r.text for r in results])

    def detect_text_regions(
        self,
        image: Image.Image,
        min_confidence: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Detect text regions with bounding boxes

        Args:
            image: PIL Image
            min_confidence: Minimum confidence threshold

        Returns:
            List of text regions with metadata
        """
        results = self.extract_text(image, detail_level=1)

        regions = []
        for result in results:
            if result.confidence >= min_confidence:
                regions.append({
                    "text": result.text,
                    "bbox": result.bbox,
                    "confidence": result.confidence,
                    "type": "text"
                })

        return regions


# Global instance
_ocr_extractor: Optional[EasyOCRExtractor] = None


def get_ocr_extractor() -> EasyOCRExtractor:
    """Get or create global OCR extractor instance"""
    global _ocr_extractor
    if _ocr_extractor is None:
        _ocr_extractor = EasyOCRExtractor()
    return _ocr_extractor
