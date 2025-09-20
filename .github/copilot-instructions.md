# Academic Anki Deck Generator - AI Instructions

## Project Overview
Multi-class educational flashcard generator that transforms course materials into optimized Anki CSV decks. Originally designed for PSYC 2240 (Biological Basis of Behaviour), now supports unlimited courses with scalable architecture. The project emphasizes memory-retention principles over simple term-definition cards.

## Key Architecture Patterns

### Card Optimization Philosophy
- **Question format** over term-definition: `"What does the cerebellum do?"` vs `"Cerebellum"`
- **Functional focus**: Emphasize what structures/concepts DO, not just definitions
- **Concise answers**: 1-2 sentences max for better memorization
- **Context preservation**: Cloze cards maintain textbook context while testing recall

### File Structure & Data Flow
```
courses/[COURSE_CODE]/content/ → shared/tools/ → courses/[COURSE_CODE]/decks/
```
1. **courses/**: Course-specific content organized by course code
2. **shared/**: Cross-course utilities and PowerShell tools
3. **templates/**: Standardized course structure templates
4. **docs/**: Multi-class documentation and methodology

### CSV Format Standards
```csv
Front,Back,Tags
"What characterizes locked-in syndrome?","Aware and awake but cannot move or speak (eyes can move)","PSYC2240 Chapter1 Optimized"
```
- **Front**: Always question format, clear and specific
- **Back**: Concise, functional answer
- **Tags**: `PSYC2240 Chapter[X] [CardType]` pattern for organization

## Critical Compatibility Issues

### PowerShell Dependencies
⚠️ **Current scripts require Windows PowerShell** - use `pwsh` (PowerShell Core) for cross-platform compatibility:
- `scripts/setup.ps1`: Status checker and card counter
- `scripts/extract_content.ps1`: XML parsing (hardcoded Windows paths)
- `scripts/extract_chapters.ps1`: Chapter segmentation

### Development Environment
- **Primary**: GitHub Codespaces (Linux environment)
- **Script execution**: Install PowerShell Core via `apt install powershell` or equivalent
- **Path issues**: Scripts contain hardcoded `C:\Users\...` paths - need parameterization

## Content Generation Workflow

### Card Creation Principles
1. **Cross-reference validation**: Terms must appear in BOTH textbook AND lecture materials
2. **Memory optimization**: Follow `docs/anki_creation_prompt.md` guidelines
3. **Chapter organization**: Maintain clear chapter boundaries (1-3 currently covered)
4. **Clinical examples**: Prioritize real-world applications (locked-in syndrome, TBI cases)

### Quality Assurance
- **Card count tracking**: `setup.ps1` validates deck completeness
- **Format consistency**: CSV structure must match Anki import requirements
- **Tag standardization**: Consistent chapter/topic tagging for study organization

## Development Commands

### Setup & Validation
```bash
# Install PowerShell (if needed)
sudo apt update && sudo apt install -y powershell

# Validate project structure
pwsh scripts/setup.ps1

# Check deck statistics
wc -l decks/*.csv
```

### Content Processing
```bash
# Extract new textbook content (requires path updates)
pwsh scripts/extract_content.ps1

# Process chapter structure
pwsh scripts/extract_chapters.ps1
```

## Integration Points

### Anki Import Process
1. **Main Deck**: Select "Basic" note type, map Field 1→Front, Field 2→Back, Field 3→Tags
2. **Cloze Deck**: Select "Cloze" note type, map Field 1→Text, Field 2→Tags
3. **Validation**: Total cards should match README.md counts (74 main + 47 cloze = 121)

### Content Updates
When adding new chapters or content:
1. Update `source/textbook_full_content.txt`
2. Run extraction scripts with updated parameters
3. Follow existing optimization patterns in `docs/anki_creation_prompt.md`
4. Update README.md card counts and coverage information

## Cross-Platform Considerations
- Replace hardcoded Windows paths with relative/parameterized paths
- Use PowerShell Core (`pwsh`) instead of Windows PowerShell
- Consider bash script alternatives for core functionality
- Ensure CSV files use UTF-8 encoding for international character support

## AI Agent Guidelines
- **Preserve card optimization principles** when modifying content
- **Maintain CSV format consistency** for Anki compatibility
- **Follow chapter organization** patterns when adding content
- **Test script changes** across different platforms (Windows/Linux/macOS)
- **Update documentation** (README.md, docs/) when making structural changes