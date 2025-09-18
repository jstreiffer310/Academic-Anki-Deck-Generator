#!/usr/bin/env python3
"""
Verify that Anki cards have been properly fixed
"""

import requests
import random
from bs4 import BeautifulSoup

def verify_card_quality():
    url = "http://127.0.0.1:8765"
    
    print("🔍 Verifying card quality after fixes...")
    
    # Get all PSYC cards
    response = requests.post(url, json={
        "action": "findCards",
        "version": 6,
        "params": {"query": "deck:\"PSYC 2240*\""}
    })
    
    if response.json().get("error"):
        print(f"Error: {response.json()['error']}")
        return
    
    all_cards = response.json()["result"]
    print(f"📚 Total cards found: {len(all_cards)}")
    
    # Sample random cards for verification
    sample_size = min(50, len(all_cards))
    sample_cards = random.sample(all_cards, sample_size)
    
    # Get card details
    response = requests.post(url, json={
        "action": "cardsInfo",
        "version": 6,
        "params": {"cards": sample_cards}
    })
    
    cards = response.json()["result"]
    
    # Analyze quality
    clean_cards = 0
    issues_found = 0
    issue_types = {
        "figure_captions": 0,
        "double_spaces": 0,
        "empty_fields": 0,
        "grammar_issues": 0
    }
    
    print(f"\n📋 Analyzing {len(cards)} sample cards...")
    
    for i, card in enumerate(cards):
        fields = card["fields"]
        question = fields.get("Question", {}).get("value", "")
        answer = fields.get("Answer", {}).get("value", "")
        
        # Clean HTML to analyze text
        q_text = BeautifulSoup(question, 'html.parser').get_text()
        a_text = BeautifulSoup(answer, 'html.parser').get_text()
        
        card_issues = []
        
        # Check for issues
        if "Figure" in q_text or "Figure" in a_text or "Fig." in q_text or "Fig." in a_text:
            card_issues.append("figure_captions")
            issue_types["figure_captions"] += 1
            
        if "  " in q_text or "  " in a_text:
            card_issues.append("double_spaces")
            issue_types["double_spaces"] += 1
            
        if not q_text.strip() or not a_text.strip():
            card_issues.append("empty_fields")
            issue_types["empty_fields"] += 1
            
        if q_text.count("  ") > 0 or a_text.count("  ") > 0:
            card_issues.append("grammar_issues")
            issue_types["grammar_issues"] += 1
        
        if card_issues:
            issues_found += 1
            if issues_found <= 5:  # Show first 5 problematic cards
                print(f"⚠️  Card {i+1} issues: {', '.join(card_issues)}")
                print(f"   Q: {q_text[:100]}...")
                print(f"   A: {a_text[:100]}...")
        else:
            clean_cards += 1
    
    # Summary
    print(f"\n📊 VERIFICATION RESULTS:")
    print(f"✅ Clean cards: {clean_cards}/{len(cards)} ({clean_cards/len(cards)*100:.1f}%)")
    print(f"⚠️  Cards with issues: {issues_found}/{len(cards)} ({issues_found/len(cards)*100:.1f}%)")
    
    if issues_found > 0:
        print(f"\n🔍 Issue breakdown:")
        for issue_type, count in issue_types.items():
            if count > 0:
                print(f"   {issue_type.replace('_', ' ').title()}: {count}")
    
    # Overall assessment
    success_rate = clean_cards / len(cards) * 100
    if success_rate >= 95:
        print(f"\n🎉 EXCELLENT! {success_rate:.1f}% of cards are clean and ready for studying!")
    elif success_rate >= 85:
        print(f"\n✅ GOOD! {success_rate:.1f}% of cards are clean. Minor issues remain.")
    else:
        print(f"\n⚠️  NEEDS MORE WORK! Only {success_rate:.1f}% of cards are clean.")
    
    return success_rate

if __name__ == "__main__":
    verify_card_quality()