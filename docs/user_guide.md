# Academic Anki Deck Generator - Complete User Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Course Creation](#course-creation)
3. [Content Processing](#content-processing)
4. [Deck Generation](#deck-generation)
5. [Anki Import](#anki-import)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites
- Python 3.8+ installed
- Anki Desktop application
- Course materials (PDFs, Word docs, transcripts)

### 30-Second Setup
```bash
# 1. Clone and install
git clone https://github.com/jstreiffer310/Academic-Anki-Deck-Generator.git
cd Academic-Anki-Deck-Generator
pip install -r requirements.txt

# 2. Create your course
python tools/course_manager.py create PSYC3100 "Cognitive Psychology" "Fall 2024" --template psychology

# 3. Add your materials to courses/PSYC3100/content/

# 4. Generate deck
cd courses/PSYC3100
python -c "
from shared.core.content_extractor import CourseExtractor
from shared.core.deck_builder import CourseDeckBuilder

extractor = CourseExtractor('.')
content = extractor.extract_all_content()

builder = CourseDeckBuilder('.')
csv_path, apkg_path = builder.build_complete_deck()
print(f'Deck ready: {apkg_path}')
"

# 5. Import the generated .apkg file into Anki
```

## Course Creation

### Available Templates

#### Basic Template
Best for: Standard academic courses
```bash
python tools/course_manager.py create HIST2100 "World History" "Fall 2024" --template basic
```

#### Psychology Template
Best for: Psychology courses with clinical focus
```bash
python tools/course_manager.py create PSYC3200 "Abnormal Psychology" "Fall 2024" --template psychology
```

#### Science Template  
Best for: STEM courses with formulas and equations
```bash
python tools/course_manager.py create CHEM2100 "Organic Chemistry" "Fall 2024" --template science
```

#### Humanities Template
Best for: Text-heavy courses with quotations and themes
```bash
python tools/course_manager.py create ENGL2100 "American Literature" "Fall 2024" --template humanities
```

### Custom Course Configuration

After creation, edit `courses/YOUR_COURSE/config/course_config.json`:

```json
{
  "course_code": "PSYC3100",
  "course_name": "Cognitive Psychology",
  "card_generation": {
    "target_count": 200,
    "question_format": "interrogative",
    "clinical_examples": true,
    "priority_scoring": true
  },
  "content_sources": {
    "textbook": true,
    "lectures": true,
    "clinical_cases": true
  }
}
```

## Content Processing

### Organizing Your Materials

Place materials in the appropriate directories:

```
courses/YOUR_COURSE/content/
├── textbooks/           # PDF textbooks
│   └── cognitive_psych.pdf
├── lectures/            # Lecture transcripts, notes
│   ├── week1_notes.docx
│   ├── lecture1_transcript.txt
│   └── slides.pdf
├── materials/           # Additional materials
│   ├── syllabus.pdf
│   ├── study_guide.docx
│   └── handouts/
└── raw/                 # Unprocessed files
```

### Supported File Formats
- **PDFs**: Textbooks, slides, handouts
- **Word Documents (.docx)**: Lecture notes, study guides
- **Text Files (.txt)**: Transcripts, notes
- **Markdown (.md)**: Documentation, notes

### Content Extraction

#### Basic Extraction
```python
from shared.core.content_extractor import CourseExtractor

# Initialize extractor
extractor = CourseExtractor('courses/YOUR_COURSE')

# Discover all content sources
sources = extractor.discover_content_sources()
print(f"Found sources: {sources}")

# Extract all content
content = extractor.extract_all_content()
print(f"Extracted {len(content['cards'])} cards")
```

#### Advanced Extraction with Custom Rules

Create `courses/YOUR_COURSE/config/extraction_rules.json`:

```json
{
  "custom_patterns": [
    "(?i)remember[:\\-]?\\s*(.+?)(?=\\n|$)",
    "(?i)important[:\\-]?\\s*(.+?)(?=\\n|$)"
  ],
  "exclude_sections": [
    "References",
    "Bibliography", 
    "Index"
  ],
  "priority_keywords": [
    "key concept",
    "important",
    "remember",
    "critical",
    "essential"
  ]
}
```

#### Learning Objectives Focus (LOQ Method)

For courses with explicit learning objectives:

```python
from shared.core.content_extractor import CourseExtractor

extractor = CourseExtractor('courses/YOUR_COURSE')

# Extract content
content = extractor.extract_all_content()

# Focus on learning objectives
objectives = content['learning_objectives']
print(f"Found {len(objectives)} learning objectives")

# Generate cards primarily from objectives
objective_cards = extractor.generate_cards_from_objectives(objectives)
print(f"Generated {len(objective_cards)} objective-based cards")
```

## Deck Generation

### Basic Deck Building

```python
from shared.core.deck_builder import CourseDeckBuilder

# Initialize builder
builder = CourseDeckBuilder('courses/YOUR_COURSE')

# Build complete deck
csv_path, apkg_path = builder.build_complete_deck()

print(f"CSV deck: {csv_path}")
print(f"Anki package: {apkg_path}")
```

### Priority-Based Decks

Generate separate decks for different priority levels:

```python
builder = CourseDeckBuilder('courses/YOUR_COURSE')

# Build priority-separated decks
priority_decks = builder.build_priority_decks()

for priority, (csv_path, apkg_path) in priority_decks.items():
    print(f"{priority.title()} priority: {csv_path}")
```

### Custom Deck Configuration

Modify deck settings in your course config:

```json
{
  "deck_settings": {
    "css_styling": true,
    "enable_cloze": true,
    "split_by_priority": false,
    "max_cards_per_deck": 500
  },
  "card_quality": {
    "min_front_length": 15,
    "max_front_length": 150,
    "remove_duplicates": true,
    "validate_format": true
  },
  "tagging": {
    "format": "{course_code} {chapter} {priority}"
  }
}
```

## Anki Import

### Method 1: Direct Package Import (Recommended)
1. Open Anki Desktop
2. File → Import
3. Select the generated `.apkg` file from `courses/YOUR_COURSE/decks/final/`
4. Click Import

### Method 2: CSV Import
1. Open Anki Desktop  
2. File → Import
3. Select the generated CSV file
4. Configure import settings:
   - **Note Type**: Basic
   - **Field 1**: Front
   - **Field 2**: Back  
   - **Field 3**: Tags
5. Click Import

### Import Validation

After import, verify your deck:
- Check total card count matches the generated summary
- Verify tags are properly applied
- Test a few cards to ensure formatting is correct

## Advanced Features

### Cross-Course Analysis

Compare content across multiple courses:

```python
from shared.core.content_extractor import CourseExtractor

# Analyze multiple courses
courses = ['PSYC2120', 'PSYC2240', 'PSYC3100']
all_content = {}

for course in courses:
    extractor = CourseExtractor(f'courses/{course}')
    all_content[course] = extractor.extract_all_content()

# Find common concepts
common_terms = set()
for course_content in all_content.values():
    for definition in course_content['definitions']:
        common_terms.add(definition[0].lower())

print(f"Common terms across courses: {len(common_terms)}")
```

### Bulk Course Management

```bash
# List all courses
python tools/course_manager.py list courses

# Validate all courses
for course in $(python tools/course_manager.py list courses); do
    python tools/course_manager.py validate $course
done

# Migrate old courses to new structure
python tools/course_manager.py migrate old_psyc2240_path PSYC2240 --template psychology
```

### Custom Content Processors

Create course-specific processors in `courses/YOUR_COURSE/tools/`:

```python
# courses/PSYC3100/tools/cognitive_processor.py
from shared.core.content_extractor import CourseExtractor

class CognitiveExtractor(CourseExtractor):
    def extract_cognitive_models(self, text):
        """Extract cognitive models and theories."""
        models = []
        # Custom extraction logic for cognitive models
        return models
    
    def generate_model_cards(self, models):
        """Generate cards specific to cognitive models."""
        cards = []
        # Custom card generation logic
        return cards
```

### Quality Assurance Pipeline

Set up automated quality checks:

```python
from shared.core.deck_builder import CourseDeckBuilder

builder = CourseDeckBuilder('courses/YOUR_COURSE')

# Load and process cards
content = builder.load_extracted_content()
cards = builder.process_cards(content['cards'])

# Generate quality statistics
stats = builder.generate_deck_statistics(cards)

print(f"Quality Report:")
print(f"  Total cards: {stats['total_cards']}")
print(f"  Average question length: {stats['avg_front_length']}")
print(f"  Average answer length: {stats['avg_back_length']}")
print(f"  Card types: {stats['card_types']}")
```

## Troubleshooting

### Common Issues

#### No Cards Generated
**Problem**: Extraction returns 0 cards
**Solutions**:
1. Check file formats are supported (.pdf, .docx, .txt)
2. Verify content files exist in `content/` directories
3. Check extraction patterns in logs
4. Add custom patterns to `extraction_rules.json`

#### Poor Card Quality
**Problem**: Generated cards are unclear or too long
**Solutions**:
1. Adjust quality filters in course config
2. Modify `min_front_length` and `max_front_length`
3. Add custom extraction patterns for your content
4. Use the psychology template for better question formatting

#### Import Errors
**Problem**: Anki import fails or formats incorrectly
**Solutions**:
1. Use `.apkg` files instead of CSV for better compatibility
2. Check CSV encoding (should be UTF-8)
3. Verify field mapping: Front→Question, Back→Answer, Tags→Tags
4. Remove special characters if import fails

#### Missing Dependencies
**Problem**: Import errors for required packages
**Solutions**:
```bash
# Install all required packages
pip install genanki python-docx PyMuPDF nltk

# For PDF processing issues
pip install --upgrade PyMuPDF

# For Word document issues  
pip install --upgrade python-docx
```

### Debugging Commands

```bash
# Check course structure
python tools/course_manager.py validate YOUR_COURSE

# List available templates
python tools/course_manager.py list templates

# Check Python dependencies
python -c "import genanki, docx, fitz; print('All dependencies OK')"

# Test content extraction
python -c "
from shared.core.content_extractor import CourseExtractor
extractor = CourseExtractor('courses/YOUR_COURSE')
sources = extractor.discover_content_sources()
print('Content sources:', sources)
"
```

### Getting Help

1. **Check Logs**: Look in `courses/YOUR_COURSE/processing/logs/`
2. **Validate Structure**: Run `python tools/course_manager.py validate YOUR_COURSE`
3. **Review Examples**: Check existing courses (PSYC2120, PSYC2240) for working examples
4. **Configuration**: Verify `course_config.json` has required fields

### Performance Optimization

For large courses (500+ pages):
1. Enable chunked processing in config
2. Use smaller target card counts initially
3. Process content in batches by chapter
4. Consider splitting into multiple decks by topic

---

**Need more help?** Check the specific course READMEs in `courses/COURSE_CODE/README.md` for course-specific guidance.