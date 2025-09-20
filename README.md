# Academic Anki Deck Generator

A comprehensive, multi-class flashcard generation system that transforms course materials into optimized Anki decks. Originally designed for PSYC 2240, now supports unlimited courses with organized deck generation.

## Repository Structure

```
├── courses/                    # All class-specific content
│   ├── PSYC2240/              # Psychology 2240: Biological Basis of Behaviour
│   │   ├── content/           # Course materials (textbooks, lectures)
│   │   ├── decks/             # Generated Anki decks
│   │   ├── tools/             # Course-specific tools
│   │   ├── source/            # Source materials and extracts
│   │   └── output/            # Generated outputs
│   └── [ANY_COURSE]/          # Template for unlimited courses
├── shared/                     # Cross-course utilities
│   ├── tools/                 # Generic Anki tools
│   └── scripts/               # Shared PowerShell scripts
├── templates/                  # Templates for new courses
└── docs/                      # Documentation and guides
```

## ✨ Key Features

- **Multi-Course Support** - Unlimited courses with organized structure
- **Memory Optimization** - Cards designed for maximum retention
- **Automated Generation** - Transform textbooks and lectures into cards
- **Quality Assurance** - Built-in validation and corruption detection
- **Template System** - Standardized setup for new courses
- **Cross-Platform** - Windows, macOS, Linux support

## Adding a New Course

1. **Copy the template:**
   ```bash
   cp -r templates/course-template courses/YOUR_COURSE_CODE
   ```

2. **Add your course materials:**
   - Place textbooks/PDFs in `courses/YOUR_COURSE_CODE/content/`
   - Add lecture transcripts to `content/lectures/`
   - Update course-specific information

3. **Use shared tools:**
   - Leverage `shared/tools/` for generic Anki operations
   - Adapt tools from existing courses as needed

## Existing Courses

### PSYC 2240 - Biological Basis of Behaviour
- **Status:** Fully implemented with 585+ optimized cards
- **Content:** Neuroanatomy, brain disorders, cognitive processes
- **Tools:** PDF analysis, content optimization, corruption fixing

## 🚀 Quick Start (PSYC 2240)

### Ready-to-Use Decks
Import the pre-built CSV files directly into Anki:

```
courses/PSYC2240/decks/PSYC2240_Complete_AnkiDeck.csv       # Main study cards
decks/PSYC2240_Complete_Cloze_Cards.csv   # Cloze deletion cards
```

**Total Cards**: 585+ optimized for memory retention and exam success.

## 📊 Current Deck Status

| Component | Cards | Description |
|-----------|-------|-------------|
| **Main Deck** | 400+ | Question-format cards with functional answers |
| **Cloze Cards** | 185+ | Context-preserving fill-in-the-blank cards |
| **Total Coverage** | **585+** | Complete PSYC 2240 course material |

## 📁 Repository Structure

```
Academic-Anki-Deck-Generator/
├── 📦 courses/                 # ALL COURSE CONTENT
│   └── PSYC2240/              # Example course (Psychology)
│       ├── decks/             # Ready-to-use Anki decks
│       ├── content/           # Course materials
│       └── tools/             # Course-specific tools
├── 🛠️ shared/                  # SHARED UTILITIES
│   ├── tools/                 # Generic Anki tools
│   └── scripts/               # PowerShell automation
├── 📋 templates/               # COURSE TEMPLATES
└── 📖 docs/                   # DOCUMENTATION
│   ├── comprehensive_content_extractor.py # Content extraction
│   ├── rebuild_consolidated_deck.py       # Deck rebuilder
│   └── audio_transcript_analyzer.py       # Transcript analysis
├── 📚 content/                 # SOURCE MATERIALS
│   ├── course-materials/       # Lectures and course content
│   ├── lectures/              # Audio transcripts
│   └── textbook/              # Extracted textbook content
├── 📋 anki-cards/             # CARD TEMPLATES & EXAMPLES
│   ├── high-priority.md       # Critical concept examples
│   ├── medium-priority.md     # Core terminology examples
│   ├── low-priority.md        # Supporting detail examples
│   └── cloze-cards.md         # Context cloze examples
├── 🎯 output/                 # GENERATED PACKAGES
│   └── PSYC2240_Consolidated_Deck.apkg   # Complete Anki package
├── 📄 scripts/                # POWERSHELL UTILITIES
│   ├── extract_chapters.ps1   # Chapter extraction
│   ├── extract_content.ps1    # Content processing
│   └── deck_management.ps1    # Deck utilities
└── � source/                 # RAW EXPORTS
    └── textbook_full_content.txt          # Source textbook content
```

## 🎯 How to Use

### For Studying (Recommended)
1. **Import CSV files**:
   - Main deck: `decks/PSYC2240_Complete_AnkiDeck.csv`
   - Cloze cards: `decks/PSYC2240_Complete_Cloze_Cards.csv`
2. **Follow import guide**: `decks/COMPLETE_IMPORT_GUIDE.md`
3. **Configure study settings**: Use FSRS algorithm for optimal retention
4. **Start studying**: Cards optimized for memory retention

### For Development/Maintenance
1. **Card Quality**: Use `tools/comprehensive_card_searcher.py` to find and fix issues
2. **Content Extraction**: Use `tools/comprehensive_content_extractor.py` for new content
3. **Deck Rebuilding**: Use `tools/rebuild_consolidated_deck.py` to regenerate packages

## 🧠 Card Optimization Features

- **Question Format**: Functional questions ("What does X do?") vs definitions
- **Concise Answers**: 1-2 sentences for optimal memory retention
- **Clinical Focus**: Real-world applications and case studies
- **Context Preservation**: Cloze cards maintain textbook context
- **Quality Verified**: All cards checked for clarity and completeness

## 🔧 Technical Details

### Working Tools (Keep)
- `comprehensive_card_searcher.py` - Mass card quality improvement
- `comprehensive_content_extractor.py` - Multi-source content extraction
- `rebuild_consolidated_deck.py` - Native Anki package generation
- `audio_transcript_analyzer.py` - Lecture transcript processing

### Dependencies
- **Python**: requests, genanki (for package generation)
- **PowerShell**: For Windows-based content extraction
- **Anki**: Desktop application for importing and studying

## 📈 Success Metrics

- **Cards Created**: 585+ high-quality flashcards
- **Quality Score**: All cards verified for clarity and completeness
- **Format Consistency**: Standardized CSV format for reliable import
- **Memory Optimization**: Question-answer format proven for retention

## 🎓 Study Recommendations

1. **Daily Reviews**: Use Anki's spaced repetition algorithm
2. **Focus Areas**: Prioritize cards tagged with clinical examples
3. **Integration**: Combine with lecture notes and textbook reading
4. **Tracking**: Monitor retention rates and adjust study schedule

**Ready to master PSYC 2240! 🧠📚**

*Last updated: Repository cleaned and optimized - all tools working, 585+ cards ready for study*