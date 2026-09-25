#!/usr/bin/env python3
"""
Extract a Single PDF to the extracted_data folder

This script extracts a single PDF file and saves it to all three formats
in the extracted_data directory, just like extract_pdfs.py does.
"""

import os
import json
import sys
import pymupdf4llm
from pathlib import Path


def extract_single_pdf(pdf_path, output_base_dir="extracted_data"):
    """Extract a single PDF to all formats."""
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found: {pdf_path}")
        return False
    
    # Create output directories
    markdown_dir = os.path.join(output_base_dir, "markdown")
    json_dir = os.path.join(output_base_dir, "json")
    text_dir = os.path.join(output_base_dir, "text")
    
    for dir_path in [markdown_dir, json_dir, text_dir]:
        os.makedirs(dir_path, exist_ok=True)
    
    pdf_name = Path(pdf_path).stem
    
    print(f"📄 Processing: {os.path.basename(pdf_path)}")
    print("=" * 70)
    
    # 1. Extract to Markdown
    print("\n1️⃣  Extracting to Markdown...")
    try:
        md_text = pymupdf4llm.to_markdown(pdf_path)
        md_output = os.path.join(markdown_dir, f"{pdf_name}.md")
        
        with open(md_output, 'w', encoding='utf-8') as f:
            f.write(md_text)
        
        print(f"   ✓ Saved: {md_output}")
        print(f"   ℹ Size: {len(md_text):,} characters")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # 2. Extract to JSON (reuse markdown to avoid re-extraction)
    print("\n2️⃣  Creating JSON structure...")
    try:
        json_data = {
            "source": os.path.basename(pdf_path),
            "pages": [{
                "page_number": "all",
                "text": md_text,
                "metadata": {
                    "file_path": pdf_path,
                    "format": "markdown_conversion"
                }
            }]
        }
        
        json_output = os.path.join(json_dir, f"{pdf_name}.json")
        with open(json_output, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"   ✓ Saved: {json_output}")
        print(f"   ℹ Pages: {len(json_data['pages'])}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # 3. Extract to plain text
    print("\n3️⃣  Extracting to Plain Text...")
    try:
        txt_output = os.path.join(text_dir, f"{pdf_name}.txt")
        
        with open(txt_output, 'w', encoding='utf-8') as f:
            f.write(md_text)
        
        print(f"   ✓ Saved: {txt_output}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Extraction complete!")
    print(f"\n📁 Output location: {output_base_dir}/")
    print(f"   • Markdown: {markdown_dir}/{pdf_name}.md")
    print(f"   • JSON:     {json_dir}/{pdf_name}.json")
    print(f"   • Text:     {text_dir}/{pdf_name}.txt")
    
    return True


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Extract Single PDF to extracted_data folder")
        print("\nUsage: python3 extract_one.py <pdf_file>")
        print("\nExample:")
        print("  python3 extract_one.py pdfs/NIPS-2017-attention-is-all-you-need-Paper.pdf")
        print("  python3 extract_one.py /path/to/your/document.pdf")
        print("\nOutput:")
        print("  Files will be saved to extracted_data/markdown/, json/, and text/")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # Use extracted_data directory relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "extracted_data")
    
    success = extract_single_pdf(pdf_path, output_dir)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
