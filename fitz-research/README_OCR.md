# PDF OCR Text Extraction Tool (PaddleOCR)

A powerful Python script to extract text from scanned PDFs using PaddleOCR. This tool converts PDF pages to high-quality images and uses advanced OCR to extract text with confidence scores and bounding box information.

## Features

- ✅ **Multi-language support**: English, Chinese, French, German, Korean, Japanese, and more
- ✅ **Batch processing**: Process all PDFs in a folder automatically
- ✅ **High accuracy**: Uses PaddleOCR's state-of-the-art OCR engine
- ✅ **Structured output**: Saves text in multiple formats (TXT, JSON)
- ✅ **Confidence scores**: Provides confidence levels for each detected text
- ✅ **Bounding boxes**: Includes coordinate information for each text element
- ✅ **GPU support**: Optional GPU acceleration for faster processing
- ✅ **Page images**: Optionally save extracted page images
- ✅ **Progress tracking**: Real-time progress updates

## Installation

### 1. Install dependencies:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install paddlepaddle paddleocr PyMuPDF Pillow
```

### 2. For GPU support (optional):

```bash
# For CUDA 11.x
pip install paddlepaddle-gpu

# For CUDA 12.x
pip install paddlepaddle-gpu==2.6.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Usage

### Basic usage (English):
```bash
python extract_text_paddle_ocr.py pdfs
```

### Specify output directory:
```bash
python extract_text_paddle_ocr.py pdfs -o output_folder
```

### Different languages:
```bash
# Chinese
python extract_text_paddle_ocr.py pdfs --lang ch

# French
python extract_text_paddle_ocr.py pdfs --lang fr

# German
python extract_text_paddle_ocr.py pdfs --lang german

# Korean
python extract_text_paddle_ocr.py pdfs --lang korean

# Japanese
python extract_text_paddle_ocr.py pdfs --lang japan
```

### Enable GPU acceleration:
```bash
python extract_text_paddle_ocr.py pdfs --gpu
```

### Save page images along with text:
```bash
python extract_text_paddle_ocr.py pdfs --save-images
```

### Combine multiple options:
```bash
python extract_text_paddle_ocr.py pdfs -o results --lang ch --gpu --save-images
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
   - Confidence scores
   - Bounding box coordinates
   - Word and line counts per page

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
      "line_count": 12,
      "structured_data": [
        {
          "text": "Sample text",
          "confidence": 0.9876,
          "bbox": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
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
| `-l, --lang` | OCR language (en, ch, fr, german, korean, japan) | `en` |
| `--gpu` | Enable GPU acceleration | Disabled |
| `--save-images` | Save page images | Disabled |

## Example Output

```bash
python extract_text_paddle_ocr.py pdfs --lang en

# Output:
# ============================================================
# PDF OCR Text Extraction Tool (PaddleOCR)
# ============================================================
# Input folder: pdfs
# Output folder: extracted_text (auto-generated)
# Language: en
# GPU: Disabled
# Save images: No
# ============================================================
# Initializing PaddleOCR...
# PaddleOCR initialized successfully!
#
# [1/2] Processing: invoice.pdf
# ------------------------------------------------------------
#   Processing page 1/3... ✓ (45 lines, 234 words)
#   Processing page 2/3... ✓ (38 lines, 198 words)
#   Processing page 3/3... ✓ (22 lines, 115 words)
#   ✓ Extracted 3 page(s), 547 words
#
# [2/2] Processing: receipt.pdf
# ------------------------------------------------------------
#   Processing page 1/1... ✓ (15 lines, 78 words)
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

## Supported Languages

PaddleOCR supports 80+ languages. Common ones include:

- `en` - English
- `ch` - Chinese (Simplified & Traditional)
- `fr` - French
- `german` - German
- `korean` - Korean
- `japan` - Japanese
- `spanish` - Spanish
- `portuguese` - Portuguese
- `russian` - Russian
- `arabic` - Arabic
- `hindi` - Hindi

For a complete list, see [PaddleOCR documentation](https://github.com/PaddlePaddle/PaddleOCR).

## Performance Tips

1. **Use GPU**: Add `--gpu` flag for 3-5x faster processing
2. **Image quality**: Higher resolution PDFs = better OCR accuracy
3. **Language selection**: Use the correct language for best results
4. **Batch processing**: Process multiple PDFs at once for efficiency

## Troubleshooting

### PaddleOCR not found:
```bash
pip install paddleocr paddlepaddle
```

### GPU not detected:
```bash
pip install paddlepaddle-gpu
```

### Memory issues with large PDFs:
- Process PDFs one at a time
- Reduce zoom factor in the code (change `zoom=2.0` to `zoom=1.5`)

### Poor OCR accuracy:
- Ensure PDF is not password-protected
- Check if correct language is specified
- Try increasing the zoom factor for higher resolution

## Notes

- First run will download OCR models (~200-400MB depending on language)
- Processing time depends on PDF size, resolution, and hardware
- GPU significantly improves processing speed
- Confidence scores range from 0 to 1 (higher is better)

## Comparison with Image Extraction Script

| Feature | `extract_images_from_pdf.py` | `extract_text_paddle_ocr.py` |
|---------|------------------------------|------------------------------|
| Purpose | Extract embedded images | Extract text via OCR |
| Input | Any PDF | Scanned/image PDFs |
| Output | Image files (JPG, PNG) | Text files (TXT, JSON) |
| Processing | Fast | Slower (OCR required) |
| Use case | PDFs with embedded images | Scanned documents, photos |
