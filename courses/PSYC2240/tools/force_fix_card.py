"""
FORCE FIX THE PROBLEMATIC CARD
Direct surgical approach to fix the ovoid structure card
"""

import requests
import json

def force_fix_card():
    url = "http://127.0.0.1:8765"
    card_id = 1758156037328
    
    print(f"🎯 FORCE FIXING CARD {card_id}")
    
    # Get current note
    payload = {'action': 'cardsInfo', 'version': 6, 'params': {'cards': [card_id]}}
    response = requests.post(url, json=payload)
    card_info = response.json()['result'][0]
    note_id = card_info['note']
    
    payload2 = {'action': 'notesInfo', 'version': 6, 'params': {'notes': [note_id]}}
    response2 = requests.post(url, json=payload2)
    note_info = response2.json()['result'][0]
    
    fields = note_info['fields']
    
    # Get current answer field
    current_answer = fields['Answer']['value']
    print("Current answer length:", len(current_answer))
    
    # Simple and direct replacement
    old_text = "An ovoid structure labeled cell body is at the center of the neuron."
    new_text = "The cell body (soma) is the ovoid structure at the center of the neuron that contains the nucleus and most organelles. It integrates incoming signals from dendrites and determines whether to generate an action potential that travels down the axon."
    
    # Replace in the HTML
    new_answer = current_answer.replace(old_text, new_text)
    
    print(f"Replacement made: {old_text in current_answer}")
    print(f"New length: {len(new_answer)}")
    
    # Prepare all fields for update
    updated_fields = {
        "Question": fields['Question']['value'],
        "Answer": new_answer,
        "Priority": fields['Priority']['value'],
        "Source": fields['Source']['value'], 
        "Chapter": fields['Chapter']['value'],
        "Clinical": fields['Clinical']['value']
    }
    
    # Force update
    update_result = requests.post(url, json={
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": note_id,
                "fields": updated_fields
            }
        }
    })
    
    result = update_result.json()
    print(f"Update result: {result}")
    
    if result.get('error') is None:
        print("✅ Update successful!")
        
        # Verify the change
        verify_payload = {'action': 'notesInfo', 'version': 6, 'params': {'notes': [note_id]}}
        verify_response = requests.post(url, json=verify_payload)
        verify_note = verify_response.json()['result'][0]
        verify_answer = verify_note['fields']['Answer']['value']
        
        if new_text in verify_answer:
            print("✅ VERIFICATION PASSED - Fix is live!")
        else:
            print("❌ VERIFICATION FAILED - Fix did not stick")
            
        print(f"Verified answer contains new text: {new_text in verify_answer}")
        
    else:
        print(f"❌ Update failed: {result}")

if __name__ == "__main__":
    force_fix_card()