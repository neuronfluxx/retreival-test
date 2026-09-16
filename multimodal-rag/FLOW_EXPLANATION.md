# Multimodal RAG Application Flow

Complete explanation of how the application works from start to finish.

---

## 🎯 Overview

This is a **Retrieval-Augmented Generation (RAG)** system that:
1. Ingests documents (PDFs, images)
2. Processes and extracts content
3. Generates embeddings (vector representations)
4. Stores in a vector database
5. Answers questions using retrieved context

---

## 🚀 Application Startup Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User runs: uvicorn app.main:app --reload                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. FastAPI App Initialization (app/main.py)                 │
│    - Load configuration from .env                            │
│    - Set up CORS middleware                                  │
│    - Register API routes                                     │
│    - Initialize logging                                      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Routes Registered:                                        │
│    - Health checks: /health, /ready                          │
│    - Documents: /api/v1/documents/*                          │
│    - Query: /api/v1/query, /api/v1/search                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Server Running on http://0.0.0.0:8003                    │
│    - Waiting for incoming HTTP requests                      │
│    - Hot reload enabled (watches for code changes)           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📄 Document Upload Flow (Ingestion)

When you upload a document via `POST /api/v1/documents/upload`:

```
User uploads PDF
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: API Endpoint (app/api/v1/documents.py)              │
│ ────────────────────────────────────────────────────────────│
│ • Receives file upload                                       │
│ • Validates file size (< 50MB)                               │
│ • Validates file type (.pdf, .jpg, .png, etc.)               │
│ • Saves to data/uploads/ directory                           │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Document Processor (app/core/document_processor.py) │
│ ────────────────────────────────────────────────────────────│
│ • Determines document type (PDF, image, scanned)             │
│ • Generates unique document ID                               │
│ • Routes to appropriate processing method                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: PDF Processing Pipeline                             │
│ ────────────────────────────────────────────────────────────│
│                                                               │
│ A. Text Extraction (pdfplumber)                              │
│    ├─> Extract text from each page                           │
│    ├─> Detect if text-based or scanned                       │
│    └─> Create text chunks with overlap                       │
│                                                               │
│ B. Table Extraction (pdfplumber)                             │
│    ├─> Detect tables on each page                            │
│    ├─> Parse table structure (rows, columns, cells)          │
│    └─> Convert to markdown format                            │
│                                                               │
│ C. Layout Detection (OpenCV + LayoutParser)                  │
│    ├─> Detect regions: text, title, table, figure           │
│    ├─> Extract bounding boxes                                │
│    └─> Determine reading order                               │
│                                                               │
│ D. Image Extraction (pdf2image)                              │
│    ├─> Convert pages to images (DPI: 200)                    │
│    ├─> Save as JPEG files                                    │
│    └─> Create image chunks                                   │
│                                                               │
│ E. OCR (if scanned) (EasyOCR)                                │
│    ├─> Convert PDF to images (DPI: 300)                      │
│    ├─> Run OCR on each page                                  │
│    ├─> Extract text with confidence scores                   │
│    └─> Create chunks from OCR text                           │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Chunking Strategy                                    │
│ ────────────────────────────────────────────────────────────│
│ • Chunk Size: 512 tokens (configurable in .env)             │
│ • Overlap: 50 tokens (preserves context between chunks)      │
│ • Types of Chunks:                                           │
│   ├─> Text chunks (from paragraphs)                          │
│   ├─> Table chunks (structured data)                         │
│   └─> Image chunks (page screenshots)                        │
│                                                               │
│ Example for your 11-page PDF:                                │
│   28 chunks created = ~17 text + ~11 images                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Embedding Generation (app/core/embeddings.py)       │
│ ────────────────────────────────────────────────────────────│
│                                                               │
│ A. Text Embeddings (Azure OpenAI)                            │
│    ├─> Model: text-embedding-3-large                         │
│    ├─> Dimension: 3072                                       │
│    ├─> Process: Send text → Get vector                       │
│    └─> Time: ~100-200ms per chunk                            │
│                                                               │
│ B. Image Embeddings (CLIP)                                   │
│    ├─> Model: openai/clip-vit-base-patch32                   │
│    ├─> Dimension: 512                                        │
│    ├─> Process: Load image → Extract features → Normalize   │
│    └─> Time: ~50-100ms per image                             │
│                                                               │
│ Result: Each chunk now has a vector representation           │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 6: Vector Storage (app/core/vector_store.py)           │
│ ────────────────────────────────────────────────────────────│
│ • Database: ChromaDB                                         │
│ • Location: ./rag_service/chroma_data (persistent)           │
│ • Collection: "default" (or custom name)                     │
│                                                               │
│ What's Stored:                                               │
│   For each chunk:                                            │
│   ├─> chunk_id: "doc_xxx_text_0"                             │
│   ├─> content: "actual text content..."                      │
│   ├─> embedding: [0.234, -0.123, ...] (3072 or 512 dims)    │
│   └─> metadata:                                              │
│       ├─> document_id                                        │
│       ├─> type: "text", "table", or "image"                  │
│       ├─> page: 0, 1, 2, ...                                 │
│       ├─> image_path: (if applicable)                        │
│       └─> custom metadata                                    │
│                                                               │
│ Storage Method: HNSW (Hierarchical Navigable Small World)   │
│ Distance Metric: Cosine similarity                           │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 7: Response to User                                     │
│ ────────────────────────────────────────────────────────────│
│ {                                                             │
│   "document_id": "doc_09d98ca5_9968f995",                    │
│   "filename": "Homeowners-Guide-To-Solar-PV.pdf",            │
│   "status": "completed",                                     │
│   "num_chunks": 28,                                          │
│   "processing_time": 19.02                                   │
│ }                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Query Flow (Retrieval-Augmented Generation)

When you query via `POST /api/v1/query`:

```
User asks: "What are the benefits of solar panels?"
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Query Endpoint (app/api/v1/query.py)                │
│ ────────────────────────────────────────────────────────────│
│ • Receives query text                                        │
│ • Validates parameters (top_k, collection_name, etc.)        │
│ • Passes to RAG Engine                                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: RAG Engine (app/core/rag_engine.py)                 │
│ ────────────────────────────────────────────────────────────│
│ Orchestrates the entire RAG process                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Query Embedding (app/core/embeddings.py)            │
│ ────────────────────────────────────────────────────────────│
│ • Convert query text to embedding vector                     │
│ • Model: Azure OpenAI text-embedding-3-large                 │
│ • Result: [0.456, -0.789, ...] (3072 dimensions)             │
│                                                               │
│ Example:                                                     │
│   "What are the benefits?" →                                 │
│   [0.234, -0.123, 0.567, ..., 0.890] (3072 numbers)         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Vector Search (app/core/vector_store.py)            │
│ ────────────────────────────────────────────────────────────│
│ • Search ChromaDB for similar vectors                        │
│ • Method: Cosine similarity                                  │
│ • Retrieve top_k results (default: 5)                        │
│                                                               │
│ How Similarity Works:                                        │
│   Query embedding:    [0.5, 0.3, 0.2, ...]                   │
│   Chunk 1 embedding:  [0.4, 0.4, 0.1, ...]  → Score: 0.89    │
│   Chunk 2 embedding:  [0.1, 0.8, 0.9, ...]  → Score: 0.34    │
│   Chunk 3 embedding:  [0.5, 0.2, 0.3, ...]  → Score: 0.92    │
│   ...                                                         │
│   Return top 5 highest scores                                │
│                                                               │
│ Result: List of most relevant chunks                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Context Assembly                                     │
│ ────────────────────────────────────────────────────────────│
│ • Take top 5 chunks                                          │
│ • Format as context for LLM                                  │
│                                                               │
│ Example Context:                                             │
│   [Source 1] Solar panels convert sunlight to electricity... │
│   [Source 2] Table from page 3:                              │
│   | Benefit | Description |                                  │
│   | Cost Savings | Reduce electricity bills by 50% |         │
│   [Source 3] Image description: Installation diagram...      │
│   [Source 4] Homeowners can save thousands per year...      │
│   [Source 5] Environmental benefits include...               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 6: LLM Generation (app/core/rag_engine.py)             │
│ ────────────────────────────────────────────────────────────│
│ • Model: Azure OpenAI GPT-4o-mini                            │
│ • Temperature: 0.7 (configurable)                            │
│ • Max tokens: 1500                                           │
│                                                               │
│ Prompt Structure:                                            │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ System: You are a helpful assistant...                   │ │
│ │                                                           │ │
│ │ Context: [Retrieved chunks formatted above]              │ │
│ │                                                           │ │
│ │ Question: What are the benefits of solar panels?         │ │
│ │                                                           │ │
│ │ Instructions:                                            │ │
│ │ - Answer using only the context                          │ │
│ │ - Cite sources [Source X]                                │ │
│ │ - Be accurate and concise                                │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                               │
│ LLM generates answer based on retrieved context              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 7: Response to User                                     │
│ ────────────────────────────────────────────────────────────│
│ {                                                             │
│   "query": "What are the benefits...",                       │
│   "answer": "Solar panels offer several benefits for        │
│              homeowners: 1) Significant cost savings by     │
│              reducing electricity bills [Source 1]...        │
│              2) Environmental benefits...",                  │
│   "retrieved_chunks": [                                      │
│     {                                                        │
│       "chunk_id": "doc_xxx_text_5",                          │
│       "content": "Solar panels convert...",                  │
│       "similarity_score": 0.92,                              │
│       "page": 2                                              │
│     },                                                       │
│     ...                                                      │
│   ],                                                         │
│   "sources": ["Homeowners-Guide-To-Solar-PV.pdf"],          │
│   "processing_time": 2.3                                     │
│ }                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎭 Agentic Extraction Flow (Optional Advanced Processing)

For complex documents, the system can use multiple specialized agents:

```
Document Input
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│ Orchestrator (app/agents/orchestrator.py)                   │
│ Coordinates multiple agents for document processing          │
└───┬───────────┬───────────┬─────────────────────────────────┘
    │           │           │
    ▼           ▼           ▼
┌────────┐  ┌────────┐  ┌────────┐
│ Layout │  │  OCR   │  │ Table  │  (Future: Form, Chart agents)
│ Agent  │  │ Agent  │  │ Agent  │
└───┬────┘  └───┬────┘  └───┬────┘
    │           │           │
    └───────────┴───────────┘
              │
              ▼
     Results Combined & Refined
```

**Layout Agent** (app/agents/orchestrator.py - LayoutAgent)
- Detects: text regions, tables, figures, titles
- Uses: OpenCV contours or Detectron2 models
- Output: Bounding boxes with types

**OCR Agent** (app/agents/orchestrator.py - OCRAgent)
- Extracts: Text from images
- Uses: EasyOCR
- Output: Text with confidence scores

**Orchestrator** (app/agents/orchestrator.py - AgenticOrchestrator)
- Coordinates: Multiple agents
- Refines: Results from each agent
- Iterates: If needed for better extraction

---

## 🔄 Data Flow Diagram

```
┌─────────────┐
│   User      │
│  Browser/   │
│    API      │
└──────┬──────┘
       │
       │ HTTP Requests
       ▼
┌──────────────────────────────────────────────────────────┐
│                   FastAPI Application                     │
│  ┌────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Routes   │→ │  Business   │→ │   Models    │      │
│  │  (API v1)  │  │    Logic    │  │ (CLIP, OCR) │      │
│  └────────────┘  └─────────────┘  └─────────────┘      │
└────────┬──────────────────┬───────────────┬─────────────┘
         │                  │               │
         ▼                  ▼               ▼
    ┌─────────┐      ┌──────────┐    ┌──────────┐
    │ ChromaDB│      │  Azure   │    │  Local   │
    │ Vectors │      │ OpenAI   │    │  Files   │
    │(persist)│      │   API    │    │  System  │
    └─────────┘      └──────────┘    └──────────┘
```

---

## 📊 Component Interactions

### 1. **Configuration** (app/config.py)
- Loads settings from .env
- Provides configuration to all components
- Validates environment variables

### 2. **API Layer** (app/api/v1/)
- **documents.py**: Upload, list, delete collections
- **query.py**: Query and search endpoints
- **health.py**: Health checks

### 3. **Core Business Logic** (app/core/)
- **document_processor.py**: Process documents
- **embeddings.py**: Generate vectors
- **vector_store.py**: ChromaDB interface
- **rag_engine.py**: RAG orchestration

### 4. **Models** (app/models/)
- **clip_model.py**: CLIP for image embeddings
- **ocr_models.py**: EasyOCR wrapper
- **layout_models.py**: Layout detection

### 5. **Agents** (app/agents/)
- **base_agent.py**: Abstract agent class
- **orchestrator.py**: Multi-agent coordination

### 6. **Schemas** (app/schemas/)
- **document.py**: Document data models
- **query.py**: Query request/response models
- Pydantic validation

### 7. **Utils** (app/utils/)
- **logger.py**: Structured logging
- **metrics.py**: Prometheus metrics

---

## 🎯 Key Technologies & Their Roles

| Technology | Purpose | When Used |
|------------|---------|-----------|
| **FastAPI** | Web framework | All HTTP requests |
| **Pydantic** | Data validation | Request/response validation |
| **ChromaDB** | Vector database | Storing & searching embeddings |
| **Azure OpenAI** | Text embeddings & LLM | Query & text processing |
| **CLIP** | Image embeddings | Image understanding |
| **EasyOCR** | Text extraction | Scanned documents |
| **PDFPlumber** | PDF parsing | Text & table extraction |
| **pdf2image** | PDF to images | Image extraction |
| **OpenCV** | Layout detection | Document structure |
| **PyTorch** | ML framework | CLIP & transformers |

---

## 💡 Important Concepts

### 1. **Embeddings (Vectors)**
- Convert text/images to numbers
- Similar content → similar vectors
- Enable semantic search

Example:
```
"solar panels" → [0.5, 0.3, 0.2, ...] (3072 numbers)
"photovoltaic" → [0.4, 0.4, 0.1, ...] (similar vector!)
"banana" → [0.1, 0.8, 0.9, ...] (very different vector)
```

### 2. **Chunking**
- Break large documents into smaller pieces
- Each chunk processed independently
- Overlap preserves context

Example:
```
Page 1 (1000 words) →
  Chunk 1: words 1-512 (with metadata)
  Chunk 2: words 462-974 (50 word overlap)
  Chunk 3: words 924-1000
```

### 3. **Cosine Similarity**
- Measures angle between vectors
- Range: -1 to 1 (higher = more similar)
- Used to find relevant chunks

### 4. **RAG (Retrieval-Augmented Generation)**
- Retrieval: Find relevant chunks from database
- Augmented: Add chunks as context
- Generation: LLM generates answer

---

## 🔍 Debugging & Monitoring

### View Logs
```bash
tail -f logs/app_*.log
```

### Check Metrics
```
http://localhost:8003/metrics
```

### Database Location
```
./rag_service/chroma_data/
```

### Uploaded Files
```
./data/uploads/
./data/processed/
```

---

## 🎓 Summary

**Upload Flow**: File → Validate → Process → Extract → Chunk → Embed → Store

**Query Flow**: Question → Embed → Search → Retrieve → Generate → Answer

**Key Points**:
- Everything is converted to vectors (embeddings)
- Similar vectors = similar meaning
- RAG combines retrieval + generation
- Agents handle complex document processing
- All data persists in ChromaDB

Your document is now ready to answer questions! 🚀
