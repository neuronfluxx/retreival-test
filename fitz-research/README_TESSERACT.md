# PDF OCR Text Extraction Tool (Tesseract)

A reliable Python script to extract text from scanned PDFs using Tesseract OCR - works perfectly with Python 3.14!

## ✅ Why Use This Version?

- **Works with Python 3.14**: No compatibility issues
- **Easy Installation**: Tesseract is widely available via Homebrew
- **Fast and Reliable**: Industry-standard OCR engine
- **Multiple Languages**: Supports 100+ languages
- **No GPU Required**: Works efficiently on CPU

## Features

- ✅ **Multi-language support**: English, Chinese, French, German, Spanish, Japanese, Korean, and 100+ more
- ✅ **Batch processing**: Process all PDFs in a folder automatically
- ✅ **High accuracy**: Uses Google's Tesseract OCR engine
- ✅ **Structured output**: Saves text in multiple formats (TXT, JSON)
- ✅ **Confidence scores**: Provides confidence levels for each detected text
- ✅ **Bounding boxes**: Includes coordinate information for each text element
- ✅ **Page images**: Optionally save extracted page images
- ✅ **Progress tracking**: Real-time progress updates

## Installation

### 1. Install Tesseract (one-time):

```bash
# macOS
brew install tesseract

# Linux (Ubuntu/Debian)
sudo apt-get install tesseract-ocr

# Linux (Fedora/RHEL)
sudo dnf install tesseract
```

### 2. Install Python dependencies:

```bash
source myevn/bin/activate  # If using virtual environment
pip install pytesseract PyMuPDF Pillow
```

## Usage

### Basic usage (English):
```bash
python3 extract_text_tesseract.py scanned_pdfs
```

### Specify output directory:
```bash
python3 extract_text_tesseract.py scanned_pdfs -o output_folder
```

### Different languages:
```bash
# Chinese (Simplified)
python3 extract_text_tesseract.py scanned_pdfs --lang chi_sim

# French
python3 extract_text_tesseract.py scanned_pdfs --lang fra

# German
python3 extract_text_tesseract.py scanned_pdfs --lang deu

# Spanish
python3 extract_text_tesseract.py scanned_pdfs --lang spa

# Japanese
python3 extract_text_tesseract.py scanned_pdfs --lang jpn

# Korean
python3 extract_text_tesseract.py scanned_pdfs --lang kor
```

### Save page images along with text:
```bash
python3 extract_text_tesseract.py scanned_pdfs --save-images
```

### Combine multiple options:
```bash
python3 extract_text_tesseract.py scanned_pdfs -o results --lang fra --save-images
```

## Output Structure

For each PDF, the script creates:

### Folder Structure:
```
extracted_text/
├── document1/
│   ├── page_1.txt              # Plain text from page 1
│   ├── page_2.txt              # Plain text from page 2
│   ├── document1_full_text.txt # Combined text from all pages
│   ├── document1_ocr_data.json # Structured OCR data with confidence scores
│   └── page_1.png              # (Optional) Page image
└── document2/
    ├── page_1.txt
    ├── document2_full_text.txt
    └── document2_ocr_data.json
```

### Output Files:

1. **`page_N.txt`**: Plain text extracted from each page
2. **`{pdf_name}_full_text.txt`**: All pages combined with page break markers
3. **`{pdf_name}_ocr_data.json`**: Detailed JSON with:
   - Text content
   - Confidence scores (0-1 range)
   - Bounding box coordinates
   - Word and element counts per page

### JSON Structure Example:
```json
{
  "pdf_name": "document1",
  "total_pages": 2,
  "pages": [
    {
      "page_number": 1,
      "text": "Extracted text content...",
      "word_count": 145,
      "element_count": 78,
      "structured_data": [
        {
          "text": "Sample",
          "confidence": 0.9876,
          "bbox": {
            "x": 100,
            "y": 200,
            "width": 50,
            "height": 20
          }
        }
      ]
    }
  ]
}
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_folder` | Path to folder containing PDFs | Required |
| `-o, --output` | Output directory for extracted text | `extracted_text` |
| `-l, --lang` | OCR language code | `eng` |
| `--save-images` | Save page images | Disabled |

