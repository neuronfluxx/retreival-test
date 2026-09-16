#!/bin/bash
# Multimodal RAG Installation Script

set -e  # Exit on error

echo "🚀 Multimodal RAG Installation"
echo "================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo ""
    echo "⚠️  Virtual environment not activated!"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

echo "✓ Virtual environment active"
echo ""

# Install core packages first (fast)
echo "📦 Installing core packages..."
pip install --upgrade pip setuptools wheel

echo ""
echo "📦 Installing FastAPI and web framework..."
pip install fastapi uvicorn[standard] pydantic pydantic-settings python-dotenv

echo ""
echo "📦 Installing utilities..."
pip install loguru prometheus-client python-multipart aiofiles httpx

echo ""
echo "📦 Installing document processing..."
pip install pdf2image Pillow pdfplumber pytesseract

echo ""
echo "📦 Installing database..."
pip install chromadb sqlalchemy psycopg2-binary

echo ""
echo "📦 Installing Azure OpenAI..."
pip install openai

echo ""
echo "📦 Installing PyTorch (this may take a while)..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

echo ""
echo "📦 Installing transformers and embeddings..."
pip install transformers sentence-transformers huggingface-hub

echo ""
echo "📦 Installing EasyOCR..."
pip install easyocr

echo ""
echo "📦 Installing OpenCV..."
pip install opencv-python-headless

echo ""
echo "📦 Installing remaining packages..."
pip install unstructured tabulate numpy"<2.0.0"

echo ""
echo "📦 Installing development tools..."
pip install pytest pytest-asyncio pytest-cov black ruff

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Run validation: python validate_setup.py"
echo "2. Start service: make run"
echo "3. Open docs: http://localhost:8003/docs"
