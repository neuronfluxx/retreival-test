# Multimodal RAG Architecture

Detailed architecture documentation for the multimodal RAG system with agentic document extraction.

## System Overview

This system implements a production-grade multimodal RAG (Retrieval-Augmented Generation) pipeline inspired by DeepLearning.AI's Document AI course, with the following key capabilities:

1. **Multimodal Document Processing**: Handles PDFs, images, tables, charts, and mixed content
2. **Agentic Extraction**: Multi-step, iterative document processing workflow
3. **CLIP-based Image Understanding**: Semantic image search and retrieval
4. **Hybrid Vector Search**: Combined text and image similarity search
5. **Production-ready API**: FastAPI with monitoring, logging, and metrics

## Core Components

### 1. Document Processing Pipeline

```
Input Document → Layout Detection → OCR → Table Extraction → Image Extraction
                       ↓
              Chunking & Embedding Generation
                       ↓
                  Vector Storage
```

**Key Classes:**
- `DocumentProcessor`: Orchestrates document processing
- `LayoutDetector`: Detects document structure (headings, paragraphs, tables, figures)
- `EasyOCRExtractor`: Extracts text from images and scanned documents
- `EmbeddingGenerator`: Generates text and image embeddings

**Supported Formats:**
- Text-based PDFs
- Scanned PDFs (with OCR)
- Images (JPG, PNG, TIFF, BMP)
- Tables (simple and complex)
- Mixed content documents

### 2. Agentic Document Extraction Framework

The agentic framework processes documents through multiple specialized agents:

```
┌─────────────────────────────────────┐
│     AgenticOrchestrator             │
│                                     │
│  ┌───────────────┐                 │
│  │ LayoutAgent   │                 │
│  │ - Detects     │                 │
│  │   structure   │                 │
│  └───────┬───────┘                 │
│          │                          │
│          ▼                          │
│  ┌───────────────┐                 │
│  │ OCRAgent      │                 │
│  │ - Extracts    │                 │
│  │   text        │                 │
│  └───────┬───────┘                 │
│          │                          │
│          ▼                          │
│  ┌───────────────┐                 │
│  │ TableAgent    │ (Future)        │
│  │ - Parses      │                 │
│  │   tables      │                 │
│  └───────────────┘                 │
│                                     │
│  ┌───────────────┐                 │
│  │ FormAgent     │ (Future)        │
│  │ - Extracts    │                 │
│  │   key-values  │                 │
│  └───────────────┘                 │
└─────────────────────────────────────┘
```

**Agent Workflow:**

1. **LayoutAgent**
   - Input: Document image
   - Process: Detect regions (text, table, figure, title)
   - Output: Bounding boxes with types
   - Uses: OpenCV contours or Detectron2 models

2. **OCRAgent**
   - Input: Document image + layout regions
   - Process: Extract text from each region
   - Output: Text organized by region type
   - Uses: EasyOCR with multi-language support

3. **TableAgent** (Extensible)
   - Input: Table regions
   - Process: Parse cell structure, handle merged cells
   - Output: Structured table data (JSON/Markdown)
   - Uses: PDFPlumber, Camelot

4. **FormAgent** (Extensible)
   - Input: Form/invoice images
   - Process: Extract key-value pairs
   - Output: Structured data matching schema
   - Uses: Vision-language models

### 3. Multimodal Embeddings

**Text Embeddings:**
- Model: Azure OpenAI `text-embedding-3-large`
- Dimension: 3072
- Use case: Semantic text search

**Image Embeddings:**
- Model: CLIP `openai/clip-vit-base-patch32`
- Dimension: 512
- Use case: Image similarity and text-image matching

**Hybrid Search:**
```python
hybrid_score = (weight_text * text_similarity) + 
               (weight_image * image_similarity)
```

### 4. Vector Storage (ChromaDB)

**Collections:**
- Each collection stores document chunks
- Metadata includes: document_id, type, page, image_path
- Supports filtering by metadata

**Storage Structure:**
```
ChromaDB Collection
├── Text Chunks (with text embeddings)
├── Image Chunks (with image embeddings)
├── Table Chunks (with text embeddings)
└── Mixed Chunks (with both embeddings)
```

**Query Types:**
1. **Text Query**: Uses text embedding for search
2. **Image Query**: Uses image embedding for search
3. **Hybrid Query**: Combines text and image search
4. **Filtered Query**: Metadata-based filtering

### 5. RAG Engine

**Query Processing Flow:**

```
User Query
    ↓
Text Embedding Generation
    ↓
Vector Search (Top-K Retrieval)
    ↓
Optional Reranking
    ↓
Context Assembly
    ↓
LLM Generation (Azure GPT-4o)
    ↓
Answer + Sources
```

**Context Assembly:**
- Combines retrieved chunks with proper formatting
- Handles tables (preserves structure)
- References images (by description)
- Maintains source attribution

**LLM Prompt Structure:**
```
System: You are a helpful assistant...

Context:
[Source 1] Table from page 2: ...
[Source 2] Text: ...
[Source 3] Image description: ...

Question: {user_query}
```

## API Architecture

### FastAPI Application

**Endpoints:**

1. **Health & Monitoring**
   - `GET /health`: Health check
   - `GET /ready`: Readiness probe
   - `GET /metrics`: Prometheus metrics

