import requests

def anki_request(action, params=None):
    payload = {'action': action, 'version': 6}
    if params:
        payload['params'] = params
    response = requests.post('http://127.0.0.1:8765', json=payload, timeout=10)
    return response.json()

# Find and fix the last corrupted card
card_response = anki_request('findCards', {'query': 'deck:"PSYC 2240*"'})
card_ids = card_response['result']

for i in range(0, len(card_ids), 50):
    batch = card_ids[i:i+50]
    info_response = anki_request('cardsInfo', {'cards': batch})
    if info_response.get('error'):
        continue
    
    for card in info_response['result']:
        answer = card['fields'].get('Answer', {}).get('value', '')
        if 'summarize the symptoms of MS' in answer:
            question = card['fields'].get('Question', {}).get('value', '')
            print(f'Found last corrupted card:')
            print(f'Q: {question}')
            print(f'A: {answer}')
            
            # Fix it
            update_response = anki_request('updateNoteFields', {
                'note': {
                    'id': card['note'],
                    'fields': {
                        'Question': question,
                        'Answer': 'Autoimmune disease affecting the central nervous system myelin, causing motor and cognitive symptoms.',
                        'Priority': card['fields'].get('Priority', {}).get('value', ''),
                        'Source': card['fields'].get('Source', {}).get('value', ''),
                        'Chapter': card['fields'].get('Chapter', {}).get('value', ''),
                        'Clinical': card['fields'].get('Clinical', {}).get('value', '')
                    }
                }
            })
            
            if update_response.get('error'):
                print(f'Error: {update_response["error"]}')
            else:
                print('✅ Fixed the last corrupted card!')
            break
            
print('Done!')