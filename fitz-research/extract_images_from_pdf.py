#!/usr/bin/env python3
"""
Extract images from PDF files using PyMuPDF (fitz).
This script processes all PDF files in a folder and extracts all images from them.
"""

import pymupdf as fitz  # PyMuPDF
import os
import argparse
from pathlib import Path


def extract_images_from_pdf(pdf_path, output_dir):
    """
    Extract all images from a PDF file and save them to the output directory.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save extracted images
    
    Returns:
        int: Number of images extracted
    """
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    image_count = 0
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Get list of images on the page
        image_list = page.get_images(full=True)
        
        # Extract each image
        for img_index, img in enumerate(image_list):
            xref = img[0]  # Image XREF number
            
            # Extract image bytes
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]  # Get image extension (png, jpg, etc.)
            
            # Generate filename
            image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
            image_path = os.path.join(output_dir, image_filename)
            
            # Save the image
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
            
            image_count += 1
            print(f"  Extracted: {image_filename}")
    
    pdf_document.close()
    return image_count


def process_pdf_folder(input_folder, output_folder=None):
    """
    Process all PDF files in a folder and extract images from each.
    
    Args:
        input_folder (str): Path to folder containing PDF files
        output_folder (str): Base directory for extracted images. If None, creates
                           'extracted_images' folder in the same location as input_folder
    
    Returns:
        dict: Statistics about the extraction process
    """
    # Get all PDF files in the folder
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in '{input_folder}'")
        return {"total_pdfs": 0, "total_images": 0, "processed_files": []}
    
    # Create base output folder if not specified
    if output_folder is None:
        output_folder = os.path.join(os.path.dirname(input_folder.rstrip('/\\')), "extracted_images")
    
    os.makedirs(output_folder, exist_ok=True)
    
    stats = {
        "total_pdfs": len(pdf_files),
        "total_images": 0,
        "processed_files": []
    }
    
    # Process each PDF file
    for idx, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_name = Path(pdf_file).stem
        
        # Create a subfolder for each PDF's images
        pdf_output_dir = os.path.join(output_folder, pdf_name)
        
        print(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_file}")
        print("-" * 60)
        
        try:
            num_images = extract_images_from_pdf(pdf_path, pdf_output_dir)
            stats["total_images"] += num_images
            stats["processed_files"].append({
                "filename": pdf_file,
                "images_extracted": num_images,
                "status": "success"
            })
            print(f"  ✓ Extracted {num_images} image(s) from {pdf_file}")
        except Exception as e:
            print(f"  ✗ Error processing {pdf_file}: {e}")
            stats["processed_files"].append({
                "filename": pdf_file,
                "images_extracted": 0,
                "status": f"error: {e}"
            })
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Extract images from all PDF files in a folder using PyMuPDF (fitz)"
    )
    parser.add_argument(
        "input_folder",
        help="Path to folder containing PDF files"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory for extracted images (default: 'extracted_images' in parent directory)",
        default=None
    )
    
    args = parser.parse_args()
    
    # Check if input folder exists
    if not os.path.exists(args.input_folder):
        print(f"Error: Folder '{args.input_folder}' not found.")
        return
    
    # Check if it's a directory
    if not os.path.isdir(args.input_folder):
        print(f"Error: '{args.input_folder}' is not a directory.")
        return
    
    print("=" * 60)
    print("PDF Image Extraction Tool")
    print("=" * 60)
    print(f"Input folder: {args.input_folder}")
    print(f"Output folder: {args.output or 'extracted_images (auto-generated)'}")
    print("=" * 60)
    
    try:
        stats = process_pdf_folder(args.input_folder, args.output)
        
        print("\n" + "=" * 60)
        print("EXTRACTION SUMMARY")
        print("=" * 60)
        print(f"Total PDF files processed: {stats['total_pdfs']}")
        print(f"Total images extracted: {stats['total_images']}")
        
        # Show details for each file
        if stats['processed_files']:
            print("\nDetailed Results:")
            for file_info in stats['processed_files']:
                status_symbol = "✓" if file_info['status'] == 'success' else "✗"
                print(f"  {status_symbol} {file_info['filename']}: {file_info['images_extracted']} image(s)")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
