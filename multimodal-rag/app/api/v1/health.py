"""Health check endpoints"""

from fastapi import APIRouter
from datetime import datetime
from app.config import get_settings
from app import __version__

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": __version__
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    settings = get_settings()

    checks = {
        "azure_openai": bool(settings.azure_openai_api_key),
        "chroma": True,  # Could add actual ChromaDB check
        "version": __version__
    }

    all_ready = all(checks.values())

    return {
        "ready": all_ready,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }
