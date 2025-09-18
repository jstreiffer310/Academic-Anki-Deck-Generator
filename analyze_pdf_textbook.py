#!/usr/bin/env python3
"""
Extract text content from the textbook PDF and search for specific terms
"""

import requests
import json
import PyPDF2
import re
from pathlib import Path

def anki_connect(action, **params):
    """Connect to AnkiConnect API"""
    return requests.post('http://localhost:8765', json={
        'action': action,
        'version': 6,
        'params': params
    }).json()

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            # Extract first 100 pages to avoid overwhelming output
            max_pages = min(100, len(pdf_reader.pages))
            
            for page_num in range(max_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.lower()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def main():
    print("🧠 TEXTBOOK PDF ANALYSIS")
    print("Extracting content from actual textbook PDF")
    print("=" * 60)
    
    pdf_path = "An Introduction to Brain and Behavior 7th Edition.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print("📚 Extracting text from PDF (first 100 pages)...")
    textbook_content = extract_pdf_text(pdf_path)
    
    if not textbook_content:
        print("❌ Could not extract text from PDF")
        return
    
    print(f"📄 Extracted {len(textbook_content):,} characters from PDF")
    
    # Terms to search for from previously deleted cards
    search_terms = [
        'korsakoff',
        'wernicke',
        'thiamine',
        'vitamin b1',
        'encephalopathy',
        'amnesia',
        'anterograde amnesia',
        'memory disorder',
        'confabulation',
        'mammillary bodies',
        'alcohol',
        'alcoholism'
    ]
    
    print(f"\n🔍 Searching for {len(search_terms)} key terms...")
    
    found_terms = []
    for term in search_terms:
        if term in textbook_content:
            found_terms.append(term)
            print(f"✅ Found: '{term}'")
        else:
            print(f"❌ Not found: '{term}'")
    
    print(f"\n📊 RESULTS:")
    print(f"Found {len(found_terms)} out of {len(search_terms)} terms in textbook")
    
    if found_terms:
        print(f"\n✅ Terms found in textbook: {', '.join(found_terms)}")
        print("\n🔄 These terms suggest legitimate textbook coverage")
        print("📝 Cards related to these terms should be restored")
    else:
        print("\n❌ No relevant terms found in textbook")
        print("🚫 Previously deleted cards were correctly removed")

if __name__ == "__main__":
    main()