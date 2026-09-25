# Comprehensive PDF Extraction with PyMuPDF

A powerful all-in-one PDF extraction tool that separates and extracts **text**, **images**, **tables**, **links**, **annotations**, **fonts**, **vector graphics**, and **metadata** from PDFs using PyMuPDF.

## 🎯 What This Script Does

This script performs **deep extraction** of ALL content from PDFs, organized by type:

### Extracted Content Types:

1. **📄 Text**
   - Plain text
   - Text blocks with bounding boxes
   - Individual words with coordinates
   - HTML formatted text
   - XML structured text
   - Dictionary format with detailed layout info

2. **🖼️ Images**
   - All embedded images
   - Image metadata (dimensions, colorspace, format)
   - Bounding boxes on page
   - Transformation matrices
   - Saved as separate files (JPG, PNG, etc.)

3. **📊 Tables**
   - Detected table structures
   - Cell-by-cell content
   - Markdown format export
   - CSV export (with pandas)
   - Header detection
   - Row and column counts

4. **🔗 Links**
   - Internal links (page references)
   - External links (URLs)
   - File links
   - Link coordinates

5. **📝 Annotations**
   - Comments and notes
   - Highlights and markups
   - Stamps and signatures
   - Annotation metadata

6. **🔤 Fonts**
   - Font names and types
   - Encoding information
   - Font references (xrefs)

7. **✏️ Vector Graphics (Drawings)**
   - Lines, curves, shapes
   - Colors and fill patterns
   - Stroke widths
   - Path information

8. **ℹ️ Metadata**
   - Author, title, subject
   - Creation and modification dates
   - PDF version and encryption status
   - Page count and permissions

## Installation

```bash
# Already installed if you followed the setup
pip install PyMuPDF
```

## Usage

### Extract from a Single PDF:

```bash
python3 extract_comprehensive_pymupdf.py path/to/document.pdf
```

### Extract from a Folder of PDFs:

```bash
python3 extract_comprehensive_pymupdf.py path/to/pdf_folder
```

### Specify Custom Output Directory:

```bash
python3 extract_comprehensive_pymupdf.py document.pdf -o custom_output
```

## Output Structure

For each PDF, the script creates a comprehensive extraction folder:

```
document_extracted/
├── metadata.json                      # Document metadata
├── extraction_results.json            # Complete extraction data
├── SUMMARY.txt                        # Human-readable summary
├── page_1_text.txt                    # Plain text (page 1)
├── page_1_text.html                   # HTML text (page 1)
├── page_2_text.txt                    # Plain text (page 2)
├── page_2_text.html                   # HTML text (page 2)
├── page_1_table_1.md                  # Table 1 as Markdown
├── page_1_table_1.csv                 # Table 1 as CSV
├── page_2_table_1.md                  # Table 2 as Markdown
└── images/
    ├── page_1_img_1.jpg              # Image 1 from page 1
    ├── page_1_img_2.png              # Image 2 from page 1
    └── page_2_img_1.jpg              # Image 1 from page 2
```

## Output Files Explained

### 1. `metadata.json`
Document-level information:
```json
{
  "author": "John Doe",
  "title": "Annual Report 2024",
  "subject": "Financial Overview",
  "keywords": "finance, report",
  "page_count": 25,
  "is_encrypted": false,
  "creation_date": "2024-01-15",
  ...
}
```

### 2. `extraction_results.json`
Complete extraction data for all pages:
```json
{
  "filename": "document",
  "page_count": 3,
  "metadata": {...},
  "pages": [
    {
      "page_number": 1,
      "rect": [0, 0, 595, 842],
      "stats": {
        "text_length": 1234,
        "word_count": 234,
        "image_count": 2,
        "table_count": 1,
        "link_count": 5
      },
      "images": [...],
      "tables": [...],
      "links": [...],
      ...
    }
  ]
}
```

### 3. Text Files (`page_N_text.txt`)
Plain text extracted from each page, preserving layout.

### 4. HTML Files (`page_N_text.html`)
HTML-formatted text with styling information.

### 5. Table Files
- `.md` - Markdown format (Github-compatible)
- `.csv` - CSV format for Excel/spreadsheet import

### 6. Images Folder
All extracted images with descriptive names indicating:
- Page number
- Image index
- Original format (jpg, png, etc.)

### 7. `SUMMARY.txt`
Quick overview of extraction results:
```
PDF EXTRACTION SUMMARY
============================================================

Document: annual_report
Pages: 25

CONTENT EXTRACTED:
  • Text: 12,456 words
  • Images: 15 images
  • Tables: 8 tables
  • Links: 42 links
  • Annotations: 3 annotations

OUTPUT LOCATION: annual_report_extracted/
...
```

## Features & Capabilities

### 1. Text Extraction
- **Multiple formats**: Plain text, HTML, XML, structured dictionaries
- **Layout preservation**: Maintains reading order and structure
- **Word-level data**: Individual word coordinates for precise location
- **Block-level data**: Paragraph and block-level bounding boxes

### 2. Image Extraction
- **All formats**: JPG, PNG, TIFF, BMP, and more
- **Metadata**: Dimensions, colorspace, compression info
- **Location data**: Exact position and size on page
- **Transformation matrices**: How images are scaled/rotated

### 3. Table Detection
- **Automatic detection**: Finds tables based on gridlines or text layout
- **Structure preservation**: Maintains rows, columns, headers
- **Multiple formats**: Markdown, CSV, pandas DataFrame
- **Header recognition**: Identifies column headers

### 4. Link Extraction
- **All link types**: Internal page links, external URLs, file links
- **Coordinates**: Exact clickable area (bounding box)
- **Destination info**: Target page number or URL

