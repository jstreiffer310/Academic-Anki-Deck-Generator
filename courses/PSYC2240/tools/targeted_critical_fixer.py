"""
TARGETED CRITICAL CARD FIXER
Fix the specific problematic cards you identified by targeting their exact IDs
"""

import requests
import json
import re

def request_anki(action, params=None):
    """Send request to AnkiConnect"""
    payload = {
        "action": action,
        "version": 6,
        "params": params or {}
    }
    
    try:
        response = requests.post("http://127.0.0.1:8765", json=payload, timeout=15)
        result = response.json()
        return result
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def extract_text_between_divs(html_content):
    """Extract text between <div class='front'> and <div class='back'> tags"""
    if not html_content:
        return ""
    
    # Look for content between div tags
    patterns = [
        r'<div class=["\']front["\'][^>]*>(.*?)<div class=["\']back["\']',
        r'<div class=["\']back["\'][^>]*>(.*?)</div>',
        r'<div[^>]*class=["\'][^"\']*question[^"\']*["\'][^>]*>(.*?)</div>',
        r'<div[^>]*class=["\'][^"\']*answer[^"\']*["\'][^>]*>(.*?)</div>',
        r'<div[^>]*>(.*?)</div>'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
        if matches:
            # Clean the first match
            text = matches[0]
            # Remove nested HTML tags
            text = re.sub(r'<[^>]+>', ' ', text)
            # Clean whitespace
            text = re.sub(r'\\s+', ' ', text).strip()
            if text and len(text) > 10:  # Must be substantial text
                return text
    
    # Fallback: remove all HTML and extract text
    text = re.sub(r'<style>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\\s+', ' ', text).strip()
    return text

def fix_critical_cards():
    """Find and fix the specific critical cards"""
    print("🎯 TARGETED CRITICAL CARD FIXER")
    print("=" * 50)
    
    # Search for cards with problematic content
    searches = [
        ("Flow through neuron", "*flow through*"),
        ("Parcellated cortex", "*parcellated*"),
        ("Ovoid structure", "*ovoid*"),
        ("Cell body center", "*cell body*")
    ]
    
    critical_cards = {}
    
    for description, query in searches:
        result = request_anki("findCards", {"query": query})
        if result and result.get("result"):
            cards = result["result"]
            print(f"🔍 {description}: {len(cards)} cards found")
            critical_cards[description] = cards
    
    # Process each critical card
    fixes_applied = 0
    
    for description, card_ids in critical_cards.items():
        print(f"\\n📋 Processing {description} cards...")
        
        for card_id in card_ids[:3]:  # Limit to first 3 cards per category
            print(f"\\n  🎯 Analyzing card {card_id}")
            
            # Get card info
            card_result = request_anki("cardsInfo", {"cards": [card_id]})
            if not card_result or not card_result.get("result"):
                continue
            
            card_info = card_result["result"][0]
            note_id = card_info.get("note")
            
            # Get note info
            note_result = request_anki("notesInfo", {"notes": [note_id]})
            if not note_result or not note_result.get("result"):
                continue
            
            note_info = note_result["result"][0]
            fields = note_info.get("fields", {})
            
            # Extract current content
            question_html = fields.get("Question", {}).get("value", "")
            answer_html = fields.get("Answer", {}).get("value", "")
            
            question_text = extract_text_between_divs(question_html)
            answer_text = extract_text_between_divs(answer_html)
            
            print(f"    Q: {question_text[:80]}...")
            print(f"    A: {answer_text[:80]}...")
            
            # Determine fixes needed
            new_question = question_text
            new_answer = answer_text
            issues_fixed = []
            
            # CRITICAL FIX 1: Flow through neuron grammar
            if "flow through" in question_text.lower() and "how do" in question_text.lower():
                new_question = "How does neural transmission flow through a neuron?"
                issues_fixed.append("FLOW_GRAMMAR")
            
            # CRITICAL FIX 2: Parcellated cortex
            elif "parcellated" in question_text.lower() and "cerebral cortex" in question_text.lower():
                new_question = "What are the main functional regions of the cerebral cortex?"
                new_answer = "The cerebral cortex is organized into primary motor cortex (voluntary movement), primary somatosensory cortex (touch sensation), visual cortex (vision processing), auditory cortex (hearing processing), and association areas (complex cognitive functions like language, memory, and decision-making)."
                issues_fixed.append("PARCELLATED_CORTEX")
            
            # CRITICAL FIX 3: Ovoid structure incomplete
            elif "ovoid structure" in answer_text.lower() and "cell body" in answer_text.lower():
                if len(answer_text.split()) < 25:  # Very short/incomplete
                    new_answer = "The cell body (soma) is the ovoid structure at the center of the neuron that contains the nucleus and most organelles. It integrates incoming signals from dendrites and generates action potentials that travel down the axon to communicate with other neurons."
                    issues_fixed.append("OVOID_INCOMPLETE")
            
            # General grammar fixes
            elif "how do" in question_text.lower() and "function" in question_text.lower():
                new_question = re.sub(r"How do (.+) function", r"How does \\1 function", question_text, flags=re.IGNORECASE)
                issues_fixed.append("GRAMMAR_HOW_DO")
            
            if not issues_fixed:
                print(f"    ✅ No issues found")
                continue
            
            print(f"    🔧 Issues to fix: {', '.join(issues_fixed)}")
            
            # Apply fixes by replacing content in HTML
            new_question_html = question_html
            new_answer_html = answer_html
            
            if new_question != question_text:
                # Try to replace the text portion while preserving HTML structure
                if question_text in question_html:
                    new_question_html = question_html.replace(question_text, new_question)
                else:
                    # More aggressive replacement
                    # Find content within div tags and replace
                    pattern = r'(<div[^>]*>)(.*?)(</div>)'
                    def replace_div_content(match):
                        if question_text.lower() in match.group(2).lower():
                            return match.group(1) + new_question + match.group(3)
                        return match.group(0)
                    
                    new_question_html = re.sub(pattern, replace_div_content, question_html, flags=re.DOTALL | re.IGNORECASE)
            
            if new_answer != answer_text:
                if answer_text in answer_html:
                    new_answer_html = answer_html.replace(answer_text, new_answer)
                else:
                    # More aggressive replacement for answer
                    pattern = r'(<div[^>]*>)(.*?)(</div>)'
                    def replace_div_content(match):
                        if answer_text.lower() in match.group(2).lower():
                            return match.group(1) + new_answer + match.group(3)
                        return match.group(0)
                    
                    new_answer_html = re.sub(pattern, replace_div_content, answer_html, flags=re.DOTALL | re.IGNORECASE)
            
            # Prepare update
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
                print(f"    ✅ FIXED: {', '.join(issues_fixed)}")
                fixes_applied += 1
                
                if any("CRITICAL" in issue or issue in ["FLOW_GRAMMAR", "PARCELLATED_CORTEX", "OVOID_INCOMPLETE"] for issue in issues_fixed):
                    print(f"    🔥 CRITICAL ISSUE RESOLVED!")
            else:
                print(f"    ❌ Fix failed: {update_result}")
    
    print(f"\\n🎉 TARGETED FIX COMPLETE!")
    print(f"🔧 Critical cards fixed: {fixes_applied}")

if __name__ == "__main__":
    fix_critical_cards()