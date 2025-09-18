"""
Find and Fix Specific Problem Cards
Target the exact issues mentioned:
1. "How is the cerebral cortex parcellated into functional regions?"
2. "How do Flow through a Neuron function?" 
3. "An ovoid structure labeled cell body is at the center of the neuron."
"""

import requests
import json
import re

class SpecificProblemFinder:
    def __init__(self, host="127.0.0.1", port=8765):
        self.url = f"http://{host}:{port}"
        self.fixes_applied = 0
        
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
        """Remove HTML tags"""
        import re
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()
    
    def find_all_cards(self):
        """Find ALL cards in ALL PSYC2240 decks"""
        print("🔍 Searching ALL PSYC2240 decks...")
        
        # Search for all PSYC2240 cards across all possible deck names
        queries = [
            "deck:PSYC2240",
            "deck:\"PSYC2240\"",
            "deck:*PSYC2240*",
            "deck:\"PSYC 2240\"",
            "deck:*2240*",
            "tag:PSYC2240",
            "tag:*2240*"
        ]
        
        all_card_ids = set()
        
        for query in queries:
            result = self.request("findCards", {"query": query})
            if result and result.get("result"):
                card_ids = result["result"]
                all_card_ids.update(card_ids)
                print(f"   Query '{query}': {len(card_ids)} cards")
        
        print(f"🎯 Total unique PSYC2240 cards found: {len(all_card_ids)}")
        return list(all_card_ids)
    
    def get_card_info(self, card_ids):
        """Get detailed info for cards"""
        result = self.request("cardsInfo", {"cards": card_ids})
        return result.get("result", []) if result else []
    
    def find_problem_cards(self):
        """Find cards with the specific problems mentioned"""
        print("\n🎯 Finding specific problem cards...")
        
        all_card_ids = self.find_all_cards()
        
        if not all_card_ids:
            print("❌ No PSYC2240 cards found!")
            return
        
        # Process in batches to avoid overwhelming AnkiConnect
        batch_size = 50
        problem_cards = []
        
        for i in range(0, len(all_card_ids), batch_size):
            batch = all_card_ids[i:i+batch_size]
            cards_info = self.get_card_info(batch)
            
            if not cards_info:
                continue
                
            for card in cards_info:
                card_id = card.get("cardId")
                question = self.clean_html(card.get("question", ""))
                answer = self.clean_html(card.get("answer", ""))
                
                # Check for specific problems
                problems = []
                
                # Problem 1: Parcellated cerebral cortex
                if "parcellated" in question.lower() and "cerebral cortex" in question.lower():
                    problems.append("parcellated_cortex")
                
                # Problem 2: Flow through neuron grammar
                if ("flow through" in question.lower() and "neuron" in question.lower() and 
                    "function" in question.lower()):
                    problems.append("flow_grammar")
                
                # Problem 3: Incomplete/nonsensical answers
                if ("ovoid structure" in answer.lower() and "cell body" in answer.lower() and
                    len(answer) < 100):
                    problems.append("incomplete_answer")
                
                # Additional grammar issues
                if "how do" in question.lower() and "function" in question.lower():
                    problems.append("grammar_issue")
                    
                # Very short answers that make no sense
                if len(answer) < 30 or answer.count(" ") < 3:
                    problems.append("very_short_nonsense")
                
                if problems:
                    problem_cards.append({
                        "id": card_id,
                        "question": question,
                        "answer": answer,
                        "problems": problems
                    })
                    
                    print(f"\n🚨 PROBLEM CARD FOUND (ID: {card_id})")
                    print(f"   Question: {question[:100]}...")
                    print(f"   Answer: {answer[:100]}...")
                    print(f"   Issues: {', '.join(problems)}")
        
        print(f"\n📊 Found {len(problem_cards)} cards with specific problems")
        return problem_cards
    
    def fix_specific_card(self, card_id, question, answer, problems):
        """Fix a specific problematic card"""
        new_question = question
        new_answer = answer
        
        # Fix parcellated cortex
        if "parcellated_cortex" in problems:
            new_question = "What are the main functional regions of the cerebral cortex?"
            new_answer = "The cerebral cortex is divided into primary motor cortex (movement control), primary sensory cortex (touch processing), visual cortex (vision processing), auditory cortex (hearing processing), and association areas (complex cognitive functions)."
        
        # Fix flow grammar
        if "flow_grammar" in problems or "grammar_issue" in problems:
            if "flow through" in new_question.lower():
                new_question = new_question.replace("How do Flow through a Neuron function", "How does neural transmission work through a neuron")
                new_question = new_question.replace("How do ", "How does ")
                new_question = new_question.replace(" function?", " work?")
        
        # Fix incomplete answers
        if "incomplete_answer" in problems or "very_short_nonsense" in problems:
            if "ovoid structure" in new_answer.lower():
                new_answer = "The cell body (soma) contains the nucleus and most organelles, integrates incoming signals from dendrites, and generates action potentials that travel down the axon to communicate with other neurons."
        
        # Update the card
        note_info_result = self.request("cardsInfo", {"cards": [card_id]})
        if not note_info_result or not note_info_result.get("result"):
            return False
            
        card_info = note_info_result["result"][0]
        note_id = card_info.get("note")
        
        if not note_id:
            return False
        
        # Get note info to update fields properly
        note_result = self.request("notesInfo", {"notes": [note_id]})
        if not note_result or not note_result.get("result"):
            return False
            
        note_info = note_result["result"][0]
        fields = note_info.get("fields", {})
        
        # Update the appropriate fields
        updated_fields = {}
        for field_name, field_info in fields.items():
            if field_name.lower() in ["front", "question"]:
                updated_fields[field_name] = new_question
            elif field_name.lower() in ["back", "answer"]:
                updated_fields[field_name] = new_answer
            else:
                updated_fields[field_name] = field_info.get("value", "")
        
        # Update the note
        update_result = self.request("updateNoteFields", {
            "note": {
                "id": note_id,
                "fields": updated_fields
            }
        })
        
        if update_result and update_result.get("error") is None:
            # Verify the update worked
            verify_result = self.request("cardsInfo", {"cards": [card_id]})
            if verify_result and verify_result.get("result"):
                updated_card = verify_result["result"][0]
                updated_question = self.clean_html(updated_card.get("question", ""))
                updated_answer = self.clean_html(updated_card.get("answer", ""))
                
                if updated_question != question or updated_answer != answer:
                    print(f"   ✅ VERIFIED: Card {card_id} successfully updated")
                    print(f"      New Q: {updated_question[:80]}...")
                    print(f"      New A: {updated_answer[:80]}...")
                    return True
                else:
                    print(f"   ❌ FAILED: Card {card_id} update not applied")
                    return False
        
        return False
    
    def fix_all_problems(self):
        """Find and fix all specific problem cards"""
        print("🎯 Starting comprehensive problem card search and fix...")
        
        problem_cards = self.find_problem_cards()
        
        if not problem_cards:
            print("✅ No specific problem cards found!")
            return
        
        print(f"\n🔧 Fixing {len(problem_cards)} problem cards...")
        
        for card in problem_cards:
            success = self.fix_specific_card(
                card["id"], 
                card["question"], 
                card["answer"], 
                card["problems"]
            )
            
            if success:
                self.fixes_applied += 1
        
        print(f"\n🎉 SPECIFIC PROBLEM FIX COMPLETE!")
        print(f"✅ Fixed {self.fixes_applied} specific problem cards")

if __name__ == "__main__":
    fixer = SpecificProblemFinder()
    fixer.fix_all_problems()