"""Document processing pipeline with multimodal support"""

import time
import uuid
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from PIL import Image
import pdf2image
import pdfplumber
import io

from app.config import get_settings
from app.utils.logger import app_logger
from app.utils.metrics import (
    documents_processed_total,
    document_processing_duration_seconds
)
from app.schemas.document import (
    DocumentType,
    ProcessingStatus,
    DocumentChunk,
    DocumentMetadata,
    ProcessedDocument,
    BoundingBox,
    ExtractedTable,
    TableCell,
    LayoutElement
)
from app.models import get_ocr_extractor, get_layout_detector
from app.core.embeddings import get_embedding_generator


class DocumentProcessor:
    """Process various document types and extract multimodal content"""

    def __init__(self):
        """Initialize document processor"""
        self.settings = get_settings()
        self.data_dir = Path(self.settings.data_dir)
        self.upload_dir = Path(self.settings.upload_dir)
        self.processed_dir = Path(self.settings.processed_dir)

        # Create directories
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.ocr_extractor = get_ocr_extractor()
        self.layout_detector = get_layout_detector(use_deep_learning=False)
        self.embedding_generator = get_embedding_generator()

        app_logger.info("Document processor initialized")

    def process_document(
        self,
        file_path: Path,
        extract_images: bool = True,
        extract_tables: bool = True,
        use_ocr: bool = True,
        use_layout: bool = True
    ) -> ProcessedDocument:
        """
        Process document and extract multimodal content

        Args:
            file_path: Path to document file
            extract_images: Extract images from document
            extract_tables: Extract and parse tables
            use_ocr: Use OCR for text extraction
            use_layout: Use layout detection

        Returns:
            ProcessedDocument with extracted content
        """
        start_time = time.time()

        try:
            # Generate document ID
            doc_id = self._generate_document_id(file_path)

            app_logger.info(f"Processing document: {file_path.name}")

            # Determine document type
            doc_type = self._determine_document_type(file_path)

            # Process based on type
            if doc_type == DocumentType.PDF:
                chunks, layout_elements, tables = self._process_pdf(
                    file_path, doc_id, extract_images, extract_tables,
                    use_ocr, use_layout
                )
            elif doc_type == DocumentType.IMAGE:
                chunks, layout_elements, tables = self._process_image(
                    file_path, doc_id, use_ocr, use_layout
                )
            else:
                raise ValueError(f"Unsupported document type: {doc_type}")

            # Create metadata
            metadata = self._create_metadata(file_path)

            # Generate embeddings for chunks
            chunks = self._generate_embeddings(chunks)

            # Calculate processing time
            processing_time = time.time() - start_time

            # Create processed document
            processed_doc = ProcessedDocument(
                document_id=doc_id,
                filename=file_path.name,
                document_type=doc_type,
                status=ProcessingStatus.COMPLETED,
                chunks=chunks,
                layout_elements=layout_elements,
                tables=tables,
                metadata=metadata,
                processing_time=processing_time
            )

            # Update metrics
            documents_processed_total.labels(
                document_type=doc_type.value,
                status="success"
            ).inc()
            document_processing_duration_seconds.labels(
                document_type=doc_type.value
            ).observe(processing_time)

            app_logger.info(
                f"Processed {file_path.name} with {len(chunks)} chunks "
                f"in {processing_time:.2f}s"
            )

            return processed_doc

        except Exception as e:
            app_logger.error(f"Failed to process document {file_path}: {e}")
            documents_processed_total.labels(
                document_type="unknown",
                status="error"
            ).inc()
            raise

    def _process_pdf(
        self,
        file_path: Path,
        doc_id: str,
        extract_images: bool,
        extract_tables: bool,
        use_ocr: bool,
        use_layout: bool
    ) -> Tuple[List[DocumentChunk], List[LayoutElement], List[ExtractedTable]]:
        """Process PDF document"""

        chunks = []
        layout_elements = []
        tables = []

        try:
            # First, try to extract text directly (for text-based PDFs)
            with pdfplumber.open(file_path) as pdf:
                num_pages = len(pdf.pages)

                for page_num, page in enumerate(pdf.pages):
                    # Extract text
                    text = page.extract_text()

                    # Check if text exists (text-based PDF)
                    if text and len(text.strip()) > 50:
                        # Text-based PDF - chunk the text
                        page_chunks = self._chunk_text(
                            text, doc_id, page_num
                        )
                        chunks.extend(page_chunks)

                        app_logger.debug(
                            f"Extracted text from page {page_num + 1}/{num_pages}"
                        )

                    # Extract tables if requested
                    if extract_tables:
                        page_tables = self._extract_tables_from_page(
                            page, page_num
                        )
                        tables.extend(page_tables)

                        # Add table chunks
                        for table in page_tables:
                            table_chunk = self._create_table_chunk(
                                table, doc_id, page_num
                            )
                            chunks.append(table_chunk)

            # If OCR requested or no text extracted, use OCR
            if use_ocr and len(chunks) == 0:
                app_logger.info("No text found, using OCR")
                ocr_chunks, ocr_layout = self._process_pdf_with_ocr(
                    file_path, doc_id, use_layout
                )
                chunks.extend(ocr_chunks)
                layout_elements.extend(ocr_layout)

            # Extract images if requested
            if extract_images:
                image_chunks = self._extract_images_from_pdf(
                    file_path, doc_id
                )
                chunks.extend(image_chunks)

        except Exception as e:
            app_logger.error(f"PDF processing failed: {e}")
            raise

        return chunks, layout_elements, tables

    def _process_pdf_with_ocr(
        self,
        file_path: Path,
        doc_id: str,
        use_layout: bool
    ) -> Tuple[List[DocumentChunk], List[LayoutElement]]:
        """Process PDF using OCR (for scanned PDFs)"""

        chunks = []
        layout_elements = []

        try:
            # Convert PDF pages to images
            images = pdf2image.convert_from_path(
                str(file_path),
                dpi=300
            )

            app_logger.info(f"Converting PDF to {len(images)} images for OCR")

            for page_num, image in enumerate(images):
                # Detect layout if requested
                if use_layout:
                    page_layout = self.layout_detector.detect_layout(
                        image, page_num
                    )
                    layout_elements.extend(page_layout)

                # OCR extraction
                ocr_results = self.ocr_extractor.extract_text(image)

                # Create chunks from OCR results
                page_text = " ".join([r.text for r in ocr_results])
                page_chunks = self._chunk_text(page_text, doc_id, page_num)
                chunks.extend(page_chunks)

                app_logger.debug(f"OCR processed page {page_num + 1}/{len(images)}")

        except Exception as e:
            app_logger.error(f"OCR processing failed: {e}")
            raise

        return chunks, layout_elements

    def _process_image(
        self,
        file_path: Path,
        doc_id: str,
        use_ocr: bool,
        use_layout: bool
    ) -> Tuple[List[DocumentChunk], List[LayoutElement], List[ExtractedTable]]:
        """Process image document"""

        chunks = []
        layout_elements = []
        tables = []

        try:
            # Open image
            image = Image.open(file_path).convert("RGB")

            # Detect layout if requested
            if use_layout:
                layout_elements = self.layout_detector.detect_layout(image, 0)

            # OCR if requested
            if use_ocr:
                ocr_results = self.ocr_extractor.extract_text(image)
                text = " ".join([r.text for r in ocr_results])

                if text.strip():
                    text_chunks = self._chunk_text(text, doc_id, 0)
                    chunks.extend(text_chunks)

            # Save image and create image chunk
            image_filename = f"{doc_id}_img_0.jpg"
            image_path = self.processed_dir / image_filename
            image.save(image_path, "JPEG", quality=95)

            image_chunk = DocumentChunk(
                chunk_id=f"{doc_id}_img_0",
                document_id=doc_id,
                type="image",
                content=f"Image from {file_path.name}",
                image_path=str(image_path),
                page=0
            )
            chunks.append(image_chunk)

        except Exception as e:
            app_logger.error(f"Image processing failed: {e}")
            raise

        return chunks, layout_elements, tables

    def _chunk_text(
        self,
        text: str,
        doc_id: str,
        page: int
    ) -> List[DocumentChunk]:
        """Chunk text into smaller pieces with overlap"""

        chunk_size = self.settings.chunk_size
        chunk_overlap = self.settings.chunk_overlap

        chunks = []
        words = text.split()

        for i in range(0, len(words), chunk_size - chunk_overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)

            if chunk_text.strip():
                chunk_id = f"{doc_id}_text_{page}_{i}"
                chunks.append(
                    DocumentChunk(
                        chunk_id=chunk_id,
                        document_id=doc_id,
                        type="text",
                        content=chunk_text,
                        page=page
                    )
                )

        return chunks

    def _extract_tables_from_page(
        self,
        page,
        page_num: int
    ) -> List[ExtractedTable]:
        """Extract tables from PDF page"""

        tables = []

        try:
            # Extract tables using pdfplumber
            page_tables = page.extract_tables()

            for table_idx, table_data in enumerate(page_tables):
                if not table_data or len(table_data) == 0:
                    continue

                # Convert to TableCell objects
                cells = []
                for row_idx, row in enumerate(table_data):
                    for col_idx, cell_content in enumerate(row):
                        if cell_content:
                            cells.append(
                                TableCell(
                                    row=row_idx,
                                    col=col_idx,
                                    content=str(cell_content)
                                )
                            )

                # Create ExtractedTable
                extracted_table = ExtractedTable(
                    cells=cells,
                    rows=len(table_data),
                    cols=len(table_data[0]) if table_data else 0,
                    bbox=BoundingBox(x=0, y=0, width=0, height=0, page=page_num),
                    page=page_num
                )

                tables.append(extracted_table)

        except Exception as e:
            app_logger.warning(f"Table extraction failed: {e}")

        return tables

    def _create_table_chunk(
        self,
        table: ExtractedTable,
        doc_id: str,
        page: int
    ) -> DocumentChunk:
        """Create chunk from extracted table"""

        # Convert table to markdown format
        table_content = self._table_to_markdown(table)

        chunk_id = f"{doc_id}_table_{page}_{id(table)}"

        return DocumentChunk(
            chunk_id=chunk_id,
            document_id=doc_id,
            type="table",
            content=table_content,
            page=page,
            metadata={"rows": table.rows, "cols": table.cols}
        )

    def _table_to_markdown(self, table: ExtractedTable) -> str:
        """Convert table to markdown format"""

        # Create a 2D array
        grid = [["" for _ in range(table.cols)] for _ in range(table.rows)]

        # Fill the grid
        for cell in table.cells:
            if cell.row < table.rows and cell.col < table.cols:
                grid[cell.row][cell.col] = cell.content

        # Convert to markdown
        markdown_lines = []
        for row_idx, row in enumerate(grid):
            markdown_lines.append("| " + " | ".join(row) + " |")

            # Add header separator after first row
            if row_idx == 0:
                markdown_lines.append("| " + " | ".join(["---"] * len(row)) + " |")

        return "\n".join(markdown_lines)

    def _extract_images_from_pdf(
        self,
        file_path: Path,
        doc_id: str
    ) -> List[DocumentChunk]:
        """Extract images from PDF"""

        chunks = []

        try:
            # Convert PDF pages to images
            images = pdf2image.convert_from_path(
                str(file_path),
                dpi=200  # Lower DPI for storage
            )

            for page_num, image in enumerate(images):
                # Save image
                image_filename = f"{doc_id}_page_{page_num}.jpg"
                image_path = self.processed_dir / image_filename
                image.save(image_path, "JPEG", quality=85)

                # Create chunk
                chunk_id = f"{doc_id}_img_{page_num}"
                chunks.append(
                    DocumentChunk(
                        chunk_id=chunk_id,
                        document_id=doc_id,
                        type="image",
                        content=f"Page {page_num + 1} image",
                        image_path=str(image_path),
                        page=page_num
                    )
                )

        except Exception as e:
            app_logger.warning(f"Image extraction failed: {e}")

        return chunks

    def _generate_embeddings(
        self,
        chunks: List[DocumentChunk]
    ) -> List[DocumentChunk]:
        """Generate embeddings for all chunks"""

        for chunk in chunks:
            try:
                # Generate text embedding
                if chunk.content:
                    chunk.text_embedding = self.embedding_generator.generate_text_embedding(
                        chunk.content
                    )

                # Generate image embedding if image present
                if chunk.image_path and Path(chunk.image_path).exists():
                    chunk.image_embedding = self.embedding_generator.generate_image_embedding(
                        chunk.image_path
                    )

            except Exception as e:
                app_logger.warning(f"Failed to generate embedding for chunk {chunk.chunk_id}: {e}")

        return chunks

    def _determine_document_type(self, file_path: Path) -> DocumentType:
        """Determine document type from file"""

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return DocumentType.PDF
        elif suffix in [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]:
            return DocumentType.IMAGE
        else:
            return DocumentType.PDF  # Default

    def _generate_document_id(self, file_path: Path) -> str:
        """Generate unique document ID"""

        file_hash = hashlib.md5(str(file_path).encode()).hexdigest()[:8]
        return f"doc_{file_hash}_{uuid.uuid4().hex[:8]}"

    def _create_metadata(self, file_path: Path) -> DocumentMetadata:
        """Create document metadata"""

        stat = file_path.stat()

        return DocumentMetadata(
            filename=file_path.name,
            file_size=stat.st_size,
            mime_type=self._get_mime_type(file_path),
            num_pages=1  # Will be updated during processing
        )

    def _get_mime_type(self, file_path: Path) -> str:
        """Get MIME type from file extension"""

        suffix = file_path.suffix.lower()
        mime_types = {
            ".pdf": "application/pdf",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".tiff": "image/tiff",
            ".bmp": "image/bmp",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }

        return mime_types.get(suffix, "application/octet-stream")


# Global instance
_document_processor: Optional[DocumentProcessor] = None


def get_document_processor() -> DocumentProcessor:
    """Get or create global document processor instance"""
    global _document_processor
    if _document_processor is None:
        _document_processor = DocumentProcessor()
    return _document_processor
