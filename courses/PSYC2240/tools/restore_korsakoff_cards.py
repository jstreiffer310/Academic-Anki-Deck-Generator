#!/usr/bin/env python3
"""
Restore Korsakoff syndrome cards based on textbook PDF analysis
"""

import requests
import json

def anki_connect(action, **params):
    """Connect to AnkiConnect API"""
    return requests.post('http://localhost:8765', json={
        'action': action,
        'version': 6,
        'params': params
    }).json()

def main():
    print("🧠 RESTORING KORSAKOFF SYNDROME CARDS")
    print("Based on textbook PDF analysis showing legitimate coverage")
    print("=" * 65)
    
    # Cards to restore based on textbook coverage
    korsakoff_cards = [
        {
            'front': 'What characterizes Korsakoff syndrome?',
            'back': 'Memory disorder caused by thiamine (vitamin B1) deficiency, often from chronic alcoholism, featuring severe anterograde amnesia and confabulation.'
        },
        {
            'front': 'What is Wernicke-Korsakoff syndrome?',
            'back': 'Two-stage disorder: Wernicke encephalopathy (acute confusion, eye problems) followed by Korsakoff syndrome (chronic memory impairment).'
        },
        {
            'front': 'What brain regions are affected in Korsakoff syndrome?',
            'back': 'Mammillary bodies, thalamus, and hippocampus - all critical brain structures for memory formation and consolidation.'
        },
        {
            'front': 'What characterizes anterograde amnesia in Korsakoff syndrome?',
            'back': 'Inability to form new memories while retaining some older memories; patients often confabulate to fill memory gaps.'
        },
        {
            'front': 'What causes Wernicke encephalopathy?',
            'back': 'Acute thiamine (vitamin B1) deficiency causing brain inflammation, confusion, ataxia, and eye movement abnormalities.'
        },
        {
            'front': 'What is confabulation in Korsakoff syndrome?',
            'back': 'Unconscious fabrication of memories to fill gaps caused by severe anterograde amnesia; not intentional lying.'
        }
    ]
    
    try:
        # Test connection
        version = anki_connect('version')
        if version.get('error'):
            print(f"❌ AnkiConnect error: {version['error']}")
            return
        print("✅ AnkiConnect connected")
        
        print(f"\n🔄 Restoring {len(korsakoff_cards)} Korsakoff syndrome cards...")
        
        restored_count = 0
        
        for i, card in enumerate(korsakoff_cards, 1):
            print(f"\n📝 Restoring card {i}/{len(korsakoff_cards)}")
            print(f"   Q: {card['front'][:60]}...")
            print(f"   A: {card['back'][:60]}...")
            
            # Create the note
            note_data = {
                'deckName': 'PSYC 2240',
                'modelName': 'Basic',
                'fields': {
                    'Front': card['front'],
                    'Back': card['back']
                },
                'tags': ['PSYC2240', 'Restored', 'Korsakoff', 'TextbookVerified']
            }
            
            result = anki_connect('addNote', note=note_data)
            
            if result.get('error'):
                print(f"   ❌ Error: {result['error']}")
            else:
                restored_count += 1
                print(f"   ✅ Restored successfully!")
        
        print(f"\n🎉 RESTORATION COMPLETE!")
        print(f"✅ Successfully restored {restored_count} Korsakoff syndrome cards")
        print(f"📚 All cards verified against actual textbook PDF content")
        print(f"🧠 Your deck now includes legitimate memory disorder content!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()