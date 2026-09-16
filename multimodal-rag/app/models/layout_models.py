"""Layout detection models"""

import cv2
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional, Dict, Any
from app.utils.logger import app_logger
from app.schemas.document import BoundingBox, LayoutElement

try:
    import layoutparser as lp
    LAYOUTPARSER_AVAILABLE = True
except ImportError:
    LAYOUTPARSER_AVAILABLE = False
    app_logger.info("layoutparser not available, using OpenCV-based layout detection")


class LayoutDetector:
    """Layout detection using various methods"""

    def __init__(self, use_deep_learning: bool = False):
        """
        Initialize layout detector

        Args:
            use_deep_learning: Use deep learning models (requires detectron2)
        """
        self.use_deep_learning = use_deep_learning

        if use_deep_learning and LAYOUTPARSER_AVAILABLE:
            try:
                # Load pre-trained layout detection model
                app_logger.info("Loading layout detection model...")
                self.model = lp.Detectron2LayoutModel(
                    'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
                    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.7],
                    label_map={
                        0: "text",
                        1: "title",
                        2: "list",
                        3: "table",
                        4: "figure"
                    }
                )
                app_logger.info("Layout detection model loaded successfully")
            except Exception as e:
                app_logger.warning(f"Failed to load deep learning model: {e}")
                self.use_deep_learning = False
                self.model = None
        else:
            self.model = None

    def detect_layout(
        self,
        image: Image.Image,
        page: int = 0
    ) -> List[LayoutElement]:
        """
        Detect document layout elements

        Args:
            image: PIL Image
            page: Page number

        Returns:
            List of layout elements
        """
        if self.use_deep_learning and self.model is not None:
            return self._detect_with_model(image, page)
        else:
            return self._detect_with_cv(image, page)

    def _detect_with_model(
        self,
        image: Image.Image,
        page: int = 0
    ) -> List[LayoutElement]:
        """Detect layout using deep learning model"""
        try:
            # Convert to numpy
            image_np = np.array(image)

            # Detect layout
            layout = self.model.detect(image_np)

            # Convert to LayoutElement schema
            elements = []
            for block in layout:
                bbox = BoundingBox(
                    x=float(block.coordinates[0]),
                    y=float(block.coordinates[1]),
                    width=float(block.coordinates[2] - block.coordinates[0]),
                    height=float(block.coordinates[3] - block.coordinates[1]),
                    page=page
                )

                elements.append(
                    LayoutElement(
                        type=block.type,
                        bbox=bbox,
                        confidence=float(block.score)
                    )
                )

            app_logger.debug(f"Detected {len(elements)} layout elements")
            return elements

        except Exception as e:
            app_logger.error(f"Layout detection failed: {e}")
            return self._detect_with_cv(image, page)

    def _detect_with_cv(
        self,
        image: Image.Image,
        page: int = 0
    ) -> List[LayoutElement]:
        """
        Detect layout using OpenCV (fallback method)

        Uses contour detection and heuristics to identify regions
        """
        try:
            # Convert to OpenCV format
            image_np = np.array(image)
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

            # Apply binary threshold
            _, binary = cv2.threshold(
                gray, 0, 255,
                cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )

            # Find contours
            contours, _ = cv2.findContours(
                binary,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            # Filter and classify contours
            elements = []
            height, width = image_np.shape[:2]
            min_area = (width * height) * 0.001  # Minimum 0.1% of image

            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    continue

                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0

                # Classify based on heuristics
                element_type = self._classify_region(
                    aspect_ratio, area, width * height
                )

                bbox = BoundingBox(
                    x=float(x),
                    y=float(y),
                    width=float(w),
                    height=float(h),
                    page=page
                )

                elements.append(
                    LayoutElement(
                        type=element_type,
                        bbox=bbox,
                        confidence=0.7
                    )
                )

            app_logger.debug(f"Detected {len(elements)} regions with CV")
            return elements

        except Exception as e:
            app_logger.error(f"CV layout detection failed: {e}")
            return []

    def _classify_region(
        self,
        aspect_ratio: float,
        area: float,
        total_area: float
    ) -> str:
        """Classify region type based on heuristics"""

        area_ratio = area / total_area

        # Large horizontal regions -> text
        if aspect_ratio > 3 and area_ratio < 0.5:
            return "text"

        # Square/rectangular large regions -> table or figure
        if 0.5 < aspect_ratio < 2:
            if area_ratio > 0.1:
                return "table" if aspect_ratio < 1.2 else "figure"

        # Wide regions at top -> title
        if aspect_ratio > 2 and area_ratio < 0.05:
            return "title"

        return "text"

    def sort_reading_order(
        self,
        elements: List[LayoutElement]
    ) -> List[LayoutElement]:
        """
        Sort layout elements in reading order (top-to-bottom, left-to-right)

        Args:
            elements: List of layout elements

        Returns:
            Sorted list of elements
        """
        # Sort by y-coordinate (top to bottom) then x-coordinate (left to right)
        sorted_elements = sorted(
            elements,
            key=lambda e: (e.bbox.y // 50, e.bbox.x)  # Group by rows
        )

        return sorted_elements


# Global instance
_layout_detector: Optional[LayoutDetector] = None


def get_layout_detector(use_deep_learning: bool = False) -> LayoutDetector:
    """Get or create global layout detector instance"""
    global _layout_detector
    if _layout_detector is None:
        _layout_detector = LayoutDetector(use_deep_learning=use_deep_learning)
    return _layout_detector
