import requests

def anki_request(action, params=None):
    payload = {'action': action, 'version': 6}
    if params:
        payload['params'] = params
    response = requests.post('http://127.0.0.1:8765', json=payload, timeout=10)
    return response.json()

# Find the Korsakoff syndrome card
card_response = anki_request('findCards', {'query': 'deck:"PSYC 2240*" Korsakoff'})
if card_response.get('error'):
    print(f'Error finding cards: {card_response["error"]}')
else:
    card_ids = card_response['result']
    print(f'Found {len(card_ids)} Korsakoff syndrome cards')
    
    if card_ids:
        # Get card info to confirm
        info_response = anki_request('cardsInfo', {'cards': card_ids})
        if not info_response.get('error'):
            for card in info_response['result']:
                question = card['fields'].get('Question', {}).get('value', '')
                answer = card['fields'].get('Answer', {}).get('value', '')
                print(f'Card found: {question}')
                print(f'Answer: {answer}')
                
                # Delete the note (which will delete all associated cards)
                delete_response = anki_request('deleteNotes', {'notes': [card['note']]})
                if delete_response.get('error'):
                    print(f'Error deleting: {delete_response["error"]}')
                else:
                    print('✅ Korsakoff syndrome card deleted successfully!')
    else:
        print('No Korsakoff syndrome cards found to delete.')