#!/usr/bin/env python3
"""
PSYC 2240 - Consolidated Content to Native Anki Deck
Rebuilds deck from comprehensive content analysis using proper protocols
"""

import json
import os
import sys
import sqlite3
import zipfile
import tempfile
import shutil
import glob
from datetime import datetime
import uuid

try:
    import genanki
except ImportError:
    print("Installing genanki...")
    os.system("pip install genanki")
    import genanki

def load_comprehensive_analysis():
    """Load the comprehensive content analysis JSON"""
    # Use relative path from script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    analysis_path = os.path.join(workspace_root, "content", "analysis", "comprehensive_content_analysis.json")
    
    if not os.path.exists(analysis_path):
        print("❌ ERROR: comprehensive_content_analysis.json not found!")
        print("Run content analysis first to generate this file.")
        return None
        
    with open(analysis_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_memory_optimized_note_type():
    """Create Anki note type optimized for memory retention"""
    return genanki.Model(
        1607392319,  # Fixed model ID
        'PSYC2240 Memory Optimized',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
            {'name': 'Priority'},
            {'name': 'Source'},
            {'name': 'Chapter'},
            {'name': 'Clinical'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '''
<div class="card">
    <div class="priority priority-{{Priority}}">{{Priority}} Priority</div>
    <div class="question">{{Question}}</div>
    {{#Clinical}}<div class="clinical">Clinical Application</div>{{/Clinical}}
</div>
                ''',
                'afmt': '''
<div class="card">
    <div class="priority priority-{{Priority}}">{{Priority}} Priority</div>
    <div class="question">{{Question}}</div>
    <hr>
    <div class="answer">{{Answer}}</div>
    <div class="meta">
        <span class="source">{{Source}}</span> | 
        <span class="chapter">{{Chapter}}</span>
        {{#Clinical}} | <span class="clinical">Clinical</span>{{/Clinical}}
    </div>
</div>
                ''',
            }
        ],
        css='''
.card { 
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 18px;
    line-height: 1.5;
    color: #2c3e50;
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
}

.priority {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.priority-HIGH { background: #e74c3c; color: white; }
.priority-MEDIUM { background: #f39c12; color: white; }
.priority-LOW { background: #95a5a6; color: white; }

.question {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 15px;
    color: #2c3e50;
}

.answer {
    font-size: 18px;
    margin-bottom: 15px;
    padding: 15px;
    background: white;
    border-left: 4px solid #3498db;
    border-radius: 4px;
}

.clinical {
    background: #27ae60;
    color: white;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: bold;
}

.meta {
    font-size: 14px;
    color: #7f8c8d;
    text-align: right;
    margin-top: 10px;
}

.source, .chapter {
    font-weight: 500;
}
        '''
    )

def create_cloze_note_type():
    """Create cloze deletion note type for context retention"""
    return genanki.Model(
        1607392320,  # Fixed model ID
        'PSYC2240 Cloze Context',
        fields=[
            {'name': 'Text'},
            {'name': 'Priority'},
            {'name': 'Source'},
            {'name': 'Chapter'},
        ],
        templates=[
            {
                'name': 'Cloze',
                'qfmt': '''
<div class="card">
    <div class="priority priority-{{Priority}}">{{Priority}} Priority</div>
    <div class="cloze">{{cloze:Text}}</div>
</div>
                ''',
                'afmt': '''
<div class="card">
    <div class="priority priority-{{Priority}}">{{Priority}} Priority</div>
    <div class="cloze">{{cloze:Text}}</div>
    <div class="meta">
        <span class="source">{{Source}}</span> | 
        <span class="chapter">{{Chapter}}</span>
    </div>
</div>
                ''',
            }
        ],
        css='''
.card { 
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 18px;
    line-height: 1.6;
    color: #2c3e50;
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
}

.priority {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.priority-HIGH { background: #e74c3c; color: white; }
.priority-MEDIUM { background: #f39c12; color: white; }
.priority-LOW { background: #95a5a6; color: white; }

.cloze {
    font-size: 18px;
    line-height: 1.8;
    padding: 20px;
    background: white;
    border-radius: 6px;
    border-left: 4px solid #9b59b6;
}

.meta {
    font-size: 14px;
    color: #7f8c8d;
    text-align: right;
    margin-top: 15px;
}
        '''
    )

