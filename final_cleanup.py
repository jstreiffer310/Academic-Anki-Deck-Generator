#!/usr/bin/env python3
"""
Final cleanup - fix remaining empty fields and edge cases
"""

import requests
import re
from bs4 import BeautifulSoup

def final_cleanup():
    url = "http://127.0.0.1:8765"
    
    print("🔧 FINAL CLEANUP - Fixing remaining issues...")
    
    # Get all PSYC cards
    response = requests.post(url, json={
        "action": "findCards",
        "version": 6,
        "params": {"query": "deck:\"PSYC 2240*\""}
    })
    
    card_ids = response.json()["result"]
    print(f"📚 Checking {len(card_ids)} cards for final cleanup...")
    
    # Process in batches
    batch_size = 50
    fixed_empty = 0
    fixed_other = 0
    
    for i in range(0, len(card_ids), batch_size):
        batch = card_ids[i:i + batch_size]
        
        # Get card details
        response = requests.post(url, json={
            "action": "cardsInfo",
            "version": 6,
            "params": {"cards": batch}
        })
        
        cards = response.json()["result"]
        
        for card in cards:
            note_id = card["note"]
            fields = card["fields"]
            
            question = fields.get("Question", {}).get("value", "")
            answer = fields.get("Answer", {}).get("value", "")
            priority = fields.get("Priority", {}).get("value", "")
            source = fields.get("Source", {}).get("value", "")
            chapter = fields.get("Chapter", {}).get("value", "")
            clinical = fields.get("Clinical", {}).get("value", "")
            
            # Clean text
            q_text = BeautifulSoup(question, 'html.parser').get_text().strip()
            a_text = BeautifulSoup(answer, 'html.parser').get_text().strip()
            
            needs_update = False
            
            # Fix empty fields
            if not q_text:
                q_text = "Review this question"
                needs_update = True
                fixed_empty += 1
                
            if not a_text:
                a_text = "Review this answer"
                needs_update = True
                fixed_empty += 1
            
            # Additional cleaning
            if "Figure" in q_text:
                q_text = re.sub(r'Figure \d+\.\d+[^.]*\.', '', q_text).strip()
                needs_update = True
                fixed_other += 1
                
            if "Figure" in a_text:
                a_text = re.sub(r'Figure \d+\.\d+[^.]*\.', '', a_text).strip()
                needs_update = True
                fixed_other += 1
            
            # Fix double spaces
            if "  " in q_text:
                q_text = re.sub(r'\s+', ' ', q_text).strip()
                needs_update = True
                fixed_other += 1
                
            if "  " in a_text:
                a_text = re.sub(r'\s+', ' ', a_text).strip()
                needs_update = True
                fixed_other += 1
            
            # Update if needed
            if needs_update:
                update_response = requests.post(url, json={
                    "action": "updateNoteFields",
                    "version": 6,
                    "params": {
                        "note": {
                            "id": note_id,
                            "fields": {
                                "Question": q_text,
                                "Answer": a_text,
                                "Priority": priority,
                                "Source": source,
                                "Chapter": chapter,
                                "Clinical": clinical
                            }
                        }
                    }
                })
                
                if update_response.json().get("error"):
                    print(f"❌ Error updating note {note_id}")
    
    print(f"\n🎯 FINAL CLEANUP COMPLETE!")
    print(f"✅ Fixed empty fields: {fixed_empty}")
    print(f"✅ Fixed other issues: {fixed_other}")
    print(f"📊 Total fixes: {fixed_empty + fixed_other}")

if __name__ == "__main__":
    final_cleanup()