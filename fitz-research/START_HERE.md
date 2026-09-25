# 🚀 START HERE - PDF Processing Toolkit

Welcome! This toolkit contains **4 powerful PDF extraction scripts** based on PyMuPDF.

---

## ⚡ Quick Start (3 steps)

### 1️⃣ Choose Your Script

| I want to... | Use this script |
|--------------|----------------|
| Extract **everything** with **smart filtering** (RECOMMENDED) | `extract_comprehensive_improved.py` 🌟 |
| Extract **everything** (original, all images) | `extract_comprehensive_pymupdf.py` |
| Extract **images only** | `extract_images_from_pdf.py` |
| Extract **text from scanned PDFs** (OCR) | `extract_text_tesseract.py` |

### 2️⃣ Run It

```bash
# Activate environment
source myevn/bin/activate

# Example: Extract everything (RECOMMENDED)
python3 extract_comprehensive_improved.py your_document.pdf
```

### 3️⃣ Check Output

```bash
# Output will be in a folder like:
ls your_document_extracted/
```

---

## 📚 Full Documentation

| Document | When to Read |
|----------|--------------|
| **`GUIDE.md`** ⭐ | Complete overview & decision tree |
| `FINAL_SETUP.md` | Installation status & verification |
| `QUICK_START.md` | Command reference |
| `README_COMPREHENSIVE.md` | Comprehensive extraction details |
| `README_TESSERACT.md` | OCR extraction details |
| `README.md` | Image extraction details |

---

## 🎯 Common Scenarios

### Scenario 1: Business Report with Charts
**Goal:** Extract text, images, and tables

```bash
python3 extract_comprehensive_pymupdf.py quarterly_report.pdf
```

**Result:** Complete folder with text, images, and tables separated

---

### Scenario 2: Scanned Contract
**Goal:** Extract text via OCR

```bash
python3 extract_text_tesseract.py scanned_contract.pdf
```

**Result:** Text files with OCR'd content

---

### Scenario 3: Presentation with Photos
**Goal:** Extract all images

```bash
python3 extract_images_from_pdf.py presentation.pdf
```

**Result:** Images folder with all photos

---

### Scenario 4: Batch Processing
**Goal:** Process multiple PDFs

```bash
python3 extract_comprehensive_pymupdf.py documents_folder/
```

**Result:** Separate extraction folder for each PDF

---

## ✅ What's Installed

| Component | Status | Version |
|-----------|--------|---------|
| Python | ✅ | 3.14.7 |
| PyMuPDF | ✅ | Latest |
| Tesseract | ✅ | 5.5.3 |
| pytesseract | ✅ | Latest |

---

## 🎓 Learning Path

1. **Start:** Read this file (you are here!)
2. **Next:** Try the comprehensive script with a sample PDF
3. **Then:** Read `GUIDE.md` for complete overview
4. **Advanced:** Customize scripts for your needs

---

## 📦 What's in This Toolkit

### 🔧 Scripts (4 total)

1. **`extract_comprehensive_pymupdf.py`** 🌟
   - Extracts: text, images, tables, links, annotations, fonts, metadata
   - Best for: Complete document analysis
   
2. **`extract_images_from_pdf.py`**
   - Extracts: embedded images only
   - Best for: Quick image extraction

3. **`extract_text_tesseract.py`**
   - Extracts: text via OCR
   - Best for: Scanned documents

4. **`extract_text_paddle_ocr.py`** ⚠️
   - Extracts: text via advanced OCR
   - Note: Requires Python 3.11/3.12

### 📖 Documentation (8 files)

- `START_HERE.md` - This file!
- `GUIDE.md` - Complete guide
- `FINAL_SETUP.md` - Setup status
- `QUICK_START.md` - Quick reference
- `README_COMPREHENSIVE.md` - Comprehensive extraction
- `README_TESSERACT.md` - Tesseract OCR
- `README.md` - Image extraction
- `README_OCR.md` - PaddleOCR

---

## 🎯 Decision Tree

