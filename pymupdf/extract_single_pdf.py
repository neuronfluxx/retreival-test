#!/usr/bin/env python3
"""
Single PDF Extraction Example with PyMuPDF4LLM

This script demonstrates various extraction options for a single PDF.
"""

import pymupdf4llm
import json
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_single_pdf.py <pdf_file>")
        print("\nExample:")
        print("  python3 extract_single_pdf.py pdfs/NIPS-2017-attention-is-all-you-need-Paper.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    print(f"Processing: {pdf_path}\n")
    print("=" * 70)
    
    # 1. Basic Markdown extraction (most common use case)
    print("\n1. Basic Markdown Extraction:")
    print("-" * 70)
    md_text = pymupdf4llm.to_markdown(pdf_path)
    print(f"Extracted {len(md_text)} characters")
    print("\nFirst 500 characters:")
    print(md_text[:500])
    print("...")
    
    # 2. Extract with page chunks (useful for RAG systems)
    print("\n\n2. Page-Chunked Extraction:")
    print("-" * 70)
    try:
        page_chunks = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
        if isinstance(page_chunks, list):
            print(f"Extracted {len(page_chunks)} page chunks")
            if page_chunks:
                print(f"\nFirst chunk preview:")
                first_chunk = page_chunks[0]
                print(f"  Page: {first_chunk.get('metadata', {}).get('page', 'unknown')}")
                print(f"  Text length: {len(first_chunk.get('text', ''))}")
                print(f"  Preview: {first_chunk.get('text', '')[:200]}...")
        else:
            print("Page chunks not available in this format")
    except Exception as e:
        print(f"Error with page chunks: {e}")
    
    # 3. Extract with image extraction
    print("\n\n3. Markdown with Images:")
    print("-" * 70)
    try:
        md_with_images = pymupdf4llm.to_markdown(
            pdf_path,
            write_images=True,
            image_path="extracted_images"
        )
        print(f"Extracted markdown with images saved to 'extracted_images' folder")
        print(f"Total length: {len(md_with_images)} characters")
    except Exception as e:
        print(f"Error with image extraction: {e}")
    
    # 4. Extract specific pages only
    print("\n\n4. Extract Specific Pages (first 2 pages):")
    print("-" * 70)
    try:
        first_pages = pymupdf4llm.to_markdown(pdf_path, pages=[0, 1])
        print(f"Extracted {len(first_pages)} characters from first 2 pages")
        print("\nPreview:")
        print(first_pages[:300])
        print("...")
    except Exception as e:
        print(f"Error with page selection: {e}")
    
    # 5. Disable OCR (faster, but may miss scanned content)
    print("\n\n5. Extract Without OCR (faster):")
    print("-" * 70)
    try:
        no_ocr = pymupdf4llm.to_markdown(pdf_path, use_ocr=False)
        print(f"Extracted {len(no_ocr)} characters without OCR")
    except Exception as e:
        print(f"Error without OCR: {e}")
    
    # 6. Force OCR on all pages
    print("\n\n6. Force OCR on All Pages:")
    print("-" * 70)
    try:
        force_ocr = pymupdf4llm.to_markdown(pdf_path, force_ocr=True)
        print(f"Extracted {len(force_ocr)} characters with forced OCR")
    except Exception as e:
        print(f"Error with forced OCR: {e}")
    
    print("\n" + "=" * 70)
    print("Extraction complete!")


if __name__ == "__main__":
    main()