2. **Document Management**
   - `POST /api/v1/documents/upload`: Upload document
   - `GET /api/v1/documents/collections`: List collections
   - `DELETE /api/v1/documents/collections/{name}`: Delete collection

3. **Query & Search**
   - `POST /api/v1/query`: RAG query with generation
   - `POST /api/v1/search`: Similarity search only
   - `POST /api/v1/search/multimodal`: Hybrid search

**Request/Response Flow:**

```
Client Request
    ↓
FastAPI Router
    ↓
Request Validation (Pydantic)
    ↓
Business Logic (Core modules)
    ↓
Response Serialization
    ↓
Client Response
```

## Monitoring & Observability

### Metrics (Prometheus)

**Application Metrics:**
- `http_requests_total`: HTTP request count
- `http_request_duration_seconds`: Request latency
- `documents_processed_total`: Document processing count
- `embeddings_generated_total`: Embedding generation count
- `queries_total`: Query count
- `vector_store_operations_total`: Vector store operations

**Business Metrics:**
- `document_processing_duration_seconds`: Processing time
- `embedding_generation_duration_seconds`: Embedding time
- `query_duration_seconds`: Query latency
- `retrieval_results_count`: Results retrieved

### Logging (Loguru)

**Log Levels:**
- `DEBUG`: Detailed execution information
- `INFO`: Key operations and milestones
- `WARNING`: Recoverable issues
- `ERROR`: Operation failures

**Log Files:**
- `logs/app_{date}.log`: All logs (30-day retention)
- `logs/errors_{date}.log`: Error logs only (90-day retention)

### Tracing (OpenTelemetry)

Optional distributed tracing support:
- Trace document processing pipeline
- Track query execution
- Monitor external API calls
- Identify performance bottlenecks

## Scalability Considerations

### Horizontal Scaling

**Stateless Design:**
- All state in ChromaDB/PostgreSQL
- No in-memory session storage
- Supports multiple replicas

**Load Balancing:**
```
            Load Balancer
                 ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
Service 1   Service 2   Service 3
    ↓           ↓           ↓
        Shared ChromaDB
        Shared PostgreSQL
```

### Vertical Scaling

**CPU-bound Operations:**
- OCR processing
- Layout detection
- Embedding generation

**Memory-bound Operations:**
- Large PDF processing
- Image conversion
- Vector search

**Optimization Strategies:**
1. Use GPU for CLIP embeddings
2. Batch embedding generation
3. Implement caching layer
4. Async processing for uploads

### Caching Strategy

**Embedding Cache (Redis):**
```python
cache_key = hash(content)
if cached_embedding := redis.get(cache_key):
    return cached_embedding
else:
    embedding = generate_embedding(content)
    redis.set(cache_key, embedding, ttl=86400)
    return embedding
```

**Query Result Cache:**
- Cache top-K results for frequent queries
- TTL: 1 hour for dynamic content
- Invalidate on document updates

## Security Considerations

### API Security

1. **Authentication**: JWT tokens (configured in .env)
2. **Rate Limiting**: Prevent abuse
3. **Input Validation**: Pydantic schemas
4. **File Upload**: Size limits, type validation

### Data Security

1. **Encryption at Rest**: ChromaDB data encryption
2. **Secrets Management**: Environment variables
3. **Access Control**: Collection-level permissions
4. **Audit Logging**: Track all operations

## Extension Points

### Custom Agents

Add new agents by extending `BaseAgent`:

```python
from app.agents.base_agent import BaseAgent, AgentResult

class CustomAgent(BaseAgent):
    def execute(self, input_data):
        # Your logic here
        return AgentResult(...)
```

### Custom Document Processors

```python
from app.core.document_processor import DocumentProcessor

class CustomProcessor(DocumentProcessor):
    def process_custom_format(self, file_path):
        # Your processing logic
        pass
```

### Custom Embeddings

```python
from app.core.embeddings import EmbeddingGenerator

class CustomEmbedder:
    def generate_embedding(self, content):
        # Your embedding logic
        return embedding
```

## Performance Benchmarks

**Document Processing:**
- Text-based PDF (10 pages): ~2-5 seconds
- Scanned PDF (10 pages): ~15-30 seconds
- Image (high-res): ~2-3 seconds
- Table extraction: ~1-2 seconds per table

**Embedding Generation:**
- Text embedding (512 tokens): ~100-200ms
- Image embedding (CLIP): ~50-100ms
- Batch (10 texts): ~500-800ms

**Query Performance:**
- Vector search (5k docs): ~50-100ms
- LLM generation: ~1-3 seconds
- Total query latency: ~2-5 seconds

## Future Enhancements

1. **Advanced Table Understanding**
   - Complex table parsing with merged cells
   - Table question answering
   - Cross-table reasoning

2. **Chart & Diagram Understanding**
   - Extract data from charts
   - Interpret diagrams
   - Flow chart parsing

3. **Multi-Document Reasoning**
   - Cross-document citations
   - Document comparison
   - Timeline extraction

4. **Active Learning**
   - User feedback integration
   - Model fine-tuning
   - Query refinement

5. **Batch Processing**
   - Async document processing
   - Queue-based architecture
   - Progress tracking

## Conclusion

This architecture provides a solid foundation for production-grade multimodal RAG applications. The modular design allows for easy extension and customization while maintaining high performance and reliability.