def extract_question_answer_pairs(analysis_data):
    """Extract Q&A pairs from comprehensive analysis following protocols"""
    
    cards = []
    
    # Process overlap terms (highest quality - cross-validated)
    for term in analysis_data.get('overlap_terms', []):
        if 'definition_preview' not in term or not term['definition_preview']:
            continue
            
        # Fix the cortex definition error
        definition = term['definition_preview']
        if 'cortex' in term.get('term', '').lower():
            if 'containing most neurons' in definition:
                definition = "Outer layer of brain tissue responsible for higher-order processing and consciousness"
        
        # Create memory-optimized question format
        question = f"What is {term['term']}?" if not term['term'].endswith('?') else term['term']
        
        # Determine priority based on content analysis and clinical importance
        priority = term.get('priority', 'MEDIUM').upper()
        if priority not in ['HIGH', 'MEDIUM', 'LOW']:
            priority = 'MEDIUM'
        
        # Boost priority for clinical terms and key concepts
        term_lower = term['term'].lower()
        definition_lower = definition.lower()
        
        if (term.get('clinical', False) or 
            any(clinical_word in term_lower for clinical_word in 
                ['disease', 'disorder', 'syndrome', 'patient', 'case']) or
            any(key_concept in term_lower for key_concept in 
                ['cortex', 'brain', 'neuron', 'synapse', 'memory', 'learning'])):
            if priority == 'MEDIUM':
                priority = 'HIGH'
        
        # Set some terms to LOW priority for balanced distribution
        if (len(definition) < 50 or 
            any(background_word in term_lower for background_word in 
                ['history', 'background', 'introduction', 'overview']) and 
            priority == 'MEDIUM'):
            priority = 'LOW'
            
        # Determine source and chapter
        source = determine_source_from_term(term)
        chapter = determine_chapter_from_term(term)
        is_clinical = term.get('clinical', False)
        
        cards.append({
            'question': question,
            'answer': definition,
            'priority': priority,
            'source': source,
            'chapter': chapter,
            'clinical': is_clinical,
            'type': 'basic'
        })
    
    return cards

def determine_source_from_term(term):
    """Determine source based on term characteristics"""
    term_text = term.get('term', '').lower()
    definition = term.get('definition_preview', '').lower()
    
    if any(keyword in term_text for keyword in ['case', 'patient', 'disease', 'disorder', 'syndrome']):
        return 'Clinical Cases'
    elif any(keyword in definition for keyword in ['chapter', 'figure', 'page']):
        return 'Textbook'
    elif any(keyword in definition for keyword in ['lecture', 'class', 'discuss']):
        return 'Lectures'
    else:
        return 'Cross-Reference'

def determine_chapter_from_term(term):
    """Determine chapter based on term content"""
    term_text = term.get('term', '').lower()
    definition = term.get('definition_preview', '').lower()
    
    # Chapter 1: Introduction and overview
    if any(keyword in term_text + definition for keyword in 
           ['introduction', 'history', 'evolution', 'overview', 'principles']):
        return 'Chapter 1'
    
    # Chapter 2: Brain anatomy and structure  
    elif any(keyword in term_text + definition for keyword in 
             ['cortex', 'brain', 'anatomy', 'structure', 'lobe', 'hemisphere']):
        return 'Chapter 2'
    
    # Chapter 3: Cellular and molecular
    elif any(keyword in term_text + definition for keyword in 
             ['neuron', 'cell', 'molecular', 'synapse', 'neurotransmitter']):
        return 'Chapter 3'
    
    else:
        return 'Multiple Chapters'

def create_cloze_cards_from_analysis(analysis_data):
    """Create cloze cards from contextual content"""
    
    cloze_cards = []
    
    # Extract key contextual passages and create cloze deletions
    for term in analysis_data.get('overlap_terms', []):
        definition = term.get('definition_preview', '')
        if len(definition) > 50:  # Good context length
            
            # Create cloze deletion for key terms
            term_name = term['term']
            
            # Create meaningful cloze deletions
            if len(definition) > 100:
                # Find key concepts to hide
                key_concepts = [term_name]
                
                # Add important keywords based on context
                if 'brain' in definition.lower():
                    key_concepts.extend(['brain', 'cortex', 'neurons'])
                if 'disease' in definition.lower():
                    key_concepts.extend(['disease', 'symptoms', 'treatment'])
                if 'function' in definition.lower():
                    key_concepts.extend(['function', 'process', 'mechanism'])
                
                cloze_text = definition
                cloze_num = 1
                
                for concept in key_concepts:
                    if concept.lower() in cloze_text.lower() and cloze_num <= 3:
                        # Case-insensitive replacement
                        import re
                        pattern = re.compile(re.escape(concept), re.IGNORECASE)
                        match = pattern.search(cloze_text)
                        if match:
                            original = match.group()
                            cloze_text = pattern.sub(f"{{{{c{cloze_num}::{original}}}}}", cloze_text, count=1)
                            cloze_num += 1
                
                if '{{c1::' in cloze_text:  # Only add if we created cloze deletions
                    cloze_cards.append({
                        'text': cloze_text,
                        'priority': term.get('priority', 'MEDIUM').upper(),
                        'source': determine_source_from_term(term),
                        'chapter': determine_chapter_from_term(term),
                        'type': 'cloze'
                    })
    
    return cloze_cards[:50]  # Reasonable number for study

