#!/usr/bin/env python3
"""
Test script to verify AnkiConnect is properly installed and working.
Supports both local and remote connections for Codespace usage.
"""

import json
import urllib.request
import urllib.parse
import os

def get_anki_host():
    """Get AnkiConnect host from VS Code settings or environment"""
    try:
        # Try to read from VS Code settings
        with open('.vscode/settings.json', 'r') as f:
            settings = json.load(f)
            hostname = settings.get('anki.api.hostname', '127.0.0.1')
            if hostname != 'YOUR_LOCAL_IP_HERE':
                return hostname
    except:
        pass
    
    # Fallback to environment variable or localhost
    return os.environ.get('ANKI_HOST', '127.0.0.1')

def invoke_anki(action, version=6, **params):
    """Send a request to AnkiConnect"""
    host = get_anki_host()
    url = f'http://{host}:8765'
    
    request_data = {'action': action, 'version': version}
    if params:
        request_data['params'] = params
    
    request_json = json.dumps(request_data).encode('utf-8')
    
    try:
        print(f"   🔗 Connecting to: {url}")
        request = urllib.request.Request(url, request_json)
        response = urllib.request.urlopen(request, timeout=10)
        response_json = json.loads(response.read().decode('utf-8'))
        
        if response_json.get('error'):
            raise Exception(f"AnkiConnect error: {response_json['error']}")
        
        return response_json.get('result')
    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        if host != '127.0.0.1':
            print(f"   💡 Make sure Anki is running on {host} with ANKICONNECT_BIND_ADDRESS=0.0.0.0")
        else:
            print("   💡 Make sure Anki is running and AnkiConnect is installed")
        return None

def test_anki_connection():
    """Test AnkiConnect installation and configuration"""
    host = get_anki_host()
    
    print("🧪 Testing AnkiConnect Connection...")
    print("=" * 50)
    print(f"🎯 Target: {host}:8765")
    
    if host == 'YOUR_LOCAL_IP_HERE':
        print("⚠️  Please update .vscode/settings.json with your local IP address!")
        print("   See CODESPACE_ANKI_SETUP.md for instructions")
        return False
    
    # Test 1: Basic connection
    print("\n1. Testing basic connection...")
    version = invoke_anki('version')
    if version:
        print(f"   ✅ AnkiConnect v{version} is running on {host}")
    else:
        print("   ❌ Could not connect to AnkiConnect")
        return False
    
    # Test 2: Get deck names
    print("\n2. Testing deck access...")
    decks = invoke_anki('deckNames')
    if decks:
        print(f"   ✅ Found {len(decks)} decks:")
        psyc_decks = [d for d in decks if 'PSYC' in d or 'psyc' in d]
        if psyc_decks:
            print("   🎯 PSYC 2240 decks found:")
            for deck in psyc_decks:
                print(f"      - {deck}")
        else:
            print("   ⚠️  No PSYC 2240 decks found")
            print("   💡 Import your PSYC2240_Consolidated_Deck.apkg first")
    else:
        print("   ❌ Could not retrieve deck names")
        return False
    
    # Test 3: Get model names  
    print("\n3. Testing note types...")
    models = invoke_anki('modelNames')
    if models:
        print(f"   ✅ Found {len(models)} note types:")
        basic_found = 'Basic' in models
        cloze_found = 'Cloze' in models
        if basic_found and cloze_found:
            print("   ✅ Basic and Cloze note types available")
        else:
            print("   ⚠️  Missing required note types")
            if not basic_found:
                print("      - Basic note type not found")
            if not cloze_found:
                print("      - Cloze note type not found")
    else:
        print("   ❌ Could not retrieve note types")
        return False
        
    print("\n" + "=" * 50)
    print("🎉 AnkiConnect is working properly!")
    print("💡 You can now use VS Code extensions to create Anki cards")
    print("🔗 Next step: Configure your VS Code extensions")
    return True

if __name__ == "__main__":
    test_anki_connection()