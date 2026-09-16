"""Agentic orchestrator for document extraction"""

import time
from typing import Dict, Any, List, Optional
from PIL import Image

from app.utils.logger import app_logger
from app.utils.metrics import agent_iterations_total, agent_execution_duration_seconds
from app.config import get_settings
from app.agents.base_agent import BaseAgent, AgentResult, AgentStatus
from app.models import get_ocr_extractor, get_layout_detector
from app.schemas.document import LayoutElement


class LayoutAgent(BaseAgent):
    """Agent for layout detection"""

    def __init__(self):
        super().__init__("LayoutAgent")
        self.layout_detector = get_layout_detector(use_deep_learning=False)

    def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """Detect document layout"""
        start_time = time.time()
        self.log_execution("Starting layout detection")

        try:
            image = input_data.get("image")
            page = input_data.get("page", 0)

            if not image:
                raise ValueError("No image provided")

            # Detect layout
            layout_elements = self.layout_detector.detect_layout(image, page)

            # Sort in reading order
            sorted_elements = self.layout_detector.sort_reading_order(layout_elements)

            duration = time.time() - start_time
            agent_iterations_total.labels(agent_type="layout").inc()
            agent_execution_duration_seconds.labels(agent_type="layout").observe(duration)

            self.log_execution(f"Detected {len(sorted_elements)} layout elements")

            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                data={"layout_elements": sorted_elements},
                metadata={"duration": duration, "num_elements": len(sorted_elements)}
            )

        except Exception as e:
            self.log_error(f"Layout detection failed: {e}")
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                data={},
                metadata={},
                error=str(e)
            )


class OCRAgent(BaseAgent):
    """Agent for OCR text extraction"""

    def __init__(self):
        super().__init__("OCRAgent")
        self.ocr_extractor = get_ocr_extractor()

    def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """Extract text using OCR"""
        start_time = time.time()
        self.log_execution("Starting OCR extraction")

        try:
            image = input_data.get("image")
            layout_elements = input_data.get("layout_elements", [])

            if not image:
                raise ValueError("No image provided")

            # Extract text from entire image
            ocr_results = self.ocr_extractor.extract_text(image, detail_level=1)

            # Organize by layout regions if available
            text_by_region = {}
            if layout_elements:
                for elem in layout_elements:
                    region_text = []
                    for ocr_result in ocr_results:
                        if self._is_text_in_region(ocr_result.bbox, elem.bbox):
                            region_text.append(ocr_result.text)

                    if region_text:
                        text_by_region[elem.type] = " ".join(region_text)
            else:
                # No layout, just combine all text
                text_by_region["text"] = " ".join([r.text for r in ocr_results])

            duration = time.time() - start_time
            agent_iterations_total.labels(agent_type="ocr").inc()
            agent_execution_duration_seconds.labels(agent_type="ocr").observe(duration)

            self.log_execution(f"Extracted {len(ocr_results)} text blocks")

            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                data={
                    "ocr_results": ocr_results,
                    "text_by_region": text_by_region
                },
                metadata={"duration": duration, "num_blocks": len(ocr_results)}
            )

        except Exception as e:
            self.log_error(f"OCR extraction failed: {e}")
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                data={},
                metadata={},
                error=str(e)
            )

    def _is_text_in_region(self, text_bbox, region_bbox) -> bool:
        """Check if text bounding box is within region"""
        return (
            text_bbox.x >= region_bbox.x and
            text_bbox.y >= region_bbox.y and
            (text_bbox.x + text_bbox.width) <= (region_bbox.x + region_bbox.width) and
            (text_bbox.y + text_bbox.height) <= (region_bbox.y + region_bbox.height)
        )


class AgenticOrchestrator:
    """Orchestrates multiple agents for document extraction"""

    def __init__(self):
        """Initialize orchestrator with agents"""
        self.settings = get_settings()
        self.layout_agent = LayoutAgent()
        self.ocr_agent = OCRAgent()

        app_logger.info("Agentic orchestrator initialized")

    def process_document(
        self,
        image: Image.Image,
        page: int = 0,
        use_layout: bool = True,
        use_ocr: bool = True
    ) -> Dict[str, Any]:
        """
        Process document using multi-agent workflow

        Args:
            image: PIL Image
            page: Page number
            use_layout: Enable layout detection
            use_ocr: Enable OCR extraction

        Returns:
            Processed document data
        """
        start_time = time.time()
        results = {}

        try:
            app_logger.info(f"Starting agentic extraction for page {page}")

            # Step 1: Layout Detection
            layout_result = None
            if use_layout:
                layout_result = self.layout_agent.execute({
                    "image": image,
                    "page": page
                })
                results["layout"] = layout_result

            # Step 2: OCR Extraction
            if use_ocr:
                ocr_input = {
                    "image": image,
                    "layout_elements": (
                        layout_result.data.get("layout_elements", [])
                        if layout_result and layout_result.status == AgentStatus.COMPLETED
                        else []
                    )
                }

                ocr_result = self.ocr_agent.execute(ocr_input)
                results["ocr"] = ocr_result

            # Step 3: Refinement (if needed)
            # This is where additional agents could be added for:
            # - Table parsing
            # - Form extraction
            # - Chart understanding
            # - Key-value pair extraction

            duration = time.time() - start_time
            results["processing_time"] = duration

            app_logger.info(f"Agentic extraction completed in {duration:.2f}s")

            return results

        except Exception as e:
            app_logger.error(f"Agentic extraction failed: {e}")
            raise

    def extract_structured_data(
        self,
        image: Image.Image,
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract structured data based on schema

        Args:
            image: PIL Image
            schema: Expected data schema

        Returns:
            Extracted structured data
        """
        # This would use vision-language models to extract specific fields
        # based on the schema definition
        # For now, return basic OCR extraction
        results = self.process_document(image, use_layout=True, use_ocr=True)

        ocr_result = results.get("ocr")
        if ocr_result and ocr_result.status == AgentStatus.COMPLETED:
            return ocr_result.data.get("text_by_region", {})

        return {}


# Global instance
_orchestrator: Optional[AgenticOrchestrator] = None


def get_orchestrator() -> AgenticOrchestrator:
    """Get or create global orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgenticOrchestrator()
    return _orchestrator
