#!/usr/bin/env python3
"""
Test AnkiConnect connection using direct IP address
"""

import json
import urllib.request
import urllib.parse

# Use your local machine's IP address
ANKI_URL = "http://10.0.0.123:8765/"

def test_anki_connection():
    print("🧪 Testing AnkiConnect via Direct IP...")
    print("=" * 50)
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
                    for deck in psyc_decks:
                        print(f"   🧠 {deck}")
                        
            print(f"\n🚀 AnkiConnect is working! VS Code integration ready!")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Make sure:")
        print("   1. Anki is running on your local machine")
        print("   2. AnkiConnect webBindAddress is set to '0.0.0.0'")
        print("   3. Your firewall allows connections on port 8765")
        return False
        
    return True

if __name__ == "__main__":
    test_anki_connection()