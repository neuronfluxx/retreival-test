# Complete PDF Processing Guide

## 🚀 Quick Decision Tree

```
Do you need to extract from PDFs?
│
├─ Images only?
│  └─ Use: extract_images_from_pdf.py
│
├─ Text from scanned documents?
│  └─ Use: extract_text_tesseract.py
│
├─ Everything (text + images + tables + links + fonts)?
│  └─ Use: extract_comprehensive_pymupdf.py ⭐
│
└─ Just tables?
   └─ Use: extract_comprehensive_pymupdf.py
```

---

## 📚 Complete Script Comparison

| Feature | Images Script | Tesseract OCR | **Comprehensive** | PaddleOCR |
|---------|--------------|---------------|-------------------|-----------|
| **Extracts Images** | ✅ | ❌ | ✅ | ❌ |
| **Extracts Text** | ❌ | ✅ (OCR) | ✅ (Native) | ✅ (OCR) |
| **Extracts Tables** | ❌ | ❌ | ✅ | ❌ |
| **Extracts Links** | ❌ | ❌ | ✅ | ❌ |
| **Extracts Annotations** | ❌ | ❌ | ✅ | ❌ |
| **Extracts Fonts** | ❌ | ❌ | ✅ | ❌ |
| **Extracts Metadata** | ❌ | ❌ | ✅ | ❌ |
| **Vector Graphics** | ❌ | ❌ | ✅ | ❌ |
| **Works with Scans** | ✅ | ✅ | ⚠️ | ✅ |
| **Python 3.14** | ✅ | ✅ | ✅ | ❌ |
| **Speed** | ⚡⚡⚡ | ⚡⚡ | ⚡⚡⚡ | ⚡ |
| **Best For** | Image PDFs | Scanned docs | **Everything** | Advanced OCR |

---

## 🎯 Use Case Guide

### 1. I have a report with charts and want to extract the images
```bash
python3 extract_images_from_pdf.py report.pdf
```
**Output:** `extracted_images/report/` with all images

---

### 2. I have a scanned contract and need the text
```bash
python3 extract_text_tesseract.py contract.pdf
```
**Output:** `extracted_text/contract/` with text files

---

### 3. I have an invoice and need to extract the table
```bash
python3 extract_comprehensive_pymupdf.py invoice.pdf
```
**Output:** `invoice_extracted/` with tables in Markdown and CSV

---

### 4. I need everything from a document (text, images, tables, links)
```bash
python3 extract_comprehensive_pymupdf.py document.pdf
```
**Output:** Complete extraction with all content types separated

---

### 5. I have 100 PDFs and need to process them all
```bash
python3 extract_comprehensive_pymupdf.py pdf_folder/
```
**Output:** Organized folders for each PDF

---

### 6. I have a multilingual document (French)
```bash
python3 extract_text_tesseract.py document.pdf --lang fra
```
**Output:** Text extracted with French language support

---

## 📋 Feature Matrix

### What Each Script Extracts:

#### `extract_images_from_pdf.py`
- ✅ Embedded images (JPG, PNG, etc.)
- ✅ Image metadata (dimensions, format)
- ✅ Fast extraction
- ❌ Text, tables, links

**When to use:** Quick image extraction only

---

#### `extract_text_tesseract.py`
- ✅ Text via OCR
- ✅ Confidence scores
- ✅ Bounding boxes
- ✅ 100+ languages
- ❌ Native PDF text
- ❌ Tables, images

**When to use:** Scanned documents, photos of documents

---

#### `extract_comprehensive_pymupdf.py` ⭐
- ✅ Native PDF text (not OCR)
- ✅ Images with metadata
- ✅ Tables with structure
- ✅ Links (internal & external)
- ✅ Annotations & comments
- ✅ Fonts & styling
- ✅ Vector graphics
- ✅ Document metadata
- ❌ OCR for scanned text

**When to use:** Complete PDF analysis, data extraction, document processing

---

#### `extract_text_paddle_ocr.py`
- ✅ Advanced OCR
- ✅ Multiple languages
- ✅ High accuracy
- ❌ Python 3.14 support

**When to use:** Only if you have Python 3.11/3.12 and need advanced OCR

---

## 🔄 Workflow Examples

### Workflow 1: Mixed Content PDF
**Goal:** Extract text, images, and tables

```bash
# Use the comprehensive script
python3 extract_comprehensive_pymupdf.py document.pdf
```

Result:
- Text in `document_extracted/page_*_text.txt`
- Images in `document_extracted/images/`
- Tables in `document_extracted/page_*_table_*.md`

---

### Workflow 2: Scanned Document
**Goal:** Extract text from scanned pages

```bash
# Use OCR script
python3 extract_text_tesseract.py scanned.pdf
```

Result:
- Text in `extracted_text/scanned/page_*.txt`
- Full text in `extracted_text/scanned/scanned_full_text.txt`

---

