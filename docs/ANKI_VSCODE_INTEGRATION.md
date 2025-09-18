# Anki for VSCode Integration Guide

## 🚀 Setup Instructions for PSYC 2240

### 1. Install AnkiConnect

AnkiConnect enables VS Code extensions to communicate with Anki through a local server running on port 8765.

1. Open Anki
2. Go to **Tools > Add-ons > Browse & Install**
3. Enter the code: `2055492159`
4. Click **OK** and restart Anki
5. Verify installation by visiting http://localhost:8765 in your browser
   - You should see "AnkiConnect v.5" or higher displayed
6. **Important**: Keep Anki running in the background for VS Code integration to work

**Note for Windows users**: You may see a firewall dialog when starting Anki. Allow the connection for AnkiConnect to function properly.

### Step 2: Configure VSCode Extension Settings
1. In VSCode: **File** → **Preferences** → **Settings**
2. Search for "anki" and configure:

```json
{
    "anki.defaultDeck": "PSYC 2240 - Supplemental",
    "anki.md.createTagForTitle": true,
    "anki.template": "BasicWithHighlightVSCode",
    "anki.saveStrategy": "useDirStructure"
}
```

### Step 3: Create Directory Structure
```
content/
├── vscode-cards/
│   ├── high-priority/
│   │   └── clinical-cases.md
│   ├── medium-priority/
│   │   └── key-concepts.md
│   ├── low-priority/
│   │   └── definitions.md
│   └── cloze-context/
│       └── chapter-content.md
```

## 📝 Card Creation Templates

### High Priority Cards (clinical-cases.md)
```markdown
# High Priority Clinical Cases

## What characterizes locked-in syndrome?

Patient is conscious and aware but cannot move or speak due to brainstem damage. Eye movements typically preserved.

[#high-priority]() [#clinical]() [#PSYC2240]()

## Patient with Broca's aphasia can do what?

Understand speech but cannot produce fluent language - "knows what they want to say but can't say it."

[#high-priority]() [#clinical]() [#language]()

## {{c1::Phineas Gage}} case demonstrated what about brain function?

Frontal lobe damage can dramatically alter personality while preserving basic cognitive functions.

[#high-priority]() [#clinical]() [#frontal-cortex]()
```

### Key Concepts (key-concepts.md)
```markdown
# Medium Priority Concepts

## What is neuroplasticity?

%

The brain's ability to reorganize and form new neural connections throughout life, especially important for recovery after injury.

[#medium-priority]() [#neuroplasticity]() [#PSYC2240]()

## How do neurotransmitters work?

%

Chemical messengers released at synapses that bind to receptors on postsynaptic neurons, causing excitatory or inhibitory effects.

[#medium-priority]() [#neurotransmitters]() [#synapses]()
```

### Definitions (definitions.md)
```markdown
# Low Priority Definitions

## Action potential

Brief electrical signal that travels down an axon when a neuron fires.

[#low-priority]() [#action-potential]() [#PSYC2240]()

## Myelin

Fatty insulation around axons that speeds up neural transmission.

[#low-priority]() [#myelin]() [#neural-transmission]()
```

### Cloze Context (chapter-content.md)
```markdown
# Cloze Context Cards

## Sleep stages involve {{c1::NREM}} and {{c2::REM}} phases

NREM (Non-Rapid Eye Movement) sleep has stages 1-3, while REM sleep is characterized by vivid dreams and memory consolidation.

[#cloze]() [#sleep]() [#PSYC2240]()

## The {{c1::hippocampus}} is crucial for {{c2::declarative memory}} formation

Located in the medial temporal lobe, it processes new information into long-term memory storage.

[#cloze]() [#memory]() [#hippocampus]()
```

## 🎯 Integration Strategy with Existing Deck

### Option 1: Supplemental Deck (Recommended)
Create a separate "PSYC 2240 - Supplemental" deck for new content:

1. **Configure extension** to send to supplemental deck
2. **Use directory structure** to organize by priority
3. **Import regularly** to your main study routine
4. **Merge before exam** if desired

### Option 2: Direct Integration
Send cards directly to your existing 4 decks:

**VSCode Settings for Direct Integration:**
```json
{
    "anki.defaultDeck": "PSYC 2240 - High Priority",
    "anki.saveStrategy": "default"
}
```

**Then manually change deck** based on content priority:
- High Priority → Clinical cases, core concepts
- Medium Priority → Supporting knowledge  
- Low Priority → Background definitions
- Cloze Context → Contextual understanding

## 📅 Daily Workflow Integration

### During Study Sessions:
1. **Read textbook/notes** in your preferred app
2. **Open VSCode** with your markdown files
3. **Add cards as you go:**
   ```markdown
   ## New concept you encounter
   
   Definition or explanation
   
   [#appropriate-priority]() [#topic]() [#PSYC2240]()
   ```
