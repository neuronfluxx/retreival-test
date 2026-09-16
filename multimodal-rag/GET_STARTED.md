# 🚀 Get Started with Your Multimodal RAG System

Welcome! Your production-grade multimodal RAG system is complete and ready to use.

## ✅ What You Have

A fully functional multimodal Retrieval-Augmented Generation system that can:
- Process PDFs, images, and scanned documents
- Extract text, tables, and images
- Generate multimodal embeddings (CLIP + Azure OpenAI)
- Store in ChromaDB vector database
- Answer questions with citations
- Search with text or images
- Handle complex document layouts

## 📋 Before You Start

Make sure you have:
- ✅ Python 3.10+ (you have 3.14.7)
- ✅ macOS with Homebrew
- ✅ Azure OpenAI API access (already configured in .env)
- ✅ 4GB+ free disk space

## 🏃 Quick Start (3 Steps)

### Step 1: Install System Dependencies (1 minute)

```bash
# Install poppler and tesseract
brew install poppler tesseract
```

### Step 2: Install Python Packages (5 minutes)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Start the Service (30 seconds)

```bash
# Run the validation first (optional but recommended)
python validate_setup.py

# Start the service
make run
# or
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

You should see:
```
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8003
```

## 🧪 Test Your Installation

### 1. Check Health
```bash
curl http://localhost:8003/health
```

Should return:
```json
{"status": "healthy", "timestamp": "...", "version": "1.0.0"}
```

### 2. Open API Documentation
Visit: http://localhost:8003/docs

You'll see the interactive Swagger UI with all endpoints.

### 3. Upload Your First Document

```bash
# Replace with your PDF path
curl -X POST "http://localhost:8003/api/v1/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf" \
  -F "collection_name=my_first_collection"
```

### 4. Query Your Document

```bash
curl -X POST "http://localhost:8003/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this document about?",
    "collection_name": "my_first_collection",
    "top_k": 5
  }'
```

## 📚 Documentation Guide

Your project includes comprehensive documentation:

1. **GET_STARTED.md** (this file) - Start here
2. **QUICKSTART.md** - 10-minute quick start guide
3. **README.md** - Project overview and architecture
4. **SETUP.md** - Detailed installation instructions
5. **ARCHITECTURE.md** - System design and components
6. **FEATURES.md** - Complete feature list
7. **ADVANCED_USAGE.md** - Advanced patterns and examples
8. **STATUS.md** - Current project status
9. **PROJECT_SUMMARY.md** - Project overview

## 🎯 What to Read Based on Your Need

### I want to get started quickly
→ Read: **QUICKSTART.md**

### I want detailed setup instructions
→ Read: **SETUP.md**

### I'm having installation issues
→ Run: `python validate_setup.py`  
→ Read: **SETUP.md** (Troubleshooting section)

### I want to understand the architecture
→ Read: **ARCHITECTURE.md**

### I want to see what features are available
→ Read: **FEATURES.md**

### I want advanced examples and patterns
→ Read: **ADVANCED_USAGE.md**

### I want to deploy to production
→ Read: **ARCHITECTURE.md** (Deployment section)  
→ Use: `docker-compose up -d`

## 🔧 Common Operations

### Start the service
```bash
make run
```

### Run tests
```bash
make test
```

### Format code
```bash
make format
```

### View logs
```bash
tail -f logs/app_$(date +%Y-%m-%d).log
```

### Stop the service
```
Press Ctrl+C in the terminal
```

### Deploy with Docker
```bash
docker-compose up -d
```

## 📖 Example: Complete Workflow

```python
import requests

BASE_URL = "http://localhost:8003"

# 1. Upload a document
with open("document.pdf", "rb") as f:
    files = {"file": f}
    data = {"collection_name": "research"}
    
    response = requests.post(
        f"{BASE_URL}/api/v1/documents/upload",
        files=files,
        data=data
    )
    print("Upload:", response.json())

# 2. Query the document
payload = {
    "query": "What are the key findings?",
    "collection_name": "research",
    "top_k": 5
}

response = requests.post(
    f"{BASE_URL}/api/v1/query",
    json=payload
)

result = response.json()
print("\nAnswer:", result['answer'])
print("\nSources:", result['sources'])

# 3. Search for specific content
payload = {
    "query": "methodology section",
    "collection_name": "research",
    "filters": {"type": "text"}
}

response = requests.post(
    f"{BASE_URL}/api/v1/search",
    json=payload
)

print("\nSearch results:", len(response.json()['results']))
```

## 🐛 Troubleshooting

### Service won't start
```bash
# Check if port is in use
lsof -i :8003

# Kill existing process if needed
kill -9 <PID>

# Check logs
cat logs/app_*.log
```

### Import errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Azure OpenAI errors
```bash
# Verify .env configuration
grep AZURE_OPENAI .env

# Check API key is set
echo $AZURE_OPENAI_API_KEY
```

### ChromaDB errors
```bash
# Clear and recreate database
rm -rf chroma_data/
mkdir chroma_data
```

## 🚀 Next Steps

### 1. Explore the API
Visit: http://localhost:8003/docs

Try the interactive endpoints directly in Swagger UI.

### 2. Upload Your Documents
```bash
# Upload multiple documents to a collection
for file in documents/*.pdf; do
    curl -X POST "http://localhost:8003/api/v1/documents/upload" \
      -F "file=@$file" \
      -F "collection_name=my_collection"
done
```

### 3. Build a UI
Check `examples/sample_usage.py` for Python examples, or see `ADVANCED_USAGE.md` for Streamlit integration.

### 4. Customize for Your Use Case
- Add custom agents in `app/agents/`
- Extend document processors in `app/core/`
- Add custom embeddings in `app/models/`

### 5. Deploy to Production
```bash
# Using Docker Compose
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f
```

## 📊 Monitoring

### View Metrics
http://localhost:8003/metrics

### Prometheus (if using Docker Compose)
http://localhost:9090

### Grafana (if using Docker Compose)
http://localhost:3000 (admin/admin)

## 🔗 Important Links

- **Application**: http://localhost:8003
- **API Docs**: http://localhost:8003/docs
- **Health Check**: http://localhost:8003/health
- **Metrics**: http://localhost:8003/metrics

## 💡 Tips

1. **Start small**: Upload a single document first, test queries
2. **Check logs**: Monitor `logs/` directory for issues
3. **Use validation**: Run `python validate_setup.py` if something doesn't work
4. **Read docs**: Each markdown file has specific information
5. **Experiment**: Try different query types and filters

## 🤝 Need Help?

1. Run the validation script: `python validate_setup.py`
2. Check the appropriate documentation file (see guide above)
3. Review logs in `logs/` directory
4. Check API documentation at `/docs`

## ✅ Success Checklist

- [ ] System dependencies installed (poppler, tesseract)
- [ ] Python environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Validation passed (`python validate_setup.py`)
- [ ] Service started (`make run`)
- [ ] Health check passed (http://localhost:8003/health)
- [ ] API docs accessible (http://localhost:8003/docs)
- [ ] First document uploaded successfully
- [ ] First query returned results

## 🎉 You're Ready!

Your multimodal RAG system is ready to process documents and answer questions. Start uploading your documents and querying!

**Happy building! 🚀**
