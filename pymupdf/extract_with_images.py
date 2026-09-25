#!/usr/bin/env python3
"""
Extract PDF with Actual Images

This script extracts PDFs and saves actual image files from diagrams, 
charts, and figures in the PDF.
"""

import os
import sys
import pymupdf4llm
from pathlib import Path


def extract_with_images(pdf_path, output_dir="extracted_with_images"):
    """Extract PDF with actual image files."""
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found: {pdf_path}")
        return False
    
    pdf_name = Path(pdf_path).stem
    
    # Create output directories
    markdown_dir = os.path.join(output_dir, "markdown")
    images_dir = os.path.join(output_dir, "images", pdf_name)
    
    os.makedirs(markdown_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    print(f"📄 Processing: {os.path.basename(pdf_path)}")
    print("=" * 80)
    
    # Extract with images
    print("\n🖼️  Extracting markdown with images...")
    try:
        md_text = pymupdf4llm.to_markdown(
            pdf_path,
            write_images=True,
            image_path=images_dir,
            image_format="png",  # or "jpg"
            dpi=150  # Image resolution
        )
        
        # Save markdown
        md_output = os.path.join(markdown_dir, f"{pdf_name}.md")
        with open(md_output, 'w', encoding='utf-8') as f:
            f.write(md_text)
        
        print(f"   ✓ Markdown saved: {md_output}")
        print(f"   ℹ Size: {len(md_text):,} characters")
        
        # Check for extracted images
        image_files = list(Path(images_dir).glob("*.*"))
        if image_files:
            print(f"\n📸 Extracted {len(image_files)} image(s):")
            for img in sorted(image_files)[:10]:  # Show first 10
                img_size = img.stat().st_size / 1024  # KB
                print(f"   • {img.name} ({img_size:.1f} KB)")
            if len(image_files) > 10:
                print(f"   ... and {len(image_files) - 10} more")
            print(f"\n   📁 Images location: {images_dir}/")
        else:
            print(f"   ℹ No images found in PDF (or images embedded as text)")
        
        # Show how images appear in markdown
        print("\n📝 Image references in markdown:")
        image_refs = [line for line in md_text.split('\n') if '![' in line or '<img' in line]
        if image_refs:
            for ref in image_refs[:5]:  # Show first 5
                print(f"   {ref[:100]}...")
        else:
            print("   ℹ No image references found in markdown")
        
        print("\n" + "=" * 80)
        print("✅ Extraction complete!")
        print(f"\n📁 Output locations:")
        print(f"   • Markdown: {md_output}")
        print(f"   • Images:   {images_dir}/")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Extract PDF with Actual Image Files")
        print("\nUsage: python3 extract_with_images.py <pdf_file>")
        print("\nExample:")
        print("  python3 extract_with_images.py pdfs/NIPS-2017-attention-is-all-you-need-Paper.pdf")
        print("\nOutput:")
        print("  • Markdown with image references: extracted_with_images/markdown/")
        print("  • Actual image files: extracted_with_images/images/<pdf_name>/")
        print("\nNote:")
        print("  This extracts actual diagrams, charts, and figures as image files,")
        print("  not just OCR text from within images.")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # Use script directory as base
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "extracted_with_images")
    
    success = extract_with_images(pdf_path, output_dir)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