4. **Send to Anki:** `Ctrl+Shift+P` → "Anki: Send To Deck"

### Weekly Maintenance:
1. **Review supplemental deck** cards
2. **Move important cards** to main priority decks
3. **Delete redundant cards** that overlap with main deck
4. **Optimize tags** for better organization

## 🔧 Advanced Configuration

### Custom Tag Patterns
For more sophisticated tagging, create patterns like:

```markdown
## What is the function of the cerebellum?

Balance, coordination, and motor learning - "little brain" fine-tunes movement.

[#high-priority]() [#cerebellum]() [#motor-control]() [#exam-likely]()
```

### Deck Name Mapping
Use directory structure to auto-assign deck names:

```
content/vscode-cards/
├── high-priority/        → "PSYC 2240 - High Priority"  
├── medium-priority/      → "PSYC 2240 - Medium Priority"
├── low-priority/         → "PSYC 2240 - Low Priority"
└── cloze-context/        → "PSYC 2240 - Context Cloze"
```

### Batch Processing
Create multiple cards efficiently:

```markdown
# Chapter 3 Review Session

## What is a synapse?

Connection point between two neurons where neurotransmission occurs.

[#medium-priority]() [#synapse]() [#chapter3]()

## What is synaptic plasticity?

Ability of synapses to strengthen or weaken over time based on activity levels.

[#high-priority]() [#plasticity]() [#chapter3]()

## What is long-term potentiation (LTP)?

Persistent strengthening of synapses based on recent patterns of activity.

[#high-priority]() [#LTP]() [#memory]() [#chapter3]()
```

## 🎯 Best Practices for October 8th Exam

### Priority Guidelines:
- **High Priority:** Clinical cases, key mechanisms, exam-likely content
- **Medium Priority:** Supporting concepts that aid understanding  
- **Low Priority:** Definitions, background information
- **Cloze:** Complex processes that benefit from context

### Time Management:
- **Daily:** 5-10 minutes adding new cards while studying
- **Weekly:** 15-20 minutes organizing and optimizing
- **Don't overdo it:** Supplement, don't replace your main 829-card deck

### Quality Control:
- **Avoid duplicates:** Check if concept exists in main deck first
- **Keep it concise:** Follow the same style as your optimized deck
- **Use consistent tags:** Maintain your existing tagging system

## 🚀 Quick Start Commands

### Essential VSCode Commands:
- `Ctrl+Shift+P` → "Anki: Send To Deck" (main command)
- `Ctrl+Shift+P` → "Anki: Send To Own Deck" (creates deck from file title)
- `Ctrl+Shift+P` → "Anki: Sync Anki" (sync with AnkiWeb)

### File Templates:
Create `.md` files in your content/vscode-cards/ directories and start adding content using the templates above!

## 🧪 Testing the Integration

### Verify AnkiConnect is Working

1. **Start Anki** (must be running for integration to work)
2. **Test the connection**:
   ```bash
   curl http://localhost:8765 -X POST -d '{"action": "deckNames", "version": 5}'
   ```
   - Should return your deck names including "PSYC 2240 - High Priority", etc.
   - If you get a connection error, restart Anki and check firewall settings

3. **Test VS Code Extension**:
   - Open any markdown file in `content/vscode-cards/`
   - Try the "Anki: Send note to Anki" command  
   - Check if the card appears in your Anki collection

### Verify Deck Structure

Your existing PSYC 2240 decks should be organized as:
```
PSYC 2240 - High Priority        (Clinical cases, exam-critical concepts)
PSYC 2240 - Medium Priority      (Core terminology, important processes)  
PSYC 2240 - Low Priority         (Supplementary facts, context details)
PSYC 2240 - Cloze Context        (Contextual fill-in-the-blank cards)
```

### Troubleshooting Common Issues

**AnkiConnect not responding:**
- Restart Anki
- Check http://localhost:8765 shows "AnkiConnect v.5"
- Windows: Allow firewall access for Anki

**Cards not appearing in correct deck:**
- Verify deck names match exactly (case-sensitive)
- Check VS Code extension settings for default deck
- Manually move cards if needed using Anki browser

## 📊 Integration Success Metrics

### Week 1 Goals:
- ✅ AnkiConnect installed and working
- ✅ First 10 supplemental cards created
- ✅ Directory structure established

### Ongoing Success:
- 📈 **5-10 new cards weekly** from active study
- 📈 **Improved understanding** of difficult concepts
- 📈 **Better retention** through active card creation
- 📈 **Exam confidence** from comprehensive coverage

**This integration will make your PSYC 2240 study even more effective! 🧠📚**
