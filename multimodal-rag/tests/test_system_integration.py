"""Integration tests for the multimodal RAG system"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that all core modules can be imported"""
    try:
        from app.config import get_settings
        from app.utils.logger import app_logger
        from app.core.embeddings import get_embedding_generator
        from app.core.vector_store import get_vector_store
        from app.models import get_clip_embedder, get_ocr_extractor
        
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_config_loading():
    """Test configuration loading"""
    from app.config import get_settings
    
    settings = get_settings()
    
    assert settings.azure_openai_api_key
    assert settings.azure_openai_endpoint
    assert settings.chroma_persist_dir
    assert settings.vectorstore_provider == "chroma"


def test_clip_model():
    """Test CLIP model initialization"""
    from app.models import get_clip_embedder
    
    embedder = get_clip_embedder()
    
    # Test text embedding
    text_embedding = embedder.encode_text("test document")
    assert len(text_embedding) > 0
    assert text_embedding.shape[0] == 1
    
    # Get embedding dimension
    dim = embedder.get_embedding_dimension()
    assert dim > 0


def test_vector_store():
    """Test vector store initialization"""
    from app.core.vector_store import get_vector_store
    
    vector_store = get_vector_store()
    
    # Test collection creation
    collection = vector_store.get_or_create_collection("test_collection")
    assert collection is not None
    
    # Test listing collections
    collections = vector_store.list_collections()
    assert "test_collection" in collections


def test_embedding_generator():
    """Test embedding generation"""
    from app.core.embeddings import get_embedding_generator
    
    generator = get_embedding_generator()
    
    # Test single text embedding
    text = "This is a test document"
    embedding = generator.generate_text_embedding(text)
    
    assert embedding is not None
    assert len(embedding) > 0
    assert isinstance(embedding, list)
    
    # Test batch embeddings
    texts = ["First text", "Second text", "Third text"]
    embeddings = generator.generate_text_embeddings_batch(texts)
    
    assert len(embeddings) == len(texts)
    
    # Test similarity
    sim = generator.compute_similarity(embeddings[0], embeddings[1])
    assert 0.0 <= sim <= 1.0


def test_document_processor():
    """Test document processor initialization"""
    from app.core.document_processor import get_document_processor
    
    processor = get_document_processor()
    
    assert processor.data_dir.exists()
    assert processor.upload_dir.exists()
    assert processor.processed_dir.exists()


def test_rag_engine():
    """Test RAG engine initialization"""
    from app.core.rag_engine import get_rag_engine
    
    engine = get_rag_engine()
    
    assert engine.vector_store is not None
    assert engine.embedding_generator is not None
    assert engine.azure_client is not None


def test_ocr_extractor():
    """Test OCR extractor initialization"""
    from app.models import get_ocr_extractor
    
    extractor = get_ocr_extractor()
    
    assert extractor.reader is not None
    assert extractor.languages


def test_agentic_orchestrator():
    """Test agentic orchestrator initialization"""
    from app.agents import get_orchestrator
    
    orchestrator = get_orchestrator()
    
    assert orchestrator.layout_agent is not None
    assert orchestrator.ocr_agent is not None


def test_api_schemas():
    """Test Pydantic schemas"""
    from app.schemas import (
        DocumentType,
        ProcessingStatus,
        QueryRequest,
        UploadRequest
    )
    
    # Test enum values
    assert DocumentType.PDF == "pdf"
    assert ProcessingStatus.COMPLETED == "completed"
    
    # Test schema instantiation
    query_req = QueryRequest(
        query="test query",
        collection_name="test",
        top_k=5
    )
    
    assert query_req.query == "test query"
    assert query_req.top_k == 5


def test_metrics():
    """Test metrics initialization"""
    from app.utils.metrics import (
        documents_processed_total,
        queries_total,
        embeddings_generated_total
    )
    
    # Verify metrics exist
    assert documents_processed_total is not None
    assert queries_total is not None
    assert embeddings_generated_total is not None


def test_logger():
    """Test logger configuration"""
    from app.utils.logger import app_logger
    
    # Test logging
    app_logger.info("Test log message")
    app_logger.debug("Test debug message")
    app_logger.warning("Test warning message")
    
    assert True


@pytest.mark.asyncio
async def test_fastapi_app():
    """Test FastAPI application"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    
    # Test health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    
    # Test ready endpoint
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert "ready" in data


def test_directory_structure():
    """Test required directories exist"""
    from pathlib import Path
    
    base_dir = Path(__file__).parent.parent
    
    required_dirs = [
        "app",
        "app/api",
        "app/core",
        "app/models",
        "app/agents",
        "app/schemas",
        "app/utils",
        "data",
        "logs",
        "tests"
    ]
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        assert dir_path.exists(), f"Directory {dir_name} does not exist"


def test_required_files():
    """Test required files exist"""
    from pathlib import Path
    
    base_dir = Path(__file__).parent.parent
    
    required_files = [
        ".env",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md",
        "SETUP.md",
        "app/main.py",
        "app/config.py"
    ]
    
    for file_name in required_files:
        file_path = base_dir / file_name
        assert file_path.exists(), f"File {file_name} does not exist"


if __name__ == "__main__":
    """Run tests manually"""
    pytest.main([__file__, "-v", "-s"])
