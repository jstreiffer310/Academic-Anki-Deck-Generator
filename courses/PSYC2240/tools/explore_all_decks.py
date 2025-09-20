"""
Find ALL PSYC2240 Cards Across ALL Decks
Debug script to see exactly what decks and cards exist
"""

import requests
import json

class DeckExplorer:
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
    
    def explore_all_decks(self):
        """Find all decks and PSYC2240 cards"""
        print("🔍 EXPLORING ALL DECKS...")
        
        # Get all deck names
        deck_result = self.request("deckNames")
        if not deck_result:
            print("❌ Could not get deck names")
            return
            
        all_decks = deck_result.get("result", [])
        print(f"📚 Total decks found: {len(all_decks)}")
        
        psyc_decks = []
        for deck in all_decks:
            if "psyc" in deck.lower() or "2240" in deck:
                psyc_decks.append(deck)
                print(f"   🎯 PSYC deck: {deck}")
        
        print(f"\n📊 Found {len(psyc_decks)} PSYC2240-related decks")
        
        # Search for cards in each deck
        total_cards = 0
        for deck in psyc_decks:
            print(f"\n🔍 Searching deck: {deck}")
            
            # Try different query formats
            queries = [
                f'deck:"{deck}"',
                f'deck:{deck}',
                f'deck:*{deck}*'
            ]
            
            deck_cards = set()
            for query in queries:
                result = self.request("findCards", {"query": query})
                if result and result.get("result"):
                    cards = result["result"]
                    deck_cards.update(cards)
            
            print(f"   📈 Cards in {deck}: {len(deck_cards)}")
            total_cards += len(deck_cards)
            
            # Get some sample card info
            if deck_cards:
                sample_cards = list(deck_cards)[:3]  # First 3 cards
                card_info = self.request("cardsInfo", {"cards": sample_cards})
                if card_info and card_info.get("result"):
                    for i, card in enumerate(card_info["result"]):
                        question = card.get("question", "").replace("<br>", " ").replace("<div>", " ")
                        question = question.replace("</div>", "").replace("<span>", "").replace("</span>", "")
                        question = question[:100]
                        print(f"      Sample {i+1}: {question}...")
        
        print(f"\n🎯 TOTAL PSYC2240 CARDS FOUND: {total_cards}")
        
        # Also try broad searches
        print(f"\n🔍 TRYING BROAD SEARCHES...")
        broad_queries = [
            "deck:*PSYC*",
            "deck:*2240*", 
            "tag:PSYC2240",
            "tag:*2240*",
            "*cerebral*",
            "*neuron*"
        ]
        
        all_found = set()
        for query in broad_queries:
            result = self.request("findCards", {"query": query})
            if result and result.get("result"):
                cards = result["result"]
                all_found.update(cards)
                print(f"   Query '{query}': {len(cards)} cards")
        
        print(f"\n🎯 TOTAL FROM BROAD SEARCH: {len(all_found)} unique cards")
        
        return all_found

if __name__ == "__main__":
    explorer = DeckExplorer()
    explorer.explore_all_decks()