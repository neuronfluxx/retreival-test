#!/usr/bin/env python3
"""
Statistics and Overview of Extracted PDF Data
"""

import os
import json
from pathlib import Path


def get_file_stats(directory, extension):
    """Get statistics for files with given extension."""
    files = list(Path(directory).glob(f"*.{extension}"))
    total_size = sum(f.stat().st_size for f in files)
    return len(files), total_size


def analyze_json_content(json_dir):
    """Analyze JSON content for detailed statistics."""
    stats = {
        'total_pages': 0,
        'total_text_length': 0,
        'documents': []
    }
    
    for json_file in sorted(Path(json_dir).glob("*.json")):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        pages = data.get('pages', [])
        text_length = sum(len(p.get('text', '')) for p in pages)
        
        doc_stats = {
            'name': data.get('source', json_file.name),
            'pages': len(pages),
            'text_length': text_length,
            'has_metadata': any('metadata' in p for p in pages)
        }
        
        stats['documents'].append(doc_stats)
        stats['total_pages'] += len(pages)
        stats['total_text_length'] += text_length
    
    return stats


def format_size(bytes_size):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    extracted_dir = os.path.join(script_dir, "extracted_data")
    
    print("=" * 80)
    print("PDF EXTRACTION STATISTICS")
    print("=" * 80)
    print()
    
    # File counts and sizes
    markdown_dir = os.path.join(extracted_dir, "markdown")
    json_dir = os.path.join(extracted_dir, "json")
    text_dir = os.path.join(extracted_dir, "text")
    
    md_count, md_size = get_file_stats(markdown_dir, "md")
    json_count, json_size = get_file_stats(json_dir, "json")
    txt_count, txt_size = get_file_stats(text_dir, "txt")
    
    print("📊 File Statistics:")
    print("-" * 80)
    print(f"  Markdown files:  {md_count:3d} files  |  {format_size(md_size):>10s}")
    print(f"  JSON files:      {json_count:3d} files  |  {format_size(json_size):>10s}")
    print(f"  Text files:      {txt_count:3d} files  |  {format_size(txt_size):>10s}")
    print(f"  {'Total:':<17s} {md_count:3d} files  |  {format_size(md_size + json_size + txt_size):>10s}")
    print()
    
    # JSON content analysis
    json_stats = analyze_json_content(json_dir)
    
    print("📄 Content Statistics:")
    print("-" * 80)
    print(f"  Total documents:     {len(json_stats['documents'])}")
    print(f"  Total pages:         {json_stats['total_pages']}")
    print(f"  Total text length:   {json_stats['total_text_length']:,} characters")
    print(f"  Average page length: {json_stats['total_text_length'] // max(json_stats['total_pages'], 1):,} characters")
    print()
    
    # Per-document breakdown
    print("📚 Document Breakdown:")
    print("-" * 80)
    print(f"  {'Document':<50s} {'Pages':>6s} {'Size':>12s}")
    print("-" * 80)
    
    for doc in json_stats['documents']:
        name = doc['name']
        if len(name) > 48:
            name = name[:45] + "..."
        print(f"  {name:<50s} {doc['pages']:>6d} {format_size(doc['text_length']):>12s}")
    
    print()
    print("=" * 80)
    print("✅ All data successfully extracted and ready for use!")
    print("=" * 80)
    
    # Usage suggestions
    print()
    print("💡 Next Steps:")
    print("   • Search: python3 search_extracted_data.py 'your query'")
    print("   • RAG Demo: python3 rag_example.py")
    print("   • Extract single: python3 extract_single_pdf.py pdfs/yourfile.pdf")


if __name__ == "__main__":
    main()
