# 🚀 Quick Setup Guide for Anki + VSCode Integration

## ✅ Prerequisites Checklist

- [ ] **Anki Desktop** installed and running
- [ ] **AnkiConnect addon** installed (code: `2055492159`)  
- [ ] **VS Code extensions** installed:
  - [ ] Anki for VSCode
  - [ ] Anki Editor  
  - [ ] Anki Sidebar (optional)
- [ ] **PSYC 2240 deck** imported (`PSYC2240_Consolidated_Deck.apkg`)

## 🧪 Quick Test

1. **Start Anki** (keep it running)
2. **Test connection** from terminal:
   ```bash
   python3 test_anki_connection.py
   ```
3. **Create a test card** in VSCode:
   ```markdown
   ## Test Question
   
   Test answer to verify integration works.
   
   [#test]() [#PSYC2240]()
   ```

## 📁 Directory Structure

```
content/vscode-cards/
├── high-priority/        → Clinical cases, exam-critical concepts
├── medium-priority/      → Core terminology, important processes  
├── low-priority/         → Supplementary facts, context details
└── cloze-context/        → Contextual fill-in-the-blank cards
```

## ⚡ Essential Commands

- **Send to Anki:** `Ctrl+Shift+P` → "Anki: Send To Deck"
- **Sync Anki:** `Ctrl+Shift+P` → "Anki: Sync Anki"  
- **Browse Cards:** `Ctrl+Shift+P` → "Anki: Browse"

## 🎯 Card Creation Template

```markdown
## [Question format - what/how/why]

[Concise answer in 1-2 sentences]

[#priority-level]() [#topic]() [#PSYC2240]()
```

**Example:**
```markdown  
## What is the function of the hippocampus?

Forms new declarative memories and spatial navigation maps.

[#high-priority]() [#hippocampus]() [#memory]()
```

## 🔧 VSCode Settings Configuration

Add to your VSCode settings.json (`Ctrl+Shift+P` → "Preferences: Open Settings (JSON)"):

```json
{
    "anki.defaultDeck": "PSYC 2240 - Supplemental",
    "anki.md.createTagForTitle": true,
    "anki.template": "BasicWithHighlightVSCode", 
    "anki.saveStrategy": "useDirStructure",
    "anki.api.hostname": "127.0.0.1",
    "anki.api.port": 8765,
    "anki.api.schema": "http"
}
```

## 🔧 Troubleshooting

**AnkiConnect not working?**
- Restart Anki
- Check http://localhost:8765 shows "AnkiConnect v.5"
- Allow firewall access (Windows)

**Cards not in right deck?**  
- Check deck names match exactly
- Use Anki browser to move cards manually

## 📚 Integration with Existing Deck

**Your main deck (829 cards):**
- Use for primary studying
- FSRS optimized for October 8th exam

**VSCode cards (supplemental):**
- Create 5-10 new cards weekly  
- Focus on gaps in understanding
- Merge with main deck before exam if desired

**Ready to start? Open any `.md` file and begin creating cards! 🧠**