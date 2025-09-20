"""
BETTER ANKI WORKFLOW - Export to Excel for Easy Editing
This approach bypasses AnkiConnect issues entirely.
"""

import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import json

def extract_clean_text(html):
    """Extract text content from CSS-heavy HTML"""
    if not html:
        return ""
    
    # Use BeautifulSoup for robust parsing
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove style and script tags
    for tag in soup(['style', 'script']):
        tag.decompose()
    
    # Get text and clean it
    text = soup.get_text(' ', strip=True)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def export_anki_to_excel():
    """Export all Anki cards to Excel for easy editing"""
    url = 'http://127.0.0.1:8765'
    
    # Get all cards
    all_cards = requests.post(url, json={
        'action': 'findCards', 
        'version': 6, 
        'params': {'query': 'deck:*PSYC*'}
    }).json()['result']
    
    print(f"Exporting {len(all_cards)} cards to Excel...")
    
    data = []
    
    for i, card_id in enumerate(all_cards):
        if i % 100 == 0:
            print(f"Processing {i}/{len(all_cards)}...")
        
        try:
            # Get card info
            card_info = requests.post(url, json={
                'action': 'cardsInfo',
                'version': 6,
                'params': {'cards': [card_id]}
            }).json()
            
            if not card_info.get('result'):
                continue
                
            card = card_info['result'][0]
            note_id = card.get('note')
            
            if not note_id:
                continue
            
            # Get note info
            note_info = requests.post(url, json={
                'action': 'notesInfo',
                'version': 6,
                'params': {'notes': [note_id]}
            }).json()
            
            if not note_info.get('result'):
                continue
                
            note = note_info['result'][0]
            fields = note['fields']
            
            # Extract clean content
            question_raw = fields.get('Question', {}).get('value', '')
            answer_raw = fields.get('Answer', {}).get('value', '')
            
            question_clean = extract_clean_text(question_raw)
            answer_clean = extract_clean_text(answer_raw)
            
            # Identify issues
            issues = []
            if 'Figure' in question_clean or 'Figure' in answer_clean:
                issues.append('Figure_Caption')
            if 'What characterizes' in question_clean and 'is' in question_clean:
                issues.append('Grammar_What_Characterizes')
            if len(answer_clean.split()) < 10:
                issues.append('Short_Answer')
            if not question_clean.endswith('?'):
                issues.append('Missing_Punctuation')
            
            data.append({
                'Card_ID': card_id,
                'Note_ID': note_id,
                'Question_Clean': question_clean,
                'Answer_Clean': answer_clean,
                'Priority': fields.get('Priority', {}).get('value', ''),
                'Source': fields.get('Source', {}).get('value', ''),
                'Chapter': fields.get('Chapter', {}).get('value', ''),
                'Clinical': fields.get('Clinical', {}).get('value', ''),
                'Issues': '; '.join(issues),
                'Question_Raw': question_raw[:200] + '...' if len(question_raw) > 200 else question_raw,
                'Answer_Raw': answer_raw[:200] + '...' if len(answer_raw) > 200 else answer_raw
            })
            
        except Exception as e:
            print(f"Error processing card {card_id}: {e}")
            continue
    
    # Create DataFrame and export
    df = pd.DataFrame(data)
    
    # Export to Excel with formatting
    with pd.ExcelWriter('PSYC2240_Cards_Export.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='All_Cards', index=False)
        
        # Get workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['All_Cards']
        
        # Format columns
        worksheet.set_column('A:A', 12)  # Card_ID
        worksheet.set_column('C:C', 50)  # Question_Clean
        worksheet.set_column('D:D', 50)  # Answer_Clean
        worksheet.set_column('I:I', 30)  # Issues
        
        # Add conditional formatting for issues
        red_format = workbook.add_format({'bg_color': '#FFC7CE'})
        worksheet.conditional_format('I:I', {
            'type': 'text',
            'criteria': 'containing',
            'value': 'Figure_Caption',
            'format': red_format
        })
    
    print(f"✅ Exported {len(data)} cards to PSYC2240_Cards_Export.xlsx")
    print("✅ Open in Excel to easily edit questions/answers")
    print("✅ Then use import script to update Anki")
    
    return df

def create_import_script():
    """Create a script to import Excel edits back to Anki"""
    script = '''
"""
IMPORT EXCEL EDITS BACK TO ANKI
Read the edited Excel file and update Anki cards
"""

import pandas as pd
import requests

def import_excel_edits():
    url = 'http://127.0.0.1:8765'
    
    # Read the edited Excel file
    df = pd.read_excel('PSYC2240_Cards_Export_EDITED.xlsx', sheet_name='All_Cards')
    
    print(f"Importing {len(df)} card edits...")
    
    success_count = 0
    
    for i, row in df.iterrows():
        if i % 50 == 0:
            print(f"Importing {i}/{len(df)}...")
        
        try:
            note_id = row['Note_ID']
            new_question = row['Question_Clean']
            new_answer = row['Answer_Clean']
            
            # Update note
            result = requests.post(url, json={
                'action': 'updateNoteFields',
                'version': 6,
                'params': {
                    'note': {
                        'id': note_id,
                        'fields': {
                            'Question': new_question,
                            'Answer': new_answer,
                            'Priority': row['Priority'],
                            'Source': row['Source'],
                            'Chapter': row['Chapter'],
                            'Clinical': row['Clinical']
                        }
                    }
                }
            })
            
            if result.json().get('error') is None:
                success_count += 1
            else:
                print(f"Error updating note {note_id}: {result.json()}")
                
        except Exception as e:
            print(f"Error processing row {i}: {e}")
    
    print(f"✅ Successfully imported {success_count}/{len(df)} edits")

if __name__ == '__main__':
    import_excel_edits()
'''
    
    with open('import_excel_edits.py', 'w', encoding='utf-8') as f:
        f.write(script)
    
    print("✅ Created import_excel_edits.py")

if __name__ == '__main__':
    # Export to Excel
    df = export_anki_to_excel()
    
    # Create import script
    create_import_script()
    
    print("\\n🎯 WORKFLOW:")
    print("1. Open PSYC2240_Cards_Export.xlsx in Excel")
    print("2. Edit Question_Clean and Answer_Clean columns")
    print("3. Save as PSYC2240_Cards_Export_EDITED.xlsx")
    print("4. Run: python import_excel_edits.py")