"""
Search for SPECIFIC problem cards mentioned by user
Find and fix exact issues:
1. "How is the cerebral cortex parcellated into functional regions?" 
2. "How do Flow through a Neuron function?"
3. "An ovoid structure labeled cell body is at the center of the neuron."
"""

import requests
import json
import re

class SpecificCardFinder:
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
        """Remove HTML tags"""
        clean = re.sub(r'<[^>]+>', '', text)
        return clean.strip()
    
    def search_for_specific_text(self):
        """Search for cards containing specific problematic text"""
        print("🔍 Searching for specific problem cards...")
        
        # Search terms that should find the problematic cards
        search_terms = [
            "parcellated",
            "Flow through a Neuron", 
            "ovoid structure",
            "cerebral cortex",
            "cell body"
        ]
        
        all_card_ids = set()
        
        for term in search_terms:
            print(f"\n🔍 Searching for: '{term}'")
            
            # Search in both question and answer fields
            queries = [
                f'"{term}"',
                f'*{term}*',
                f'front:*{term}*',
                f'back:*{term}*'
            ]
            
            for query in queries:
                result = self.request("findCards", {"query": query})
                if result and result.get("result"):
                    cards = result["result"]
                    all_card_ids.update(cards)
                    if cards:
                        print(f"   Query '{query}': {len(cards)} cards found")
        
        print(f"\n📊 Total cards found with search terms: {len(all_card_ids)}")
        
        # Get detailed info for each card
        if all_card_ids:
            print("\n🔍 Examining cards for specific issues...")
            
            card_ids = list(all_card_ids)
            batch_size = 50
            
            problem_cards = []
            
            for i in range(0, len(card_ids), batch_size):
                batch = card_ids[i:i+batch_size]
                cards_info = self.request("cardsInfo", {"cards": batch})
                
                if not cards_info or not cards_info.get("result"):
                    continue
                
                for card in cards_info["result"]:
                    card_id = card.get("cardId")
                    question = self.clean_html(card.get("question", ""))
                    answer = self.clean_html(card.get("answer", ""))
                    
                    # Check for specific problems
                    issues = []
                    
                    # Problem 1: Parcellated
                    if "parcellated" in question.lower():
                        issues.append("PARCELLATED_ISSUE")
                    
                    # Problem 2: Grammar issue with "Flow through"
                    if "flow through" in question.lower() and "function" in question.lower():
                        issues.append("FLOW_GRAMMAR_ISSUE") 
                    
                    # Problem 3: Incomplete answer about ovoid structure
                    if "ovoid structure" in answer.lower() and len(answer) < 50:
                        issues.append("INCOMPLETE_OVOID_ANSWER")
                    
                    # Show any card with these issues
                    if issues or "parcellated" in question.lower() or "flow through" in question.lower() or "ovoid" in answer.lower():
                        problem_cards.append({
                            "id": card_id,
                            "question": question,
                            "answer": answer,
                            "issues": issues
                        })
                        
                        print(f"\n🚨 FOUND POTENTIAL PROBLEM CARD (ID: {card_id})")
                        print(f"   Question: {question}")
                        print(f"   Answer: {answer}")
                        print(f"   Issues: {issues}")
                        print("-" * 80)
            
            print(f"\n📈 Found {len(problem_cards)} cards with potential issues")
            return problem_cards
        
        return []

if __name__ == "__main__":
    finder = SpecificCardFinder()
    finder.search_for_specific_text()