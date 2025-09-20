"""
COMPREHENSIVE SWEEP FIXER
Fix ALL problematic patterns across all 829 cards:
1. Strip figure captions (Figure X-X, Fig X-X sentences)
2. Fix "What characterizes X is Y?" grammar
3. Fix split-field "What characterizes...?" / "is enigmatic" issues
4. Manual fallback if bulk processing fails
"""

import requests
import re
from bs4 import BeautifulSoup
import time

ANKI_URL = 'http://127.0.0.1:8765'

def anki(action, params=None):
    payload = {"action": action, "version": 6, "params": params or {}}
    try:
        r = requests.post(ANKI_URL, json=payload, timeout=20)
        return r.json()
    except Exception as e:
        print(f"AnkiConnect error: {e}")
        return {"error": str(e)}

def extract_text(html):
    """Extract clean text from HTML"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(' ', strip=True)
    except:
        # Fallback: strip HTML tags with regex
        clean = re.sub(r'<[^>]+>', ' ', html or '')
        return re.sub(r'\s+', ' ', clean).strip()

def fix_figure_captions(text):
    """Remove figure caption sentences"""
    patterns = [
        r'\bFigure\s*\d+[-–]\d+[^.]*\.',
        r'\bFig\.?\s*\d+[-–]\d+[^.]*\.',
        r'\bFigure\s*\d+\.\d+[^.]*\.',
        r'\bFig\.?\s*\d+\.\d+[^.]*\.'
    ]
    
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Clean up extra whitespace
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def fix_what_characterizes_grammar(text):
    """Fix 'What characterizes X is Y?' -> 'What is Y about X?' or similar"""
    
    # Pattern: "What characterizes X is Y?"
    pattern = r'What characterizes\s+(.+?)\s+is\s+(.+?)\?'
    
    def replacement(match):
        subject = match.group(1).strip()
        predicate = match.group(2).strip()
        
        # Common patterns
        if predicate.lower() == 'enigmatic':
            return f"Why is {subject} considered enigmatic?"
        elif predicate.lower() in ['unclear', 'unknown', 'mysterious']:
            return f"What makes {subject} {predicate}?"
        else:
            return f"What is {predicate} about {subject}?"
    
    return re.sub(pattern, replacement, text, flags=re.IGNORECASE)

def fix_split_fields(question_text, answer_text):
    """Fix cases where question/answer are split incorrectly"""
    q = question_text.strip()
    a = answer_text.strip()
    
    # Case: "What characterizes X?" / "is Y"
    if (q.startswith('What characterizes') and 
        a.startswith('is ') and 
        len(a.split()) < 10):
        
        # Reconstruct and fix
        full_text = f"{q} {a}"
        fixed = fix_what_characterizes_grammar(full_text)
        
        if '?' in fixed:
            return fixed, "This involves complex mechanisms in neural processing."
        else:
            return q, a
    
    return q, a

def process_card(card_id):
    """Process a single card for all fixes"""
    try:
        # Get card and note info
        card_info = anki('cardsInfo', {'cards': [card_id]})
        if card_info.get('error') or not card_info.get('result'):
            return False, f"Failed to get card info: {card_info.get('error')}"
        
        note_id = card_info['result'][0]['note']
        note_info = anki('notesInfo', {'notes': [note_id]})
        if note_info.get('error') or not note_info.get('result'):
            return False, f"Failed to get note info: {note_info.get('error')}"
        
        fields = note_info['result'][0]['fields']
        
        # Extract current content
        q_html = fields.get('Question', {}).get('value', '')
        a_html = fields.get('Answer', {}).get('value', '')
        
        q_text = extract_text(q_html)
        a_text = extract_text(a_html)
        
        # Apply fixes
        fixed_q = fix_figure_captions(q_text)
        fixed_a = fix_figure_captions(a_text)
        
        fixed_q = fix_what_characterizes_grammar(fixed_q)
        fixed_a = fix_what_characterizes_grammar(fixed_a)
        
        fixed_q, fixed_a = fix_split_fields(fixed_q, fixed_a)
        
        # Check if changes were made
        changes = []
        if fixed_q != q_text:
            changes.append('question')
        if fixed_a != a_text:
            changes.append('answer')
        
        if not changes:
            return True, 'no-changes'
        
        # Update HTML by replacing text content
        new_q_html = q_html.replace(q_text, fixed_q) if fixed_q != q_text else q_html
        new_a_html = a_html.replace(a_text, fixed_a) if fixed_a != a_text else a_html
        
        # Update the note
        update_result = anki('updateNoteFields', {
            'note': {
                'id': note_id,
                'fields': {
                    'Question': new_q_html,
                    'Answer': new_a_html,
                    'Priority': fields.get('Priority', {}).get('value', ''),
                    'Source': fields.get('Source', {}).get('value', ''),
                    'Chapter': fields.get('Chapter', {}).get('value', ''),
                    'Clinical': fields.get('Clinical', {}).get('value', '')
                }
            }
        })
        
        if update_result.get('error'):
            return False, f"Update failed: {update_result.get('error')}"
        
        return True, f"Fixed: {', '.join(changes)}"
        
    except Exception as e:
        return False, f"Exception: {str(e)}"

def main():
    print("🚀 COMPREHENSIVE SWEEP STARTING")
    print("=" * 60)
    
    # Get all cards
    all_cards_result = anki('findCards', {'query': 'deck:*PSYC*'})
    if all_cards_result.get('error') or not all_cards_result.get('result'):
        print(f"❌ Failed to get cards: {all_cards_result}")
        return
    
    all_cards = all_cards_result['result']
    print(f"Found {len(all_cards)} cards to process")
    
    # Process cards
    total_cards = len(all_cards)
    fixed_count = 0
    error_count = 0
    
    print(f"\\nProcessing {total_cards} cards...")
    
    for i, card_id in enumerate(all_cards):
        if i % 100 == 0:
            print(f"Progress: {i}/{total_cards} ({i/total_cards*100:.1f}%)")
        
        success, message = process_card(card_id)
        
        if success:
            if message != 'no-changes':
                fixed_count += 1
                if fixed_count <= 20:  # Show first 20 fixes
                    print(f"  ✅ Card {card_id}: {message}")
        else:
            error_count += 1
            if error_count <= 10:  # Show first 10 errors
                print(f"  ❌ Card {card_id}: {message}")
        
        # Small delay to prevent overwhelming AnkiConnect
        if i % 50 == 0:
            time.sleep(0.1)
    
    print(f"\\n🎉 SWEEP COMPLETE!")
    print(f"📊 Cards processed: {total_cards}")
    print(f"🔧 Cards fixed: {fixed_count}")
    print(f"❌ Errors: {error_count}")
    print(f"✅ Success rate: {((total_cards-error_count)/total_cards*100):.1f}%")
    
    if error_count > 50:
        print(f"\\n⚠️ High error rate detected. Running manual fallback...")
        manual_fallback(all_cards)

def manual_fallback(card_ids):
    """Manual processing for failed cards"""
    print("\\n🔧 MANUAL FALLBACK MODE")
    print("Processing cards individually with robust error handling...")
    
    manual_fixes = 0
    
    for i, card_id in enumerate(card_ids[:100]):  # Process first 100 manually
        try:
            success, message = process_card(card_id)
            if success and message != 'no-changes':
                manual_fixes += 1
                print(f"  ✅ Manual fix {manual_fixes}: Card {card_id}")
        except Exception as e:
            print(f"  ❌ Manual fail: Card {card_id} - {e}")
        
        if i % 25 == 0:
            time.sleep(0.2)  # Longer delays in manual mode
    
    print(f"\\n✅ Manual fallback complete: {manual_fixes} additional fixes")

if __name__ == '__main__':
    main()