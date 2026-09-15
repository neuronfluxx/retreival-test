# Retrieval Test

A RAG (Retrieval-Augmented Generation) testing framework using ChromaDB for vector storage and Azure OpenAI for embeddings.

## Features

- 📄 **PDF Ingestion** - Extract and chunk documents with configurable splitting
- 🔍 **Semantic Search** - Query documents using vector similarity
- 🤖 **Answer Generation** - Generate answers using retrieved context with Azure OpenAI
- 💾 **Local Storage** - ChromaDB provides fast, local vector database
- 🏷️ **Namespace Support** - Organize documents with metadata filtering

## Prerequisites

- Python 3.9 or later
- Azure OpenAI account with API access
- Azure OpenAI embedding deployment (e.g., `text-embedding-3-large`)

## Installation

1. **Clone the repository and install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**

Create a `.env` file in the project root:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-01

# ChromaDB Configuration (optional, defaults shown)
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=rag-test-collection
```

## Usage

### 1. Ingest Documents

**Ingest a single PDF:**

```bash
python ingest_documents.py /path/to/document.pdf
```

**Ingest all PDFs from a directory:**

```bash
python ingest_documents.py /path/to/pdfs/
```

**Ingest with namespace (for organization):**

```bash
python ingest_documents.py /path/to/pdfs/ --namespace project-docs
```

**Clear existing data before ingesting:**

```bash
python ingest_documents.py /path/to/pdfs/ --clear
```

### 2. Query Documents (AI-Powered Answers Enabled by Default)

**Interactive mode (recommended - AI answers enabled):**

```bash
python test_retrieval.py
```

This opens an interactive prompt where you can:
- ✨ **Get AI-generated answers** based on retrieved context (enabled by default)
- 📄 **View source chunks** with similarity scores and metadata
- 🔍 Use `filter:source=filename` to search specific documents
- 🔄 Type `toggle` to enable/disable AI answers
- 🧹 Type `clear` to remove filters
- 👋 Type `quit` or `exit` to stop

**Single question mode (with AI answer):**

```bash
python test_retrieval.py --question "What is the installation process?"
```

**Disable AI answer generation (chunks only):**

```bash
python test_retrieval.py --question "How do I configure the system?" --no-generate
```

**Specify number of results:**

```bash
python test_retrieval.py --question "What are the features?" --top-k 10
```

**Query specific namespace:**

```bash
python test_retrieval.py --namespace project-docs
```

**Batch testing from file:**

```bash
# Create questions.txt with one question per line
python test_retrieval.py --batch questions.txt
```

### 3. Example Workflow

```bash
# 1. Clear any existing data and ingest documents
python ingest_documents.py ./documents --clear

# 2. Test retrieval interactively (AI answers enabled by default)
python test_retrieval.py

# 3. Ask a question
❓ Question: What are the system requirements?

# 4. View AI-generated answer first
💡 AI ANSWER
================================================================================
Based on the documentation, the system requirements are...

# 5. Then see the source chunks used to generate the answer
📊 Retrieved 5 relevant chunks:
────────────────────────────────────────────────────────────────────────────────
📄 Chunk 1 | Score: 0.8923
   Source: installation-guide.pdf (chunk #3)

System requirements include Python 3.9+, 8GB RAM minimum...
```

## Command Reference

### ingest_documents.py

```bash
python ingest_documents.py <path> [options]

Arguments:
  path                  Path to PDF file or directory

Options:
  --namespace, -n      Namespace for organizing documents
  --clear              Clear namespace before ingesting
```

### test_retrieval.py

```bash
python test_retrieval.py [options]

Options:
  --question, -q       Single question (non-interactive mode)
  --namespace, -n      Query specific namespace
  --top-k, -k         Number of results (default: 5)
  --no-generate       Disable AI answer generation (enabled by default)
  --batch, -b         Path to file with questions
  --no-text           Hide chunk text in output

Interactive Commands:
  toggle              Enable/disable AI answer generation
  filter:key=value    Filter results by metadata
  clear               Remove active filters
  quit/exit           Exit the program
```

## Project Structure

```
retrieval-test/
├── ingest_documents.py      # Document ingestion script
├── test_retrieval.py         # Retrieval testing and Q&A
├── lambda_function_all.py    # AWS Lambda S3 integration
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── chroma_db/               # ChromaDB storage (auto-created)
├── MIGRATION_GUIDE.md       # Pinecone to ChromaDB migration notes
└── EXAMPLE_OUTPUT.md        # Sample output showing AI answers + chunks
```

## Advanced Usage

### Filter by Source

In interactive mode:

```bash
❓ Question: filter:source=installation-guide
✅ Filter set: {'source': 'installation-guide'}

❓ Question: How do I install this?
# Now searches only in installation-guide document
```

### Clear Specific Namespace

```bash
python ingest_documents.py dummy.pdf --namespace old-docs --clear
# This clears 'old-docs' namespace without ingesting
```

### Backup Your Data

ChromaDB stores data locally:

```bash
# Backup
cp -r ./chroma_db ./chroma_db_backup

# Restore
cp -r ./chroma_db_backup ./chroma_db
```

## Troubleshooting

**Issue: "No vectors to delete" when clearing**
- This is normal if the namespace is already empty

**Issue: "No extractable text in PDF"**
- PDF might be image-based - consider using OCR preprocessing

**Issue: Azure OpenAI rate limits**
- Embeddings are batched (16 per request) to reduce rate limit issues
- Add delays if needed in the `embed()` function

**Issue: ChromaDB errors on import**
- Ensure Python 3.9+ is installed: `python --version`
- Reinstall: `pip install --upgrade chromadb`

## Tips

- **AI answers are enabled by default** - See both the answer and supporting chunks
- Use `toggle` command in interactive mode to switch between answer/chunks-only views
- Use descriptive filenames - they become the `source` in metadata
- Start with `--top-k 3` for focused results, increase for broader context
- Validate retrieval quality by reviewing the chunks shown with each answer
- Test with `--namespace` to isolate different document sets
- The interactive mode is best for iterative testing and refinement
- Use `--no-text` to see only scores and sources for quick evaluation

## License

See LICENSE file for details.
