#!/usr/bin/env python3
"""
Test AnkiConnect connection using GitHub Codespace port forwarding
"""

import json
import urllib.request
import urllib.parse

# Use the forwarded URL instead of localhost
ANKI_URL = "https://glowing-space-dollop-wr5r957xv9wqfgq6g-8765.app.github.dev/"

def test_anki_connection():
    print("🧪 Testing AnkiConnect via GitHub Codespace Port Forwarding...")
    print("=" * 60)
    print(f"URL: {ANKI_URL}")
    print()
    
    # Test basic version request
    try:
        request_data = {
            'action': 'version',
            'version': 6
        }
        
        request_json = json.dumps(request_data).encode('utf-8')
        request = urllib.request.Request(ANKI_URL, request_json)
        request.add_header('Content-Type', 'application/json')
        
        print("Sending version request...")
        response = urllib.request.urlopen(request, timeout=10)
        response_data = response.read().decode('utf-8')
        
        print(f"✅ Raw response: {response_data}")
        
        response_json = json.loads(response_data)
        if response_json.get('error'):
            print(f"❌ AnkiConnect error: {response_json['error']}")
        else:
            print(f"🎉 SUCCESS! AnkiConnect version: {response_json.get('result')}")
            
            # Test getting deck names
            print("\n📚 Testing deck access...")
            deck_request = {
                'action': 'deckNames',
                'version': 6
            }
            
            deck_json = json.dumps(deck_request).encode('utf-8')
            deck_req = urllib.request.Request(ANKI_URL, deck_json)
            deck_req.add_header('Content-Type', 'application/json')
            
            deck_response = urllib.request.urlopen(deck_req, timeout=10)
            deck_data = json.loads(deck_response.read().decode('utf-8'))
            
            if deck_data.get('error'):
                print(f"❌ Deck access error: {deck_data['error']}")
            else:
                decks = deck_data.get('result', [])
                print(f"✅ Found {len(decks)} decks:")
                for deck in decks:
                    print(f"   - {deck}")
                    
                psyc_decks = [d for d in decks if 'PSYC' in d or 'psyc' in d]
                if psyc_decks:
                    print(f"\n🎯 PSYC 2240 decks found: {len(psyc_decks)}")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure Anki is running on your local machine")
        print("   2. Verify AnkiConnect addon is installed and configured")
        print("   3. Check that port forwarding is active in VS Code")
        return False
        
    return True

if __name__ == "__main__":
    test_anki_connection()