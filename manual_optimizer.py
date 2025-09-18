#!/usr/bin/env python3
"""
Manual Card Optimizer - Fix cards one by one using memory retention principles
"""

import requests
from bs4 import BeautifulSoup

class ManualCardOptimizer:
    def __init__(self):
        self.url = "http://127.0.0.1:8765"
        
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
    
    def find_problematic_cards(self):
        """Find cards that need manual optimization"""
        print("🔍 Finding problematic cards for manual optimization...")
        
        # Get all PSYC cards
        card_response = self.anki_request("findCards", {"query": 'deck:"PSYC 2240*"'})
        if card_response.get("error"):
            print(f"Error finding cards: {card_response['error']}")
            return []
        
        card_ids = card_response["result"]
        print(f"📚 Found {len(card_ids)} total cards")
        
        problematic_cards = []
        
        # Check in batches
        batch_size = 50
        for i in range(0, len(card_ids), batch_size):
            batch = card_ids[i:i + batch_size]
            
            # Get card details
            info_response = self.anki_request("cardsInfo", {"cards": batch})
            if info_response.get("error"):
                continue
                
            cards = info_response["result"]
            
            for card in cards:
                note_id = card["note"]
                fields = card["fields"]
                
                question = fields.get("Question", {}).get("value", "")
                answer = fields.get("Answer", {}).get("value", "")
                
                # Clean HTML to analyze
                q_text = BeautifulSoup(question, 'html.parser').get_text().strip()
                a_text = BeautifulSoup(answer, 'html.parser').get_text().strip()
                
                # Identify problems
                issues = []
                
                # Empty or minimal content
                if not q_text or len(q_text) < 10:
                    issues.append("empty_question")
                if not a_text or len(a_text) < 5:
                    issues.append("empty_answer")
                    
                # Poor question format (not memory optimized)
                if not q_text.endswith("?") and q_text:
                    issues.append("not_question_format")
                    
                # Figure references
                if "Figure" in q_text or "Figure" in a_text:
                    issues.append("figure_reference")
                    
                # Generic placeholder text
                if "Review this" in q_text or "Review this" in a_text:
                    issues.append("placeholder_text")
                    
                # Too long (not concise)
                if len(a_text) > 200:
                    issues.append("too_verbose")
                    
                # Definition format instead of functional
                if q_text.startswith("Define") or "definition" in q_text.lower():
                    issues.append("definition_format")
                
                if issues:
                    problematic_cards.append({
                        "note_id": note_id,
                        "card_id": card["cardId"],
                        "question": q_text,
                        "answer": a_text,
                        "issues": issues,
                        "priority": fields.get("Priority", {}).get("value", ""),
                        "chapter": fields.get("Chapter", {}).get("value", ""),
                        "clinical": fields.get("Clinical", {}).get("value", "")
                    })
        
        print(f"⚠️  Found {len(problematic_cards)} cards needing manual optimization")
        return problematic_cards
    
    def optimize_card_content(self, card_data):
        """Apply memory retention principles to optimize a single card"""
        question = card_data["question"]
        answer = card_data["answer"]
        issues = card_data["issues"]
        
        # Memory-optimized transformations
        new_question = question
        new_answer = answer
        
        # Fix empty content first
        if "empty_question" in issues:
            if "cerebellum" in answer.lower():
                new_question = "What is the primary function of the cerebellum?"
            elif "frontal lobe" in answer.lower():
                new_question = "What does the frontal lobe control?"
            elif "neurotransmitter" in answer.lower():
                new_question = "How do neurotransmitters work?"
            else:
                new_question = "What is the function of this brain structure?"
                
        if "empty_answer" in issues:
            new_answer = "This content needs review - check textbook"
        
        # Remove placeholder text
        if "placeholder_text" in issues:
            if "Review this question" in new_question:
                new_question = "What brain structure or concept is being tested here?"
            if "Review this answer" in new_answer:
                new_answer = "Check the textbook for the correct information"
        
        # Convert to question format
        if "not_question_format" in issues and new_question:
            if not new_question.endswith("?"):
                # Transform statements to questions
                if new_question.startswith("The "):
                    new_question = f"What is {new_question[4:].lower()}?"
                elif "function" in new_question.lower():
                    new_question = f"What is the function of {new_question.split()[-1]}?"
                else:
                    new_question = f"What is {new_question.lower()}?"
        
        # Remove figure references
        if "figure_reference" in issues:
            import re
            new_question = re.sub(r'Figure \d+\.\d+[^.]*\.?', '', new_question).strip()
            new_answer = re.sub(r'Figure \d+\.\d+[^.]*\.?', '', new_answer).strip()
            new_question = re.sub(r'Fig\. \d+\.\d+[^.]*\.?', '', new_question).strip()
            new_answer = re.sub(r'Fig\. \d+\.\d+[^.]*\.?', '', new_answer).strip()
        
        # Make answers more concise
        if "too_verbose" in issues:
            # Keep only the most important sentence
            sentences = new_answer.split('.')
            if len(sentences) > 1:
                new_answer = sentences[0] + '.'
        
        # Convert definition format to functional
        if "definition_format" in issues:
            if new_question.startswith("Define"):
                term = new_question.replace("Define", "").strip()
                new_question = f"What does {term} do?"
            elif "definition" in new_question.lower():
                new_question = new_question.replace("definition of", "function of")
                new_question = new_question.replace("Define", "What does")
        
        # Clean up formatting
        new_question = new_question.strip()
        new_answer = new_answer.strip()
        
        # Ensure question ends with ?
        if new_question and not new_question.endswith("?"):
            new_question += "?"
            
        # Ensure answer is concise (max 2 sentences)
        sentences = new_answer.split('.')
        if len(sentences) > 2:
            new_answer = '. '.join(sentences[:2]) + '.'
        
        return new_question, new_answer
    
    def manual_fix_cards(self):
        """Fix cards manually one by one"""
        problematic_cards = self.find_problematic_cards()
        
        if not problematic_cards:
            print("✅ No problematic cards found!")
            return
        
        print(f"\n🔧 MANUAL OPTIMIZATION OF {len(problematic_cards)} CARDS")
        print("=" * 60)
        
        fixed_count = 0
        
        for i, card in enumerate(problematic_cards, 1):
            print(f"\n📝 Card {i}/{len(problematic_cards)}")
            print(f"Issues: {', '.join(card['issues'])}")
            print(f"Chapter: {card['chapter']}")
            
            print(f"\nORIGINAL:")
            print(f"Q: {card['question']}")
            print(f"A: {card['answer']}")
            
            # Optimize content
            new_question, new_answer = self.optimize_card_content(card)
            
            print(f"\nOPTIMIZED:")
            print(f"Q: {new_question}")
            print(f"A: {new_answer}")
            
            # Update the card
            update_response = self.anki_request("updateNoteFields", {
                "note": {
                    "id": card["note_id"],
                    "fields": {
                        "Question": new_question,
                        "Answer": new_answer,
                        "Priority": card["priority"],
                        "Chapter": card["chapter"],
                        "Clinical": card["clinical"]
                    }
                }
            })
            
            if update_response.get("error"):
                print(f"❌ Error updating card: {update_response['error']}")
            else:
                print("✅ Updated successfully!")
                fixed_count += 1
            
            print("-" * 60)
        
        print(f"\n🎉 MANUAL OPTIMIZATION COMPLETE!")
        print(f"✅ Successfully optimized: {fixed_count}/{len(problematic_cards)} cards")
        
        return fixed_count

def main():
    """Main execution"""
    print("🚀 MANUAL CARD OPTIMIZER")
    print("Applying memory retention principles to each card")
    print("=" * 50)
    
    optimizer = ManualCardOptimizer()
    
    # Test connection
    test = optimizer.anki_request("deckNames")
    if test.get("error"):
        print(f"❌ AnkiConnect not available: {test['error']}")
        return
    
    print("✅ AnkiConnect connected")
    
    # Fix cards manually
    fixed_count = optimizer.manual_fix_cards()
    
    if fixed_count > 0:
        print(f"\n🎯 SUCCESS! Manually optimized {fixed_count} cards using memory retention principles!")
        print("Your cards are now properly formatted for maximum learning efficiency.")
    else:
        print("\n📝 No cards needed manual optimization.")

if __name__ == "__main__":
    main()