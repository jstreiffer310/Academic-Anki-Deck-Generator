# 🎯 Git-Based Local Setup for PSYC 2240 Study Project

## 🚀 One-Command Setup

**Copy and paste this into PowerShell on your local computer:**

```powershell
# Download and run the setup script
iwr -Uri "https://raw.githubusercontent.com/jstreiffer310/PSYC2240-Anki-Deck-Generator/main/setup-local-project.ps1" -OutFile "setup-local-project.ps1"; .\setup-local-project.ps1
```

**That's it!** The script will:
- ✅ Clone the repository
- ✅ Extract only the essential study files
- ✅ Set up VS Code workspace
- ✅ Create clean project structure
- ✅ Configure AnkiConnect for local use

## 🏗️ What Gets Created:

```
📁 PSYC2240-Study/
├── 📁 .vscode/
│   └── settings.json           # AnkiConnect settings
├── 📁 anki-cards/
│   ├── high-priority.md        # Clinical cases
│   ├── medium-priority.md      # Core concepts  
│   ├── low-priority.md         # Background facts
│   ├── cloze-cards.md         # Context cards
│   └── SETUP_GUIDE.md         # Quick reference
├── 📁 study-deck/
│   ├── PSYC2240_Consolidated_Deck.apkg    # 829 cards
│   └── FSRS_SETUP_GUIDE.md              # Exam settings
├── 📁 docs/
│   └── CREATE_LOCAL_PROJECT.md
├── PSYC2240-Study.code-workspace         # VS Code workspace
├── QUICK_START.md                        # Next steps guide
└── README.md                             # Project overview
```

## 🎯 Alternative: Manual Git Commands

If you prefer manual control:

```bash
# Create project folder
mkdir ~/Documents/PSYC2240-Study
cd ~/Documents/PSYC2240-Study

# Clone with sparse checkout (only essential files)
git clone --filter=blob:none --sparse https://github.com/jstreiffer310/PSYC2240-Anki-Deck-Generator.git
cd PSYC2240-Anki-Deck-Generator

# Configure sparse checkout for essential files only
git sparse-checkout set .vscode anki-cards output README.md

# Move files to clean structure
cd ..
mkdir study-workspace
cp -r PSYC2240-Anki-Deck-Generator/.vscode study-workspace/
cp -r PSYC2240-Anki-Deck-Generator/anki-cards study-workspace/
cp -r PSYC2240-Anki-Deck-Generator/output study-workspace/study-deck
cp PSYC2240-Anki-Deck-Generator/README.md study-workspace/

# Open in VS Code
cd study-workspace
code .
```

## 🎮 Quick Start After Setup:

1. **📥 Import Deck**: Double-click `study-deck/PSYC2240_Consolidated_Deck.apkg`
2. **⚙️ Configure FSRS**: Follow `study-deck/FSRS_SETUP_GUIDE.md`  
3. **🔧 Open VS Code**: Double-click `PSYC2240-Study.code-workspace`
4. **🔌 Install Extension**: Accept prompt to install "Anki for VSCode"

## 🎯 Ready to Study!

- **829 optimized flashcards** ready for import
- **VS Code integration** for creating supplemental cards
- **FSRS optimization** for October 8th exam timeline
- **Clean, focused workspace** with no extra files

**Your local study environment will be completely independent and ready to go!**
   - VS Code will prompt you

4. **Update Settings** (already configured)
   - Settings are in `.vscode/settings.json`
   - Should work with localhost automatically

5. **Test Integration**
   - Open `test-cards.md`
   - Ctrl+Shift+P → "Anki: Send to Deck"
   - Should work perfectly!

### VS Code Settings (Local):
```json
{
    "anki.api.hostname": "127.0.0.1",
    "anki.api.port": 8765,
    "anki.api.schema": "http"
}
```

## 🎯 Benefits of Local Setup:
- ✅ Direct AnkiConnect access
- ✅ Faster performance
- ✅ No network issues
- ✅ Full integration works

## 📚 Your Study Workflow:
1. **Main deck**: Import `output/PSYC2240_Consolidated_Deck.apkg` (829 cards)
2. **Supplemental**: Use VS Code integration for additional cards
3. **October 8th**: You're fully prepared!