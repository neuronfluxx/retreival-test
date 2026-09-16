# Multimodal RAG System

A production-grade multimodal Retrieval-Augmented Generation (RAG) system with agentic document extraction capabilities.

## Features

- **Multi-format Document Processing**: PDFs, images, scanned documents, tables, handwriting
- **Advanced OCR**: EasyOCR with layout detection and reading order
- **Multimodal Embeddings**: CLIP for images, Azure OpenAI for text
- **Agentic Extraction**: Multi-step document processing workflow
- **Vector Storage**: ChromaDB with persistence
- **Production Ready**: FastAPI, monitoring, error handling, logging

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Document Upload                             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Document Processing Agent                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Layout       │  │ OCR          │  │ Table        │          │
│  │ Detection    │──▶│ Extraction   │──▶│ Parsing      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Multimodal Chunking                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Text Chunks  │  │ Image Chunks │  │ Table Chunks │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Embedding Generation                                │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │ Text Embeddings  │         │ Image Embeddings │             │
│  │ (Azure OpenAI)   │         │ (CLIP)           │             │
│  └──────────────────┘         └──────────────────┘             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ChromaDB Storage                               │
│  (Multimodal vectors with metadata)                             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Retrieval & Generation                              │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │ Hybrid Search    │────────▶│ LLM Generation   │             │
│  │ (Text + Images)  │         │ (Azure GPT-4o)   │             │
│  └──────────────────┘         └──────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

1. Install Python 3.14.7 (or 3.10+)

2. Install system dependencies:
```bash
# macOS
brew install poppler tesseract

# For detectron2 (optional but recommended for layout detection)
pip install 'git+https://github.com/facebookresearch/detectron2.git'
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (see `.env` file)

## Usage

### Start the service

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

### API Endpoints

#### 1. Upload and Process Document
```bash
curl -X POST "http://localhost:8003/api/v1/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "collection_name=my_docs"
```

#### 2. Query Documents
```bash
curl -X POST "http://localhost:8003/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key findings?",
    "collection_name": "my_docs",
    "top_k": 5,
    "include_images": true
  }'
```

#### 3. Multimodal Search
```bash
curl -X POST "http://localhost:8003/api/v1/search/multimodal" \
  -H "Content-Type: multipart/form-data" \
  -F "query_text=financial charts" \
  -F "query_image=@reference.jpg" \
  -F "collection_name=my_docs"
```

## Project Structure

```
multimodal-rag/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration
│   ├── api/
│   │   └── v1/
│   │       ├── documents.py    # Document endpoints
│   │       ├── query.py        # Query endpoints
│   │       └── health.py       # Health checks
│   ├── core/
│   │   ├── document_processor.py    # Document processing pipeline
│   │   ├── agentic_extractor.py     # Agentic extraction workflow
│   │   ├── embeddings.py            # Embedding generation
│   │   ├── vector_store.py          # ChromaDB interface
│   │   └── rag_engine.py            # RAG orchestration
│   ├── models/
│   │   ├── ocr_models.py           # OCR models
│   │   ├── layout_models.py        # Layout detection
│   │   └── clip_model.py           # CLIP embeddings
│   ├── agents/
│   │   ├── base_agent.py           # Base agent class
│   │   ├── layout_agent.py         # Layout detection agent
│   │   ├── ocr_agent.py            # OCR extraction agent
│   │   ├── table_agent.py          # Table parsing agent
│   │   └── orchestrator.py         # Agent orchestrator
│   ├── schemas/
│   │   ├── document.py             # Document schemas
│   │   ├── query.py                # Query schemas
│   │   └── response.py             # Response schemas
│   └── utils/
│       ├── logger.py               # Logging setup
│       ├── metrics.py              # Prometheus metrics
│       └── helpers.py              # Utility functions
├── tests/
│   ├── test_document_processor.py
│   ├── test_embeddings.py
│   └── test_rag_engine.py
├── data/                           # Input documents
├── chroma_data/                    # ChromaDB persistence
├── logs/                           # Application logs
├── .env
├── requirements.txt
└── README.md
```

## Advanced Features

### Agentic Document Extraction

The system uses a multi-agent approach:

1. **Layout Agent**: Detects document structure (headers, paragraphs, tables, images)
2. **OCR Agent**: Extracts text with reading order
3. **Table Agent**: Parses complex tables with merged cells
4. **Image Agent**: Processes and embeds images
5. **Orchestrator**: Coordinates agents and refines extraction

### Supported Document Types

- ✅ PDFs (text-based and scanned)
- ✅ Images (JPG, PNG, TIFF)
- ✅ Tables (simple and complex with merged cells)
- ✅ Charts and diagrams
- ✅ Handwritten text
- ✅ Forms and invoices
- ✅ Multi-column layouts
- ✅ Mixed content (text + images + tables)

## Configuration

Key environment variables:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large

# ChromaDB
CHROMA_PERSIST_DIR=./chroma_data
VECTORSTORE_PROVIDER=chroma

# Data Directory
DATA_DIR=./data
```

## Monitoring

- Prometheus metrics at `/metrics`
- Health check at `/health`
- OpenTelemetry tracing support
- Structured logging with Loguru

## Testing

```bash
pytest tests/ -v --cov=app
```

## License

MIT
