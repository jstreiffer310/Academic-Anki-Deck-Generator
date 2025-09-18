# PSYC 2240 Anki Deck Generator

Comprehensive flashcard system for PSYC 2240 (Biological Basis of Behaviour) optimized for memory retention and October 8th exam preparation.

## 🚀 Quick Start

### Option 1: Main Study Deck (Recommended)
```bash
./setup.sh
# Choose option 1 - Main study deck
```

Your 829-card deck is ready to import:
- **File**: `output/PSYC2240_Consolidated_Deck.apkg`
- **Setup Guide**: `output/FSRS_SETUP_GUIDE.md`
- **FSRS Optimized**: Pre-configured for 20-day study timeline

### Option 2: VS Code Integration (Advanced)
```bash
./setup.sh
# Choose option 2 - VS Code integration
```

Create supplemental cards directly from VS Code while studying.

## 📊 Deck Statistics

| Deck | Cards | Focus |
|------|-------|-------|
| **High Priority** | ~250 | Clinical cases, exam-critical concepts |
| **Medium Priority** | ~300 | Core terminology, important processes |
| **Low Priority** | ~200 | Supporting facts, context details |
| **Cloze Context** | ~79 | Fill-in-the-blank with context |
| **Total** | **829** | **Complete PSYC 2240 coverage** |

## 📁 Repository Structure

```
PSYC2240-Anki-Deck-Generator/
├── � setup.sh                  # Main setup script - START HERE
├── �📦 output/                   # Ready-to-use deck files
│   ├── PSYC2240_Consolidated_Deck.apkg  # 829-card study deck
│   └── FSRS_SETUP_GUIDE.md              # Optimization settings
├── 🃏 anki-cards/              # VS Code card templates
│   ├── high-priority.md        # Clinical cases examples
│   ├── medium-priority.md      # Core concepts examples
│   ├── low-priority.md         # Background facts examples
│   ├── cloze-cards.md         # Context cloze examples
│   ├── test-cards.md          # Test file for integration
│   └── SETUP_GUIDE.md         # Card creation guide
├── 📚 content/                 # Source materials
│   ├── course-materials/       # Lectures, textbook, notes
│   ├── lectures/              # Audio transcripts
│   └── textbook/              # Extracted content
├── � setup/                   # Setup and connection scripts
│   ├── connect_to_anki.sh     # Main connection setup
│   ├── test_connection.sh     # Connection tester
│   ├── test_anki_connection.py # Python connection test
│   └── setup_anki_windows.bat # Windows Anki setup
├── � docs/                    # Documentation
│   ├── SIMPLE_TEST_GUIDE.md   # Quick VS Code setup
│   ├── ANKI_VSCODE_INTEGRATION.md # Detailed integration
│   └── CODESPACE_ANKI_SETUP.md # Codespace-specific setup
└── 🛠️ tools/                   # Build scripts
    └── rebuild_consolidated_deck.py # Deck generator
```

## 🎯 Usage Guide

### For Studying (Primary Use)
1. **Run setup**: `./setup.sh` → Option 1
2. **Import deck**: `output/PSYC2240_Consolidated_Deck.apkg` to Anki
3. **Configure FSRS**: Follow `output/FSRS_SETUP_GUIDE.md`
4. **Study daily**: Optimized for October 8th exam

### For Creating Cards (Optional)
1. **Run setup**: `./setup.sh` → Option 2
2. **Follow prompts**: Set up connection to local Anki
3. **Create cards**: Edit files in `anki-cards/` directory
4. **Send to Anki**: Ctrl+Shift+P → "Anki: Send to Deck"

## 📈 Exam Preparation Timeline

- **Week 1-2**: Import main deck, configure FSRS, establish routine
- **Week 3-4**: Daily reviews + optional supplemental cards via VS Code
- **Final Week**: Focus review on weak areas identified by Anki
- **October 8th**: Exam day - you're prepared! 🎯

## 🧠 Memory Optimization Features

- **Question Format**: "What does X do?" vs simple definitions
- **Concise Answers**: 1-2 sentences for optimal retention
- **Clinical Focus**: Real-world applications and case examples
- **FSRS Algorithm**: Scientifically-optimized review scheduling

**Ready to ace PSYC 2240! 🧠📚**

**Start with: `./setup.sh`**