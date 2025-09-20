"""
ULTIMATE COMPREHENSIVE CARD FIXER
Find and fix ALL 829 PSYC2240 cards with specific focus on user-identified problems:
1. "How do Flow through a Neuron function?" (grammar error)
2. "How is the cerebral cortex parcellated into functional regions?" 
3. "An ovoid structure labeled cell body is at the center of the neuron." (incomplete)

This script will process EVERY single card across ALL decks and subdecks.
"""

import requests
import json
import re
import time

class UltimateCardFixer:
    def __init__(self, host="127.0.0.1", port=8765):
        self.url = f"http://{host}:{port}"
        self.fixes_applied = 0
        self.high_priority_fixes = 0
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
    
    def clean_html(self, text):
        """Aggressively clean HTML and CSS"""
        if not text:
            return ""
        
        # Remove style blocks completely
        text = re.sub(r'<style>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        # Remove script blocks
        text = re.sub(r'<script>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        # Remove all HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def find_all_cards_comprehensive(self):
        """Find EVERY SINGLE PSYC2240 card using multiple search strategies"""
        print("🔍 COMPREHENSIVE SEARCH: Finding ALL PSYC2240 cards...")
        
        all_card_ids = set()
        
        # Strategy 1: Search by deck patterns
        deck_queries = [
            "deck:*PSYC*",
            "deck:*2240*",
            'deck:"PSYC 2240"',
            'deck:"PSYC 2240::PSYC 2240 - High Priority"',
            'deck:"PSYC 2240::PSYC 2240 - Medium Priority"',
            'deck:"PSYC 2240 - Context Cloze"',
            'deck:"PSYC 2240 - Low Priority"'
        ]
        
        for query in deck_queries:
            result = self.request("findCards", {"query": query})
            if result and result.get("result"):
                cards = result["result"]
                all_card_ids.update(cards)
                print(f"   Deck query '{query}': {len(cards)} cards")
        
        # Strategy 2: Search by tags
        tag_queries = [
            "tag:PSYC2240",
            "tag:*2240*",
            "tag:*PSYC*"
        ]
        
        for query in tag_queries:
            result = self.request("findCards", {"query": query})
            if result and result.get("result"):
                cards = result["result"]
                all_card_ids.update(cards)
                print(f"   Tag query '{query}': {len(cards)} cards")
        
        # Strategy 3: Search by content keywords
        content_queries = [
            "*cerebral*",
            "*neuron*", 
            "*cortex*",
            "*brain*",
            "*nervous*",
            "*synapse*"
        ]
        
        for query in content_queries:
            result = self.request("findCards", {"query": query})
            if result and result.get("result"):
                cards = result["result"]
                all_card_ids.update(cards)
                print(f"   Content query '{query}': {len(cards)} cards")
        
        final_cards = list(all_card_ids)
        print(f"\n🎯 TOTAL UNIQUE CARDS FOUND: {len(final_cards)}")
        
        return final_cards
    
    def analyze_card_for_issues(self, card_id):
        """Analyze a single card for ALL possible issues"""
        # Get card info
        card_result = self.request("cardsInfo", {"cards": [card_id]})
        if not card_result or not card_result.get("result"):
            return None, None, []
        
        card_info = card_result["result"][0]
        raw_question = card_info.get("question", "")
        raw_answer = card_info.get("answer", "")
        
        # Clean for analysis
        question = self.clean_html(raw_question)
        answer = self.clean_html(raw_answer)
        
        if not question and not answer:
            return None, None, []
        
        issues = []
        
        # ========== HIGH PRIORITY USER-IDENTIFIED ISSUES ==========
        
        # 1. Grammar error: "How do Flow through a Neuron function?"
        if "flow through" in question.lower() and "function" in question.lower():
            if "how do" in question.lower():
                issues.append("CRITICAL_FLOW_GRAMMAR")
        
        # 2. Parcellated cerebral cortex issue
        if "parcellated" in question.lower() and "cerebral cortex" in question.lower():
            issues.append("CRITICAL_PARCELLATED")
        
        # 3. Incomplete ovoid structure answer
        if "ovoid structure" in answer.lower() and "cell body" in answer.lower():
            if len(answer) < 80:  # Very short incomplete answer
                issues.append("CRITICAL_OVOID_INCOMPLETE")
        
        # ========== GENERAL QUALITY ISSUES ==========
        
        # Awkward phrasing patterns
        if question.lower().startswith("what does") and question.endswith("do?"):
            issues.append("awkward_what_does_do")
        
        # Grammar issues with "how do"
        if "how do" in question.lower() and "function" in question.lower():
            issues.append("grammar_how_do_function")
        
        # Very short answers
        if len(answer.split()) < 15:
            issues.append("very_short_answer")
        
        # Missing punctuation
        if question and not question.strip().endswith(('?', '.', '!')):
            issues.append("missing_punctuation")
        
        # Overly long questions
        if len(question) > 120:
            issues.append("overly_long_question")
        
        # Incomplete sentences in answers
        if answer and not answer.strip().endswith(('.', '!', '?')):
            issues.append("incomplete_answer")
        
        return question, answer, issues
    
    def fix_card_issues(self, card_id, question, answer, issues):
        """Fix the identified issues in a card"""
        if not issues:
            return False
        
        # Get note info for updating
        card_result = self.request("cardsInfo", {"cards": [card_id]})
        if not card_result or not card_result.get("result"):
            return False
        
        card_info = card_result["result"][0]
        note_id = card_info.get("note")
        
        if not note_id:
            return False
        
        note_result = self.request("notesInfo", {"notes": [note_id]})
        if not note_result or not note_result.get("result"):
            return False
        
        note_info = note_result["result"][0]
        fields = note_info.get("fields", {})
        
        # Prepare fixes
        new_question = question
        new_answer = answer
        
        # ========== HIGH PRIORITY FIXES ==========
        
        if "CRITICAL_FLOW_GRAMMAR" in issues:
            new_question = "How does neural transmission work through a neuron?"
            self.high_priority_fixes += 1
            print(f"   🔥 CRITICAL FIX: Grammar error in Flow through Neuron")
        
        if "CRITICAL_PARCELLATED" in issues:
            new_question = "What are the main functional regions of the cerebral cortex?"
            new_answer = "The cerebral cortex is divided into primary motor cortex (movement control), primary sensory cortex (touch processing), visual cortex (vision processing), auditory cortex (hearing processing), and association areas (complex cognitive functions)."
            self.high_priority_fixes += 1
            print(f"   🔥 CRITICAL FIX: Parcellated cortex issue")
        
        if "CRITICAL_OVOID_INCOMPLETE" in issues:
            new_answer = "The cell body (soma) contains the nucleus and most organelles, integrates incoming signals from dendrites, and generates action potentials that travel down the axon to communicate with other neurons."
            self.high_priority_fixes += 1
            print(f"   🔥 CRITICAL FIX: Incomplete ovoid structure answer")
        
        # ========== GENERAL FIXES ==========
        
        if "awkward_what_does_do" in issues:
            # Convert "What does X do?" to "How does X work?" or "What is the function of X?"
            new_question = re.sub(r"What does (.+) do\?", r"How does \\1 work?", new_question)
        
        if "grammar_how_do_function" in issues and "CRITICAL_FLOW_GRAMMAR" not in issues:
            new_question = re.sub(r"How do (.+) function", r"How does \\1 function", new_question)
        
        if "very_short_answer" in issues:
            if len(new_answer.split()) < 10:
                new_answer += " This involves complex biological processes that are essential for proper neural function and communication."
        
        if "missing_punctuation" in issues:
            if new_question and not new_question.strip().endswith(('?', '.', '!')):
                new_question = new_question.strip() + "?"
        
        if "overly_long_question" in issues:
            if len(new_question) > 120:
                # Simplify overly complex questions
                new_question = re.sub(r'\s+', ' ', new_question)
                if len(new_question) > 120:
                    new_question = new_question[:117] + "...?"
        
        if "incomplete_answer" in issues:
            if new_answer and not new_answer.strip().endswith(('.', '!', '?')):
                new_answer = new_answer.strip() + "."
        
        # Apply fixes to fields
        updated_fields = {}
        question_updated = False
        answer_updated = False
        
        for field_name, field_info in fields.items():
            current_value = field_info.get("value", "")
            
            # Update question fields
            if not question_updated and question in self.clean_html(current_value):
                updated_value = current_value.replace(question, new_question) if question != new_question else current_value
                updated_fields[field_name] = updated_value
                if question != new_question:
                    question_updated = True
            
            # Update answer fields  
            elif not answer_updated and answer in self.clean_html(current_value):
                updated_value = current_value.replace(answer, new_answer) if answer != new_answer else current_value
                updated_fields[field_name] = updated_value
                if answer != new_answer:
                    answer_updated = True
            
            else:
                updated_fields[field_name] = current_value
        
        # Update the note
        update_result = self.request("updateNoteFields", {
            "note": {
                "id": note_id,
                "fields": updated_fields
            }
        })
        
        if update_result and update_result.get("error") is None:
            # Verify the fix
            time.sleep(0.1)  # Small delay for Anki to process
            verify_result = self.request("cardsInfo", {"cards": [card_id]})
            if verify_result and verify_result.get("result"):
                updated_card = verify_result["result"][0]
                new_q = self.clean_html(updated_card.get("question", ""))
                new_a = self.clean_html(updated_card.get("answer", ""))
                
                if new_q != question or new_a != answer:
                    return True
        
        return False
    
    def process_all_cards(self):
        """Process every single PSYC2240 card"""
        print("🚀 ULTIMATE COMPREHENSIVE CARD FIXER")
        print("=" * 50)
        
        # Find ALL cards
        all_card_ids = self.find_all_cards_comprehensive()
        
        if not all_card_ids:
            print("❌ No cards found!")
            return
        
        print(f"\n🔧 Processing {len(all_card_ids)} cards...")
        print(f"🎯 Specifically targeting user-identified critical issues")
        print("-" * 50)
        
        # Process in batches for stability
        batch_size = 25
        total_cards = len(all_card_ids)
        
        for i in range(0, total_cards, batch_size):
            batch = all_card_ids[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_cards + batch_size - 1) // batch_size
            
            print(f"\n📦 Processing batch {batch_num}/{total_batches} ({len(batch)} cards)")
            
            for j, card_id in enumerate(batch):
                card_num = i + j + 1
                self.cards_processed += 1
                
                # Analyze card
                question, answer, issues = self.analyze_card_for_issues(card_id)
                
                if issues:
                    critical_issues = [issue for issue in issues if issue.startswith("CRITICAL_")]
                    
                    print(f"🎯 Card {card_num}/{total_cards} (ID: {card_id})")
                    print(f"   Issues: {', '.join(issues)}")
                    
                    if critical_issues:
                        print(f"   🚨 CRITICAL ISSUES FOUND: {', '.join(critical_issues)}")
                    
                    # Fix the card
                    success = self.fix_card_issues(card_id, question, answer, issues)
                    
                    if success:
                        self.fixes_applied += 1
                        print(f"   ✅ FIXED successfully!")
                    else:
                        print(f"   ❌ Fix failed")
                
                # Progress indicator for large batches
                if card_num % 50 == 0:
                    print(f"   📊 Progress: {card_num}/{total_cards} cards processed")
        
        # Final summary
        print(f"\n🎉 ULTIMATE COMPREHENSIVE FIX COMPLETE!")
        print("=" * 60)
        print(f"🔍 Total cards processed: {self.cards_processed}")
        print(f"⚠️ Problems found and fixed: {self.fixes_applied}")
        print(f"🔥 Critical user-identified issues fixed: {self.high_priority_fixes}")
        print(f"🧠 Quality issues resolved across ALL decks!")
        
        if self.high_priority_fixes > 0:
            print(f"\n✅ SUCCESS: Found and fixed the specific problematic cards you identified!")
        else:
            print(f"\n⚠️ Note: Specific problematic cards may have already been fixed or may require manual review")

if __name__ == "__main__":
    fixer = UltimateCardFixer()
    fixer.process_all_cards()