## Language Codes

Common language codes for Tesseract:

| Language | Code |
|----------|------|
| English | `eng` |
| Chinese (Simplified) | `chi_sim` |
| Chinese (Traditional) | `chi_tra` |
| French | `fra` |
| German | `deu` |
| Spanish | `spa` |
| Japanese | `jpn` |
| Korean | `kor` |
| Portuguese | `por` |
| Russian | `rus` |
| Arabic | `ara` |
| Hindi | `hin` |

### Install Additional Languages:

```bash
# macOS
brew install tesseract-lang

# Linux (Ubuntu/Debian)
sudo apt-get install tesseract-ocr-all

# Or install specific languages
sudo apt-get install tesseract-ocr-fra tesseract-ocr-deu
```

## Example Output

```bash
python3 extract_text_tesseract.py scanned_pdfs

# Output:
# ============================================================
# PDF OCR Text Extraction Tool (Tesseract)
# ============================================================
# Input folder: scanned_pdfs
# Output folder: extracted_text (auto-generated)
# Language: eng
# Save images: No
# ============================================================
# Initializing Tesseract OCR...
# Tesseract version: 5.5.3
# Tesseract OCR initialized successfully!
#
# [1/2] Processing: invoice.pdf
# ------------------------------------------------------------
#   Processing page 1/3... ✓ (156 elements, 234 words)
#   Processing page 2/3... ✓ (128 elements, 198 words)
#   Processing page 3/3... ✓ (89 elements, 115 words)
#   ✓ Extracted 3 page(s), 547 words
#
# [2/2] Processing: receipt.pdf
# ------------------------------------------------------------
#   Processing page 1/1... ✓ (42 elements, 78 words)
#   ✓ Extracted 1 page(s), 78 words
#
# ============================================================
# EXTRACTION SUMMARY
# ============================================================
# Total PDF files processed: 2
# Total pages processed: 4
# Total words extracted: 625
#
# Detailed Results:
#   ✓ invoice.pdf: 3 page(s), 547 words
#   ✓ receipt.pdf: 1 page(s), 78 words
# ============================================================
```

## Performance Tips

1. **Image quality**: Higher resolution PDFs = better OCR accuracy
2. **Language selection**: Use the correct language code for best results
3. **Preprocessing**: Clean, high-contrast scans work best
4. **Batch processing**: Process multiple PDFs at once for efficiency

## Troubleshooting

### Tesseract not found:
```bash
# Check if installed
tesseract --version

# Install if missing
brew install tesseract  # macOS
```

### Language data not found:
```bash
# Install language packs
brew install tesseract-lang  # macOS (all languages)
```

### Poor OCR accuracy:
- Ensure PDF is not password-protected
- Check if correct language is specified
- Verify image quality is good
- Try increasing zoom factor (edit script, change `zoom=2.0` to `zoom=3.0`)

## Comparison: Tesseract vs PaddleOCR

| Feature | Tesseract | PaddleOCR |
|---------|-----------|-----------|
| Python 3.14 Support | ✅ Yes | ❌ No |
| Installation | Easy (brew) | Complex |
| Speed | Fast | Faster |
| Accuracy | Very Good | Excellent |
| Languages | 100+ | 80+ |
| Dependencies | Minimal | Many |
| **Recommendation** | **Use this!** | Use with Python 3.11/3.12 |

## Notes

- Tesseract is an open-source OCR engine maintained by Google
- Supports 100+ languages out of the box
- Industry-standard for text recognition
- Works perfectly with Python 3.14
- No GPU required (CPU-only is efficient)
