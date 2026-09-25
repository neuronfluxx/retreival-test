#!/usr/bin/env python3
"""
Comprehensive PDF extraction using PyMuPDF (fitz).
Extracts text, images, tables, links, annotations, fonts, and metadata separately.

Based on official PyMuPDF documentation:
https://pymupdf.readthedocs.io/en/latest/
"""

import pymupdf as fitz
import os
import json
import argparse
from pathlib import Path
from collections import defaultdict


class ComprehensivePDFExtractor:
    def __init__(self, pdf_path, output_dir=None):
        """
        Initialize the comprehensive PDF extractor.
        
        Args:
            pdf_path (str): Path to the PDF file
            output_dir (str): Directory to save extracted content
        """
        self.pdf_path = pdf_path
        self.pdf_name = Path(pdf_path).stem
        
        if output_dir is None:
            output_dir = f"{self.pdf_name}_extracted"
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.doc = fitz.open(pdf_path)
        self.results = {
            "filename": self.pdf_name,
            "page_count": len(self.doc),
            "metadata": {},
            "pages": []
        }
    
    def extract_metadata(self):
        """Extract document-level metadata."""
        print("Extracting document metadata...")
        
        metadata = {
            "author": self.doc.metadata.get("author", ""),
            "title": self.doc.metadata.get("title", ""),
            "subject": self.doc.metadata.get("subject", ""),
            "keywords": self.doc.metadata.get("keywords", ""),
            "creator": self.doc.metadata.get("creator", ""),
            "producer": self.doc.metadata.get("producer", ""),
            "creation_date": self.doc.metadata.get("creationDate", ""),
            "mod_date": self.doc.metadata.get("modDate", ""),
            "format": self.doc.metadata.get("format", ""),
            "encryption": self.doc.metadata.get("encryption", ""),
            "page_count": len(self.doc),
            "is_pdf": self.doc.is_pdf,
            "is_encrypted": self.doc.is_encrypted,
            "is_form_pdf": self.doc.is_form_pdf,
            "permissions": self.doc.permissions,
        }
        
        self.results["metadata"] = metadata
        
        # Save metadata
        metadata_path = os.path.join(self.output_dir, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return metadata
    
    def extract_text(self, page, page_num):
        """Extract text from a page in multiple formats."""
        print(f"  Extracting text from page {page_num + 1}...")
        
        text_data = {}
        
        # Plain text
        text_data["plain"] = page.get_text("text")
        
        # Text with blocks (includes bbox information)
        text_data["blocks"] = page.get_text("blocks")
        
        # Text with words (useful for NLP)
        text_data["words"] = page.get_text("words")
        
        # Text in dictionary format (most detailed)
        text_data["dict"] = page.get_text("dict")
        
        # HTML format
        text_data["html"] = page.get_text("html")
        
        # XML format
        text_data["xml"] = page.get_text("xml")
        
        # Save plain text
        text_file = os.path.join(self.output_dir, f"page_{page_num + 1}_text.txt")
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text_data["plain"])
        
        # Save HTML
        html_file = os.path.join(self.output_dir, f"page_{page_num + 1}_text.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(text_data["html"])
        
        return text_data
    
    def extract_images(self, page, page_num):
        """Extract images from a page."""
        print(f"  Extracting images from page {page_num + 1}...")
        
        images_data = []
        
        # Get image info (lightweight, doesn't load image data)
        image_info_list = page.get_image_info(xrefs=True)
        
        # Create images subdirectory
        images_dir = os.path.join(self.output_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # Get detailed image list
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                
                # Extract image
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Get image bbox on page
                try:
                    image_rects = page.get_image_rects(img, transform=True)
                    if image_rects:
                        bbox, transform = image_rects[0]
                    else:
                        bbox = None
                        transform = None
                except:
                    bbox = None
                    transform = None
                
                # Save image
                image_filename = f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
                image_path = os.path.join(images_dir, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                # Store image metadata
                img_data = {
                    "filename": image_filename,
                    "xref": xref,
                    "width": base_image["width"],
                    "height": base_image["height"],
                    "colorspace": base_image["colorspace"],
                    "bpc": base_image["bpc"],
                    "size": len(image_bytes),
                    "ext": image_ext,
                    "bbox": list(bbox) if bbox else None,
                    "transform": list(transform) if transform else None,
                }
                
                images_data.append(img_data)
                
            except Exception as e:
                print(f"    Warning: Could not extract image {img_index + 1}: {e}")
        
        return images_data
    
    def extract_tables(self, page, page_num):
        """Extract tables from a page."""
        print(f"  Extracting tables from page {page_num + 1}...")
        
        tables_data = []
        
        try:
            # Find tables on the page
            tabs = page.find_tables()
            
            for table_index, table in enumerate(tabs.tables):
                table_dict = {
                    "table_number": table_index + 1,
                    "bbox": list(table.bbox),
                    "row_count": table.row_count,
                    "col_count": table.col_count,
                    "header": {
                        "bbox": list(table.header.bbox) if table.header else None,
                        "names": table.header.names if table.header else [],
                        "external": table.header.external if table.header else None,
                    },
                    "cells": [[list(cell) if cell else None for cell in row] for row in table.extract()],
                    "markdown": table.to_markdown(),
                }
                
                tables_data.append(table_dict)
                
                # Save table as markdown
                markdown_file = os.path.join(
                    self.output_dir, 
                    f"page_{page_num + 1}_table_{table_index + 1}.md"
                )
                with open(markdown_file, "w", encoding="utf-8") as f:
                    f.write(table.to_markdown())
                
                # Try to save as pandas DataFrame (if available)
                try:
                    df = table.to_pandas()
                    csv_file = os.path.join(
                        self.output_dir,
                        f"page_{page_num + 1}_table_{table_index + 1}.csv"
                    )
                    df.to_csv(csv_file, index=False)
                except ImportError:
                    pass  # pandas not installed
                
        except Exception as e:
            print(f"    Warning: Could not extract tables: {e}")
        
        return tables_data
    
    def extract_links(self, page, page_num):
        """Extract links from a page."""
        print(f"  Extracting links from page {page_num + 1}...")
        
        links_data = []
        
        for link in page.get_links():
            link_dict = {
                "type": link["kind"],
                "from": list(link["from"]),
                "uri": link.get("uri", ""),
                "page": link.get("page", -1),
                "to": list(link["to"]) if isinstance(link.get("to"), (tuple, list)) else link.get("to", ""),
                "file": link.get("file", ""),
                "xref": link.get("xref", -1),
            }
            links_data.append(link_dict)
        
        return links_data
    
    def extract_annotations(self, page, page_num):
        """Extract annotations from a page."""
        print(f"  Extracting annotations from page {page_num + 1}...")
        
        annotations_data = []
        
        for annot in page.annots():
            try:
                annot_dict = {
                    "type": annot.type[1],  # Annotation type name
                    "rect": list(annot.rect),
                    "info": annot.info,
                    "flags": annot.flags,
                    "opacity": annot.opacity,
                    "xref": annot.xref,
                }
                
                # Try to get annotation contents
                try:
                    annot_dict["contents"] = annot.info.get("content", "")
                except:
                    pass
                
                annotations_data.append(annot_dict)
                
            except Exception as e:
                print(f"    Warning: Could not process annotation: {e}")
        
        return annotations_data
    
    def extract_fonts(self, page, page_num):
        """Extract font information from a page."""
        print(f"  Extracting fonts from page {page_num + 1}...")
        
        fonts_data = []
        
        for font in page.get_fonts(full=True):
            font_dict = {
                "xref": font[0],
                "name": font[3],
                "type": font[1],
                "encoding": font[2],
            }
            fonts_data.append(font_dict)
        
        return fonts_data
    
    def extract_drawings(self, page, page_num):
        """Extract vector graphics/drawings from a page."""
        print(f"  Extracting drawings from page {page_num + 1}...")
        
        drawings_data = []
        
        try:
            paths = page.get_drawings()
            
            for path_index, path in enumerate(paths):
                # Simplify path data for JSON serialization
                path_dict = {
                    "index": path_index,
                    "rect": list(path.get("rect", [])),
                    "color": path.get("color"),
                    "fill": path.get("fill"),
                    "width": path.get("width", 0),
                    "type": path.get("type", ""),
                    "items_count": len(path.get("items", [])),
                }
                drawings_data.append(path_dict)
                
        except Exception as e:
            print(f"    Warning: Could not extract drawings: {e}")
        
        return drawings_data
    
    def extract_page(self, page_num):
        """Extract all content from a single page."""
        print(f"\nProcessing page {page_num + 1}/{len(self.doc)}...")
        
        page = self.doc[page_num]
        
        page_data = {
            "page_number": page_num + 1,
            "rect": list(page.rect),
            "rotation": page.rotation,
            "mediabox": list(page.mediabox),
            "cropbox": list(page.cropbox),
        }
        
        # Extract different types of content
        page_data["text"] = self.extract_text(page, page_num)
        page_data["images"] = self.extract_images(page, page_num)
        page_data["tables"] = self.extract_tables(page, page_num)
        page_data["links"] = self.extract_links(page, page_num)
        page_data["annotations"] = self.extract_annotations(page, page_num)
        page_data["fonts"] = self.extract_fonts(page, page_num)
        page_data["drawings"] = self.extract_drawings(page, page_num)
        
        # Statistics
        page_data["stats"] = {
            "text_length": len(page_data["text"]["plain"]),
            "word_count": len(page_data["text"]["plain"].split()),
            "block_count": len(page_data["text"]["blocks"]),
            "image_count": len(page_data["images"]),
            "table_count": len(page_data["tables"]),
            "link_count": len(page_data["links"]),
            "annotation_count": len(page_data["annotations"]),
            "font_count": len(page_data["fonts"]),
            "drawing_count": len(page_data["drawings"]),
        }
        
        return page_data
    
    def extract_all(self):
        """Extract all content from the PDF."""
        print(f"\nExtracting from: {self.pdf_path}")
        print(f"Output directory: {self.output_dir}")
        print("=" * 60)
        
        # Extract metadata
        self.extract_metadata()
        
        # Extract content from each page
        for page_num in range(len(self.doc)):
            page_data = self.extract_page(page_num)
            
            # Don't store full text in JSON (save separately)
            page_data_summary = page_data.copy()
            page_data_summary["text"] = {
                "plain_length": len(page_data["text"]["plain"]),
                "blocks_count": len(page_data["text"]["blocks"]),
                "words_count": len(page_data["text"]["words"]),
            }
            
            self.results["pages"].append(page_data_summary)
        
        # Save comprehensive results
        self.save_results()
        
        # Generate summary report
        self.generate_summary()
        
        self.doc.close()
        
        return self.results
    
    def save_results(self):
        """Save extraction results to JSON."""
        print("\nSaving results...")
        
        results_file = os.path.join(self.output_dir, "extraction_results.json")
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"  Saved: {results_file}")
    
    def generate_summary(self):
        """Generate a summary report."""
        print("\nGenerating summary report...")
        
        total_images = sum(p["stats"]["image_count"] for p in self.results["pages"])
        total_tables = sum(p["stats"]["table_count"] for p in self.results["pages"])
        total_links = sum(p["stats"]["link_count"] for p in self.results["pages"])
        total_annotations = sum(p["stats"]["annotation_count"] for p in self.results["pages"])
        total_words = sum(p["stats"]["word_count"] for p in self.results["pages"])
        
        summary = f"""
PDF EXTRACTION SUMMARY
{"=" * 60}

Document: {self.pdf_name}
Pages: {self.results["page_count"]}

CONTENT EXTRACTED:
  • Text: {total_words} words
  • Images: {total_images} images
  • Tables: {total_tables} tables
  • Links: {total_links} links
  • Annotations: {total_annotations} annotations

OUTPUT LOCATION: {self.output_dir}

FILES GENERATED:
  ✓ metadata.json - Document metadata
  ✓ extraction_results.json - Complete extraction data
  ✓ page_*_text.txt - Plain text per page
  ✓ page_*_text.html - HTML formatted text per page
  ✓ page_*_table_*.md - Tables in Markdown format
  ✓ page_*_table_*.csv - Tables in CSV format (if pandas available)
  ✓ images/ - Extracted images folder

{"=" * 60}
"""
        
        print(summary)
        
        # Save summary
        summary_file = os.path.join(self.output_dir, "SUMMARY.txt")
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary)


def process_folder(input_folder, output_folder=None):
    """Process all PDFs in a folder."""
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in '{input_folder}'")
        return
    
    if output_folder is None:
        output_folder = os.path.join(os.path.dirname(input_folder.rstrip('/\\')), "comprehensive_extraction")
    
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"\nFound {len(pdf_files)} PDF file(s)")
    print("=" * 60)
    
    results_summary = []
    
    for idx, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_name = Path(pdf_file).stem
        pdf_output_dir = os.path.join(output_folder, pdf_name)
        
        print(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_file}")
        
        try:
            extractor = ComprehensivePDFExtractor(pdf_path, pdf_output_dir)
            results = extractor.extract_all()
            
            results_summary.append({
                "filename": pdf_file,
                "pages": results["page_count"],
                "status": "success"
            })
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results_summary.append({
                "filename": pdf_file,
                "pages": 0,
                "status": f"error: {e}"
            })
    
    # Save overall summary
    print("\n" + "=" * 60)
    print("OVERALL SUMMARY")
    print("=" * 60)
    for item in results_summary:
        status_symbol = "✓" if item["status"] == "success" else "✗"
        print(f"  {status_symbol} {item['filename']}: {item['pages']} page(s)")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive PDF extraction using PyMuPDF - extracts text, images, tables, links, fonts, and more"
    )
    parser.add_argument(
        "input",
        help="Path to PDF file or folder containing PDFs"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory (default: auto-generated)",
        default=None
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: '{args.input}' not found.")
        return
    
    if os.path.isfile(args.input):
        # Single file
        extractor = ComprehensivePDFExtractor(args.input, args.output)
        extractor.extract_all()
    elif os.path.isdir(args.input):
        # Folder
        process_folder(args.input, args.output)
    else:
        print(f"Error: '{args.input}' is neither a file nor a directory.")


if __name__ == "__main__":
    main()
