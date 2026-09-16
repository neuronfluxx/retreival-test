# Quick Start Guide

Get your multimodal RAG system up and running in 10 minutes.

## Prerequisites Check

Ensure you have:
- ✅ Python 3.10+ installed
- ✅ macOS with Homebrew
- ✅ Azure OpenAI API access
- ✅ 4GB+ free disk space

## 5-Minute Setup

### 1. Install System Dependencies (2 minutes)

```bash
# Install required system tools
brew install poppler tesseract
```

### 2. Set Up Python Environment (1 minute)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Python Packages (5 minutes)

```bash
# Install all dependencies
pip install -r requirements.txt
```

### 4. Verify Environment Variables (30 seconds)

Your `.env` file is already configured. Verify these key settings:

```bash
# Check Azure OpenAI configuration
grep AZURE_OPENAI .env
```

Should show:
```
AZURE_OPENAI_API_KEY=<your_key>
AZURE_OPENAI_ENDPOINT=<your_endpoint>
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
```

### 5. Create Required Directories (10 seconds)

```bash
mkdir -p data/uploads data/processed chroma_data logs
```

## Start the Service

```bash
# Option 1: Using Make
make run

# Option 2: Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8003
```

## Verify Installation

### 1. Check Health Endpoint

Open your browser or use curl:

```bash
curl http://localhost:8003/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-09-16T...",
  "version": "1.0.0"
}
```

### 2. Open API Documentation

Visit: http://localhost:8003/docs

You should see the interactive Swagger UI with all available endpoints.

### 3. Check Metrics

Visit: http://localhost:8003/metrics

You should see Prometheus metrics output.

## Your First Document

### Upload a Document

```bash
# Replace with your actual PDF path
curl -X POST "http://localhost:8003/api/v1/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf" \
  -F "collection_name=quickstart"
```

Expected response:
```json
{
  "document_id": "doc_abc123_xyz789",
  "filename": "document.pdf",
  "status": "completed",
  "message": "Document processed successfully",
  "num_chunks": 25,
  "processing_time": 3.45
}
```

### Query the Document

```bash
curl -X POST "http://localhost:8003/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this document about?",
    "collection_name": "quickstart",
    "top_k": 5
  }'
```

You'll receive an answer with retrieved context and sources!

## Using Python

### Install the Sample Script

```bash
# The sample script is already in examples/sample_usage.py
python examples/sample_usage.py
```

### Quick Python Example

```python
import requests

# Upload document
with open("document.pdf", "rb") as f:
    files = {"file": f}
    data = {"collection_name": "demo"}
    
    response = requests.post(
        "http://localhost:8003/api/v1/documents/upload",
        files=files,
        data=data
    )
    print("Upload:", response.json())

# Query document
payload = {
    "query": "What are the key findings?",
    "collection_name": "demo",
    "top_k": 5
}

response = requests.post(
    "http://localhost:8003/api/v1/query",
    json=payload
)

result = response.json()
print("\nAnswer:", result['answer'])
print("\nSources:", result['sources'])
```

## Common Commands

### Start Service
```bash
make run
# or
uvicorn app.main:app --reload
```

### Run Tests
```bash
make test
# or
pytest tests/ -v
```

### Format Code
```bash
make format
```

### View Logs
```bash
tail -f logs/app_$(date +%Y-%m-%d).log
```

### List Collections
```bash
curl http://localhost:8003/api/v1/documents/collections
```

### Delete Collection
```bash
curl -X DELETE http://localhost:8003/api/v1/documents/collections/quickstart
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution:**
```bash
# Make sure you're in the project root directory
cd /Users/shantanu/retrieval-test/multimodal-rag

