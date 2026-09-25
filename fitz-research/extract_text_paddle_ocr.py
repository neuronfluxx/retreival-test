#!/usr/bin/env python3
"""
Extract text from scanned PDFs using PaddleOCR.
This script processes all PDF files in a folder and extracts text using OCR.
"""

import pymupdf as fitz  # PyMuPDF
import os
import argparse
from pathlib import Path
from paddleocr import PaddleOCR
import certifi
import json
import ssl
import shutil
import subprocess
import tempfile
from PIL import Image
import io


class PDFTextExtractor:
    def __init__(self, lang='en', use_gpu=False, fast=False):
        """
        Initialize the PDF text extractor with PaddleOCR.
        
        Args:
            lang (str): Language for OCR (default: 'en', also supports 'ch', 'fr', 'german', etc.)
            use_gpu (bool): Whether to use GPU for processing (note: may not be supported in all versions)
        """
        print("Initializing PaddleOCR...")
        ssl._create_default_https_context = lambda: ssl.create_default_context(
            cafile=certifi.where()
        )
        # Simplified initialization for newer PaddleOCR version
        self.ocr = PaddleOCR(
            lang=lang,
            device="gpu:0" if use_gpu else "cpu",
            use_doc_orientation_classify=not fast,
            use_doc_unwarping=not fast,
            use_textline_orientation=not fast,
        )
        print("PaddleOCR initialized successfully!")
    
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
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        return img
    
    def extract_text_from_image(self, image):
        """
        Extract text from an image using PaddleOCR.
        
        Args:
            image: PIL Image object
        
        Returns:
            list: List of detected text elements with bounding boxes and confidence
        """
        # Convert PIL Image to numpy array for PaddleOCR
        import numpy as np
        img_array = np.array(image)
        
        # PaddleOCR 3.x uses predict() and returns structured result objects.
        if hasattr(self.ocr, "predict"):
            result = self.ocr.predict(img_array)
        else:
            result = self.ocr.ocr(img_array, cls=True)
        
        return result
    
    def format_ocr_result(self, result):
        """
        Format OCR result into readable text and structured data.
        
        Args:
            result: Raw OCR result from PaddleOCR
        
        Returns:
            tuple: (full_text, structured_data)
        """
        if not result:
            return "", []

        full_text = []
        structured_data = []

        # PaddleOCR 3.x returns one result object per image.
        first_result = result[0]
        if hasattr(first_result, "json"):
            data = first_result.json
            if isinstance(data, str):
                data = json.loads(data)
            data = data.get("res", data)

            texts = data.get("rec_texts", [])
            scores = data.get("rec_scores", [])
            boxes = data.get("rec_polys", data.get("dt_polys", []))
            for text, confidence, bbox in zip(texts, scores, boxes):
                full_text.append(text)
                structured_data.append({
                    "text": text,
                    "confidence": round(float(confidence), 4),
                    "bbox": [[int(point[0]), int(point[1])] for point in bbox],
                })
            return "\n".join(full_text), structured_data

        # PaddleOCR 2.x fallback: [[box, (text, confidence), ...]].
        legacy_result = first_result
        if legacy_result is None:
            return "", []
        for line in legacy_result:
            bbox = line[0]
            text, confidence = line[1]
            full_text.append(text)
            structured_data.append({
                "text": text,
                "confidence": round(float(confidence), 4),
                "bbox": [[int(point[0]), int(point[1])] for point in bbox],
            })
        
        return "\n".join(full_text), structured_data
    
    def extract_from_pdf(self, pdf_path, output_dir, save_images=False, zoom=2.0):
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
            print(
                f"  Processing page {page_num + 1}/{len(pdf_document)}...",
                flush=True,
            )
            
            page = pdf_document[page_num]
            
            # Convert page to image
            img = self.pdf_page_to_image(page, zoom=zoom)
            print(f"    Rendered image: {img.width}x{img.height}px; running OCR...", flush=True)
            
            # Save image if requested
            if save_images:
                img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
                img.save(img_path)
            
            # Extract text using OCR
            ocr_result = self.extract_text_from_image(img)
            full_text, structured_data = self.format_ocr_result(ocr_result)
            
            # Save page results
            page_result = {
                "page_number": page_num + 1,
                "text": full_text,
                "word_count": len(full_text.split()),
                "line_count": len(structured_data),
                "structured_data": structured_data
            }
            results["pages"].append(page_result)
            
            # Save individual page text
            page_text_path = os.path.join(output_dir, f"page_{page_num + 1}.md")
            with open(page_text_path, "w", encoding="utf-8") as f:
                f.write(f"## Page {page_num + 1}\n\n{full_text}\n")
            
            print(f"    Done: {len(structured_data)} lines, {len(full_text.split())} words")
        
        pdf_document.close()
        
        # Save combined text from all pages
        all_text = "\n\n--- Page Break ---\n\n".join([p["text"] for p in results["pages"]])
        full_text_path = os.path.join(output_dir, f"{pdf_name}_full_text.md")
        with open(full_text_path, "w", encoding="utf-8") as f:
            f.write(f"# {pdf_name}\n\n{all_text}\n")
        
        # Save structured JSON data
        json_path = os.path.join(output_dir, f"{pdf_name}_ocr_data.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return results


def convert_pptx_to_pdf(pptx_path, output_dir):
    """Convert a PowerPoint presentation to PDF using LibreOffice."""
    soffice = (
        shutil.which("soffice")
        or shutil.which("libreoffice")
        or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    )
    if not Path(soffice).exists():
        raise RuntimeError(
            "PPTX input requires LibreOffice. Install it from https://www.libreoffice.org/ "
            "and ensure the 'soffice' command is available on PATH."
        )

    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(pptx_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    pdf_path = Path(output_dir) / f"{Path(pptx_path).stem}.pdf"
    if not pdf_path.exists():
        raise RuntimeError(f"LibreOffice did not create the expected PDF: {pdf_path}")
    return pdf_path


def process_pdf_folder(
    input_folder, output_folder=None, lang='en', use_gpu=False,
    save_images=False, zoom=2.0, fast=False
):
    """
    Process all PDF files in a folder with PaddleOCR.
    
    Args:
        input_folder (str): Path to folder containing PDF files
        output_folder (str): Base directory for extracted text
        lang (str): Language for OCR
        use_gpu (bool): Whether to use GPU
        save_images (bool): Whether to save page images
    
    Returns:
        dict: Processing statistics
    """
    input_path = Path(input_folder)
    supported_extensions = {".pdf", ".pptx"}
    if input_path.is_file() and input_path.suffix.lower() in supported_extensions:
        pdf_files = [input_path.name]
        input_folder = str(input_path.parent)
    else:
        pdf_files = [
            f for f in os.listdir(input_folder)
            if Path(f).suffix.lower() in supported_extensions
            and not f.startswith("~$")
        ]
    
    if not pdf_files:
        print(f"No PDF files found in '{input_folder}'")
        return {"total_pdfs": 0, "total_pages": 0, "processed_files": []}
    
    # Create output folder
    if output_folder is None:
        output_folder = os.path.join(
            os.path.dirname(input_folder.rstrip('/\\')), "extracted_text_paddle_ocr"
        )
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Initialize OCR
    extractor = PDFTextExtractor(lang=lang, use_gpu=use_gpu, fast=fast)
    
    stats = {
        "total_pdfs": len(pdf_files),
        "total_pages": 0,
        "total_words": 0,
        "processed_files": []
    }
    
    # Process each PDF
    with tempfile.TemporaryDirectory(prefix="paddleocr_pptx_") as temp_dir:
        for idx, pdf_file in enumerate(pdf_files, 1):
            source_path = Path(input_folder) / pdf_file
            pdf_path = source_path
            if source_path.suffix.lower() == ".pptx":
                pdf_path = convert_pptx_to_pdf(source_path, Path(temp_dir))
            pdf_name = source_path.stem
            pdf_output_dir = os.path.join(output_folder, pdf_name)
        
            print(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_file}")
            print("-" * 60)
        
            try:
                results = extractor.extract_from_pdf(
                    pdf_path, pdf_output_dir, save_images, zoom=zoom
                )
            
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
        description="Extract text from scanned PDF files using PaddleOCR"
    )
    parser.add_argument(
        "input_folder",
        help="Path to a PDF/PPTX file or folder containing PDF/PPTX files"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory for extracted text (default: 'extracted_text_paddle_ocr')",
        default=None
    )
    parser.add_argument(
        "-l", "--lang",
        help="Language for OCR (default: 'en', options: 'ch', 'en', 'fr', 'german', 'korean', 'japan')",
        default='en'
    )
    parser.add_argument(
        "--gpu",
        help="Use GPU for processing",
        action="store_true"
    )
    parser.add_argument(
        "--save-images",
        help="Save page images along with text",
        action="store_true"
    )
    parser.add_argument(
        "--zoom",
        type=float,
        default=2.0,
        help="PDF rendering scale before OCR (default: 2.0; use 1.0 for faster processing)",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Skip document orientation and unwarping for faster CPU OCR",
    )
    
    args = parser.parse_args()
    
    # Validate input folder
    if not os.path.exists(args.input_folder):
        print(f"Error: Folder '{args.input_folder}' not found.")
        return
    
    if not os.path.isdir(args.input_folder) and not (
        os.path.isfile(args.input_folder)
        and Path(args.input_folder).suffix.lower() in {".pdf", ".pptx"}
    ):
        print(f"Error: '{args.input_folder}' is not a PDF/PPTX file or directory.")
        return
    
    print("=" * 60)
    print("PDF OCR Text Extraction Tool (PaddleOCR)")
    print("=" * 60)
    print(f"Input folder: {args.input_folder}")
    print(f"Output folder: {args.output or 'extracted_text_paddle_ocr (auto-generated)'}")
    print(f"Language: {args.lang}")
    print(f"GPU: {'Enabled' if args.gpu else 'Disabled'}")
    print(f"Save images: {'Yes' if args.save_images else 'No'}")
    print(f"Render zoom: {args.zoom}")
    print(f"Fast mode: {'Enabled' if args.fast else 'Disabled'}")
    print("=" * 60)
    
    try:
        stats = process_pdf_folder(
            args.input_folder,
            args.output,
            lang=args.lang,
            use_gpu=args.gpu,
            save_images=args.save_images,
            zoom=args.zoom,
            fast=args.fast,
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
