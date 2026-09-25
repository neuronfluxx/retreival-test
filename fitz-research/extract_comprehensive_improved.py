#!/usr/bin/env python3
"""
Improved Comprehensive PDF extraction with smart image filtering and better table detection.

Improvements:
1. Filters out small icons, logos, and non-meaningful images
2. Enhanced table detection with multiple strategies
3. Better table structure recognition
"""

import pymupdf as fitz
import os
import json
import argparse
from pathlib import Path
from collections import defaultdict


class ImprovedPDFExtractor:
    def __init__(self, pdf_path, output_dir=None, 
                 min_image_size=10000,  # Minimum pixels (width * height)
                 min_image_dimension=100):  # Minimum width or height
        """
        Initialize the improved PDF extractor.
        
        Args:
            pdf_path (str): Path to the PDF file
            output_dir (str): Directory to save extracted content
            min_image_size (int): Minimum image size in pixels to extract
            min_image_dimension (int): Minimum width or height in pixels
        """
        self.pdf_path = pdf_path
        self.pdf_name = Path(pdf_path).stem
        
        if output_dir is None:
            output_dir = f"{self.pdf_name}_extracted"
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.doc = fitz.open(pdf_path)
        
        # Image filtering parameters
        self.min_image_size = min_image_size
        self.min_image_dimension = min_image_dimension
        
        self.results = {
            "filename": self.pdf_name,
            "page_count": len(self.doc),
            "metadata": {},
            "pages": []
        }
    
    def is_meaningful_image(self, width, height, size_bytes):
        """
        Determine if an image is meaningful enough to extract.
        Filters out icons, logos, and small graphics.
        
        Args:
            width (int): Image width in pixels
            height (int): Image height in pixels
            size_bytes (int): Image file size in bytes
        
        Returns:
            bool: True if image should be extracted
        """
        # Calculate total pixels
        total_pixels = width * height
        
        # Filter criteria:
        # 1. Must be at least min_image_size pixels (default: 10,000)
        if total_pixels < self.min_image_size:
            return False
        
        # 2. At least one dimension must be >= min_image_dimension (default: 100px)
        if width < self.min_image_dimension and height < self.min_image_dimension:
            return False
        
        # 3. Aspect ratio should be reasonable (not too extreme)
        # This filters out decorative lines/borders
        aspect_ratio = max(width, height) / max(min(width, height), 1)
        if aspect_ratio > 20:  # Too narrow/wide
            return False
        
        # 4. File size should be reasonable (not tiny compression artifacts)
        if size_bytes < 1000:  # Less than 1KB
            return False
        
        return True
    
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
            "page_count": len(self.doc),
            "is_pdf": self.doc.is_pdf,
            "is_encrypted": self.doc.is_encrypted,
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
        
        # Text with blocks
        text_data["blocks"] = page.get_text("blocks")
        
        # Text with words
        text_data["words"] = page.get_text("words")
        
        # Dictionary format
        text_data["dict"] = page.get_text("dict")
        
        # Save plain text
        text_file = os.path.join(self.output_dir, f"page_{page_num + 1}_text.txt")
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text_data["plain"])
        
        return text_data
    
    def extract_images(self, page, page_num):
        """Extract only meaningful images from a page (filters out icons/logos)."""
        print(f"  Extracting meaningful images from page {page_num + 1}...")
        
        images_data = []
        
        # Create images subdirectory
        images_dir = os.path.join(self.output_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # Get detailed image list
        image_list = page.get_images(full=True)
        
        extracted_count = 0
        filtered_count = 0
        
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                
                # Extract image
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                width = base_image["width"]
                height = base_image["height"]
                
                # Check if image is meaningful
                if not self.is_meaningful_image(width, height, len(image_bytes)):
                    filtered_count += 1
                    print(f"    Filtered: {width}x{height}px ({len(image_bytes)} bytes) - too small")
                    continue
                
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
                extracted_count += 1
                image_filename = f"page_{page_num + 1}_img_{extracted_count}.{image_ext}"
                image_path = os.path.join(images_dir, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                # Store image metadata
                img_data = {
                    "filename": image_filename,
                    "xref": xref,
                    "width": width,
                    "height": height,
                    "colorspace": base_image["colorspace"],
                    "size": len(image_bytes),
                    "ext": image_ext,
                    "bbox": list(bbox) if bbox else None,
                }
                
                images_data.append(img_data)
                print(f"    Extracted: {width}x{height}px ({len(image_bytes)} bytes)")
                
            except Exception as e:
                print(f"    Warning: Could not extract image {img_index + 1}: {e}")
        
        print(f"  Summary: {extracted_count} meaningful images extracted, {filtered_count} small images filtered")
        
        return images_data
    
    def extract_tables_improved(self, page, page_num):
        """
        Extract tables with improved detection using multiple strategies.
        """
        print(f"  Extracting tables from page {page_num + 1}...")
        
        tables_data = []
        
        # Strategy 1: Lines-based detection (default)
        print("    Trying strategy: lines")
        try:
            tabs1 = page.find_tables(strategy="lines")
            if tabs1.tables:
                print(f"    Found {len(tabs1.tables)} table(s) with 'lines' strategy")
                tables_data.extend(self._process_tables(tabs1, page_num, "lines"))
        except Exception as e:
            print(f"    Strategy 'lines' failed: {e}")
        
        # Strategy 2: Lines-strict (ignore borderless rectangles)
        print("    Trying strategy: lines_strict")
        try:
            tabs2 = page.find_tables(strategy="lines_strict")
            # Check for new tables not already found
            existing_bboxes = {tuple(t["bbox"]) for t in tables_data}
            new_tables = [t for t in tabs2.tables if tuple(t.bbox) not in existing_bboxes]
            if new_tables:
                print(f"    Found {len(new_tables)} additional table(s) with 'lines_strict' strategy")
                # Process only new tables
                for table in new_tables:
                    tables_data.extend(self._process_single_table(table, page_num, len(tables_data) + 1, "lines_strict"))
        except Exception as e:
            print(f"    Strategy 'lines_strict' failed: {e}")
        
        # Strategy 3: Text-based detection (for tables without gridlines)
        print("    Trying strategy: text")
        try:
            tabs3 = page.find_tables(
                strategy="text",
                min_words_vertical=2,
                min_words_horizontal=2
            )
            # Check for new tables
            existing_bboxes = {tuple(t["bbox"]) for t in tables_data}
            new_tables = [t for t in tabs3.tables if tuple(t.bbox) not in existing_bboxes]
            if new_tables:
                print(f"    Found {len(new_tables)} additional table(s) with 'text' strategy")
                for table in new_tables:
                    tables_data.extend(self._process_single_table(table, page_num, len(tables_data) + 1, "text"))
        except Exception as e:
            print(f"    Strategy 'text' failed: {e}")
        
        print(f"  Total: {len(tables_data)} table(s) extracted from page {page_num + 1}")
        
        return tables_data
    
    def _process_tables(self, tabs, page_num, strategy):
        """Process tables from a TableFinder object."""
        tables_data = []
        for table_index, table in enumerate(tabs.tables):
            tables_data.extend(self._process_single_table(table, page_num, table_index + 1, strategy))
        return tables_data
    
    def _process_single_table(self, table, page_num, table_number, strategy):
        """Process a single table."""
        try:
            table_dict = {
                "table_number": table_number,
                "bbox": list(table.bbox),
                "row_count": table.row_count,
                "col_count": table.col_count,
                "strategy": strategy,
                "header": {
                    "bbox": list(table.header.bbox) if table.header else None,
                    "names": table.header.names if table.header else [],
                    "external": table.header.external if table.header else None,
                },
                "cells": table.extract(),
            }
            
            # Save table as markdown
            markdown_file = os.path.join(
                self.output_dir, 
                f"page_{page_num + 1}_table_{table_number}.md"
            )
            with open(markdown_file, "w", encoding="utf-8") as f:
                f.write(f"<!-- Extracted using strategy: {strategy} -->\n\n")
                f.write(table.to_markdown())
            
            # Save as CSV
            try:
                import pandas as pd
                df = table.to_pandas()
                csv_file = os.path.join(
                    self.output_dir,
                    f"page_{page_num + 1}_table_{table_number}.csv"
                )
                df.to_csv(csv_file, index=False)
            except ImportError:
                pass
            except Exception as e:
                print(f"    Warning: Could not save table as CSV: {e}")
            
            return [table_dict]
            
        except Exception as e:
            print(f"    Warning: Could not process table {table_number}: {e}")
            return []
    
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
                    "type": annot.type[1],
                    "rect": list(annot.rect),
                    "contents": annot.info.get("content", ""),
                }
                annotations_data.append(annot_dict)
            except Exception as e:
                print(f"    Warning: Could not process annotation: {e}")
        
        return annotations_data
    
    def extract_page(self, page_num):
        """Extract all content from a single page."""
        print(f"\nProcessing page {page_num + 1}/{len(self.doc)}...")
        
        page = self.doc[page_num]
        
        page_data = {
            "page_number": page_num + 1,
            "rect": list(page.rect),
            "rotation": page.rotation,
        }
        
        # Extract different types of content
        page_data["text"] = self.extract_text(page, page_num)
        page_data["images"] = self.extract_images(page, page_num)
        page_data["tables"] = self.extract_tables_improved(page, page_num)
        page_data["links"] = self.extract_links(page, page_num)
        page_data["annotations"] = self.extract_annotations(page, page_num)
        
        # Statistics
        page_data["stats"] = {
            "text_length": len(page_data["text"]["plain"]),
            "word_count": len(page_data["text"]["plain"].split()),
            "image_count": len(page_data["images"]),
            "table_count": len(page_data["tables"]),
            "link_count": len(page_data["links"]),
        }
        
        return page_data
    
    def extract_all(self):
        """Extract all content from the PDF."""
        print(f"\nExtracting from: {self.pdf_path}")
        print(f"Output directory: {self.output_dir}")
        print(f"Image filters: min_size={self.min_image_size}px, min_dimension={self.min_image_dimension}px")
        print("=" * 60)
        
        # Extract metadata
        self.extract_metadata()
        
        # Extract content from each page
        for page_num in range(len(self.doc)):
            page_data = self.extract_page(page_num)
            
            # Store summary
            page_data_summary = page_data.copy()
            page_data_summary["text"] = {
                "plain_length": len(page_data["text"]["plain"]),
            }
            
            self.results["pages"].append(page_data_summary)
        
        # Save results
        self.save_results()
        
        # Generate summary
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
        total_words = sum(p["stats"]["word_count"] for p in self.results["pages"])
        
        summary = f"""
PDF EXTRACTION SUMMARY (IMPROVED)
{"=" * 60}

Document: {self.pdf_name}
Pages: {self.results["page_count"]}

CONTENT EXTRACTED:
  • Text: {total_words} words
  • Meaningful Images: {total_images} images (filtered for vision models)
  • Tables: {total_tables} tables (multi-strategy detection)
  • Links: {total_links} links

IMAGE FILTERING:
  • Minimum size: {self.min_image_size} pixels
  • Minimum dimension: {self.min_image_dimension}px
  • Filtered out: icons, logos, small graphics

TABLE DETECTION:
  • Multiple strategies used: lines, lines_strict, text
  • Improved detection for tables without gridlines

OUTPUT LOCATION: {self.output_dir}

FILES GENERATED:
  ✓ metadata.json - Document metadata
  ✓ extraction_results.json - Complete extraction data
  ✓ page_*_text.txt - Plain text per page
  ✓ page_*_table_*.md - Tables in Markdown format
  ✓ page_*_table_*.csv - Tables in CSV format
  ✓ images/ - Meaningful images only (suitable for vision models)

{"=" * 60}
"""
        
        print(summary)
        
        # Save summary
        summary_file = os.path.join(self.output_dir, "SUMMARY.txt")
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary)