# And virtual environment is activated
source venv/bin/activate
```

### Issue: EasyOCR downloading models

**First run**: EasyOCR will download language models (~50MB). This is normal and happens once.

**To pre-download:**
```bash
python -c "import easyocr; reader = easyocr.Reader(['en'])"
```

### Issue: Port 8003 already in use

**Solution:**
```bash
# Find process using port
lsof -i :8003

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8004
```

### Issue: Azure OpenAI API errors

**Check:**
1. API key is correct in `.env`
2. Endpoint URL is correct
3. Deployment names match your Azure setup
4. You have quota available

### Issue: ChromaDB errors

**Solution:**
```bash
# Clear ChromaDB data
rm -rf chroma_data/
mkdir chroma_data
```

## Next Steps

### 1. Process Your Documents

```bash
# Create a collection for your documents
# Then upload multiple files
for file in documents/*.pdf; do
    curl -X POST "http://localhost:8003/api/v1/documents/upload" \
      -F "file=@$file" \
      -F "collection_name=my_collection"
done
```

### 2. Build a UI

- See `examples/sample_usage.py` for Python client
- Use the Streamlit example in `ADVANCED_USAGE.md`
- Build your own frontend using the REST API

### 3. Customize Agents

- Edit `app/agents/orchestrator.py`
- Add custom agents in `app/agents/`
- Extend document processing in `app/core/document_processor.py`

### 4. Deploy to Production

```bash
# Using Docker
docker-compose up -d

# Using Docker manually
docker build -t multimodal-rag .
docker run -p 8003:8003 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/chroma_data:/app/chroma_data \
  multimodal-rag
```

### 5. Monitor Your System

- **Prometheus**: http://localhost:9090 (if using docker-compose)
- **Grafana**: http://localhost:3000 (if using docker-compose)
- **Metrics**: http://localhost:8003/metrics
- **Logs**: `logs/` directory

## Useful URLs

- **API Docs (Swagger)**: http://localhost:8003/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8003/redoc
- **Health Check**: http://localhost:8003/health
- **Readiness Check**: http://localhost:8003/ready
- **Prometheus Metrics**: http://localhost:8003/metrics
- **Root Info**: http://localhost:8003/

## Example Workflows

### Workflow 1: Research Paper Analysis

```bash
# 1. Upload papers
curl -X POST "http://localhost:8003/api/v1/documents/upload" \
  -F "file=@paper1.pdf" \
  -F "collection_name=research"

# 2. Query methodology
curl -X POST "http://localhost:8003/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What methodology was used?", "collection_name": "research"}'

# 3. Find tables
curl -X POST "http://localhost:8003/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "results table", "collection_name": "research", "filters": {"type": "table"}}'
```

### Workflow 2: Financial Reports

```bash
# 1. Upload annual reports
for year in 2021 2022 2023; do
    curl -X POST "http://localhost:8003/api/v1/documents/upload" \
      -F "file=@annual_report_${year}.pdf" \
      -F "collection_name=financials_${year}"
done

# 2. Query revenue trends
curl -X POST "http://localhost:8003/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "revenue by quarter", "collection_name": "financials_2023"}'
```

### Workflow 3: Image-Heavy Documents

```bash
# 1. Upload document with extract_images enabled
curl -X POST "http://localhost:8003/api/v1/documents/upload" \
  -F "file=@presentation.pdf" \
  -F "collection_name=presentations" \
  -F "extract_images=true"

# 2. Search for specific charts
curl -X POST "http://localhost:8003/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "architecture diagram", "collection_name": "presentations", "filters": {"type": "image"}}'
```

## Performance Tips

1. **Batch Processing**: Process multiple documents in parallel
2. **GPU Support**: Use GPU for CLIP embeddings (set `CLIP_DEVICE=cuda`)
3. **Caching**: Implement Redis caching for frequent queries
4. **Chunk Size**: Adjust `chunk_size` in `.env` for your use case
5. **Top-K**: Use smaller `top_k` values for faster queries

## Getting Help

- **Documentation**: See `README.md`, `SETUP.md`, `ARCHITECTURE.md`
- **Advanced Examples**: See `ADVANCED_USAGE.md`
- **API Reference**: http://localhost:8003/docs
- **Logs**: Check `logs/` directory for errors

## Summary

You now have a fully functional multimodal RAG system! The system can:

✅ Process PDFs, images, and scanned documents  
✅ Extract text, tables, and images  
✅ Generate multimodal embeddings  
✅ Perform semantic search  
✅ Answer questions with citations  
✅ Handle complex layouts and tables  

Start experimenting with your own documents and queries!
