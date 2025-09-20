"""
ANKI FIELD STRUCTURE INVESTIGATOR
Deep dive into exactly how these cards are structured to understand why updates fail
"""

import requests
import json
from bs4 import BeautifulSoup

def investigate_card_structure():
    url = "http://127.0.0.1:8765"
    
    # Find a problematic card
    payload = {"action": "findCards", "version": 6, "params": {"query": "*flow*"}}
    response = requests.post(url, json=payload)
    result = response.json()
    
    if not result.get("result"):
        print("No flow cards found")
        return
    
    card_id = result["result"][0]
    print(f"Investigating card ID: {card_id}")
    
    # Get card info
    payload2 = {"action": "cardsInfo", "version": 6, "params": {"cards": [card_id]}}
    response2 = requests.post(url, json=payload2)
    card_info = response2.json()["result"][0]
    
    note_id = card_info["note"]
    print(f"Note ID: {note_id}")
    
    # Get note info
    payload3 = {"action": "notesInfo", "version": 6, "params": {"notes": [note_id]}}
    response3 = requests.post(url, json=payload3)
    note_info = response3.json()["result"][0]
    
    print("\n=== FIELD STRUCTURE ===")
    fields = note_info.get("fields", {})
    for field_name, field_info in fields.items():
        field_value = field_info.get("value", "")
        print(f"\nField: {field_name}")
        print(f"Length: {len(field_value)} characters")
        print(f"First 300 chars:")
        print(repr(field_value[:300]))
        
        # Extract text
        soup = BeautifulSoup(field_value, 'html.parser')
        text = soup.get_text()
        print(f"Extracted text: {repr(text[:100])}")
    
    print("\n=== CARD QUESTION ===")
    print(f"Card question field: {repr(card_info['question'][:300])}")
    
    print("\n=== CARD ANSWER ===") 
    print(f"Card answer field: {repr(card_info['answer'][:300])}")

if __name__ == "__main__":
    investigate_card_structure()