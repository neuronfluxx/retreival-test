"""Document schemas"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Supported document types"""
    PDF = "pdf"
    IMAGE = "image"
    SCANNED = "scanned"
    TABLE = "table"
    MIXED = "mixed"


class ProcessingStatus(str, Enum):
    """Document processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class BoundingBox(BaseModel):
    """Bounding box coordinates"""
    x: float
    y: float
    width: float
    height: float
    page: int = 0


class LayoutElement(BaseModel):
    """Document layout element"""
    type: str  # text, image, table, heading, etc.
    bbox: BoundingBox
    content: Optional[str] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TableCell(BaseModel):
    """Table cell data"""
    row: int
    col: int
    rowspan: int = 1
    colspan: int = 1
    content: str
    bbox: Optional[BoundingBox] = None


class ExtractedTable(BaseModel):
    """Extracted table structure"""
    cells: List[TableCell]
    rows: int
    cols: int
    bbox: BoundingBox
    caption: Optional[str] = None
    page: int = 0


class DocumentChunk(BaseModel):
    """Document chunk with multimodal content"""
    chunk_id: str
    document_id: str
    type: str  # text, image, table, mixed
    content: str
    image_path: Optional[str] = None
    image_embedding: Optional[List[float]] = None
    text_embedding: Optional[List[float]] = None
    bbox: Optional[BoundingBox] = None
    page: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentMetadata(BaseModel):
    """Document metadata"""
    filename: str
    file_size: int
    mime_type: str
    num_pages: int = 1
    language: Optional[str] = "en"
    author: Optional[str] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    extra: Dict[str, Any] = Field(default_factory=dict)


class ProcessedDocument(BaseModel):
    """Processed document with extracted content"""
    document_id: str
    filename: str
    document_type: DocumentType
    status: ProcessingStatus
    chunks: List[DocumentChunk] = Field(default_factory=list)
    layout_elements: List[LayoutElement] = Field(default_factory=list)
    tables: List[ExtractedTable] = Field(default_factory=list)
    metadata: DocumentMetadata
    processing_time: float = 0.0
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UploadRequest(BaseModel):
    """Document upload request"""
    collection_name: str = "default"
    extract_images: bool = True
    extract_tables: bool = True
    use_ocr: bool = True
    use_layout_detection: bool = True


class UploadResponse(BaseModel):
    """Document upload response"""
    document_id: str
    filename: str
    status: ProcessingStatus
    message: str
    num_chunks: int = 0
    processing_time: float = 0.0
