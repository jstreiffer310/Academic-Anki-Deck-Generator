"""
Fix the SPECIFIC problematic card found
Card ID: 1758156037328 
- Fix grammar: "How do Flow through a Neuron function?" 
- Fix incomplete answer: "An ovoid structure labeled cell body is at the center of the neuron."
"""

import requests
import json
import re

class SpecificCardFixer:
    def __init__(self, host="127.0.0.1", port=8765):
        self.url = f"http://{host}:{port}"
        
    def request(self, action, params=None):
        """Send request to AnkiConnect"""
        payload = {
            "action": action,
            "version": 6,
            "params": params or {}
        }
        
        try:
            response = requests.post(self.url, json=payload, timeout=10)
            result = response.json()
            return result
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return None
    
    def clean_html(self, text):
        """Remove HTML tags but preserve structure"""
        # Remove style blocks completely
        text = re.sub(r'<style>.*?</style>', '', text, flags=re.DOTALL)
        # Remove other HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()
    
    def fix_specific_card(self, card_id=1758156037328):
        """Fix the specific problematic card"""
        print(f"🎯 Fixing card ID: {card_id}")
        
        # Get current card info
        card_result = self.request("cardsInfo", {"cards": [card_id]})
        if not card_result or not card_result.get("result"):
            print("❌ Could not get card info")
            return False
        
        card_info = card_result["result"][0]
        note_id = card_info.get("note")
        
        if not note_id:
            print("❌ Could not get note ID")
            return False
        
        # Get note info
        note_result = self.request("notesInfo", {"notes": [note_id]})
        if not note_result or not note_result.get("result"):
            print("❌ Could not get note info")
            return False
        
        note_info = note_result["result"][0]
        fields = note_info.get("fields", {})
        
        print("📋 Current fields:")
        for field_name, field_info in fields.items():
            value = field_info.get("value", "")
            clean_value = self.clean_html(value)
            print(f"   {field_name}: {clean_value[:100]}...")
        
        # Prepare new field values
        updated_fields = {}
        
        for field_name, field_info in fields.items():
            current_value = field_info.get("value", "")
            clean_current = self.clean_html(current_value)
            
            # Fix the question field
            if "How do Flow through a Neuron function" in clean_current:
                # Keep the styling but fix the question text
                new_value = current_value.replace(
                    "How do Flow through a Neuron function?",
                    "How does neural transmission work through a neuron?"
                )
                updated_fields[field_name] = new_value
                print(f"✅ Fixed question in field: {field_name}")
            
            # Fix the answer field
            elif "An ovoid structure labeled cell body is at the center of the neuron." in clean_current:
                # Replace the incomplete answer with a proper one
                new_answer = "The cell body (soma) contains the nucleus and most organelles, integrates incoming signals from dendrites, and generates action potentials that travel down the axon to communicate with other neurons."
                
                # Replace just the answer text, keep the styling
                new_value = current_value.replace(
                    "An ovoid structure labeled cell body is at the center of the neuron.",
                    new_answer
                )
                updated_fields[field_name] = new_value
                print(f"✅ Fixed answer in field: {field_name}")
            
            else:
                # Keep other fields unchanged
                updated_fields[field_name] = current_value
        
        # Update the note
        print("🔧 Updating note...")
        update_result = self.request("updateNoteFields", {
            "note": {
                "id": note_id,
                "fields": updated_fields
            }
        })
        
        if update_result and update_result.get("error") is None:
            print("✅ Note update successful!")
            
            # Verify the fix
            verify_result = self.request("cardsInfo", {"cards": [card_id]})
            if verify_result and verify_result.get("result"):
                updated_card = verify_result["result"][0]
                question = self.clean_html(updated_card.get("question", ""))
                answer = self.clean_html(updated_card.get("answer", ""))
                
                print(f"\n🎉 VERIFICATION:")
                print(f"   New Question: {question}")
                print(f"   New Answer: {answer}")
                
                # Check if the fix actually worked
                if "How does neural transmission work" in question and "cell body (soma) contains" in answer:
                    print("✅ FIX VERIFIED SUCCESSFUL!")
                    return True
                else:
                    print("❌ Fix not applied correctly")
                    return False
        else:
            error = update_result.get("error") if update_result else "Unknown error"
            print(f"❌ Update failed: {error}")
            return False

if __name__ == "__main__":
    fixer = SpecificCardFixer()
    fixer.fix_specific_card()