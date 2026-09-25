# PyMuPDF4LLM PDF Extraction Project - Index

## 📁 Project Structure

```
pymupdf/
├── pdfs/                      # Source PDF files (7 documents)
├── extracted_data/            # Extracted content in multiple formats
│   ├── markdown/             # Markdown format (7 files, ~395 KB)
│   ├── json/                 # JSON format with metadata (7 files, ~533 KB)
│   └── text/                 # Plain text format (7 files, ~395 KB)
├── extracted_images/          # Images extracted from PDFs (optional)
├── extract_pdfs.py           # Main batch extraction script
├── extract_single_pdf.py     # Single PDF extraction demo
├── search_extracted_data.py  # Search tool for extracted content
├── rag_example.py            # Simple RAG implementation demo
├── stats.py                  # Statistics and overview
├── README.md                 # Complete documentation
├── SUMMARY.md                # Extraction summary report
└── INDEX.md                  # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install pymupdf4llm
```

### 2. Extract All PDFs
```bash
python3 extract_pdfs.py
```

### 3. Search Extracted Data
```bash
python3 search_extracted_data.py "your search query"
```

### 4. View Statistics
```bash
python3 stats.py
```

## 📋 Scripts Overview

### Core Extraction Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `extract_pdfs.py` | Batch extract all PDFs in `pdfs/` directory | `python3 extract_pdfs.py` |
| `extract_single_pdf.py` | Demo various extraction options for one PDF | `python3 extract_single_pdf.py pdfs/file.pdf` |

### Utility Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `search_extracted_data.py` | Search across all extracted content | `python3 search_extracted_data.py "query"` |
| `rag_example.py` | Demo RAG retrieval pattern | `python3 rag_example.py` |
| `stats.py` | Show extraction statistics | `python3 stats.py` |

## 📊 Extraction Summary

- **Total Documents**: 7 PDFs
- **Total Pages**: 192 pages
- **Total Content**: ~402,000 characters
- **Output Size**: 1.3 MB (all formats)
- **Formats**: Markdown, JSON, Plain Text

### Document List

1. **NIPS-2017-attention-is-all-you-need-Paper.pdf** (11 pages)
   - Famous Transformer architecture paper
   
2. **acmi.0.001255.v1.pdf** (19 pages)
   - Machine learning workshops paper
   
3. **Homeowners-Guide-To-Solar-PV.pdf** (11 pages)
   - Solar PV guide for homeowners
   
4. **Handbook on Installation & maintenance of Solar Panel(1).pdf** (41 pages)
   - Comprehensive solar installation handbook
   
5. **Installation_Manual_of_Standard_Solar_Modules_en.pdf** (47 pages)
   - Detailed solar module installation manual
   
6. **sop_gcpv_installation_c.pdf** (57 pages)
   - Grid-connected PV installation procedures
   
7. **fileserve.pdf** (6 pages)
   - Technical documentation

## 🔍 Usage Examples

### Search Examples
```bash
# Search for transformer architecture
python3 search_extracted_data.py "transformer"

# Search for solar installation
python3 search_extracted_data.py "solar installation"

# Search for attention mechanism
python3 search_extracted_data.py "attention mechanism"
```

### Python Integration
```python
import pymupdf4llm

# Basic extraction
md_text = pymupdf4llm.to_markdown("document.pdf")

# Page-chunked for RAG
page_chunks = pymupdf4llm.to_markdown("document.pdf", page_chunks=True)

# With images
md_with_images = pymupdf4llm.to_markdown(
    "document.pdf",
    write_images=True,
    image_path="output_images"
)

# Specific pages only
first_pages = pymupdf4llm.to_markdown("document.pdf", pages=[0, 1, 2])

# Control OCR
no_ocr = pymupdf4llm.to_markdown("document.pdf", use_ocr=False)
force_ocr = pymupdf4llm.to_markdown("document.pdf", force_ocr=True)
```

## 🎯 Use Cases

### 1. RAG Systems
- Use JSON format for structured retrieval
- Page-level chunking already implemented
- Metadata included for citations

### 2. LLM Context
- Use Markdown format for clean text
- Direct input to language models
- Preserved formatting and structure

### 3. Search & Indexing
- Full-text search across documents
- Keyword extraction from text files
- Build search indices (Elasticsearch, etc.)

### 4. Data Analysis
- Extract tables and structured data
- Process with pandas or other tools
- Analyze document content

## 🛠️ Features Demonstrated

✅ Automatic OCR detection and application
✅ Multi-format output (Markdown, JSON, Text)
✅ Page-level chunking for RAG
✅ Metadata extraction (title, author, dates)
✅ Image extraction capability
✅ Specific page selection
✅ OCR control (enable/disable/force)
✅ Layout analysis for complex documents
✅ Multi-column support
✅ Table preservation

## 📚 Documentation Files

| File | Description |
|------|-------------|
| `README.md` | Complete usage documentation |
| `SUMMARY.md` | Extraction results summary |
| `INDEX.md` | This file - project overview |

## 🔗 Resources

- [PyMuPDF4LLM Documentation](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/index.html)
- [PyMuPDF GitHub](https://github.com/pymupdf/PyMuPDF)
- [PyMuPDF4LLM API Reference](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/index.html#api)

## ⚡ Performance Notes

- **OCR Processing**: ~5-10 seconds per page with OCR
- **Text-based PDFs**: Much faster (<1 second per page)
- **Hybrid OCR**: Automatically selective for speed
- **Batch Processing**: Processes 7 documents in ~2-3 minutes

## 🎓 Learning Outcomes

This project demonstrates:
1. PDF text extraction with PyMuPDF4LLM
2. Multi-format output generation
3. OCR integration for scanned documents
4. RAG pattern implementation
5. Search functionality across documents
6. Metadata preservation and usage

## 📝 Notes

- All PDFs successfully extracted with OCR where needed
- Output validated for quality and accuracy
- Ready for integration with LLM/RAG systems
- Scripts include error handling and user feedback
- Metadata preserved for citation and tracking

## 🚀 Next Steps

1. **For Production RAG**:
   - Add semantic embeddings (OpenAI, Sentence Transformers)
   - Implement vector database (Pinecone, Weaviate, Chroma)
   - Add LLM integration (GPT-4, Claude, local models)
   - Implement proper chunking strategies

2. **For Search**:
   - Build full-text search index
   - Add Elasticsearch integration
   - Implement ranking algorithms
   - Add filtering and faceting

3. **For Analysis**:
   - Extract structured data (tables, lists)
   - Build knowledge graphs
   - Implement entity recognition
   - Add summarization capabilities

---

**Status**: ✅ All extraction complete and validated
**Last Updated**: September 25, 2026
