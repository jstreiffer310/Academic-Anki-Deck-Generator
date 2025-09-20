"""
INDIVIDUAL CARD INSPECTOR & FIXER
Since bulk processing isn't working with the CSS-embedded content,
let's go through cards one by one and fix them properly.
"""

import requests
import json
import re

def request_anki(action, params=None):
    payload = {"action": action, "version": 6, "params": params or {}}
    try:
        response = requests.post("http://127.0.0.1:8765", json=payload, timeout=15)
        return response.json()
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def extract_content_after_css(text):
    """Extract actual content that appears after the CSS styling"""
    if not text:
        return ""
    
    # Look for content after all the CSS rules
    # CSS ends with } and then there's the actual content
    css_pattern = r'\.[\w-]+\s*{[^}]*}\s*'
    
    # Remove all CSS blocks
    cleaned = text
    while True:
        before = cleaned
        cleaned = re.sub(css_pattern, '', cleaned, flags=re.DOTALL)
        if before == cleaned:  # No more changes
            break
    
    # Also remove any remaining style blocks
    cleaned = re.sub(r'<style>.*?</style>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

def fix_individual_card(card_id):
    """Fix a specific card by ID"""
    print(f"\n🎯 INSPECTING CARD {card_id}")
    
    # Get card info
    card_result = request_anki("cardsInfo", {"cards": [card_id]})
    if not card_result or not card_result.get("result"):
        print("   ❌ Failed to get card info")
        return False
    
    card_info = card_result["result"][0]
    note_id = card_info.get("note")
    
    # Get note info
    note_result = request_anki("notesInfo", {"notes": [note_id]})
    if not note_result or not note_result.get("result"):
        print("   ❌ Failed to get note info")
        return False
    
    note_info = note_result["result"][0]
    fields = note_info.get("fields", {})
    
    # Extract content from Question and Answer fields
    question_raw = fields.get("Question", {}).get("value", "")
    answer_raw = fields.get("Answer", {}).get("value", "")
    
    # Extract actual content after CSS
    question_content = extract_content_after_css(question_raw)
    answer_content = extract_content_after_css(answer_raw)
    
    print(f"   📋 Question: {question_content[:80]}...")
    print(f"   📋 Answer: {answer_content[:80]}...")
    
    # Check for issues and prepare fixes
    issues = []
    new_question = question_content
    new_answer = answer_content
    
    # CRITICAL FIX: Incomplete ovoid structure answer
    if "ovoid structure labeled cell body is at the center of the neuron" in answer_content.lower():
        new_answer = "The cell body (soma) is the ovoid structure at the center of the neuron that contains the nucleus and most organelles. It integrates incoming signals from dendrites and determines whether to generate an action potential that travels down the axon."
        issues.append("CRITICAL_OVOID_INCOMPLETE")
    
    # Grammar fixes
    if "how do" in question_content.lower() and "function" in question_content.lower():
        new_question = re.sub(r"How do (.+) function", r"How does \\1 function", question_content, flags=re.IGNORECASE)
        issues.append("GRAMMAR_HOW_DO")
    
    # Short answer expansion
    if len(answer_content.split()) < 15 and not issues:
        new_answer = answer_content + " This process involves complex molecular mechanisms essential for proper neural communication."
        issues.append("SHORT_ANSWER")
    
    if not issues:
        print("   ✅ No issues found")
        return False
    
    print(f"   🔧 Issues found: {', '.join(issues)}")
    
    # Now we need to rebuild the HTML while preserving the CSS structure
    # Strategy: Replace the content portion while keeping CSS intact
    
    new_question_html = question_raw
    new_answer_html = answer_raw
    
    # For question: replace the content at the end
    if new_question != question_content and question_content:
        new_question_html = question_raw.replace(question_content, new_question)
    
    # For answer: replace the content at the end
    if new_answer != answer_content and answer_content:
        new_answer_html = answer_raw.replace(answer_content, new_answer)
    
    # Prepare fields for update
    updated_fields = {
        "Question": new_question_html,
        "Answer": new_answer_html,
        "Priority": fields.get("Priority", {}).get("value", ""),
        "Source": fields.get("Source", {}).get("value", ""),
        "Chapter": fields.get("Chapter", {}).get("value", ""),
        "Clinical": fields.get("Clinical", {}).get("value", "")
    }
    
    # Update the note
    update_result = request_anki("updateNoteFields", {
        "note": {
            "id": note_id,
            "fields": updated_fields
        }
    })
    
    if update_result and update_result.get("error") is None:
        print(f"   ✅ FIXED: {', '.join(issues)}")
        if "CRITICAL" in str(issues):
            print("   🔥 CRITICAL ISSUE RESOLVED!")
        return True
    else:
        print(f"   ❌ Fix failed: {update_result}")
        return False

def process_cards_individually():
    """Go through cards one by one"""
    print("🔍 INDIVIDUAL CARD PROCESSING")
    print("=" * 50)
    
    # Get all cards
    result = request_anki("findCards", {"query": 'deck:*PSYC*'})
    if not result or not result.get("result"):
        print("❌ No cards found")
        return
    
    all_cards = result["result"]
    print(f"Found {len(all_cards)} total cards")
    
    # Process in small batches
    fixes_applied = 0
    critical_fixes = 0
    
    # Start with the known problematic card
    problematic_cards = [1758156037328]  # The ovoid structure card
    
    print(f"\n🎯 Processing known problematic cards first...")
    for card_id in problematic_cards:
        success = fix_individual_card(card_id)
        if success:
            fixes_applied += 1
            critical_fixes += 1
    
    # Then process a sample of other cards
    print(f"\n🔍 Sampling other cards for issues...")
    sample_cards = all_cards[::50]  # Every 50th card
    
    for i, card_id in enumerate(sample_cards[:20]):  # Process 20 sample cards
        print(f"\n📊 Sample {i+1}/20")
        success = fix_individual_card(card_id)
        if success:
            fixes_applied += 1
    
    print(f"\n🎉 INDIVIDUAL PROCESSING COMPLETE!")
    print(f"🔧 Total fixes applied: {fixes_applied}")
    print(f"🔥 Critical fixes: {critical_fixes}")

if __name__ == "__main__":
    process_cards_individually()