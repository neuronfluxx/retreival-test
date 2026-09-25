#!/usr/bin/env python3
"""
PDF Data Extraction Script using PyMuPDF4LLM

This script extracts data from PDFs in the 'pdfs' directory and saves the output
in multiple formats: Markdown, JSON, and plain text.
"""

import os
import json
import pymupdf4llm
from pathlib import Path


def extract_pdf_to_markdown(pdf_path, output_dir):
    """Extract PDF content to Markdown format."""
    try:
        print(f"  → Extracting to Markdown...")
        md_text = pymupdf4llm.to_markdown(pdf_path)
        
        # Save markdown output
        pdf_name = Path(pdf_path).stem
        output_path = os.path.join(output_dir, f"{pdf_name}.md")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_text)
        
        print(f"    ✓ Saved to: {output_path}")
        return md_text
    except Exception as e:
        print(f"    ✗ Error extracting Markdown: {e}")
        return None


def extract_pdf_to_json(pdf_path, output_dir):
    """Extract PDF content to JSON format with metadata."""
    try:
        print(f"  → Extracting to JSON...")
        
        # Extract using to_markdown with page_chunks for structured data
        md_text = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
        
        # Convert to JSON format
        json_data = {
            "source": os.path.basename(pdf_path),
            "pages": []
        }
        
        # If page_chunks returned a list of page dictionaries
        if isinstance(md_text, list):
            for page_data in md_text:
                json_data["pages"].append({
                    "page_number": page_data.get("metadata", {}).get("page", "unknown"),
                    "text": page_data.get("text", ""),
                    "metadata": page_data.get("metadata", {})
                })
        else:
            # If it's just plain text, store as single page
            json_data["pages"].append({
                "page_number": "all",
                "text": md_text,
                "metadata": {}
            })
        
        # Save JSON output
        pdf_name = Path(pdf_path).stem
        output_path = os.path.join(output_dir, f"{pdf_name}.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"    ✓ Saved to: {output_path}")
        return json_data
    except Exception as e:
        print(f"    ✗ Error extracting JSON: {e}")
        return None


def extract_pdf_to_text(pdf_path, output_dir):
    """Extract PDF content to plain text format."""
    try:
        print(f"  → Extracting to plain text...")
        
        # Extract markdown first, then strip formatting for plain text
        md_text = pymupdf4llm.to_markdown(pdf_path)
        
        # Simple conversion: remove markdown formatting
        # For better plain text, you could use a markdown-to-text converter
        plain_text = md_text
        
        # Save text output
        pdf_name = Path(pdf_path).stem
        output_path = os.path.join(output_dir, f"{pdf_name}.txt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(plain_text)
        
        print(f"    ✓ Saved to: {output_path}")
        return plain_text
    except Exception as e:
        print(f"    ✗ Error extracting text: {e}")
        return None


def process_pdfs(pdf_dir, output_base_dir):
    """Process all PDFs in the directory."""
    
    # Create output directories
    markdown_dir = os.path.join(output_base_dir, "markdown")
    json_dir = os.path.join(output_base_dir, "json")
    text_dir = os.path.join(output_base_dir, "text")
    
    for dir_path in [markdown_dir, json_dir, text_dir]:
        os.makedirs(dir_path, exist_ok=True)
    
    # Find all PDF files
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process\n")
    
    # Process each PDF
    for idx, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        print(f"[{idx}/{len(pdf_files)}] Processing: {pdf_file}")
        
        # Extract to different formats
        extract_pdf_to_markdown(pdf_path, markdown_dir)
        extract_pdf_to_json(pdf_path, json_dir)
        extract_pdf_to_text(pdf_path, text_dir)
        
        print()  # Empty line for readability
    
    print("=" * 70)
    print("Extraction complete!")
    print(f"  Markdown files: {markdown_dir}")
    print(f"  JSON files: {json_dir}")
    print(f"  Text files: {text_dir}")


def main():
    """Main execution function."""
    print("=" * 70)
    print("PDF Data Extraction using PyMuPDF4LLM")
    print("=" * 70)
    print()
    
    # Set up directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_dir = os.path.join(script_dir, "pdfs")
    output_dir = os.path.join(script_dir, "extracted_data")
    
    if not os.path.exists(pdf_dir):
        print(f"Error: PDF directory not found: {pdf_dir}")
        return
    
    # Process all PDFs
    process_pdfs(pdf_dir, output_dir)


if __name__ == "__main__":
    main()
