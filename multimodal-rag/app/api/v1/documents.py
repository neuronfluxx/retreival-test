"""Document upload and management endpoints"""

import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.utils.logger import app_logger
from app.schemas.document import UploadResponse, ProcessingStatus
from app.core.document_processor import get_document_processor
from app.core.vector_store import get_vector_store


router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    collection_name: str = Form("default"),
    extract_images: bool = Form(True),
    extract_tables: bool = Form(True),
    use_ocr: bool = Form(True),
    use_layout_detection: bool = Form(True)
):
    """
    Upload and process a document

    Args:
        file: Document file (PDF, image)
        collection_name: Collection to store embeddings
        extract_images: Extract images from document
        extract_tables: Extract tables from document
        use_ocr: Use OCR for text extraction
        use_layout_detection: Use layout detection

    Returns:
        Upload response with processing status
    """
    settings = get_settings()
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    try:
        app_logger.info(f"Uploading document: {file.filename}")

        # Validate file size
        file_size = 0
        temp_file = upload_dir / file.filename
        with temp_file.open("wb") as buffer:
            while chunk := await file.read(8192):
                file_size += len(chunk)
                buffer.write(chunk)

                if file_size > settings.max_file_size_mb * 1024 * 1024:
                    temp_file.unlink()
                    raise HTTPException(
                        status_code=413,
                        detail=f"File too large (max {settings.max_file_size_mb}MB)"
                    )

        # Validate file type
        if temp_file.suffix.lower() not in settings.supported_formats:
            temp_file.unlink()
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported: {settings.supported_formats}"
            )

        # Process document
        processor = get_document_processor()
        processed_doc = processor.process_document(
            file_path=temp_file,
            extract_images=extract_images,
            extract_tables=extract_tables,
            use_ocr=use_ocr,
            use_layout=use_layout_detection
        )

        # Store in vector database
        vector_store = get_vector_store()

        # Separate chunks by embedding type
        text_chunks = []
        text_embeddings = []
        for chunk in processed_doc.chunks:
            if chunk.text_embedding:
                text_chunks.append(chunk)
                text_embeddings.append(chunk.text_embedding)

        # Add to vector store
        if text_chunks:
            vector_store.add_documents(
                collection_name=collection_name,
                chunks=text_chunks,
                embeddings=text_embeddings
            )

        app_logger.info(
            f"Document {file.filename} processed successfully, "
            f"{len(text_chunks)} chunks added to {collection_name}"
        )

        return UploadResponse(
            document_id=processed_doc.document_id,
            filename=file.filename,
            status=ProcessingStatus.COMPLETED,
            message="Document processed successfully",
            num_chunks=len(text_chunks),
            processing_time=processed_doc.processing_time
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Document upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collections")
async def list_collections():
    """List all collections"""
    try:
        vector_store = get_vector_store()
        collections = vector_store.list_collections()

        # Get stats for each collection
        collection_stats = []
        for name in collections:
            stats = vector_store.get_collection_stats(name)
            collection_stats.append(stats)

        return {
            "collections": collection_stats,
            "total": len(collections)
        }

    except Exception as e:
        app_logger.error(f"Failed to list collections: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str):
    """Delete a collection"""
    try:
        vector_store = get_vector_store()
        success = vector_store.delete_collection(collection_name)

        if success:
            return {"message": f"Collection '{collection_name}' deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Collection not found")

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Failed to delete collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))
