"""Main FastAPI application"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST

from app.config import get_settings
from app.utils.logger import app_logger, setup_logger
from app.utils.metrics import get_metrics
from app.api.v1 import health, documents, query
from app import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    app_logger.info("Starting Multimodal RAG application...")

    # Initialize components (lazy loading will happen on first use)
    settings = get_settings()
    app_logger.info(f"Loaded configuration from .env")
    app_logger.info(f"ChromaDB persist directory: {settings.chroma_persist_dir}")
    app_logger.info(f"Data directory: {settings.data_dir}")

    yield

    # Shutdown
    app_logger.info("Shutting down Multimodal RAG application...")


# Create FastAPI app
app = FastAPI(
    title="Multimodal RAG API",
    description="Production-grade multimodal RAG system with agentic document extraction",
    version=__version__,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(
    documents.router,
    prefix="/api/v1/documents",
    tags=["Documents"]
)
app.include_router(
    query.router,
    prefix="/api/v1",
    tags=["Query"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Multimodal RAG API",
        "version": __version__,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "metrics": "/metrics",
            "upload": "/api/v1/documents/upload",
            "query": "/api/v1/query",
            "search": "/api/v1/search"
        }
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    metrics_data = get_metrics()
    return PlainTextResponse(content=metrics_data, media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    import uvicorn

    # Setup logger
    setup_logger()

    # Run application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )
