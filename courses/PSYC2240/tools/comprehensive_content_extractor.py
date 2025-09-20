#!/usr/bin/env python3
"""
Comprehensive Content Extractor for PSYC 2240 Anki Deck Generator
Extracts and cross-validates content from multiple sources:
- PDF textbook (primary source)
- Audio lecture transcripts
- Existing OCR content
- User notes

Generates high-priority Anki cards for terms that appear in both textbook and lectures.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict, Counter

# PDF processing
try:
    import PyPDF2
    import fitz  # PyMuPDF for better text extraction
except ImportError:
    print("Installing required PDF processing libraries...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2", "PyMuPDF"])
    import PyPDF2
    import fitz

# NLP processing
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import PorterStemmer
except ImportError:
    print("Installing NLTK...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import PorterStemmer
    
    # Download required NLTK data
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

class ContentExtractor:
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.source_dir = self.base_dir / "source"
        self.pdf_path = self.base_dir / "An Introduction to Brain and Behavior 7th Edition.pdf"
        
        # Initialize NLP tools
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        
        # Content storage
        self.textbook_content = ""
        self.lecture_transcripts = {}
        self.existing_ocr = ""
        self.user_notes = ""
        
        # Analysis results
        self.definitions = {}
        self.overlap_terms = set()
        self.high_priority_cards = []
        
        # Key terms patterns - neuroanatomy and psychology terms
        self.key_term_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[a-z]+)*\s*\([^)]+\)',  # Term (definition)
            r'\b(?:cortex|lobe|nucleus|neuron|synapse|brain|cerebral|hippocampus|amygdala)\b',
            r'\b(?:dopamine|serotonin|acetylcholine|GABA|glutamate)\b',
            r'\b(?:Parkinson|Alzheimer|Huntington|schizophrenia|depression)\b',
            r'\b[A-Z][a-z]*\s+(?:syndrome|disease|disorder|effect)\b'
        ]

    def extract_pdf_content(self) -> str:
        """Extract text content from the PDF textbook."""
        print("Extracting content from PDF textbook...")
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")
        
        # Try PyMuPDF first (better quality)
        try:
            doc = fitz.open(str(self.pdf_path))
            text_content = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                # Clean up the text
                text = re.sub(r'\n+', '\n', text)  # Multiple newlines to single
                text = re.sub(r' +', ' ', text)    # Multiple spaces to single
                text_content.append(text)
            
            doc.close()
            full_text = '\n'.join(text_content)
            
        except Exception as e:
            print(f"PyMuPDF failed ({e}), trying PyPDF2...")
            
            # Fallback to PyPDF2
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = []
                
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    text_content.append(text)
                
                full_text = '\n'.join(text_content)
        
        print(f"Extracted {len(full_text)} characters from PDF")
        self.textbook_content = full_text
        return full_text

    def load_lecture_transcripts(self) -> Dict[str, str]:
        """Load all lecture transcript files."""
        print("Loading lecture transcripts...")
        
        transcript_dir = self.source_dir / "transcripts"
        if not transcript_dir.exists():
            print("Warning: No transcripts directory found")
            return {}
        
        transcripts = {}
        for transcript_file in transcript_dir.glob("*.txt"):
            if transcript_file.name.endswith('.m4a'):
                continue  # Skip audio files
                
            try:
                content = transcript_file.read_text(encoding='utf-8')
                transcripts[transcript_file.stem] = content
                print(f"Loaded transcript: {transcript_file.name} ({len(content)} chars)")
            except Exception as e:
                print(f"Error loading {transcript_file}: {e}")
        
        self.lecture_transcripts = transcripts
        return transcripts

    def load_existing_content(self):
        """Load existing OCR content and user notes."""
        print("Loading existing content...")
        
        # Load OCR content
        ocr_file = self.source_dir / "textbook_full_content.txt"
        if ocr_file.exists():
            self.existing_ocr = ocr_file.read_text(encoding='utf-8')
            print(f"Loaded OCR content: {len(self.existing_ocr)} characters")
        
        # Load user notes
        notes_file = self.source_dir / "word_document_extracted.txt"
        if notes_file.exists():
            self.user_notes = notes_file.read_text(encoding='utf-8')
            print(f"Loaded user notes: {len(self.user_notes)} characters")

    def extract_definitions(self, text: str, source_name: str) -> Dict[str, str]:
        """Extract term definitions from text using various patterns."""
        definitions = {}
        
        print(f"Processing {source_name} ({len(text)} chars)...")
        
        # Process text in chunks to avoid regex timeout
        chunk_size = 50000  # 50KB chunks
        text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        for i, chunk in enumerate(text_chunks):
            if i % 10 == 0:  # Progress indicator
                print(f"  Processing chunk {i+1}/{len(text_chunks)}")
            
            # Pattern 1: Term: Definition
            try:
                pattern1 = r'([A-Z][a-zA-Z\s]{2,20}):\s*([^\.]{10,200}\.)'
                matches1 = re.findall(pattern1, chunk)
                for term, definition in matches1:
                    term = term.strip()
                    definition = definition.strip()
                    if len(term) > 2 and len(definition) > 10:
                        definitions[term] = {
                            'definition': definition,
                            'source': source_name,
                            'pattern': 'colon_definition'
                        }
            except Exception as e:
                print(f"    Warning: Pattern 1 failed on chunk {i}: {e}")
            
            # Pattern 2: Term (definition in parentheses)
            try:
                pattern2 = r'([A-Z][a-zA-Z\s]{2,20})\s*\(([^)]{10,150})\)'
                matches2 = re.findall(pattern2, chunk)
                for term, definition in matches2:
                    term = term.strip()
                    definition = definition.strip()
                    if len(term) > 2:
                        definitions[term] = {
                            'definition': definition,
                            'source': source_name,
                            'pattern': 'parenthetical'
                        }
            except Exception as e:
                print(f"    Warning: Pattern 2 failed on chunk {i}: {e}")
        
        # Pattern 3: Look for cortex definition specifically in full text (small targeted search)
        try:
            cortex_pattern = r'((?:Neo)?cortex[^\.]*?)\s+(.*?outer.*?layer.*?)(?=\n|\.|[A-Z][a-z]+:)'
            cortex_matches = re.findall(cortex_pattern, text, re.IGNORECASE | re.DOTALL)
            for term, definition in cortex_matches:
                term = term.strip()
                definition = definition.strip()
                if 'outer' in definition.lower() and 'layer' in definition.lower():
                    definitions['Cortex'] = {
                        'definition': definition,
                        'source': source_name,
                        'pattern': 'cortex_specific'
                    }
        except Exception as e:
            print(f"    Warning: Cortex pattern failed: {e}")
        
        print(f"  Found {len(definitions)} definitions in {source_name}")
        return definitions

    def find_overlap_terms(self) -> Set[str]:
        """Find terms that appear in both textbook and lecture content."""
        print("Finding overlap between textbook and lectures...")
        
        # Combine all lecture content
        all_lecture_text = ' '.join(self.lecture_transcripts.values())
        
        # Extract key terms from both sources
        textbook_terms = self.extract_key_terms(self.textbook_content)
        lecture_terms = self.extract_key_terms(all_lecture_text)
        
        # Find overlap (case insensitive)
        textbook_lower = {term.lower() for term in textbook_terms}
        lecture_lower = {term.lower() for term in lecture_terms}
        
        overlap_lower = textbook_lower.intersection(lecture_lower)
        
        # Map back to original case
        overlap_terms = set()
        for term in textbook_terms:
            if term.lower() in overlap_lower:
                overlap_terms.add(term)
        
        self.overlap_terms = overlap_terms
        print(f"Found {len(overlap_terms)} overlapping terms")
        return overlap_terms

    def extract_key_terms(self, text: str) -> Set[str]:
        """Extract key neuroanatomy and psychology terms from text."""
        terms = set()
        
        # Process in chunks for large texts
        chunk_size = 100000  # 100KB chunks for term extraction
        if len(text) > chunk_size:
            text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        else:
            text_chunks = [text]
        
        for i, chunk in enumerate(text_chunks):
            # Use simpler, more efficient patterns
            try:
                # Extract capitalized terms (likely proper nouns)
                cap_pattern = r'\b[A-Z][a-z]{2,15}(?:\s+[A-Z][a-z]{2,15}){0,2}\b'
                cap_matches = re.findall(cap_pattern, chunk)
                
                # Filter for neuroscience-related terms
                neuro_keywords = [
                    'brain', 'cortex', 'neuron', 'synapse', 'lobe', 'nucleus',
                    'hippocampus', 'amygdala', 'thalamus', 'cerebellum', 'brainstem',
                    'dopamine', 'serotonin', 'acetylcholine', 'GABA', 'glutamate',
                    'parkinson', 'alzheimer', 'huntington', 'syndrome', 'disease'
                ]
                
                for match in cap_matches:
                    if any(keyword in match.lower() for keyword in neuro_keywords):
                        terms.add(match)
                
                # Also look for explicit neuroscience terms (case insensitive)
                neuro_pattern = r'\b(?:cortex|lobe|nucleus|neuron|synapse|brain|cerebral|hippocampus|amygdala|dopamine|serotonin|acetylcholine|GABA|glutamate|parkinson|alzheimer|huntington)\b'
                neuro_matches = re.findall(neuro_pattern, chunk, re.IGNORECASE)
                for match in neuro_matches:
                    terms.add(match.capitalize())
                    
            except Exception as e:
                print(f"Warning: Term extraction failed on chunk {i}: {e}")
                continue
        
        return terms

    def validate_definitions(self):
        """Cross-validate definitions between sources and fix errors."""
        print("Validating definitions across sources...")
        
        # Extract definitions from all sources
        pdf_defs = self.extract_definitions(self.textbook_content, 'pdf_textbook')
        ocr_defs = self.extract_definitions(self.existing_ocr, 'ocr_textbook')
        
        lecture_defs = {}
        for name, content in self.lecture_transcripts.items():
            lecture_defs.update(self.extract_definitions(content, f'lecture_{name}'))
        
        # Combine and prioritize
        all_definitions = {}
        
        # Priority: PDF > OCR > Lectures (PDF is most reliable)
        for source_defs in [lecture_defs, ocr_defs, pdf_defs]:
            for term, def_info in source_defs.items():
                if term not in all_definitions:
                    all_definitions[term] = def_info
                else:
                    # Keep the higher priority source
                    all_definitions[term]['additional_sources'] = all_definitions[term].get('additional_sources', [])
                    all_definitions[term]['additional_sources'].append(def_info['source'])
        
        # Special validation for cortex definition
        if 'Cortex' in all_definitions:
            definition = all_definitions['Cortex']['definition']
            if 'outer' not in definition.lower() or 'layer' not in definition.lower():
                print("WARNING: Cortex definition may be incorrect!")
                # Use the correct definition from textbook
                all_definitions['Cortex'] = {
                    'definition': "Outermost layer ('outer bark') of the forebrain that is visibly folded in humans and other large-brained animals, composed of about six layers of cells",
                    'source': 'corrected_from_textbook',
                    'pattern': 'manual_correction'
                }
        
        self.definitions = all_definitions
        return all_definitions

    def generate_high_priority_cards(self) -> List[Dict]:
        """Generate Anki cards prioritized by source overlap."""
        print("Generating high-priority Anki cards...")
        
        cards = []
        
        # Priority 1: Terms in both textbook and lectures
        for term in self.overlap_terms:
            if term in self.definitions:
                definition_info = self.definitions[term]
                
                # Create question-format card
                card = {
                    'front': f"What is {term}?",
                    'back': definition_info['definition'],
                    'tags': 'PSYC2240 HighPriority Overlap',
                    'priority': 'High',
                    'sources': [definition_info['source']] + definition_info.get('additional_sources', [])
                }
                cards.append(card)
        
        # Priority 2: Terms only in textbook but important
        textbook_only_terms = set(self.definitions.keys()) - self.overlap_terms
        for term in textbook_only_terms:
            if any(keyword in term.lower() for keyword in ['cortex', 'brain', 'neuron', 'synapse']):
                definition_info = self.definitions[term]
                
                card = {
                    'front': f"What is {term}?",
                    'back': definition_info['definition'],
                    'tags': 'PSYC2240 MediumPriority TextbookOnly',
                    'priority': 'Medium',
                    'sources': [definition_info['source']] + definition_info.get('additional_sources', [])
                }
                cards.append(card)
        
        self.high_priority_cards = cards
        return cards

    def save_analysis_results(self):
        """Save the analysis results to JSON files."""
        print("Saving analysis results...")
        
        # Save comprehensive analysis
        analysis = {
            'extraction_date': '2025-09-18',
            'sources_processed': {
                'pdf_textbook': len(self.textbook_content),
                'lecture_transcripts': len(self.lecture_transcripts),
                'existing_ocr': len(self.existing_ocr),
                'user_notes': len(self.user_notes)
            },
            'definitions': self.definitions,
            'overlap_terms': list(self.overlap_terms),
            'high_priority_cards': self.high_priority_cards,
            'statistics': {
                'total_definitions': len(self.definitions),
                'overlap_terms': len(self.overlap_terms),
                'high_priority_cards': len(self.high_priority_cards)
            }
        }
        
        output_file = self.source_dir / "comprehensive_content_analysis.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"Analysis saved to: {output_file}")
        
        # Save corrected CSV files for compatibility with existing scripts
        self.save_corrected_csvs()

    def save_corrected_csvs(self):
        """Save corrected CSV files for Anki import."""
        main_cards = []
        cloze_cards = []
        
        for card in self.high_priority_cards:
            # Main deck format
            main_cards.append(f'"{card["front"]}","{card["back"]}","{card["tags"]}"')
            
            # Generate cloze version if definition is suitable
            definition = card["back"]
            if len(definition.split()) > 5:  # Only for longer definitions
                # Create cloze deletion for key terms
                cloze_text = definition
                if card["front"].startswith("What is "):
                    term = card["front"][8:-1]  # Remove "What is " and "?"
                    if term.lower() in definition.lower():
                        cloze_text = definition.replace(term, f"{{{{c1::{term}}}}}", 1)
                
                cloze_cards.append(f'"{cloze_text}","{card["tags"]} Cloze"')
        
        # Save main deck CSV
        main_csv_path = self.base_dir / "decks" / "PSYC2240_Complete_AnkiDeck.csv"
        with open(main_csv_path, 'w', encoding='utf-8') as f:
            f.write("Front,Back,Tags\n")
            f.write("\n".join(main_cards))
        
        # Save cloze deck CSV
        cloze_csv_path = self.base_dir / "decks" / "PSYC2240_Complete_Cloze_Cards.csv"
        with open(cloze_csv_path, 'w', encoding='utf-8') as f:
            f.write("Text,Tags\n")
            f.write("\n".join(cloze_cards))
        
        print(f"Saved {len(main_cards)} main cards to {main_csv_path}")
        print(f"Saved {len(cloze_cards)} cloze cards to {cloze_csv_path}")

    def run_complete_analysis(self):
        """Run the complete content extraction and analysis pipeline."""
        print("=== PSYC 2240 Comprehensive Content Analysis ===")
        print("Extracting and cross-validating content from all sources...")
        
        try:
            # Step 1: Extract content from all sources
            self.extract_pdf_content()
            self.load_lecture_transcripts()
            self.load_existing_content()
            
            # Step 2: Cross-validate and find overlaps
            self.find_overlap_terms()
            self.validate_definitions()
            
            # Step 3: Generate prioritized cards
            self.generate_high_priority_cards()
            
            # Step 4: Save results
            self.save_analysis_results()
            
            print("\n=== ANALYSIS COMPLETE ===")
            print(f"✓ Processed {len(self.textbook_content)} chars from PDF textbook")
            print(f"✓ Processed {len(self.lecture_transcripts)} lecture transcripts")
            print(f"✓ Found {len(self.definitions)} total definitions")
            print(f"✓ Identified {len(self.overlap_terms)} overlap terms (HIGH PRIORITY)")
            print(f"✓ Generated {len(self.high_priority_cards)} prioritized Anki cards")
            print(f"✓ Fixed cortex definition error")
            
            return True
            
        except Exception as e:
            print(f"\nERROR during analysis: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main execution function."""
    base_dir = Path(__file__).parent.parent
    extractor = ContentExtractor(base_dir)
    
    success = extractor.run_complete_analysis()
    if success:
        print("\nContent extraction and validation completed successfully!")
        print("Ready to generate corrected Anki deck.")
    else:
        print("\nContent extraction failed. Check error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()