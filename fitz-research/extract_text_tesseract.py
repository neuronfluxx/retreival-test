#!/usr/bin/env python3
"""
Extract text from scanned PDFs using Tesseract OCR.
This script processes all PDF files in a folder and extracts text using OCR.
"""

import pymupdf as fitz  # PyMuPDF
import os
import argparse
from pathlib import Path
import pytesseract
from PIL import Image
import json


class PDFTextExtractor:
    def __init__(self, lang='eng', tesseract_config=''):
        """
        Initialize the PDF text extractor with Tesseract OCR.
        
        Args:
            lang (str): Language for OCR (default: 'eng', also supports 'chi_sim', 'fra', 'deu', etc.)
            tesseract_config (str): Additional Tesseract configuration
        """
        print("Initializing Tesseract OCR...")
        self.lang = lang
        self.config = tesseract_config
        
        # Check if Tesseract is installed
        try:
            version = pytesseract.get_tesseract_version()
            print(f"Tesseract version: {version}")
        except Exception as e:
            print(f"Error: Tesseract not found. Please install it first.")
            print(f"  macOS: brew install tesseract")
            print(f"  Linux: sudo apt-get install tesseract-ocr")
            raise e
        
        print("Tesseract OCR initialized successfully!")
    
    def pdf_page_to_image(self, page, zoom=2.0):
        """
        Convert a PDF page to an image.
        
        Args:
            page: PyMuPDF page object
            zoom (float): Zoom factor for better OCR quality (default: 2.0)
        
        Returns:
            PIL.Image: Page as image
        """
        # Create transformation matrix for higher resolution
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        return img
    
    def extract_text_from_image(self, image):
        """
        Extract text from an image using Tesseract OCR.
        
        Args:
            image: PIL Image object
        
        Returns:
            tuple: (text, detailed_data)
        """
        # Extract plain text
        text = pytesseract.image_to_string(image, lang=self.lang, config=self.config)
        
        # Extract detailed data with bounding boxes and confidence
        try:
            data = pytesseract.image_to_data(image, lang=self.lang, output_type=pytesseract.Output.DICT)
            detailed_data = self.format_ocr_data(data)
        except Exception as e:
            print(f"    Warning: Could not extract detailed data: {e}")
            detailed_data = []
        
        return text, detailed_data
    
    def format_ocr_data(self, data):
        """
        Format Tesseract OCR data into structured format.
        
        Args:
            data: Dictionary from pytesseract.image_to_data
        
        Returns:
            list: Structured data with text, confidence, and bounding boxes
        """
        structured_data = []
        n_boxes = len(data['text'])
        
        for i in range(n_boxes):
            text = data['text'][i].strip()
            if text:  # Only include non-empty text
                conf = float(data['conf'][i]) if data['conf'][i] != '-1' else 0.0
                structured_data.append({
                    "text": text,
                    "confidence": round(conf / 100, 4),  # Convert to 0-1 range
                    "bbox": {
                        "x": data['left'][i],
                        "y": data['top'][i],
                        "width": data['width'][i],
                        "height": data['height'][i]
                    }
                })
        
        return structured_data
    
    def extract_from_pdf(self, pdf_path, output_dir, save_images=False):
        """
        Extract text from all pages in a PDF.
        
        Args:
            pdf_path (str): Path to PDF file
            output_dir (str): Directory to save extracted text
            save_images (bool): Whether to save page images
        
        Returns:
            dict: Extraction results
        """
        pdf_document = fitz.open(pdf_path)
        pdf_name = Path(pdf_path).stem
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        results = {
            "pdf_name": pdf_name,
            "total_pages": len(pdf_document),
            "pages": []
        }
        
        # Process each page
        for page_num in range(len(pdf_document)):
            print(f"  Processing page {page_num + 1}/{len(pdf_document)}...", end=" ", flush=True)
            
            page = pdf_document[page_num]
            
            # Convert page to image
            img = self.pdf_page_to_image(page)
            
            # Save image if requested
            if save_images:
                img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
                img.save(img_path)
            
            # Extract text using OCR
            full_text, structured_data = self.extract_text_from_image(img)
            
            # Save page results
            page_result = {
                "page_number": page_num + 1,
                "text": full_text.strip(),
                "word_count": len(full_text.split()),
                "element_count": len(structured_data),
                "structured_data": structured_data
            }
            results["pages"].append(page_result)
            
            # Save individual page text
            page_text_path = os.path.join(output_dir, f"page_{page_num + 1}.txt")
            with open(page_text_path, "w", encoding="utf-8") as f:
                f.write(full_text.strip())
            
            print(f"✓ ({len(structured_data)} elements, {len(full_text.split())} words)")
        
        pdf_document.close()
        
        # Save combined text from all pages
        all_text = "\n\n--- Page Break ---\n\n".join([p["text"] for p in results["pages"]])
        full_text_path = os.path.join(output_dir, f"{pdf_name}_full_text.txt")
        with open(full_text_path, "w", encoding="utf-8") as f:
            f.write(all_text)
        
        # Save structured JSON data
        json_path = os.path.join(output_dir, f"{pdf_name}_ocr_data.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return results


def process_pdf_folder(input_folder, output_folder=None, lang='eng', save_images=False):
    """
    Process all PDF files in a folder with Tesseract OCR.
    
    Args:
        input_folder (str): Path to folder containing PDF files
        output_folder (str): Base directory for extracted text
        lang (str): Language for OCR
        save_images (bool): Whether to save page images
    
    Returns:
        dict: Processing statistics
    """
    # Get all PDF files
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in '{input_folder}'")
        return {"total_pdfs": 0, "total_pages": 0, "processed_files": []}
    
    # Create output folder
    if output_folder is None:
        output_folder = os.path.join(os.path.dirname(input_folder.rstrip('/\\')), "extracted_text")
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Initialize OCR
    extractor = PDFTextExtractor(lang=lang)
    
    stats = {
        "total_pdfs": len(pdf_files),
        "total_pages": 0,
        "total_words": 0,
        "processed_files": []
    }
    
    # Process each PDF
    for idx, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_name = Path(pdf_file).stem
        pdf_output_dir = os.path.join(output_folder, pdf_name)
        
        print(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_file}")
        print("-" * 60)
        
        try:
            results = extractor.extract_from_pdf(pdf_path, pdf_output_dir, save_images)
            
            total_words = sum(p["word_count"] for p in results["pages"])
            stats["total_pages"] += results["total_pages"]
            stats["total_words"] += total_words
            
            stats["processed_files"].append({
                "filename": pdf_file,
                "pages": results["total_pages"],
                "words": total_words,
                "status": "success"
            })
            
            print(f"  ✓ Extracted {results['total_pages']} page(s), {total_words} words")
            
        except Exception as e:
            print(f"  ✗ Error processing {pdf_file}: {e}")
            stats["processed_files"].append({
                "filename": pdf_file,
                "pages": 0,
                "words": 0,
                "status": f"error: {e}"
            })
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from scanned PDF files using Tesseract OCR"
    )
    parser.add_argument(
        "input_folder",
        help="Path to folder containing PDF files"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory for extracted text (default: 'extracted_text')",
        default=None
    )
    parser.add_argument(
        "-l", "--lang",
        help="Language for OCR (default: 'eng', options: 'eng', 'chi_sim', 'fra', 'deu', 'spa', 'jpn', 'kor')",
        default='eng'
    )
    parser.add_argument(
        "--save-images",
        help="Save page images along with text",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    # Validate input folder
    if not os.path.exists(args.input_folder):
        print(f"Error: Folder '{args.input_folder}' not found.")
        return
    
    if not os.path.isdir(args.input_folder):
        print(f"Error: '{args.input_folder}' is not a directory.")
        return
    
    print("=" * 60)
    print("PDF OCR Text Extraction Tool (Tesseract)")
    print("=" * 60)
    print(f"Input folder: {args.input_folder}")
    print(f"Output folder: {args.output or 'extracted_text (auto-generated)'}")
    print(f"Language: {args.lang}")
    print(f"Save images: {'Yes' if args.save_images else 'No'}")
    print("=" * 60)
    
    try:
        stats = process_pdf_folder(
            args.input_folder,
            args.output,
            lang=args.lang,
            save_images=args.save_images
        )
        
        print("\n" + "=" * 60)
        print("EXTRACTION SUMMARY")
        print("=" * 60)
        print(f"Total PDF files processed: {stats['total_pdfs']}")
        print(f"Total pages processed: {stats['total_pages']}")
        print(f"Total words extracted: {stats['total_words']}")
        
        if stats['processed_files']:
            print("\nDetailed Results:")
            for file_info in stats['processed_files']:
                status_symbol = "✓" if file_info['status'] == 'success' else "✗"
                print(f"  {status_symbol} {file_info['filename']}: "
                      f"{file_info['pages']} page(s), {file_info['words']} words")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