def create_priority_decks():
    """Create separate decks for different priorities with proper scheduling"""
    
    decks = {}
    
    # High Priority Deck - Aggressive scheduling
    decks['high'] = genanki.Deck(
        2059400110,  # Fixed deck ID
        'PSYC 2240 - High Priority',
        description='Critical concepts for exam success - studied daily'
    )
    
    # Medium Priority Deck - Standard scheduling  
    decks['medium'] = genanki.Deck(
        2059400111,  # Fixed deck ID
        'PSYC 2240 - Medium Priority', 
        description='Important supporting concepts - regular review'
    )
    
    # Low Priority Deck - Conservative scheduling
    decks['low'] = genanki.Deck(
        2059400112,  # Fixed deck ID
        'PSYC 2240 - Low Priority',
        description='Background knowledge - periodic review'
    )
    
    # Cloze Context Deck
    decks['cloze'] = genanki.Deck(
        2059400113,  # Fixed deck ID
        'PSYC 2240 - Context Cloze',
        description='Contextual understanding through cloze deletion'
    )
    
    return decks

def cleanup_old_decks():
    """Clean up old deck files to prevent repository bloat"""
    # Use relative path from script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    output_dir = os.path.join(workspace_root, "output")
    
    # First, clean up existing backups (keep only the most recent one)
    backup_files = glob.glob(os.path.join(output_dir, "*_backup_*.apkg"))
    backup_files.sort(key=os.path.getmtime, reverse=True)
    old_backups = backup_files[1:]  # Keep only the newest 1, remove rest
    
    files_removed = 0
    for old_backup in old_backups:
        try:
            os.remove(old_backup)
            files_removed += 1
            print(f"   🗑️  Removed old backup: {os.path.basename(old_backup)}")
        except OSError:
            pass
    
    # Create backup of current deck if it exists
    current_deck = os.path.join(output_dir, "PSYC2240_Consolidated_Deck.apkg")
    if os.path.exists(current_deck):
        # Create timestamped backup (only if no recent backup exists)
        if len(backup_files) == 0:  # No backups exist
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"PSYC2240_Consolidated_Deck_backup_{timestamp}.apkg"
            backup_path = os.path.join(output_dir, backup_name)
            try:
                shutil.copy2(current_deck, backup_path)
                print(f"   📦 Backed up current deck: {backup_name}")
            except OSError:
                pass  # Backup failed, continue anyway
    
    # Find old deck files (keeping the FSRS guide and recent backups)
    old_deck_patterns = [
        "PSYC*_Complete_*.csv",
        "PSYC*_PROPER_*.apkg", 
        "*_OLD_*.apkg"
    ]
    
    files_removed = 0
    
    # Remove old deck patterns
    for pattern in old_deck_patterns:
        old_files = glob.glob(os.path.join(output_dir, pattern))
        for old_file in old_files:
            try:
                os.remove(old_file)
                files_removed += 1
                print(f"   🗑️  Removed: {os.path.basename(old_file)}")
            except OSError:
                pass
    
    if files_removed > 0:
        print(f"✅ Cleaned up {files_removed} old files")
    else:
        print("✅ No old files to clean up")

def cleanup_temp_analysis_files():
    """Clean up temporary analysis files that may accumulate"""
    # Use relative path from script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    analysis_dir = os.path.join(workspace_root, "content", "analysis")
    
    # Look for temporary or duplicate analysis files
    temp_patterns = [
        "*_temp_*.json",
        "temp_*.json",
        "*_backup_*.json", 
        "*_old_*.json",
        "*duplicate*.json",
        "*test*.json"
    ]
    
    files_removed = 0
    for pattern in temp_patterns:
        temp_files = glob.glob(os.path.join(analysis_dir, pattern))
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
                files_removed += 1
                print(f"   🗑️  Removed temp analysis: {os.path.basename(temp_file)}")
            except OSError:
                pass
    
    if files_removed > 0:
        print(f"✅ Cleaned up {files_removed} temporary analysis files")