### Workflow 3: Batch Processing
**Goal:** Process 50 PDFs in a folder

```bash
# Process all at once
python3 extract_comprehensive_pymupdf.py reports_folder/
```

Result:
- Separate folders for each PDF
- All content types extracted
- Summary reports

---

### Workflow 4: Data Extraction for AI/ML
**Goal:** Prepare PDFs for RAG or LLM processing

```bash
# Extract everything
python3 extract_comprehensive_pymupdf.py documents/ -o ai_ready

# Now you have:
# - Text for embeddings
# - Tables in Markdown for structured data
# - Images for multimodal AI
# - Metadata for filtering
```

---

## 💻 Installation Quick Reference

```bash
# Verify Python
python3 --version  # Should be 3.7+

# Install PyMuPDF (for all scripts)
pip install PyMuPDF

# Install Tesseract (for OCR script)
brew install tesseract

# Install pytesseract (for OCR script)
pip install pytesseract

# Install pandas (optional, for CSV export)
pip install pandas
```

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| `GUIDE.md` | This file - complete overview |
| `FINAL_SETUP.md` | Installation status & quick start |
| `QUICK_START.md` | Quick reference commands |
| `README.md` | Image extraction docs |
| `README_TESSERACT.md` | Tesseract OCR docs |
| `README_COMPREHENSIVE.md` | Comprehensive extraction docs |
| `README_OCR.md` | PaddleOCR docs (Python 3.11/3.12) |
| `INSTALLATION.md` | Troubleshooting |

---

## 🎓 Learning Path

### Beginner
1. Start with `FINAL_SETUP.md`
2. Try `extract_images_from_pdf.py` with a sample PDF
3. Try `extract_text_tesseract.py` with a scanned document

### Intermediate
4. Read `README_COMPREHENSIVE.md`
5. Try `extract_comprehensive_pymupdf.py`
6. Explore the JSON outputs

### Advanced
7. Modify scripts for custom needs
8. Integrate with your applications
9. Build processing pipelines

---

## 🔧 Customization Examples

### Extract Only Tables
Edit `extract_comprehensive_pymupdf.py`:
```python
def extract_page(self, page_num):
    page_data = {}
    # Comment out everything except:
    page_data["tables"] = self.extract_tables(page, page_num)
    return page_data
```

### Change Image Format
Edit `extract_images_from_pdf.py`:
```python
# Add after extracting image:
from PIL import Image
img = Image.open(io.BytesIO(image_bytes))
img.save(image_path, format='PNG')  # Force PNG
```

### Filter by Language
```python
# Only process English documents
if metadata.get("language") == "en":
    extract_text(pdf)
```

---

## 🚨 Common Issues & Solutions

### Issue: No tables detected
**Solution:** Try different detection strategy:
```python
tabs = page.find_tables(strategy="text")
```

### Issue: Images are rotated
**Solution:** Use transformation matrix from comprehensive extraction

### Issue: OCR text is wrong
**Solution:** Specify correct language:
```bash
python3 extract_text_tesseract.py doc.pdf --lang deu
```

### Issue: Script is slow
**Solution:** Process only needed pages:
```python
for page_num in range(0, 10):  # First 10 pages only
```

---

## 📊 Performance Benchmarks

Typical processing times (M1 MacBook):

| Pages | Images | Tesseract OCR | Comprehensive |
|-------|--------|---------------|---------------|
| 1 | < 1s | ~2s | < 1s |
| 10 | ~2s | ~15s | ~3s |
| 100 | ~15s | ~2min | ~30s |
| 1000 | ~2min | ~20min | ~5min |

*Times vary based on content complexity*

---

## 🎯 Best Practices

### 1. Choose the Right Tool
- Images only? → `extract_images_from_pdf.py`
- Scanned PDFs? → `extract_text_tesseract.py`
- Everything? → `extract_comprehensive_pymupdf.py`

### 2. Organize Your Inputs
```
inputs/
├── native_pdfs/        # For comprehensive extraction
├── scanned_pdfs/       # For OCR
└── image_pdfs/         # For image extraction
```

### 3. Batch Process When Possible
Process folders instead of individual files for efficiency.

### 4. Check Outputs
Always verify extraction quality on a sample before batch processing.

### 5. Use Version Control
Track your extraction scripts if you customize them.

---

## 🆘 Getting Help

### 1. Check Documentation
Start with `FINAL_SETUP.md` and relevant README files.

### 2. Run with --help
```bash
python3 script_name.py --help
```

### 3. Check Examples
Look at examples in each README file.

### 4. Troubleshooting
See `INSTALLATION.md` for common issues.

---

## 🎉 You're Ready!

You now have a complete PDF processing toolkit. Start with simple examples and gradually explore more features.

**Quick Start:**
```bash
# Test with a sample PDF
python3 extract_comprehensive_pymupdf.py sample.pdf

# Check the output
ls -la sample_extracted/
```

Happy extracting! 🚀
