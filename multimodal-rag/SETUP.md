# Multimodal RAG Setup Guide

Complete setup guide for the production-grade multimodal RAG system.

## Prerequisites

- Python 3.10+ (tested with 3.14.7)
- macOS (with Homebrew)
- Azure OpenAI account with API access
- At least 4GB of free disk space

## Step 1: System Dependencies

### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install poppler (for PDF processing)
brew install poppler

# Install Tesseract OCR
brew install tesseract

# Install Python 3.14 (or 3.10+)
brew install python@3.14
```

## Step 2: Python Environment

```bash
# Create virtual environment
python3.14 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

## Step 3: Install Python Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Optional: Install detectron2 for advanced layout detection
# (Requires compilation, may take some time)
pip install 'git+https://github.com/facebookresearch/detectron2.git'
```

## Step 4: Environment Configuration

Your `.env` file is already configured. Verify these key settings:

```env
# Azure OpenAI (already configured)
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large

# ChromaDB (already configured)
CHROMA_PERSIST_DIR=./chroma_data
VECTORSTORE_PROVIDER=chroma

# Data directories
DATA_DIR=./data
```

## Step 5: Create Required Directories

```bash
# Create all necessary directories
mkdir -p data/uploads data/processed chroma_data logs
```

## Step 6: Test the Installation

```bash
# Start the service
make run

# Or manually:
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

Open your browser to:
- API Docs: http://localhost:8003/docs
- Health Check: http://localhost:8003/health
- Metrics: http://localhost:8003/metrics

## Step 7: Test with Sample Document

```bash
# In a new terminal, run the sample usage script
python examples/sample_usage.py
```

Or use curl:

```bash
# Health check
curl http://localhost:8003/health

# Upload a document
curl -X POST "http://localhost:8003/api/v1/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf" \
  -F "collection_name=my_docs"

# Query documents
curl -X POST "http://localhost:8003/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main topics?",
    "collection_name": "my_docs",
    "top_k": 5
  }'
```

## Troubleshooting

### Issue: EasyOCR fails to download models

**Solution:**
```bash
# Manually download EasyOCR models
python -c "import easyocr; reader = easyocr.Reader(['en'])"
```

### Issue: ChromaDB persistence errors

**Solution:**
```bash
# Clear ChromaDB data
rm -rf chroma_data/
mkdir chroma_data
```

### Issue: Out of memory during processing

**Solution:**
- Reduce batch sizes in config
- Process documents one at a time
- Increase system memory
- Use lower DPI for image conversion

### Issue: Azure OpenAI rate limits

**Solution:**
- Add retry logic (already implemented)
- Use batch processing
- Increase rate limits with Azure support

## Performance Optimization

### For GPU Support

If you have an NVIDIA GPU:

```bash
# Install CUDA-enabled PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Update .env
CLIP_DEVICE=cuda
USE_GPU_OCR=true
```

### For Production Deployment

1. **Use Gunicorn with workers:**
```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8003
```

2. **Enable caching:**
- Add Redis for caching embeddings
- Cache OCR results for frequently accessed documents

3. **Database optimization:**
- Use PostgreSQL for metadata
- Configure ChromaDB for production

4. **Monitoring:**
- Set up Prometheus scraping at `/metrics`
- Use Grafana for visualization
- Configure OpenTelemetry tracing

## Testing

```bash
# Run all tests
make test

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Development

```bash
# Format code
make format

# Lint code
make lint

# Clean temporary files
make clean
```

## Next Steps

1. **Add your documents:**
   - Place PDFs in `data/` folder
   - Use the upload API endpoint
   - Monitor processing in logs

2. **Customize extraction:**
   - Modify agents in `app/agents/`
   - Add custom document processors
   - Extend schema extraction

3. **Integrate with your application:**
   - Use the REST API
   - Build a frontend
   - Add authentication

4. **Scale up:**
   - Deploy with Docker/Kubernetes
   - Add load balancing
   - Implement caching layer

## Support

For issues or questions:
- Check logs in `logs/` directory
- Review API documentation at `/docs`
- Enable debug logging in `.env`