def cleanup_all_backups():
    """Force cleanup of ALL backup files - useful for repository maintenance"""
    # Use relative path from script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    output_dir = os.path.join(workspace_root, "output")
    
    backup_files = glob.glob(os.path.join(output_dir, "*_backup_*.apkg"))
    files_removed = 0
    
    for backup_file in backup_files:
        try:
            os.remove(backup_file)
            files_removed += 1
            print(f"   🗑️  Removed backup: {os.path.basename(backup_file)}")
        except OSError:
            pass
    
    if files_removed > 0:
        print(f"✅ Removed all {files_removed} backup files")
    else:
        print("✅ No backup files to remove")

def main():
    """Main function to rebuild deck from consolidated analysis"""
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--clean-all":
        print("🧹 FORCE CLEANUP - Removing all backup files...")
        cleanup_all_backups()
        return
    
    print("🧠 PSYC 2240 - Rebuilding Consolidated Deck")
    print("=" * 50)
    
    # Clean up old files first
    print("🧹 Cleaning up old deck files...")
    cleanup_old_decks()
    cleanup_temp_analysis_files()
    
    # Load comprehensive analysis
    print("\n📊 Loading comprehensive content analysis...")
    analysis_data = load_comprehensive_analysis()
    if not analysis_data:
        return
        
    print(f"✅ Found {analysis_data['analysis_results']['total_terms_found']} terms")
    print(f"✅ {analysis_data['analysis_results']['overlap_terms_count']} cross-validated terms")
    
    # Create note types
    print("\n🎯 Creating memory-optimized note types...")
    basic_note_type = create_memory_optimized_note_type()
    cloze_note_type = create_cloze_note_type()
    
    # Create priority decks
    print("📚 Creating priority-based decks...")
    decks = create_priority_decks()
    
    # Extract Q&A pairs
    print("\n📝 Extracting question-answer pairs...")
    basic_cards = extract_question_answer_pairs(analysis_data)
    print(f"✅ Generated {len(basic_cards)} Q&A cards")
    
    # Create cloze cards
    print("🧩 Creating cloze context cards...")
    cloze_cards = create_cloze_cards_from_analysis(analysis_data)
    print(f"✅ Generated {len(cloze_cards)} cloze cards")
    
    # Add cards to appropriate decks
    print("\n🏗️  Building deck structure...")
    
    total_cards = 0
    priority_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    
    # Add basic cards
    for card_data in basic_cards:
        note = genanki.Note(
            model=basic_note_type,
            fields=[
                card_data['question'],
                card_data['answer'], 
                card_data['priority'],
                card_data['source'],
                card_data['chapter'],
                'Yes' if card_data['clinical'] else ''
            ]
        )
        
        priority = card_data['priority']
        if priority == 'HIGH':
            decks['high'].add_note(note)
        elif priority == 'MEDIUM':
            decks['medium'].add_note(note)
        else:
            decks['low'].add_note(note)
            
        priority_counts[priority] += 1
        total_cards += 1
    
    # Add cloze cards
    for card_data in cloze_cards:
        note = genanki.Note(
            model=cloze_note_type,
            fields=[
                card_data['text'],
                card_data['priority'],
                card_data['source'],
                card_data['chapter']
            ]
        )
        decks['cloze'].add_note(note)
        total_cards += 1
    
    # Create package
    print("\n📦 Creating Anki package...")
    
    package = genanki.Package([
        decks['high'], 
        decks['medium'], 
        decks['low'], 
        decks['cloze']
    ])
    
    # Output path using relative path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    output_path = os.path.join(workspace_root, "output", "PSYC2240_Consolidated_Deck.apkg")
    package.write_to_file(output_path)
    
    print(f"\n🎉 SUCCESS! Consolidated deck created:")
    print(f"   📁 {output_path}")
    print(f"\n📊 Deck Statistics:")
    print(f"   🔴 High Priority: {priority_counts['HIGH']} cards")
    print(f"   🟡 Medium Priority: {priority_counts['MEDIUM']} cards") 
    print(f"   ⚫ Low Priority: {priority_counts['LOW']} cards")
    print(f"   🧩 Cloze Context: {len(cloze_cards)} cards")
    print(f"   📚 Total Cards: {total_cards}")
    
    print(f"\n🎯 Ready for exam prep - {(datetime(2025, 10, 8).date() - datetime.now().date()).days} days until October 8th!")
    print(f"\n🧹 Repository kept clean - old files automatically removed!")
    
    return output_path

if __name__ == "__main__":
    main()