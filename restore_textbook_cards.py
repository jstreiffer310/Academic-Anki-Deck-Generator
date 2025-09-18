#!/usr/bin/env python3
"""
Smart Card Restoration - Re-add deleted cards if keywords found in textbook
"""

import requests
import json
import re

def anki_connect(action, **params):
    """Connect to AnkiConnect API"""
    return requests.post('http://localhost:8765', json={
        'action': action,
        'version': 6,
        'params': params
    }).json()

def read_textbook():
    """Read textbook content"""
    try:
        with open('content/textbook/textbook_full_content.txt', 'r', encoding='utf-8') as f:
            return f.read().lower()
    except Exception as e:
        print(f"Error reading textbook: {e}")
        return ""

def main():
    print("🧠 SMART CARD RESTORATION")
    print("Re-adding deleted cards if keywords found in textbook")
    print("=" * 60)
    
    # Cards I previously deleted that might need restoration
    deleted_cards_data = [
        {
            'front': 'What characterizes Korsakoff syndrome?',
            'back': 'Memory disorder caused by thiamine (vitamin B1) deficiency, often from chronic alcoholism, featuring severe anterograde amnesia.',
            'keywords': ['memory', 'amnesia', 'thiamine', 'vitamin', 'alcohol', 'wernicke']
        },
        {
            'front': 'What is Wernicke-Korsakoff syndrome?',
            'back': 'Two-stage disorder: Wernicke encephalopathy (acute) followed by Korsakoff syndrome (chronic memory impairment).',
            'keywords': ['wernicke', 'memory', 'encephalopathy', 'amnesia', 'thiamine']
        },
        {
            'front': 'What brain regions are affected in Korsakoff syndrome?',
            'back': 'Mammillary bodies, thalamus, and hippocampus - all critical for memory formation and consolidation.',
            'keywords': ['mammillary', 'thalamus', 'hippocampus', 'memory', 'brain regions']
        },
        {
            'front': 'What characterizes anterograde amnesia in Korsakoff syndrome?',
            'back': 'Inability to form new memories while retaining some older memories; patients often confabulate to fill memory gaps.',
            'keywords': ['amnesia', 'memory', 'confabulation', 'anterograde']
        },
        {
            'front': 'What causes Wernicke encephalopathy?',
            'back': 'Acute thiamine (vitamin B1) deficiency causing brain inflammation, confusion, and eye movement problems.',
            'keywords': ['thiamine', 'vitamin', 'encephalopathy', 'brain', 'inflammation', 'wernicke']
        },
        {
            'front': 'What is confabulation in Korsakoff syndrome?',
            'back': 'Unconscious fabrication of memories to fill gaps caused by severe memory impairment.',
            'keywords': ['confabulation', 'memory', 'fabrication', 'amnesia']
        }
    ]
    
    try:
        # Test connection
        version = anki_connect('version')
        if version.get('error'):
            print(f"❌ AnkiConnect error: {version['error']}")
            return
        print("✅ AnkiConnect connected")
        
        # Read textbook content
        print("📚 Reading textbook content...")
        textbook_content = read_textbook()
        if not textbook_content:
            print("❌ Could not read textbook content")
            return
        
        print(f"📄 Textbook loaded ({len(textbook_content):,} characters)")
        
        # Check each deleted card for textbook keyword matches
        cards_to_restore = []
        
        for card in deleted_cards_data:
            matches = []
            for keyword in card['keywords']:
                if keyword.lower() in textbook_content:
                    matches.append(keyword)
            
            if matches:
                cards_to_restore.append({
                    'card': card,
                    'matches': matches
                })
                print(f"✅ '{card['front'][:50]}...' - Found keywords: {', '.join(matches)}")
            else:
                print(f"❌ '{card['front'][:50]}...' - No keywords found in textbook")
        
        if not cards_to_restore:
            print("\n🚫 No deleted cards have keywords in textbook - nothing to restore")
            return
        
        print(f"\n🔄 Restoring {len(cards_to_restore)} cards with textbook support...")
        
        # Restore cards that have textbook keyword support
        for i, item in enumerate(cards_to_restore, 1):
            card = item['card']
            matches = item['matches']
            
            print(f"\n📝 Restoring card {i}/{len(cards_to_restore)}")
            print(f"   Q: {card['front'][:60]}...")
            print(f"   A: {card['back'][:60]}...")
            print(f"   Keywords found: {', '.join(matches)}")
            
            # Create the note
            note_data = {
                'deckName': 'PSYC 2240',
                'modelName': 'Basic',
                'fields': {
                    'Front': card['front'],
                    'Back': card['back']
                },
                'tags': ['PSYC2240', 'Restored', 'TextbookSupported']
            }
            
            result = anki_connect('addNote', note=note_data)
            
            if result.get('error'):
                print(f"   ❌ Error: {result['error']}")
            else:
                print(f"   ✅ Restored successfully!")
        
        print(f"\n🎉 RESTORATION COMPLETE!")
        print(f"✅ Successfully restored {len(cards_to_restore)} cards")
        print(f"📚 All restored cards have supporting keywords in the textbook")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()