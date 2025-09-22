#!/usr/bin/env python3
"""
PSYC2120 Deck Builder - Adapted from PSYC2240 rebuild_consolidated_deck.py
Creates final CSV and .apkg files from the comprehensive analysis
"""

import json
import os
import csv
import sys
from pathlib import Path
from datetime import datetime

# Add PSYC2240 tools to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "PSYC2240" / "tools"))

try:
    import genanki
except ImportError:
    print("Installing genanki...")
    os.system("pip install genanki")
    import genanki

class PSYC2120DeckBuilder:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.analysis_file = self.base_dir / "content" / "analysis" / "psyc2120_comprehensive_analysis.json"
        self.decks_dir = self.base_dir / "decks"
        self.decks_dir.mkdir(exist_ok=True)
        
    def load_analysis(self):
        """Load the comprehensive analysis"""
        if not self.analysis_file.exists():
            print("❌ ERROR: Analysis file not found! Run content extraction first.")
            return None
            
        with open(self.analysis_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_csv_deck(self, cards):
        """Create CSV file for Anki import"""
        csv_file = self.decks_dir / "PSYC2120_Complete_AnkiDeck.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Front', 'Back', 'Tags'])  # Header
            
            for card in cards:
                front = card.get('front', '').strip()
                back = card.get('back', '').strip()
                tags = card.get('tags', '').strip()
                
                # Skip cards with placeholder answers
                if 'Answer to be extracted' in back:
                    continue
                    
                # Clean up text
                front = self.clean_text(front)
                back = self.clean_text(back)
                
                writer.writerow([front, back, tags])
        
        print(f"📄 CSV deck created: {csv_file}")
        return csv_file
    
    def clean_text(self, text):
        """Clean text for CSV export"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Escape quotes
        text = text.replace('"', '""')
        return text
    
    def create_anki_package(self, cards):
        """Create .apkg file for direct import"""
        # Create note type
        note_type = genanki.Model(
            1607392320,  # Unique model ID for PSYC2120
            'PSYC2120 Social Psychology Optimized',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
                {'name': 'Tags'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '<div class="question">{{Question}}</div>',
                    'afmt': '''
                        <div class="question">{{Question}}</div>
                        <hr id="answer">
                        <div class="answer">{{Answer}}</div>
                        <div class="tags">{{Tags}}</div>
                    ''',
                },
            ],
            css='''
                .card {
                    font-family: arial;
                    font-size: 16px;
                    text-align: center;
                    color: black;
                    background-color: white;
                }
                .question {
                    font-weight: bold;
                    margin-bottom: 10px;
                    color: #2c3e50;
                }
                .answer {
                    margin-top: 10px;
                    color: #27ae60;
                }
                .tags {
                    font-size: 12px;
                    color: #7f8c8d;
                    margin-top: 10px;
                }
            '''
        )
        
        # Create deck
        deck = genanki.Deck(
            2059400110,  # Unique deck ID for PSYC2120
            'PSYC2120 - Social Psychology (Complete Deck)'
        )
        
        # Add cards to deck
        valid_cards = 0
        for card_data in cards:
            front = card_data.get('front', '').strip()
            back = card_data.get('back', '').strip()
            tags = card_data.get('tags', '').strip()
            
            # Skip cards with placeholder answers
            if 'Answer to be extracted' in back or not back:
                continue
            
            note = genanki.Note(
                model=note_type,
                fields=[front, back, tags]
            )
            deck.add_note(note)
            valid_cards += 1
        
        # Generate package
        package_file = self.decks_dir / "PSYC2120_Complete_Deck.apkg"
        genanki.Package(deck).write_to_file(str(package_file))
        
        print(f"📦 Anki package created: {package_file}")
        print(f"   Cards included: {valid_cards}")
        return package_file
    
    def generate_summary_report(self, analysis_data, cards):
        """Generate a summary report of the deck"""
        report_file = self.decks_dir / "PSYC2120_Deck_Summary.md"
        
        valid_cards = [c for c in cards if 'Answer to be extracted' not in c.get('back', '')]
        
        # Count cards by priority
        priority_counts = {}
        for card in valid_cards:
            priority = card.get('priority', 'unknown')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Count cards by source
        source_counts = {}
        for card in valid_cards:
            source = card.get('source', 'unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# PSYC2120 - Social Psychology Anki Deck Summary\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📊 Deck Statistics\n\n")
            f.write(f"- **Total Learning Objectives Extracted**: {len(analysis_data.get('learning_objectives', []))}\n")
            f.write(f"- **Total Cards Generated**: {len(cards)}\n")
            f.write(f"- **Valid Cards**: {len(valid_cards)}\n")
            f.write(f"- **Lectures Processed**: {len(analysis_data.get('lectures', []))}\n\n")
            
            f.write("## 🎯 Card Distribution by Priority\n\n")
            for priority, count in sorted(priority_counts.items()):
                f.write(f"- **{priority.title()}**: {count} cards\n")
            f.write("\n")
            
            f.write("## 📚 Card Distribution by Source\n\n")
            for source, count in sorted(source_counts.items()):
                f.write(f"- **{source}**: {count} cards\n")
            f.write("\n")
            
            f.write("## 🎓 Content Sources\n\n")
            f.write("### Lectures Analyzed\n")
            for lecture in analysis_data.get('lectures', []):
                f.write(f"- {lecture.get('folder', 'Unknown')}\n")
            f.write("\n")
            
            f.write("### Test Focus\n")
            test_focus = analysis_data.get('test_focus', {})
            if test_focus.get('chapters'):
                f.write("**Chapters Covered**:\n")
                for chapter in test_focus['chapters']:
                    f.write(f"- {chapter}\n")
            f.write("\n")
            
            f.write("## 📖 How to Use\n\n")
            f.write("1. **Import CSV**: Use `PSYC2120_Complete_AnkiDeck.csv` for manual import\n")
            f.write("2. **Import Package**: Use `PSYC2120_Complete_Deck.apkg` for direct import\n")
            f.write("3. **Study Settings**: Enable FSRS algorithm for optimal spaced repetition\n")
            f.write("4. **Priority**: Focus on 'High' priority cards first\n\n")
            
            f.write("## 🔧 Quality Improvements\n\n")
            f.write("This deck incorporates lessons learned from PSYC2240:\n")
            f.write("- Learning Objectives (LOQ) as primary source for questions\n")
            f.write("- Natural question phrasing for better recall\n")
            f.write("- Cross-validation between lectures and textbook\n")
            f.write("- Focus on Test 1 relevant content\n")
            f.write("- Removal of irrelevant personal anecdotes\n\n")
        
        print(f"📋 Summary report created: {report_file}")
        return report_file
    
    def build_complete_deck(self):
        """Build the complete PSYC2120 deck"""
        print("🏗️ Building PSYC2120 Complete Deck")
        
        # Load analysis
        analysis_data = self.load_analysis()
        if not analysis_data:
            return False
        
        cards = analysis_data.get('generated_cards', [])
        if not cards:
            print("❌ No cards found in analysis data")
            return False
        
        print(f"📊 Processing {len(cards)} cards...")
        
        # Create CSV deck
        csv_file = self.create_csv_deck(cards)
        
        # Create Anki package
        apkg_file = self.create_anki_package(cards)
        
        # Generate summary report
        report_file = self.generate_summary_report(analysis_data, cards)
        
        print("✅ PSYC2120 deck build complete!")
        print(f"   📄 CSV: {csv_file.name}")
        print(f"   📦 Package: {apkg_file.name}")
        print(f"   📋 Report: {report_file.name}")
        
        return True

if __name__ == "__main__":
    builder = PSYC2120DeckBuilder()
    builder.build_complete_deck()