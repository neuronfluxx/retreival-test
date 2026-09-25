# PDF Data Extraction with PyMuPDF4LLM

This project uses PyMuPDF4LLM to extract data from PDF files in various formats suitable for LLM and RAG applications.

## Installation

```bash
pip install pymupdf4llm
```

## Features

- **Markdown Extraction**: Clean, structured markdown output
- **JSON Extraction**: Structured data with metadata
- **Text Extraction**: Plain text format
- **Automatic OCR**: Detects scanned pages and applies OCR when needed
- **Multi-column Support**: Handles complex layouts
- **Image Extraction**: Can extract and save images from PDFs
- **Page Chunking**: Split documents by page for RAG systems

## Scripts

### 1. Extract All PDFs (`extract_pdfs.py`)

Processes all PDF files in the `pdfs` directory and extracts them to multiple formats.

```bash
python3 extract_pdfs.py
```

**Output Structure:**
```
extracted_data/
├── markdown/     # Markdown format (.md)
├── json/         # JSON format with metadata (.json)
└── text/         # Plain text format (.txt)
```

⚠️ **Note**: This extracts text only. Images are OCR'd for text content but NOT saved as files.

### 2. Extract Single PDF to Folder (`extract_one.py`)

Extract a single PDF and save it to the `extracted_data` folder (text only).

```bash
python3 extract_one.py pdfs/yourfile.pdf
```

### 3. Extract WITH Images (`extract_with_images.py`)

⭐ **NEW**: Extract PDFs and save actual image files (diagrams, charts, figures).

```bash
python3 extract_with_images.py pdfs/NIPS-2017-attention-is-all-you-need-Paper.pdf
```

**Output Structure:**
```
extracted_with_images/
├── markdown/                    # Markdown with image references
└── images/
    └── [pdf-name]/             # Actual PNG image files
        ├── diagram1.png
        ├── chart2.png
        └── ...
```

**Use this when**: You need diagrams, charts, architecture diagrams, or visual content.

### 4. Extract Single PDF Demo (`extract_single_pdf.py`)

Demonstrates various extraction options (terminal output only, doesn't save files).

```bash
python3 extract_single_pdf.py pdfs/NIPS-2017-attention-is-all-you-need-Paper.pdf
```

**Features demonstrated:**
- Basic markdown extraction
- Page-chunked extraction
- Image extraction
- Specific page selection
- OCR control options

## Usage Examples

### Basic Extraction

```python
import pymupdf4llm

# Extract to markdown (most common use case)
md_text = pymupdf4llm.to_markdown("document.pdf")
print(md_text)
```

### Page Chunking for RAG

```python
import pymupdf4llm

# Extract with page chunks
page_chunks = pymupdf4llm.to_markdown("document.pdf", page_chunks=True)

for chunk in page_chunks:
    page_num = chunk.get('metadata', {}).get('page', 'unknown')
    text = chunk.get('text', '')
    print(f"Page {page_num}: {text[:100]}...")
```

### Extract with Images

```python
import pymupdf4llm

# Save images to a directory
md_text = pymupdf4llm.to_markdown(
    "document.pdf",
    write_images=True,
    image_path="output_images"
)
```

### Extract Specific Pages

```python
import pymupdf4llm

# Extract only pages 0, 1, and 2
md_text = pymupdf4llm.to_markdown("document.pdf", pages=[0, 1, 2])
```

### OCR Control

```python
import pymupdf4llm

# Disable OCR (faster, text-based PDFs only)
md_text = pymupdf4llm.to_markdown("document.pdf", use_ocr=False)

# Force OCR on all pages
md_text = pymupdf4llm.to_markdown("document.pdf", force_ocr=True)

# Multi-language OCR
md_text = pymupdf4llm.to_markdown("document.pdf", ocr_language="eng+deu")
```

### Disable Layout Analysis

```python
import pymupdf4llm

# Turn off layout analysis for faster processing
pymupdf4llm.use_layout(False)
md_text = pymupdf4llm.to_markdown("document.pdf")
```

## Integration with LLM Frameworks

### LlamaIndex Integration

```python
import pymupdf4llm

# Direct conversion to LlamaIndex documents
llama_reader = pymupdf4llm.LlamaMarkdownReader()
llama_docs = llama_reader.load_data("document.pdf")
```

**Note:** Requires `llama_index` to be installed:
```bash
pip install llama-index
```

### LangChain Integration

PyMuPDF4LLM provides a LangChain document loader. See the [official documentation](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/index.html) for details.

## OCR Features

PyMuPDF4LLM includes intelligent OCR capabilities:

- **Automatic Detection**: OCR runs only when needed (scanned pages, missing text)
- **Hybrid Strategy**: Only OCR text-less regions, preserving high-quality digital text
- **Multiple Engines**: Supports Tesseract (default), RapidOCR, and custom OCR functions
- **Performance**: Reduces OCR time by ~50% with selective processing

## Performance Tips

1. **Process only needed pages**: Use the `pages` parameter
2. **Cache results**: Save output to avoid re-processing
3. **Disable OCR for text-based PDFs**: Use `use_ocr=False`
4. **Turn off layout analysis if not needed**: Use `pymupdf4llm.use_layout(False)`

## Extracted Files

The `extracted_data` directory contains:

- **Markdown files**: Best for reading and LLM input
- **JSON files**: Structured data with page-level metadata
- **Text files**: Plain text for simple processing

## Resources

- [PyMuPDF4LLM Documentation](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/index.html)
- [PyMuPDF4LLM GitHub](https://github.com/pymupdf/PyMuPDF4LLM)
- [RAG/LLM and PDF Blog Post](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/index.html#blogs)

## License

This project uses PyMuPDF4LLM which is licensed under AGPL-3.0. For commercial use without AGPL requirements, consider PyMuPDF Pro.
