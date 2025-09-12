# PSYC 2240 Anki Deck Generator

## 📚 Biological Basis of Behaviour - Optimized Flashcard Collection

Comprehensive Anki flashcards for **PSYC 2240: Biological Basis of Behaviour** covering Chapters 1-3, optimized for memory retention and effective learning.

## 🎯 **Quick Start**

### Download Ready-to-Use Decks:
- **[Main Deck](decks/PSYC2240_AnkiDeck.csv)** - 74 memory-optimized question-answer cards
- **[Cloze Deck](decks/PSYC2240_Cloze_Cards.csv)** - 47 fill-in-the-blank cards

### Import into Anki:
1. Download the CSV files above
2. Open Anki → File → Import
3. **For Main Deck**: Select Basic note type, map Field 1→Front, Field 2→Back, Field 3→Tags
4. **For Cloze Deck**: Select Cloze note type, map Field 1→Text, Field 2→Tags

## 📊 **Deck Overview**

### 🧠 **Main Deck** (74 cards)
Memory-optimized cards using proven learning principles:
- ✅ Question format (more engaging than term-definition)
- ✅ Concise answers (easier to memorize)
- ✅ Functional focus (what things DO, not just definitions)
- ✅ Clear language (no awkward textbook phrasing)

### 🔤 **Cloze Deck** (47 cards)  
Fill-in-the-blank cards for context-based learning:
- ✅ Multiple deletion points per card
- ✅ Progressive difficulty
- ✅ Context reinforcement

**Total: 121 high-quality study cards**

## 📋 **Content Coverage**

### 🧠 **Chapter 1 - Origins of Brain and Behavior**
- Basic terminology (TBI, neuroplasticity, neurons)
- Historical perspectives (dualism, materialism)
- Evolution and natural selection
- Human brain evolution (hominins, EQ)
- Intelligence and culture

### 🔬 **Chapter 2 - Functional Anatomy**
- Brain lobes and their functions
- Nervous system organization
- Major brain structures (brainstem, limbic system)
- Neural pathways and connections
- Brain protection and circulation

### ⚡ **Chapter 3 - Functional Units**
- Neuron types and structures
- Glial cells and support functions
- Cellular components and genetics
- Molecular biology basics
- Inheritance patterns

## 🗂️ **Repository Structure**

```
📁 decks/
  ├── PSYC2240_AnkiDeck.csv       # Main optimized deck (74 cards)
  └── PSYC2240_Cloze_Cards.csv    # Cloze deletion deck (47 cards)

📁 scripts/
  ├── extract_content.ps1         # Content extraction tools
  ├── extract_chapters.ps1        # Chapter parsing
  └── setup.ps1                   # Quick setup script

📁 source/
  └── textbook_full_content.txt   # Original extracted content

📁 docs/
  ├── anki_creation_prompt.md     # Generation methodology
  └── PSYC2240_Cloze_Summary.txt  # Cloze deck documentation
```

## 🛠️ **Development in Codespaces**

### Launch Codespace:
Click the "Open in GitHub Codespaces" badge above or:
1. Go to the repository on GitHub
2. Click "Code" → "Codespaces" → "Create codespace"

### Available Scripts:
```bash
# Run setup script
pwsh scripts/setup.ps1

# Extract new content
pwsh scripts/extract_content.ps1

# Parse additional chapters
pwsh scripts/extract_chapters.ps1
```

## 🎓 **Study Recommendations**

### **Optimal Study Strategy:**
1. **Start with Main Deck** - Learn core concepts efficiently
2. **Add Cloze Cards** - Test understanding in context
3. **Daily Schedule**: 10-15 new cards, review all due cards
4. **Focus Areas**: Rotate between chapters, prioritize weak areas

### **Anki Settings Recommendations:**
- **New Cards/Day**: 10-15
- **Maximum Reviews**: No limit
- **Graduating Interval**: 1 day
- **Easy Interval**: 4 days
- **Maximum Interval**: 365 days

## 🔄 **Adding New Content**

### For Additional Chapters:
1. Add content to `source/textbook_full_content.txt`
2. Run extraction scripts
3. Follow existing card optimization principles
4. Update this README

### Card Optimization Principles:
- Use question format instead of term-definition
- Keep answers concise (1-2 sentences max)
- Focus on function over pure definition
- Chunk complex information
- Use clear, simple language

## 📈 **Study Progress Tracking**

Track your progress using Anki's built-in statistics:
- **Cards/Day**: Monitor daily completion
- **Retention Rate**: Aim for >90% accuracy
- **Review Time**: Optimize for efficiency
- **Mature Cards**: Build long-term retention

## 🤝 **Contributing**

### To improve existing cards:
1. Fork the repository
2. Make improvements following optimization principles
3. Test with a small group if possible
4. Submit pull request with clear description

### Guidelines:
- Maintain consistent formatting
- Test cards for clarity and accuracy
- Document any major changes
- Follow memory optimization principles

## 📝 **License & Usage**

- **Educational Use**: Free for all students and educators
- **Sharing**: Encouraged! Link to this repository
- **Modifications**: Welcome - please share improvements back

---

**Course**: PSYC 2240 - Biological Basis of Behaviour  
**Coverage**: Chapters 1-3 (Complete)  
**Last Updated**: September 2025  
**Format**: Anki CSV Import  
**Optimization**: Memory-focused design

⭐ **Star this repository if it helps your studies!**