```
What do you need?
│
├─ Everything + Smart Filtering (for AI/Vision Models)?
│  └─ extract_comprehensive_improved.py 🌟 RECOMMENDED
│
├─ Everything (all images, no filtering)?
│  └─ extract_comprehensive_pymupdf.py
│
├─ Just images?
│  └─ extract_images_from_pdf.py
│
├─ Text from scanned PDF?
│  └─ extract_text_tesseract.py
│
└─ Not sure?
   └─ Start with extract_comprehensive_improved.py
```

---

## ⚡ Quick Examples

### Example 1: Extract Everything
```bash
python3 extract_comprehensive_pymupdf.py report.pdf
```

Output structure:
```
report_extracted/
├── metadata.json
├── extraction_results.json
├── SUMMARY.txt
├── page_1_text.txt
├── page_1_text.html
├── page_1_table_1.md
├── page_1_table_1.csv
└── images/
    ├── page_1_img_1.jpg
    └── page_2_img_1.png
```

### Example 2: Extract Text (OCR)
```bash
python3 extract_text_tesseract.py scanned.pdf
```

Output:
```
extracted_text/scanned/
├── page_1.txt
├── page_2.txt
├── scanned_full_text.txt
└── scanned_ocr_data.json
```

### Example 3: Extract Images
```bash
python3 extract_images_from_pdf.py photos.pdf
```

Output:
```
extracted_images/photos/
├── page1_img1.jpg
├── page1_img2.png
└── page2_img1.jpg
```

---

## 🔍 Feature Comparison

| Feature | Images | OCR | **Comprehensive** |
|---------|--------|-----|-------------------|
| Text | ❌ | ✅ | ✅ |
| Images | ✅ | ❌ | ✅ |
| Tables | ❌ | ❌ | ✅ |
| Links | ❌ | ❌ | ✅ |
| Fonts | ❌ | ❌ | ✅ |
| Metadata | ❌ | ❌ | ✅ |
| Speed | ⚡⚡⚡ | ⚡⚡ | ⚡⚡⚡ |

**Recommendation:** Start with `extract_comprehensive_pymupdf.py` - it does everything!

---

## 💻 Verify Installation

```bash
# Check scripts work
python3 extract_comprehensive_pymupdf.py --help
python3 extract_images_from_pdf.py --help
python3 extract_text_tesseract.py --help

# Check Tesseract
tesseract --version
```

All should display help/version without errors.

---

## 🆘 Need Help?

### Quick Troubleshooting

**Script not found?**
```bash
# Make sure you're in the right directory
cd /Users/shantanu/retrieval-test/fitz-research
```

**Import errors?**
```bash
# Activate virtual environment
source myevn/bin/activate
```

**No output?**
```bash
# Check the output folder
ls -la *_extracted/
```

### More Help

1. Check `GUIDE.md` for complete documentation
2. Check `INSTALLATION.md` for troubleshooting
3. Run scripts with `--help` flag

---

## 🎉 You're Ready!

**Next steps:**
1. Try the comprehensive script: `python3 extract_comprehensive_pymupdf.py sample.pdf`
2. Check the output folder
3. Read `GUIDE.md` for more features

**Pro tip:** Start simple, then explore advanced features!

---

## 📞 Quick Reference

```bash
# Comprehensive extraction - IMPROVED (RECOMMENDED)
python3 extract_comprehensive_improved.py document.pdf

# Comprehensive extraction - original (all images)
python3 extract_comprehensive_pymupdf.py document.pdf

# Image extraction
python3 extract_images_from_pdf.py document.pdf

# OCR extraction
python3 extract_text_tesseract.py scanned.pdf

# Batch processing
python3 extract_comprehensive_improved.py folder/

# Custom filters (for vision models)
python3 extract_comprehensive_improved.py doc.pdf \
  --min-image-size 30000 --min-image-dimension 150
```

---

**See `IMPROVEMENTS.md` for details on what's improved!**

**Happy extracting! 🚀**

For complete documentation, see `GUIDE.md`