def main():
    parser = argparse.ArgumentParser(
        description="Improved PDF extraction with smart image filtering and better table detection"
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
    parser.add_argument(
        "--min-image-size",
        type=int,
        default=10000,
        help="Minimum image size in pixels (width × height) to extract (default: 10000)"
    )
    parser.add_argument(
        "--min-image-dimension",
        type=int,
        default=100,
        help="Minimum width or height in pixels (default: 100)"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: '{args.input}' not found.")
        return
    
    if os.path.isfile(args.input):
        # Single file
        extractor = ImprovedPDFExtractor(
            args.input, 
            args.output,
            min_image_size=args.min_image_size,
            min_image_dimension=args.min_image_dimension
        )
        extractor.extract_all()
    elif os.path.isdir(args.input):
        # Folder processing
        pdf_files = [f for f in os.listdir(args.input) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in '{args.input}'")
            return
        
        output_base = args.output or os.path.join(os.path.dirname(args.input.rstrip('/\\')), "improved_extraction")
        os.makedirs(output_base, exist_ok=True)
        
        for idx, pdf_file in enumerate(pdf_files, 1):
            pdf_path = os.path.join(args.input, pdf_file)
            pdf_name = Path(pdf_file).stem
            pdf_output = os.path.join(output_base, pdf_name)
            
            print(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_file}")
            
            try:
                extractor = ImprovedPDFExtractor(
                    pdf_path,
                    pdf_output,
                    min_image_size=args.min_image_size,
                    min_image_dimension=args.min_image_dimension
                )
                extractor.extract_all()
            except Exception as e:
                print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    main()
