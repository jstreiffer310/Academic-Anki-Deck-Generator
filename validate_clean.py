#!/usr/bin/env python3
"""
Quick validation to check for any remaining corruption
"""

import requests
import re

def anki_request(action, params=None):
    payload = {'action': action, 'version': 6}
    if params:
        payload['params'] = params
    response = requests.post('http://127.0.0.1:8765', json=payload, timeout=10)
    return response.json()

# Check for any remaining corruption patterns
card_response = anki_request('findCards', {'query': 'deck:"PSYC 2240*"'})
card_ids = card_response['result']
print(f'Checking {len(card_ids)} cards for remaining corruption...')

corrupted_found = 0
for i in range(0, len(card_ids), 50):
    batch = card_ids[i:i+50]
    info_response = anki_request('cardsInfo', {'cards': batch})
    if info_response.get('error'):
        continue
    
    for card in info_response['result']:
        answer = card['fields'].get('Answer', {}).get('value', '')
        if re.search(r',\s*\d+,\s*\d+|Tower of Hanoi|f\s+[A-Z]|\d+f\s+\w+', answer):
            corrupted_found += 1
            print(f'STILL CORRUPTED: {answer[:100]}...')

if corrupted_found == 0:
    print('✅ SUCCESS! No remaining corruption found in any cards!')
else:
    print(f'⚠️ Found {corrupted_found} cards still needing fixes')