### 5. Advanced Features
- **Annotations**: Comments, highlights, stamps
- **Font analysis**: All fonts used in the document
- **Vector graphics**: Lines, shapes, curves with styling
- **Comprehensive metadata**: Author, dates, permissions, encryption

## Example Usage

### Basic Extraction:
```bash
python3 extract_comprehensive_pymupdf.py invoice.pdf
```

Output:
```
Extracting from: invoice.pdf
Output directory: invoice_extracted
============================================================

Extracting document metadata...

Processing page 1/1...
  Extracting text from page 1...
  Extracting images from page 1...
  Extracting tables from page 1...
  Extracting links from page 1...
  Extracting annotations from page 1...
  Extracting fonts from page 1...
  Extracting drawings from page 1...

Saving results...
  Saved: invoice_extracted/extraction_results.json

Generating summary report...

PDF EXTRACTION SUMMARY
============================================================

Document: invoice
Pages: 1

CONTENT EXTRACTED:
  • Text: 234 words
  • Images: 1 images
  • Tables: 1 tables
  • Links: 2 links
  • Annotations: 0 annotations

OUTPUT LOCATION: invoice_extracted/
...
```

### Batch Processing:
```bash
python3 extract_comprehensive_pymupdf.py ~/Documents/contracts/
```

Processes all PDFs in the folder and organizes output by document name.

## Use Cases

### 1. Document Analysis
Extract all text, images, and structure for AI/ML processing, RAG systems, or document understanding.

### 2. Data Mining
Extract tables and structured data from reports, invoices, or forms.

### 3. Content Migration
Convert PDF content to other formats (Markdown, HTML, CSV).

### 4. Compliance & Audit
Extract metadata, annotations, and links for document tracking.

### 5. Research & Academic
Extract text and citations from academic papers and books.

### 6. Legal & Contracts
Extract clauses, signatures, and structured information.

## Comparison with Other Scripts

| Feature | extract_images | extract_text_tesseract | **extract_comprehensive** |
|---------|---------------|----------------------|-------------------------|
| Text extraction | ❌ | ✅ OCR | ✅ Native + Layout |
| Images | ✅ | ❌ | ✅ + Metadata |
| Tables | ❌ | ❌ | ✅ Auto-detect |
| Links | ❌ | ❌ | ✅ |
| Annotations | ❌ | ❌ | ✅ |
| Fonts | ❌ | ❌ | ✅ |
| Vector Graphics | ❌ | ❌ | ✅ |
| Metadata | ❌ | ❌ | ✅ |
| **Best for** | Image PDFs | Scanned docs | **Everything** |

## Performance

- **Fast**: Processes typical PDFs in seconds
- **Memory efficient**: Streams content, doesn't load entire file
- **Scalable**: Can process hundreds of pages

Typical performance:
- 1-10 pages: < 5 seconds
- 10-50 pages: < 20 seconds
- 50-100 pages: < 1 minute
- 100+ pages: ~ 1 second per page

## Requirements

- Python 3.7+
- PyMuPDF (already installed)
- Optional: pandas (for CSV table export)

```bash
pip install pandas  # Optional, for CSV exports
```

## Limitations

1. **Scanned PDFs**: For image-based/scanned PDFs, use `extract_text_tesseract.py` for OCR
2. **Complex tables**: Some complex table layouts may not be detected perfectly
3. **Encrypted PDFs**: Password-protected PDFs require decryption first
4. **Large files**: Very large PDFs (1000+ pages) may take longer

## Tips & Tricks

### Extract Only Specific Content:
Modify the script to comment out unwanted extraction methods:

```python
# Comment out what you don't need:
# page_data["images"] = self.extract_images(page, page_num)
# page_data["tables"] = self.extract_tables(page, page_num)
```

### Process Specific Pages:
```python
# In extract_all() method, change:
for page_num in range(len(self.doc)):
# To:
for page_num in range(0, 5):  # Only first 5 pages
```

### Export Tables to Excel:
If pandas is installed, add to the table extraction:
```python
df.to_excel(excel_file, index=False, engine='openpyxl')
```

## Troubleshooting

### Tables not detected?
Try adjusting table detection parameters in the script:
```python
tabs = page.find_tables(
    strategy="text",  # Try "text" instead of "lines"
    min_words_vertical=2,
    min_words_horizontal=1
)
```

### Images missing?
Some PDFs have inline images. Check if images are referenced:
```python
image_list = page.get_images(full=True)
print(f"Found {len(image_list)} images")
```

### Memory issues?
Process one page at a time instead of loading all results.

## Advanced Features

### 1. Image Transformation Data
Each image includes transformation matrices showing how it's scaled/rotated.

### 2. Font Analysis
Identifies all fonts used, useful for font licensing compliance.

### 3. Vector Graphics
Extracts drawing commands (lines, curves, shapes) with styling.

### 4. Annotation Details
Includes author, date, and content of all annotations.

## API / Programmatic Usage

Use the extractor in your own Python code:

```python
from extract_comprehensive_pymupdf import ComprehensivePDFExtractor

# Create extractor
extractor = ComprehensivePDFExtractor("document.pdf", "output_dir")

# Extract everything
results = extractor.extract_all()

# Access specific data
print(f"Total pages: {results['page_count']}")
print(f"First page text: {results['pages'][0]['text']['plain'][:100]}")
```

## Related Scripts

- `extract_images_from_pdf.py` - Fast image-only extraction
- `extract_text_tesseract.py` - OCR for scanned PDFs
- `extract_text_paddle_ocr.py` - Advanced OCR (Python 3.11/3.12)

## Credits

Built with [PyMuPDF](https://pymupdf.readthedocs.io/) - a high-performance PDF library.

Based on official documentation: https://pymupdf.readthedocs.io/en/latest/

## License

Free to use and modify for any purpose.
