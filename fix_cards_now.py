#!/usr/bin/env python3
"""
ULTIMATE ANKI CARD FIXER
Fixes all problematic PSYC 2240 cards using multiple approaches
"""

import requests
import re
import time
from bs4 import BeautifulSoup

class AnkiCardFixer:
    def __init__(self):
        self.url = "http://127.0.0.1:8765"
        self.fixed_count = 0
        self.error_count = 0
        
    def anki_request(self, action, params=None):
        """Make request to AnkiConnect"""
        payload = {"action": action, "version": 6}
        if params:
            payload["params"] = params
        
        try:
            response = requests.post(self.url, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"AnkiConnect error: {e}")
            return {"error": str(e)}
    
    def clean_text(self, text):
        """Clean and fix text content"""
        if not text:
            return text
            
        # Remove HTML and get clean text
        soup = BeautifulSoup(text, 'html.parser')
        clean = soup.get_text()
        
        # Fix common issues
        clean = re.sub(r'\s+', ' ', clean)  # Multiple spaces -> single space
        clean = re.sub(r'Figure \d+\.\d+[^.]*\.', '', clean)  # Remove figure captions
        clean = re.sub(r'Fig\. \d+\.\d+[^.]*\.', '', clean)  # Remove fig captions
        clean = re.sub(r'\bfigure \d+\b', '', clean, flags=re.IGNORECASE)  # Remove figure refs
        clean = re.sub(r'\.{2,}', '.', clean)  # Multiple dots -> single dot
        clean = clean.strip()
        
        # Grammar fixes
        clean = re.sub(r'\bi\b', 'I', clean)  # Fix lowercase 'i'
        clean = re.sub(r'\. ([a-z])', lambda m: '. ' + m.group(1).upper(), clean)  # Capitalize after periods
        
        return clean
    
    def fix_all_cards(self):
        """Fix all PSYC 2240 cards"""
        print("🔍 Finding all PSYC 2240 cards...")
        
        # Get all PSYC cards
        card_response = self.anki_request("findCards", {"query": 'deck:"PSYC 2240*"'})
        if card_response.get("error"):
            print(f"Error finding cards: {card_response['error']}")
            return
        
        card_ids = card_response["result"]
        print(f"📚 Found {len(card_ids)} cards to process")
        
        if not card_ids:
            print("No cards found!")
            return
            
        # Get card info in batches
        batch_size = 50
        total_fixed = 0
        
        for i in range(0, len(card_ids), batch_size):
            batch = card_ids[i:i + batch_size]
            print(f"📝 Processing batch {i//batch_size + 1}/{(len(card_ids) + batch_size - 1)//batch_size}...")
            
            # Get card details
            info_response = self.anki_request("cardsInfo", {"cards": batch})
            if info_response.get("error"):
                print(f"Error getting card info: {info_response['error']}")
                continue
                
            cards = info_response["result"]
            
            # Process each card
            for card in cards:
                try:
                    note_id = card["note"]
                    fields = card["fields"]
                    
                    # Get current field values
                    question = fields.get("Question", {}).get("value", "")
                    answer = fields.get("Answer", {}).get("value", "")
                    priority = fields.get("Priority", {}).get("value", "")
                    source = fields.get("Source", {}).get("value", "")
                    chapter = fields.get("Chapter", {}).get("value", "")
                    clinical = fields.get("Clinical", {}).get("value", "")
                    
                    # Clean the text
                    clean_question = self.clean_text(question)
                    clean_answer = self.clean_text(answer)
                    
                    # Check if we need to update
                    needs_update = (
                        clean_question != BeautifulSoup(question, 'html.parser').get_text().strip() or
                        clean_answer != BeautifulSoup(answer, 'html.parser').get_text().strip() or
                        not clean_answer  # Empty answers
                    )
                    
                    if needs_update:
                        # Ensure we have content
                        if not clean_question:
                            clean_question = "Question needs review"
                        if not clean_answer:
                            clean_answer = "Answer needs review"
                            
                        # Update the note
                        update_response = self.anki_request("updateNoteFields", {
                            "note": {
                                "id": note_id,
                                "fields": {
                                    "Question": clean_question,
                                    "Answer": clean_answer,
                                    "Priority": priority,
                                    "Source": source,
                                    "Chapter": chapter,
                                    "Clinical": clinical
                                }
                            }
                        })
                        
                        if update_response.get("error"):
                            print(f"❌ Error updating note {note_id}: {update_response['error']}")
                            self.error_count += 1
                        else:
                            total_fixed += 1
                            if total_fixed % 25 == 0:
                                print(f"✅ Fixed {total_fixed} cards so far...")
                                
                except Exception as e:
                    print(f"❌ Error processing card: {e}")
                    self.error_count += 1
            
            # Brief pause between batches
            time.sleep(0.5)
        
        print(f"\n🎉 COMPLETED!")
        print(f"✅ Fixed: {total_fixed} cards")
        print(f"❌ Errors: {self.error_count}")
        print(f"📊 Total processed: {len(card_ids)} cards")
        
        return total_fixed

def main():
    """Main execution"""
    print("🚀 ULTIMATE ANKI CARD FIXER")
    print("=" * 40)
    
    fixer = AnkiCardFixer()
    
    # Test connection first
    test = fixer.anki_request("deckNames")
    if test.get("error"):
        print(f"❌ AnkiConnect not available: {test['error']}")
        print("Make sure Anki is running with AnkiConnect addon")
        return
    
    print("✅ AnkiConnect connected successfully")
    
    # Fix all cards
    fixed_count = fixer.fix_all_cards()
    
    if fixed_count > 0:
        print(f"\n🎯 SUCCESS! Your {fixed_count} cards are now fixed and ready for studying!")
    else:
        print("\n📝 No cards needed fixing or there was an issue.")

if __name__ == "__main__":
    main()