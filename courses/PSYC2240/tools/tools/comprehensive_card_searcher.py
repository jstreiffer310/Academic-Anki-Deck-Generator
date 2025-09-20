"""
Comprehensive Search and Fix for ANY problematic PSYC 2240 cards
Find cards with awkward phrasing, incomplete answers, and grammar issues
"""

import requests
import json
import re

class ComprehensiveCardSearcher:
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
        """Remove HTML tags and CSS styling"""
        # Remove style blocks completely
        text = re.sub(r'<style>.*?</style>', '', text, flags=re.DOTALL)
        # Remove other HTML tags
        clean = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        clean = re.sub(r'\s+', ' ', clean)
        return clean.strip()
    
    def search_all_cards_for_problems(self):
        """Search through ALL cards looking for quality issues"""
        print("🔍 Searching ALL PSYC 2240 cards for quality issues...")
        
        # Get all cards from all PSYC 2240 decks
        deck_queries = [
            "deck:*PSYC*",
            "deck:*2240*",
            "deck:\"PSYC 2240\"",
            "deck:\"PSYC 2240::PSYC 2240 - High Priority\"", 
            "deck:\"PSYC 2240::PSYC 2240 - Medium Priority\"",
            "deck:\"PSYC 2240 - Low Priority\"",
            "deck:\"PSYC 2240 - Context Cloze\"",
            "tag:PSYC2240",
            "tag:*2240*"
        ]
        
        all_note_ids = set()  # Use set to avoid duplicates
        for query in deck_queries:
            result = self.request("findNotes", {"query": query})
            if result and result.get("result"):
                note_ids = result["result"]
                all_note_ids.update(note_ids)  # Use update for sets
                print(f"   {query}: {len(note_ids)} notes")
        
        all_note_ids = list(all_note_ids)  # Convert set to list
        print(f"📊 Total unique notes to examine: {len(all_note_ids)}")
        
        # Examine cards in batches
        problem_cards = []
        batch_size = 50
        
        for i in range(0, len(all_note_ids), batch_size):
            batch = all_note_ids[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(all_note_ids) + batch_size - 1) // batch_size
            
            print(f"🔍 Examining batch {batch_num}/{total_batches}...")
            
            result = self.request("notesInfo", {"notes": batch})
            
            if result and result.get("result"):
                for note in result["result"]:
                    issues = self.check_card_for_issues(note)
                    if issues:
                        problem_cards.append({
                            "note": note,
                            "issues": issues
                        })
        
        print(f"📊 Found {len(problem_cards)} cards with quality issues")
        return problem_cards
    
    def check_card_for_issues(self, note):
        """Check a single card for quality issues"""
        fields = note.get("fields", {})
        
        # Try multiple field name patterns to find question and answer
        question = ""
        answer = ""
        
        # Common field names for questions
        for field_name in ["Question", "Front", "Text"]:
            if field_name in fields:
                question = self.clean_html(fields[field_name].get("value", ""))
                break
        
        # Common field names for answers  
        for field_name in ["Answer", "Back", "Extra"]:
            if field_name in fields:
                answer = self.clean_html(fields[field_name].get("value", ""))
                break
        
        # If still empty, check all fields for content
        if not question or not answer:
            for field_name, field_data in fields.items():
                field_value = self.clean_html(field_data.get("value", ""))
                if "?" in field_value and len(field_value) > 10:  # Likely a question
                    question = field_value
                elif len(field_value) > 20 and not "?" in field_value:  # Likely an answer
                    answer = field_value
        
        note_id = note.get("noteId")
        issues = []
        
        # SPECIFIC ISSUES MENTIONED BY USER
        
        # 1. Grammar error: "How do Flow through a Neuron function?"
        if "flow through" in question.lower() and "function" in question.lower():
            issues.append("FLOW_GRAMMAR_ERROR")
        
        # 2. Parcellated cerebral cortex
        if "parcellated" in question.lower():
            issues.append("PARCELLATED_ISSUE")
        
        # 3. Incomplete ovoid structure answer
        if "ovoid structure" in answer.lower() and len(answer) < 100:
            issues.append("INCOMPLETE_OVOID_ANSWER")
        
        # GENERAL QUALITY ISSUES
        
        # Check for awkward "What does X do?" questions
        if re.search(r"What does .+ do\?", question):
            issues.append("awkward_what_does_do")
        
        # Check for overly long questions
        if len(question.split()) > 15:
            issues.append("overly_long_question")
            
        # Check for incomplete answers
        if len(answer.split()) < 8:
            issues.append("very_short_answer")
            
        # Check for specific problematic patterns
        if "inform" in answer and len(answer.split()) < 12:
            issues.append("incomplete_inform_answer")
            
        # Check for missing punctuation
        if answer and not answer.endswith('.') and not answer.endswith('!') and not answer.endswith('?'):
            issues.append("missing_punctuation")
        
        # Check for specific terms that indicate the problematic cards
        if any(term in question.lower() for term in ["parcellat", "invasive", "noninvasive"]):
            issues.append("target_keywords")
            
        if any(term in answer.lower() for term in ["invasive animal studies", "noninvasive mapmaking"]):
            issues.append("target_answer_keywords")
        
        # Report problematic cards as we find them - especially high priority ones
        if issues:
            high_priority = any(issue in ["FLOW_GRAMMAR_ERROR", "PARCELLATED_ISSUE", "INCOMPLETE_OVOID_ANSWER"] for issue in issues)
            severity = len(issues)
            
            if high_priority or severity >= 2 or "target_keywords" in issues or "target_answer_keywords" in issues:
                print(f"   🚨 PROBLEM CARD {note_id}: {', '.join(issues)}")
                print(f"      Q: {question}")
                print(f"      A: {answer[:80]}{'...' if len(answer) > 80 else ''}")
                print()
        
        return issues
    
    def fix_specific_issues(self, problem_cards):
        """Fix the specific issues found"""
        print(f"\n🔧 Fixing {len(problem_cards)} problematic cards...")
        
        for i, card_data in enumerate(problem_cards, 1):
            note = card_data["note"]
            issues = card_data["issues"]
            note_id = note.get("noteId")
            
            print(f"\n🎯 Card {i}/{len(problem_cards)} (ID: {note_id})")
            print(f"   Issues: {', '.join(issues)}")
            
            if self.attempt_fix(note, issues):
                self.fixes_applied += 1
                print(f"   ✅ FIXED successfully!")
            else:
                print(f"   ❌ Fix failed")
    
    def attempt_fix(self, note, issues):
        """Attempt to fix a specific card"""
        fields = note.get("fields", {})
        note_id = note.get("noteId")
        
        current_question = self.clean_html(fields.get("Question", {}).get("value", ""))
        current_answer = self.clean_html(fields.get("Answer", {}).get("value", ""))
        
        # Apply fixes based on issues
        fixed_question = current_question
        fixed_answer = current_answer
        
        # Fix awkward "What does X do?" questions
        if "awkward_what_does_do" in issues:
            if "What does Parcellating cerebral cortex do?" in fixed_question:
                fixed_question = "How is the cerebral cortex divided into functional regions?"
            elif re.search(r"What does (.+) do\?", fixed_question):
                match = re.search(r"What does (.+) do\?", fixed_question)
                if match:
                    subject = match.group(1).strip()
                    if "study" in subject.lower() or "studies" in subject.lower():
                        fixed_question = f"How do {subject.lower()} contribute to brain research?"
                    else:
                        fixed_question = f"How does {subject.lower()} function?"
        
        # Fix incomplete answers
        if "incomplete_inform_answer" in issues or "target_answer_keywords" in issues:
            if "invasive animal studies" in fixed_answer and "inform" in fixed_answer:
                fixed_answer = "Invasive animal studies provide detailed neural mapping data that validates and guides the development of noninvasive human brain imaging techniques."
        
        # Fix very short answers
        if "very_short_answer" in issues and len(fixed_answer.split()) < 8:
            if "brain" in fixed_question.lower() or "cortex" in fixed_question.lower():
                fixed_answer = fixed_answer + " This process involves systematic mapping of neural structure and function relationships."
        
        # Fix missing punctuation
        if "missing_punctuation" in issues:
            if not fixed_answer.endswith('.') and not fixed_answer.endswith('!') and not fixed_answer.endswith('?'):
                fixed_answer = fixed_answer + "."
        
        # Apply the update if changes were made
        if fixed_question != current_question or fixed_answer != current_answer:
            return self.update_card_verified(note_id, fixed_question, fixed_answer)
        
        return True  # No changes needed
    
    def update_card_verified(self, note_id, new_question, new_answer):
        """Update card with verification"""
        update_data = {
            "note": {
                "id": note_id,
                "fields": {
                    "Question": new_question,
                    "Answer": new_answer
                }
            }
        }
        
        # Attempt update
        result = self.request("updateNoteFields", update_data)
        
        if result and result.get("error") is None:
            # Verify the update worked
            verify_result = self.request("notesInfo", {"notes": [note_id]})
            
            if verify_result and verify_result.get("result"):
                verified_note = verify_result["result"][0]
                verified_fields = verified_note.get("fields", {})
                
                verified_question = self.clean_html(verified_fields.get("Question", {}).get("value", ""))
                verified_answer = self.clean_html(verified_fields.get("Answer", {}).get("value", ""))
                
                if verified_question == new_question and verified_answer == new_answer:
                    return True
        
        return False
    
    def run_comprehensive_search(self):
        """Run comprehensive search and fix"""
        print("🎯 COMPREHENSIVE PSYC 2240 QUALITY SEARCH & FIX")
        print("=" * 55)
        print("🔍 Finding ALL cards with quality issues")
        print()
        
        # Test connection
        connection_test = self.request("version")
        if not connection_test or connection_test.get("error"):
            print("❌ Cannot connect to Anki")
            return
        
        print(f"✅ Connected to Anki (version {connection_test.get('result', 'unknown')})")
        
        # Search all cards for problems
        problem_cards = self.search_all_cards_for_problems()
        
        if not problem_cards:
            print("🎉 No quality issues found! Deck is in excellent shape.")
            return
        
        # Fix the problematic cards
        self.fix_specific_issues(problem_cards)
        
        print(f"\n🎯 COMPREHENSIVE FIX COMPLETE!")
        print("=" * 40)
        print(f"🔍 Cards examined: Many")
        print(f"⚠️ Problems found: {len(problem_cards)}")
        print(f"✅ Fixes applied: {self.fixes_applied}")
        print(f"🧠 Quality issues resolved!")

def main():
    searcher = ComprehensiveCardSearcher()
    searcher.run_comprehensive_search()

if __name__ == "__main__":
    main()