#!/usr/bin/env python3
"""Extract text from scanned PDFs using EasyOCR."""

import argparse
import io
import json
import ssl
from pathlib import Path

import certifi
import easyocr
import numpy as np
import pymupdf
from PIL import Image


class PDFTextExtractor:
    """Render PDF pages and extract text with EasyOCR."""

    def __init__(self, languages, gpu=False, zoom=2.0):
        print("Initializing EasyOCR...")
        ssl._create_default_https_context = lambda: ssl.create_default_context(
            cafile=certifi.where()
        )
        self.reader = easyocr.Reader(languages, gpu=gpu)
        self.zoom = zoom
        print("EasyOCR initialized successfully!")

    def pdf_page_to_image(self, page):
        matrix = pymupdf.Matrix(self.zoom, self.zoom)
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        return Image.open(io.BytesIO(pixmap.tobytes("png"))).convert("RGB")

    def extract_text_from_image(self, image):
        """Return EasyOCR detections as (bounding box, text, confidence)."""
        return self.reader.readtext(np.array(image), detail=1, paragraph=False)

    @staticmethod
    def format_ocr_result(detections):
        structured_data = []
        for bbox, text, confidence in detections:
            structured_data.append({
                "text": text,
                "confidence": round(float(confidence), 4),
                "bbox": [[int(point[0]), int(point[1])] for point in bbox],
            })

        return "\n".join(item["text"] for item in structured_data), structured_data

    def extract_from_pdf(self, pdf_path, output_dir, save_images=False):
        pdf_name = Path(pdf_path).stem
        output_dir.mkdir(parents=True, exist_ok=True)
        results = {"pdf_name": pdf_name, "total_pages": 0, "pages": []}

        with pymupdf.open(pdf_path) as pdf_document:
            results["total_pages"] = len(pdf_document)
            for page_number, page in enumerate(pdf_document, start=1):
                print(
                    f"  Processing page {page_number}/{len(pdf_document)}...",
                    end=" ",
                    flush=True,
                )
                image = self.pdf_page_to_image(page)
                if save_images:
                    image.save(output_dir / f"page_{page_number}.png")

                detections = self.extract_text_from_image(image)
                full_text, structured_data = self.format_ocr_result(detections)
                results["pages"].append({
                    "page_number": page_number,
                    "text": full_text,
                    "word_count": len(full_text.split()),
                    "line_count": len(structured_data),
                    "structured_data": structured_data,
                })

                (output_dir / f"page_{page_number}.txt").write_text(
                    full_text, encoding="utf-8"
                )
                print(f"({len(structured_data)} lines, {len(full_text.split())} words)")

        all_text = "\n\n--- Page Break ---\n\n".join(
            page["text"] for page in results["pages"]
        )
        (output_dir / f"{pdf_name}_full_text.txt").write_text(
            all_text, encoding="utf-8"
        )
        (output_dir / f"{pdf_name}_ocr_data.json").write_text(
            json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return results


def process_pdf_folder(input_folder, output_folder, languages, gpu, zoom, save_images):
    input_path = Path(input_folder)
    pdf_files = sorted(input_path.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in '{input_folder}'")
        return

    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    extractor = PDFTextExtractor(languages, gpu=gpu, zoom=zoom)

    for index, pdf_path in enumerate(pdf_files, start=1):
        pdf_output_dir = output_path / pdf_path.stem
        print(f"\n[{index}/{len(pdf_files)}] Processing: {pdf_path.name}")
        try:
            results = extractor.extract_from_pdf(
                pdf_path, pdf_output_dir, save_images=save_images
            )
            word_count = sum(page["word_count"] for page in results["pages"])
            print(f"  Extracted {results['total_pages']} page(s), {word_count} words")
        except Exception as error:
            print(f"  Error processing {pdf_path.name}: {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from scanned PDF files using EasyOCR"
    )
    parser.add_argument("input_folder", help="Folder containing scanned PDF files")
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output folder (default: ../extracted_text_easyocr)",
    )
    parser.add_argument(
        "-l", "--lang", nargs="+", default=["en"],
        help="EasyOCR language codes, for example: en ch_sim (default: en)",
    )
    parser.add_argument("--gpu", action="store_true", help="Use GPU acceleration")
    parser.add_argument(
        "--zoom", type=float, default=2.0,
        help="PDF rendering scale before OCR (default: 2.0)",
    )
    parser.add_argument(
        "--save-images", action="store_true",
        help="Save rendered page images alongside the OCR output",
    )
    args = parser.parse_args()

    input_path = Path(args.input_folder)
    if not input_path.is_dir():
        parser.error(f"Input folder not found: {input_path}")

    output_folder = args.output or input_path.parent / "extracted_text_easyocr"
    process_pdf_folder(
        input_path, output_folder, args.lang, args.gpu, args.zoom, args.save_images
    )


if __name__ == "__main__":
    main()