#!/bin/bash
# Simple installation for Python 3.14

echo "🚀 Installing Multimodal RAG (Simplified for Python 3.14)"
echo "=========================================================="
echo ""

# Check if venv is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Please activate virtual environment first:"
    echo "   source venv/bin/activate"
    exit 1
fi

echo "Installing packages in order..."
echo ""

# Core utilities
echo "1/10 Upgrading pip..."
pip install --upgrade pip setuptools wheel -q

# Web framework
echo "2/10 Installing FastAPI..."
pip install fastapi==0.115.0 uvicorn==0.32.0 -q

# Pydantic
echo "3/10 Installing Pydantic..."
pip install pydantic==2.9.2 pydantic-settings==2.6.0 -q

# Utilities
echo "4/10 Installing utilities..."
pip install python-dotenv loguru prometheus-client python-multipart aiofiles httpx -q

# Document processing (no unstructured for now)
echo "5/10 Installing document processing..."
pip install pdf2image Pillow pdfplumber pytesseract -q

# Database
echo "6/10 Installing ChromaDB..."
pip install chromadb==0.5.23 sqlalchemy psycopg2-binary -q

# OpenAI
echo "7/10 Installing OpenAI..."
pip install openai==1.54.0 -q

# PyTorch (this takes time)
echo "8/10 Installing PyTorch (this may take 2-3 minutes)..."
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu

# Transformers
echo "9/10 Installing transformers..."
pip install transformers==4.46.3 sentence-transformers==3.3.1 huggingface-hub -q

# OCR and remaining
echo "10/10 Installing EasyOCR and final packages..."
pip install easyocr opencv-python-headless "numpy<2.0.0" tabulate -q

# Dev tools
echo "Installing dev tools..."
pip install pytest pytest-asyncio pytest-cov black ruff -q

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. python validate_setup.py"
echo "  2. make run"
echo "  3. Open http://localhost:8003/docs"
