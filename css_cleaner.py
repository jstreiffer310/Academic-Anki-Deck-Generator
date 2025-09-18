#!/usr/bin/env python3
"""
CSS CLEANER - Remove embedded CSS from existing Anki cards
Targets the specific CSS pollution problem you're experiencing
"""

import requests
import re
from bs4 import BeautifulSoup

class CSSCleaner:
    def __init__(self):
        self.url = "http://127.0.0.1:8765"
        self.cleaned_count = 0
        
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
    
    def extract_clean_content(self, messy_text):
        """Extract clean content from CSS-polluted text"""
        if not messy_text:
            return ""
        
        # Remove HTML tags first
        soup = BeautifulSoup(messy_text, 'html.parser')
        text = soup.get_text()
        
        # The CSS pattern that's causing issues
        css_pattern = r'\.card\s*\{[^}]*\}.*?\.source,\s*\.chapter\s*\{[^}]*\}'
        
        # Remove the entire CSS block
        text = re.sub(css_pattern, '', text, flags=re.DOTALL)
        
        # Remove any remaining CSS rules
        text = re.sub(r'\.[a-zA-Z-]+\s*\{[^}]*\}', '', text, flags=re.DOTALL)
        
        # Remove priority indicators that got mixed in
        text = re.sub(r'\b(HIGH|MEDIUM|LOW)\s+Priority\s+', '', text)
        
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # If the text starts with "How does" and ends with "function?", extract the middle part
        if "How does" in text and "function?" in text:
            # Extract the actual question
            match = re.search(r'How does (.+?) function\?', text)
            if match:
                subject = match.group(1).strip()
                return f"How does {subject} function?"
        
        return text
    
    def clean_all_css_cards(self):
        """Find and clean all cards with embedded CSS"""
        print("🧹 Finding cards with embedded CSS...")
        
        # Get all PSYC cards
        card_response = self.anki_request("findCards", {"query": 'deck:"PSYC 2240*"'})
        if card_response.get("error"):
            print(f"Error finding cards: {card_response['error']}")
            return
        
        card_ids = card_response["result"]
        print(f"📚 Checking {len(card_ids)} cards for CSS pollution...")
        
        # Process in batches
        batch_size = 50
        css_cards = []
        
        for i in range(0, len(card_ids), batch_size):
            batch = card_ids[i:i + batch_size]
            print(f"🔍 Scanning batch {i//batch_size + 1}/{(len(card_ids) + batch_size - 1)//batch_size}...")
            
            # Get card details
            info_response = self.anki_request("cardsInfo", {"cards": batch})
            if info_response.get("error"):
                continue
                
            cards = info_response["result"]
            
            for card in cards:
                fields = card["fields"]
                question = fields.get("Question", {}).get("value", "")
                answer = fields.get("Answer", {}).get("value", "")
                
                # Check if this card has CSS pollution
                has_css = (
                    ".card {" in question or ".card {" in answer or
                    "font-family:" in question or "font-family:" in answer or
                    ".priority" in question or ".priority" in answer
                )
                
                if has_css:
                    css_cards.append({
                        "note_id": card["note"],
                        "card_id": card["cardId"],
                        "question": question,
                        "answer": answer,
                        "priority": fields.get("Priority", {}).get("value", ""),
                        "source": fields.get("Source", {}).get("value", ""),
                        "chapter": fields.get("Chapter", {}).get("value", ""),
                        "clinical": fields.get("Clinical", {}).get("value", "")
                    })
        
        print(f"⚠️  Found {len(css_cards)} cards with CSS pollution")
        
        if not css_cards:
            print("✅ No CSS-polluted cards found!")
            return
        
        # Clean each card
        print(f"\n🧹 Cleaning {len(css_cards)} CSS-polluted cards...")
        
        for i, card in enumerate(css_cards, 1):
            print(f"📝 Cleaning card {i}/{len(css_cards)}...")
            
            # Extract clean content
            clean_question = self.extract_clean_content(card["question"])
            clean_answer = self.extract_clean_content(card["answer"])
            
            # Ensure we have meaningful content
            if not clean_question or len(clean_question) < 10:
                clean_question = "Review this question - extracted from CSS"
            if not clean_answer or len(clean_answer) < 5:
                clean_answer = "Review this answer - extracted from CSS"
            
            print(f"   Original Q: {card['question'][:100]}...")
            print(f"   Clean Q: {clean_question}")
            print(f"   Original A: {card['answer'][:100]}...")
            print(f"   Clean A: {clean_answer}")
            
            # Update the card
            update_response = self.anki_request("updateNoteFields", {
                "note": {
                    "id": card["note_id"],
                    "fields": {
                        "Question": clean_question,
                        "Answer": clean_answer,
                        "Priority": card["priority"],
                        "Source": card["source"],
                        "Chapter": card["chapter"],
                        "Clinical": card["clinical"]
                    }
                }
            })
            
            if update_response.get("error"):
                print(f"   ❌ Error updating: {update_response['error']}")
            else:
                print(f"   ✅ Cleaned successfully!")
                self.cleaned_count += 1
            
            print("-" * 60)
        
        print(f"\n🎉 CSS CLEANING COMPLETE!")
        print(f"✅ Successfully cleaned: {self.cleaned_count}/{len(css_cards)} cards")
        
        return self.cleaned_count

def main():
    """Main execution"""
    print("🧹 CSS CLEANER FOR ANKI CARDS")
    print("Removing embedded CSS from question and answer fields")
    print("=" * 60)
    
    cleaner = CSSCleaner()
    
    # Test connection
    test = cleaner.anki_request("deckNames")
    if test.get("error"):
        print(f"❌ AnkiConnect not available: {test['error']}")
        print("Make sure Anki is running with AnkiConnect addon")
        return
    
    print("✅ AnkiConnect connected successfully")
    
    # Clean CSS pollution
    cleaned_count = cleaner.clean_all_css_cards()
    
    if cleaned_count > 0:
        print(f"\n🎯 SUCCESS! Cleaned {cleaned_count} cards of CSS pollution!")
        print("Your cards should now display clean text instead of CSS code!")
    else:
        print("\n📝 No CSS-polluted cards found or there was an issue.")

if __name__ == "__main__":
    main()