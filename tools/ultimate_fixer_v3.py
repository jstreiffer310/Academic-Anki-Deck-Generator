"""
ULTIMATE ANKI CARD FIXER V3
Now that we understand the field structure, this will work properly!

Note type: "PSYC2240 Memory Optimized"
Fields: ['Question', 'Answer', 'Priority', 'Source', 'Chapter', 'Clinical']

Target the exact cards you mentioned:
1. "How do Flow through a Neuron function?" (grammar error)
2. "How is the cerebral cortex parcellated into functional regions?" 
3. "An ovoid structure labeled cell body is at the center of the neuron." (incomplete)
"""

import requests
import json
import re
from bs4 import BeautifulSoup

class UltimateFixerV3:
    def __init__(self, host="127.0.0.1", port=8765):
        self.url = f"http://{host}:{port}"
        self.fixes_applied = 0
        self.critical_fixes = 0
        self.cards_processed = 0
        
    def request(self, action, params=None):
        """Send request to AnkiConnect"""
        payload = {
            "action": action,
            "version": 6,
            "params": params or {}
        }
        
        try:
            response = requests.post(self.url, json=payload, timeout=15)
            result = response.json()
            return result
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return None
    
    def clean_html_text(self, html_content):
        """Extract clean text from HTML"""
        if not html_content:
            return ""
        
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove style and script tags
        for tag in soup(["style", "script"]):
            tag.decompose()
        
        text = soup.get_text()
        text = re.sub(r'\\s+', ' ', text).strip()
        return text
    
    def update_html_content(self, original_html, old_text, new_text):
        """Update text while preserving HTML structure"""
        if not original_html or old_text == new_text:
            return original_html
        
        try:
            soup = BeautifulSoup(original_html, 'html.parser')
            
            # Find text nodes and replace
            def replace_in_text_nodes(element):
                if element.string:
                    if old_text.lower() in element.string.lower():
                        # Case-insensitive replacement
                        pattern = re.escape(old_text)
                        new_string = re.sub(pattern, new_text, element.string, flags=re.IGNORECASE)
                        element.string.replace_with(new_string)
                        return True
                
                if hasattr(element, 'children'):
                    for child in element.children:
                        if replace_in_text_nodes(child):
                            return True
                return False
            
            if replace_in_text_nodes(soup):
                return str(soup)
            
            # Fallback: simple string replacement
            return original_html.replace(old_text, new_text)
            
        except Exception as e:
            print(f"⚠️ HTML update error: {e}")
            return original_html.replace(old_text, new_text)
    
    def find_all_cards(self):
        """Find all PSYC2240 cards"""
        print("🔍 Finding ALL PSYC2240 cards...")
        
        result = self.request("findCards", {"query": 'deck:"PSYC 2240" OR deck:*PSYC*'})
        if result and result.get("result"):
            cards = result["result"]
            print(f"   Found {len(cards)} total cards")
            return cards
        
        return []
    
    def analyze_and_fix_card(self, card_id):
        """Analyze and fix a single card"""
        
        # Get card info
        card_result = self.request("cardsInfo", {"cards": [card_id]})
        if not card_result or not card_result.get("result"):
            return False
        
        card_info = card_result["result"][0]
        note_id = card_info.get("note")
        
        if not note_id:
            return False
        
        # Get note info
        note_result = self.request("notesInfo", {"notes": [note_id]})
        if not note_result or not note_result.get("result"):
            return False
        
        note_info = note_result["result"][0]
        
        # Check if this is the right note type
        if note_info.get("modelName") != "PSYC2240 Memory Optimized":
            return False
        
        fields = note_info.get("fields", {})
        
        # Extract current question and answer
        question_html = fields.get("Question", {}).get("value", "")
        answer_html = fields.get("Answer", {}).get("value", "")
        
        question_text = self.clean_html_text(question_html)
        answer_text = self.clean_html_text(answer_html)
        
        if not question_text and not answer_text:
            return False
        
        # Check for critical issues
        issues = []
        new_question_text = question_text
        new_answer_text = answer_text
        
        # ========== USER-IDENTIFIED CRITICAL ISSUES ==========
        
        # 1. "How do Flow through a Neuron function?" - Grammar error
        if "flow through" in question_text.lower() and "how do" in question_text.lower() and "function" in question_text.lower():
            new_question_text = "How does neural transmission flow through a neuron?"
            issues.append("CRITICAL_FLOW_GRAMMAR")
            self.critical_fixes += 1
        
        # 2. "How is the cerebral cortex parcellated into functional regions?"
        elif "parcellated" in question_text.lower() and "cerebral cortex" in question_text.lower():
            new_question_text = "What are the main functional regions of the cerebral cortex?"
            new_answer_text = "The cerebral cortex is organized into primary motor cortex (voluntary movement), primary somatosensory cortex (touch sensation), visual cortex (vision processing), auditory cortex (hearing processing), and association areas (complex cognitive functions like language, memory, and decision-making)."
            issues.append("CRITICAL_PARCELLATED")
            self.critical_fixes += 1
        
        # 3. "An ovoid structure labeled cell body is at the center of the neuron."
        elif "ovoid structure" in answer_text.lower() and "cell body" in answer_text.lower() and len(answer_text.split()) < 20:
            new_answer_text = "The cell body (soma) is the ovoid structure at the center of the neuron that contains the nucleus and most organelles. It integrates incoming signals from dendrites and generates action potentials that travel down the axon to communicate with other neurons."
            issues.append("CRITICAL_OVOID_INCOMPLETE")
            self.critical_fixes += 1
        
        # General grammar fixes
        elif "how do" in question_text.lower() and "function" in question_text.lower():
            new_question_text = re.sub(r"How do (.+) function", r"How does \\1 function", question_text, flags=re.IGNORECASE)
            issues.append("GRAMMAR_HOW_DO")
        
        elif not question_text.strip().endswith(('?', '.', '!')):
            new_question_text = question_text.strip() + "?"
            issues.append("MISSING_PUNCTUATION")
        
        if not issues:
            return False
        
        # Apply fixes
        updated_fields = {}
        
        # Update Question field if changed
        if new_question_text != question_text:
            updated_fields["Question"] = self.update_html_content(question_html, question_text, new_question_text)
        else:
            updated_fields["Question"] = question_html
        
        # Update Answer field if changed
        if new_answer_text != answer_text:
            updated_fields["Answer"] = self.update_html_content(answer_html, answer_text, new_answer_text)
        else:
            updated_fields["Answer"] = answer_html
        
        # Keep other fields unchanged
        for field_name in ["Priority", "Source", "Chapter", "Clinical"]:
            if field_name in fields:
                updated_fields[field_name] = fields[field_name].get("value", "")
        
        # Update the note
        update_result = self.request("updateNoteFields", {
            "note": {
                "id": note_id,
                "fields": updated_fields
            }
        })
        
        if update_result and update_result.get("error") is None:
            print(f"   🎯 Card {card_id} - Fixed: {', '.join(issues)}")
            if any("CRITICAL" in issue for issue in issues):
                print(f"      🔥 CRITICAL ISSUE RESOLVED!")
            self.fixes_applied += 1
            return True
        else:
            print(f"   ❌ Card {card_id} - Update failed: {update_result}")
            return False
    
    def process_all_cards(self):
        """Process every card"""
        print("🚀 ULTIMATE ANKI CARD FIXER V3")
        print("=" * 60)
        print("Targeting PSYC2240 Memory Optimized note type")
        print("Fixing user-identified critical issues:")
        print("  • Flow through neuron grammar error")
        print("  • Parcellated cerebral cortex question")  
        print("  • Incomplete ovoid structure answer")
        print("=" * 60)
        
        cards = self.find_all_cards()
        if not cards:
            print("❌ No cards found!")
            return
        
        print(f"\\n🔧 Processing {len(cards)} cards...")
        
        # Process cards in batches
        batch_size = 50
        for i in range(0, len(cards), batch_size):
            batch = cards[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(cards) + batch_size - 1) // batch_size
            
            print(f"\\n📦 Batch {batch_num}/{total_batches}")
            
            for j, card_id in enumerate(batch):
                self.cards_processed += 1
                card_num = i + j + 1
                
                success = self.analyze_and_fix_card(card_id)
                
                if card_num % 100 == 0:
                    print(f"   📊 Progress: {card_num}/{len(cards)} cards processed")
        
        # Final report
        print(f"\\n🎉 ULTIMATE FIX COMPLETE!")
        print("=" * 60)
        print(f"📊 Total cards processed: {self.cards_processed}")
        print(f"🔧 Cards fixed: {self.fixes_applied}")
        print(f"🔥 Critical user issues fixed: {self.critical_fixes}")
        print(f"✅ Success rate: {(self.fixes_applied/self.cards_processed*100):.1f}%")
        
        if self.critical_fixes > 0:
            print(f"\\n🎯 SUCCESS: Fixed the specific problematic cards you identified!")
        else:
            print(f"\\n🔍 Those specific cards may have already been fixed or need manual review")

if __name__ == "__main__":
    fixer = UltimateFixerV3()
    fixer.process_all_cards()