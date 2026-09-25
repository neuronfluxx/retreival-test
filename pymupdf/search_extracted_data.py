#!/usr/bin/env python3
"""
Search Tool for Extracted PDF Data

This script provides simple search functionality across extracted PDF content.
"""

import os
import json
import sys
from pathlib import Path


def search_markdown(query, markdown_dir):
    """Search through markdown files."""
    results = []
    query_lower = query.lower()
    
    for md_file in Path(markdown_dir).glob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if query_lower in content.lower():
            # Find context around the match
            lines = content.split('\n')
            matching_lines = []
            
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    # Get context: 2 lines before and after
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    context = '\n'.join(lines[start:end])
                    matching_lines.append((i + 1, context))
            
            if matching_lines:
                results.append({
                    'file': md_file.name,
                    'matches': matching_lines
                })
    
    return results


def search_json(query, json_dir):
    """Search through JSON files."""
    results = []
    query_lower = query.lower()
    
    for json_file in Path(json_dir).glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        matches = []
        if 'pages' in data:
            for page in data['pages']:
                text = page.get('text', '')
                if query_lower in text.lower():
                    # Get a snippet around the match
                    idx = text.lower().find(query_lower)
                    start = max(0, idx - 100)
                    end = min(len(text), idx + len(query) + 100)
                    snippet = text[start:end]
                    
                    matches.append({
                        'page': page.get('page_number', 'unknown'),
                        'snippet': f"...{snippet}..."
                    })
        
        if matches:
            results.append({
                'file': json_file.name,
                'source': data.get('source', 'unknown'),
                'matches': matches
            })
    
    return results


def display_results(query, markdown_results, json_results):
    """Display search results."""
    print("=" * 80)
    print(f"Search Results for: '{query}'")
    print("=" * 80)
    
    if markdown_results:
        print(f"\n📄 Found in {len(markdown_results)} Markdown file(s):\n")
        
        for result in markdown_results:
            print(f"  File: {result['file']}")
            print(f"  Matches: {len(result['matches'])}")
            
            for line_num, context in result['matches'][:3]:  # Show first 3 matches
                print(f"\n    Line {line_num}:")
                print(f"    {'-' * 70}")
                for line in context.split('\n'):
                    print(f"    {line}")
                print()
            
            if len(result['matches']) > 3:
                print(f"    ... and {len(result['matches']) - 3} more match(es)\n")
            print()
    
    if json_results:
        print(f"\n📋 Found in {len(json_results)} JSON file(s):\n")
        
        for result in json_results:
            print(f"  File: {result['file']}")
            print(f"  Source: {result['source']}")
            print(f"  Matches: {len(result['matches'])}")
            
            for match in result['matches'][:3]:  # Show first 3 matches
                print(f"\n    Page {match['page']}:")
                print(f"    {'-' * 70}")
                print(f"    {match['snippet']}")
                print()
            
            if len(result['matches']) > 3:
                print(f"    ... and {len(result['matches']) - 3} more match(es)\n")
            print()
    
    total_matches = len(markdown_results) + len(json_results)
    if total_matches == 0:
        print(f"\n❌ No results found for '{query}'")
    else:
        print("=" * 80)
        print(f"Total: {total_matches} file(s) with matches")


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("PDF Data Search Tool")
        print("\nUsage: python3 search_extracted_data.py <search_query>")
        print("\nExample:")
        print("  python3 search_extracted_data.py 'solar panel'")
        print("  python3 search_extracted_data.py 'transformer'")
        print("  python3 search_extracted_data.py 'attention mechanism'")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    
    # Set up directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    extracted_dir = os.path.join(script_dir, "extracted_data")
    markdown_dir = os.path.join(extracted_dir, "markdown")
    json_dir = os.path.join(extracted_dir, "json")
    
    # Check if extracted data exists
    if not os.path.exists(extracted_dir):
        print(f"Error: Extracted data directory not found: {extracted_dir}")
        print("Please run 'python3 extract_pdfs.py' first.")
        sys.exit(1)
    
    # Search both formats
    markdown_results = search_markdown(query, markdown_dir) if os.path.exists(markdown_dir) else []
    json_results = search_json(query, json_dir) if os.path.exists(json_dir) else []
    
    # Display results
    display_results(query, markdown_results, json_results)


if __name__ == "__main__":
    main()
