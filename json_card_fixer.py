#!/usr/bin/env python3
"""
JSON-based Anki Card Fixer using proper VS Code extension format
"""

import requests
import json

def send_cards_via_ankiconnect():
    """Send properly formatted cards using AnkiConnect"""
    url = "http://127.0.0.1:8765"
    
    # Cards with proper memory retention principles
    cards = [
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "What characterizes locked-in syndrome?",
                "Back": "Patient is aware and conscious but cannot move or speak (only eye movements possible)."
            },
            "tags": ["PSYC2240", "high-priority", "clinical", "brainstem"]
        },
        {
            "deckName": "PSYC 2240", 
            "modelName": "Basic",
            "fields": {
                "Front": "What is the primary function of the cerebellum?",
                "Back": "Coordinates voluntary movements and maintains balance and posture."
            },
            "tags": ["PSYC2240", "high-priority", "cerebellum", "motor-control"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic", 
            "fields": {
                "Front": "How does the frontal lobe control executive functions?",
                "Back": "Plans complex behaviors, makes decisions, and controls working memory processes."
            },
            "tags": ["PSYC2240", "high-priority", "frontal-lobe", "executive-function"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "What happens during REM sleep?", 
                "Back": "Rapid eye movements, vivid dreams, and memory consolidation occur while muscles are paralyzed."
            },
            "tags": ["PSYC2240", "medium-priority", "sleep", "memory"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "How do neurotransmitters communicate between neurons?",
                "Back": "Chemical messengers cross synapses to bind with receptors on postsynaptic neurons."
            },
            "tags": ["PSYC2240", "medium-priority", "neurotransmitters", "synapses"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "What is the role of the hippocampus in memory?",
                "Back": "Converts short-term memories into long-term declarative memories and supports spatial navigation."
            },
            "tags": ["PSYC2240", "high-priority", "hippocampus", "memory"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "How does the autonomic nervous system function?",
                "Back": "Controls involuntary bodily functions through sympathetic (fight/flight) and parasympathetic (rest/digest) divisions."
            },
            "tags": ["PSYC2240", "medium-priority", "autonomic", "nervous-system"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic", 
            "fields": {
                "Front": "What characterizes Alzheimer's disease?",
                "Back": "Progressive memory loss due to amyloid plaques and neurofibrillary tangles destroying brain tissue."
            },
            "tags": ["PSYC2240", "high-priority", "clinical", "alzheimer"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "How does the visual cortex process information?",
                "Back": "Primary visual cortex detects basic features (lines, edges) while higher areas recognize objects and faces."
            },
            "tags": ["PSYC2240", "medium-priority", "visual-cortex", "perception"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "What is the function of the amygdala?",
                "Back": "Processes emotions, especially fear responses, and forms emotional memories."
            },
            "tags": ["PSYC2240", "high-priority", "amygdala", "emotion"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "How do action potentials propagate?",
                "Back": "Electrical impulses travel down axons through depolarization and repolarization cycles."
            },
            "tags": ["PSYC2240", "medium-priority", "action-potential", "neurons"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "What distinguishes white matter from gray matter?",
                "Back": "White matter contains myelinated axons for communication; gray matter contains cell bodies for processing."
            },
            "tags": ["PSYC2240", "medium-priority", "brain-structure", "anatomy"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic", 
            "fields": {
                "Front": "How does the corpus callosum function?",
                "Back": "Connects left and right brain hemispheres, allowing interhemispheric communication."
            },
            "tags": ["PSYC2240", "medium-priority", "corpus-callosum", "brain-communication"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "What is the blood-brain barrier?",
                "Back": "Selective barrier that protects the brain by filtering substances from blood circulation."
            },
            "tags": ["PSYC2240", "low-priority", "blood-brain-barrier", "protection"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "How does neuroplasticity work?",
                "Back": "Brain's ability to reorganize and form new neural connections throughout life in response to experience."
            },
            "tags": ["PSYC2240", "high-priority", "neuroplasticity", "learning"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "What triggers neurotransmitter release?",
                "Back": "Calcium influx at axon terminals when action potentials reach synaptic endings."
            },
            "tags": ["PSYC2240", "medium-priority", "neurotransmitter-release", "calcium"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "How does the reticular formation function?",
                "Back": "Controls arousal, sleep-wake cycles, and filters sensory information for attention."
            },
            "tags": ["PSYC2240", "medium-priority", "reticular-formation", "arousal"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "What is the role of glial cells?",
                "Back": "Support neurons by providing nutrients, maintaining homeostasis, and forming myelin sheaths."
            },
            "tags": ["PSYC2240", "low-priority", "glial-cells", "support"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "How does long-term potentiation work?",
                "Back": "Strengthening of synaptic connections through repeated stimulation, forming basis of learning and memory."
            },
            "tags": ["PSYC2240", "high-priority", "LTP", "synaptic-plasticity"]
        },
        {
            "deckName": "PSYC 2240",
            "modelName": "Basic",
            "fields": {
                "Front": "What characterizes hemispheric specialization?",
                "Back": "Left hemisphere typically handles language and logic; right hemisphere processes spatial and creative tasks."
            },
            "tags": ["PSYC2240", "medium-priority", "hemispheric-specialization", "lateralization"]
        }
    ]
    
    print("🚀 Adding properly formatted cards to Anki...")
    print("=" * 50)
    
    added_count = 0
    
    for i, card in enumerate(cards, 1):
        print(f"📝 Adding card {i}/{len(cards)}: {card['fields']['Front'][:50]}...")
        
        # Add note via AnkiConnect
        response = requests.post(url, json={
            "action": "addNote",
            "version": 6,
            "params": {
                "note": card
            }
        })
        
        result = response.json()
        if result.get("error"):
            print(f"   ❌ Error: {result['error']}")
        else:
            print(f"   ✅ Added successfully!")
            added_count += 1
    
    print(f"\n🎉 COMPLETE!")
    print(f"✅ Successfully added: {added_count}/{len(cards)} cards")
    print(f"🎯 All cards use proper memory retention principles:")
    print(f"   • Question format (What/How/Why)")
    print(f"   • Concise answers (1-2 sentences)")
    print(f"   • Function-focused rather than definition-based")
    print(f"   • Priority-tagged for study organization")
    
    return added_count

def main():
    """Main execution"""
    print("🎯 JSON-BASED ANKI CARD FIXER")
    print("Using proper VS Code extension format with memory optimization")
    print("=" * 60)
    
    # Test connection first
    try:
        response = requests.post("http://127.0.0.1:8765", json={
            "action": "deckNames",
            "version": 6
        })
        if response.json().get("error"):
            print("❌ AnkiConnect not available - make sure Anki is running!")
            return
        print("✅ AnkiConnect connected successfully")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    # Add cards
    added_count = send_cards_via_ankiconnect()
    
    if added_count > 0:
        print(f"\n🎯 SUCCESS! Added {added_count} properly formatted cards to your deck!")
        print("Your cards now follow memory retention best practices and are ready for studying!")
    else:
        print("\n❌ No cards were added. Check Anki connection and deck settings.")

if __name__ == "__main__":
    main()