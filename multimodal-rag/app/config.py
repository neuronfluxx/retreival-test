"""Application Configuration"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )

    # Application
    app_name: str = "Multimodal RAG"
    app_version: str = "1.0.0"
    debug: bool = False

    # Azure OpenAI
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment: str = "gpt-4o-mini"
    azure_openai_embedding_deployment: str = "text-embedding-3-large"
    azure_openai_api_version: str = "2024-02-01"

    # Vector Store
    vectorstore_provider: str = "chroma"
    chroma_persist_dir: str = "./chroma_data"

    # Data Directories
    data_dir: str = "./data"
    upload_dir: str = "./data/uploads"
    processed_dir: str = "./data/processed"

    # Document Processing
    max_file_size_mb: int = 50
    chunk_size: int = 512
    chunk_overlap: int = 50
    supported_formats: list[str] = [".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".bmp"]

    # CLIP Model
    clip_model_name: str = "openai/clip-vit-base-patch32"
    clip_device: str = "cpu"  # or "cuda" for GPU

    # OCR Settings
    ocr_languages: list[str] = ["en"]
    use_gpu_ocr: bool = False
    
    @property
    def ocr_languages_list(self) -> list[str]:
        """Get OCR languages as list, handling both string and list input"""
        if isinstance(self.ocr_languages, str):
            return [self.ocr_languages]
        return self.ocr_languages

    # Database
    postgres_user: str = "postgres"
    postgres_password: str = "123"
    postgres_db: str = "qcell_chatbot"
    database_url: str = "postgresql://postgres:123@localhost:5432/qcell_chatbot"

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 480

    # Service URLs
    rag_service_url: str = "http://localhost:8003"
    auth_service_url: str = "http://localhost:8001"
    gateway_url: str = "http://localhost:8000"

    # Tracing (OpenTelemetry)
    otel_exporter_otlp_endpoint: Optional[str] = None
    otel_service_name: str = "multimodal-rag"

    # Neo4j (for knowledge graph)
    neo4j_uri: Optional[str] = None
    neo4j_username: Optional[str] = None
    neo4j_password: Optional[str] = None

    # RAG Settings
    retrieval_top_k: int = 5
    rerank_top_k: int = 3
    temperature: float = 0.7
    max_tokens: int = 1500

    # Agent Settings
    max_agent_iterations: int = 5
    agent_timeout_seconds: int = 300


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
