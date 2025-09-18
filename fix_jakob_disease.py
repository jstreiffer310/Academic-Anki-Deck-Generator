#!/usr/bin/env python3
"""
Fix Creutzfeldt-Jakob disease cards with proper content
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

def main():
    print("🧠 FIXING CREUTZFELDT-JAKOB DISEASE CARDS")
    print("=" * 50)
    
    try:
        # Test connection
        version = anki_connect('version')
        if version.get('error'):
            print(f"❌ AnkiConnect error: {version['error']}")
            return
        print("✅ AnkiConnect connected")
        
        # Search for Jakob disease cards
        search_terms = ['Jakob', 'Creutzfeldt']
        all_cards = set()
        
        for term in search_terms:
            cards = anki_connect('findCards', query=f'*{term}*')['result']
            all_cards.update(cards)
        
        print(f"🔍 Found {len(all_cards)} potential Jakob disease cards")
        
        if not all_cards:
            print("No Jakob disease cards found")
            return
        
        # Get card info
        cards_info = anki_connect('cardsInfo', cards=list(all_cards))['result']
        
        jakob_cards = []
        for card in cards_info:
            # Check different field structures
            question = ""
            answer = ""
            
            if 'fields' in card:
                # Try different field names
                for field_name in ['Front', 'Text', 'Question']:
                    if field_name in card['fields']:
                        question = card['fields'][field_name]['value']
                        break
                
                for field_name in ['Back', 'Answer']:
                    if field_name in card['fields']:
                        answer = card['fields'][field_name]['value']
                        break
            
            # Look for Jakob/Creutzfeldt content
            if any(term.lower() in question.lower() or term.lower() in answer.lower() 
                   for term in ['jakob', 'creutzfeldt']):
                jakob_cards.append({
                    'id': card['cardId'],
                    'question': question,
                    'answer': answer,
                    'fields': card.get('fields', {}),
                    'note_id': card['note']
                })
        
        print(f"📝 Processing {len(jakob_cards)} Jakob disease cards...")
        
        for i, card in enumerate(jakob_cards, 1):
            print(f"\n🔧 Card {i}/{len(jakob_cards)}")
            print(f"   Q: {card['question'][:80]}...")
            print(f"   OLD: {card['answer'][:80]}...")
            
            # Determine proper answer based on question content
            new_answer = get_jakob_answer(card['question'], card['answer'])
            
            # Update the card
            note_info = anki_connect('notesInfo', notes=[card['note_id']])['result'][0]
            
            # Find the answer field name
            answer_field = None
            for field_name in ['Back', 'Answer', 'Text']:
                if field_name in note_info['fields']:
                    answer_field = field_name
                    break
            
            if answer_field:
                # Update the note
                update_result = anki_connect('updateNoteFields', note={
                    'id': card['note_id'],
                    'fields': {
                        answer_field: new_answer
                    }
                })
                
                if update_result.get('error'):
                    print(f"   ❌ Error updating: {update_result['error']}")
                else:
                    print(f"   NEW: {new_answer[:80]}...")
                    print("   ✅ Fixed!")
            else:
                print("   ❌ Could not find answer field")
        
        print(f"\n🎉 JAKOB DISEASE FIX COMPLETE!")
        print(f"✅ Processed {len(jakob_cards)} cards")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def get_jakob_answer(question, current_answer):
    """Generate appropriate answer for Jakob disease questions"""
    
    question_lower = question.lower()
    
    # Check if it's asking about characteristics/what it is
    if any(phrase in question_lower for phrase in ['what characterizes', 'what is', 'characterizes']):
        if 'jakob' in question_lower or 'creutzfeldt' in question_lower:
            return "Rare, rapidly progressive neurodegenerative disease caused by prions, leading to dementia and death within months."
    
    # Check if it's about progression or symptoms
    if any(phrase in question_lower for phrase in ['progress', 'symptom', 'degenerative']):
        return "Rapidly progressive dementia with motor dysfunction, typically fatal within 1 year of onset."
    
    # Check if it's about cause or mechanism
    if any(phrase in question_lower for phrase in ['cause', 'mechanism', 'prion']):
        return "Caused by misfolded prion proteins that convert normal proteins into abnormal forms, causing brain degeneration."
    
    # Check if it's about public prominence or history
    if any(phrase in question_lower for phrase in ['prominence', '1990s', 'public']):
        return "Gained public attention in 1990s due to concerns about variant CJD linked to mad cow disease."
    
    # Default comprehensive answer
    return "Rare, rapidly progressive neurodegenerative disease caused by prions, leading to dementia and death within months."

if __name__ == "__main__":
    main()