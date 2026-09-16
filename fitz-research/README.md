# PDF Image Extractor

A Python script to extract images from all PDF files in a folder using PyMuPDF (fitz).

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install PyMuPDF directly:

```bash
pip install PyMuPDF
```

## Usage

### Basic usage:
```bash
python extract_images_from_pdf.py path/to/pdf_folder
```

This will:
- Process all PDF files in the specified folder
- Create an `extracted_images` folder
- Create a subfolder for each PDF with its images

### Specify custom output directory:
```bash
python extract_images_from_pdf.py path/to/pdf_folder -o custom_output_folder
```

### Make the script executable:
```bash
chmod +x extract_images_from_pdf.py
./extract_images_from_pdf.py path/to/pdf_folder
```

## Features

- **Batch processing**: Processes all PDF files in a folder automatically
- **Organized output**: Creates separate subfolders for each PDF's images
- **Format preservation**: Keeps original image format (JPEG, PNG, etc.)
- **Smart naming**: Names images with page and image number
- **Progress tracking**: Shows detailed progress for each PDF
- **Error handling**: Continues processing even if one PDF fails
- **Summary report**: Displays extraction statistics at the end

## Folder Structure

### Input:
```
pdf_folder/
├── document1.pdf
├── document2.pdf
└── report.pdf
```

### Output:
```
extracted_images/
├── document1/
│   ├── page1_img1.jpg
│   ├── page1_img2.png
│   └── page2_img1.jpg
├── document2/
│   ├── page1_img1.jpg
│   └── page3_img1.png
└── report/
    ├── page1_img1.jpg
    └── page5_img1.jpg
```

## Image Naming Format

Images are named as: `page{page_number}_img{image_number}.{extension}`

Example: `page1_img1.jpg`, `page2_img3.png`

## Example Output

```bash
python extract_images_from_pdf.py ./my_pdfs

# Output:
# ============================================================
# PDF Image Extraction Tool
# ============================================================
# Input folder: ./my_pdfs
# Output folder: extracted_images (auto-generated)
# ============================================================
#
# [1/3] Processing: document1.pdf
# ------------------------------------------------------------
#   Extracted: page1_img1.jpg
#   Extracted: page2_img1.png
#   ✓ Extracted 2 image(s) from document1.pdf
#
# [2/3] Processing: document2.pdf
# ------------------------------------------------------------
#   Extracted: page1_img1.jpg
#   ✓ Extracted 1 image(s) from document2.pdf
#
# [3/3] Processing: report.pdf
# ------------------------------------------------------------
#   Extracted: page1_img1.jpg
#   Extracted: page1_img2.jpg
#   ✓ Extracted 2 image(s) from report.pdf
#
# ============================================================
# EXTRACTION SUMMARY
# ============================================================
# Total PDF files processed: 3
# Total images extracted: 5
#
# Detailed Results:
#   ✓ document1.pdf: 2 image(s)
#   ✓ document2.pdf: 1 image(s)
#   ✓ report.pdf: 2 image(s)
# ============================================================
```
