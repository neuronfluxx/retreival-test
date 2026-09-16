# Quick Start Guide

## 🎉 Installation Complete!

Both scripts are ready to use. Here's how to get started:

---

## 📁 Setup

1. **Place your PDF files** in the `pdfs` folder:
   ```bash
   # The folder already exists at:
   # /Users/shantanu/retrieval-test/fitz-research/pdfs
   
   # Add your PDFs there
   cp /path/to/your/*.pdf pdfs/
   ```

---

## 🖼️ Script 1: Extract Images from PDFs

**Use this for:** PDFs with embedded images (diagrams, photos, charts)

```bash
# Activate virtual environment
source myevn/bin/activate

# Extract images from all PDFs in the folder
python3 extract_images_from_pdf.py pdfs

# Or specify custom output
python3 extract_images_from_pdf.py pdfs -o my_images
```

**Output:** `extracted_images/` folder with subfolders for each PDF

---

## 📄 Script 2: Extract Text from Scanned PDFs (OCR)

**Use this for:** Scanned documents, photos of documents, image-based PDFs

### Option A: Tesseract OCR (✅ Recommended - Works with Python 3.14)

```bash
# Activate virtual environment (if not already activated)
source myevn/bin/activate

# Extract text using OCR (English)
python3 extract_text_tesseract.py scanned_pdfs

# For other languages
python3 extract_text_tesseract.py scanned_pdfs --lang chi_sim  # Chinese
python3 extract_text_tesseract.py scanned_pdfs --lang fra      # French
python3 extract_text_tesseract.py scanned_pdfs --lang deu      # German

# Save page images along with text
python3 extract_text_tesseract.py scanned_pdfs --save-images

# Specify custom output folder
python3 extract_text_tesseract.py scanned_pdfs -o my_text_output
```

### Option B: PaddleOCR (⚠️ Requires Python 3.11/3.12)

```bash
# Only use if you have Python 3.11 or 3.12
python3 extract_text_paddle_ocr.py scanned_pdfs
```

**Note:** PaddleOCR doesn't work with Python 3.14. Use Tesseract instead!

**Output:** `extracted_text/` folder with:
- Individual page text files (`.txt`)
- Combined full text file
- Structured OCR data (`.json`)
- Page images (`.png`) if `--save-images` is used

---

## 🔍 Quick Reference

### Extract Images Script
```bash
python3 extract_images_from_pdf.py <folder_with_pdfs> [-o output_folder]
```

### Extract Text (OCR) Script - Tesseract (Recommended)
```bash
python3 extract_text_tesseract.py <folder_with_pdfs> [-o output_folder] [-l language] [--save-images]
```

### Extract Text (OCR) Script - PaddleOCR (Requires Python 3.11/3.12)
```bash
python3 extract_text_paddle_ocr.py <folder_with_pdfs> [-o output_folder] [-l language] [--save-images]
```

---

## 📊 Example Workflow

```bash
# 1. Activate environment
source myevn/bin/activate

# 2. Extract images from PDFs
python3 extract_images_from_pdf.py pdfs

# 3. Extract text using OCR (Tesseract)
python3 extract_text_tesseract.py scanned_pdfs --save-images

# 4. Check the results
ls -la extracted_images/
ls -la extracted_text/
```

---

## 🎯 Which Script to Use?

| PDF Type | Script to Use | Why |
|----------|--------------|-----|
| PDF with embedded images | `extract_images_from_pdf.py` | Fast, extracts existing images |
| Scanned documents | `extract_text_paddle_ocr.py` | Uses OCR to read text |
| Photos of documents | `extract_text_paddle_ocr.py` | Recognizes text in images |
| Mixed content | **Both scripts** | Get images + extract text |

---

## 💡 Tips

1. **First run is slower**: PaddleOCR downloads models (~200-400MB) on first use
2. **Check languages**: Use `--lang` flag for non-English documents
3. **GPU acceleration**: Add `--gpu` flag if you have a compatible GPU
4. **Organize PDFs**: Keep different document types in separate folders

---

## 🆘 Need Help?

- **Image extraction**: See `README.md`
- **Text extraction (OCR)**: See `README_OCR.md`
- **Installation issues**: See `INSTALLATION.md`

---

## ✅ Verify Installation

```bash
# Check if all scripts work
python3 extract_images_from_pdf.py --help
python3 extract_text_tesseract.py --help

# Check Tesseract installation
tesseract --version
```

All should display help/version messages without errors. ✨
