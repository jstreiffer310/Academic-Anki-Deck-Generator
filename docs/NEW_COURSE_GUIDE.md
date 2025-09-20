# Adding New Courses - Quick Guide

## Step 1: Create Course Structure

```bash
python course_setup.py create YOUR_COURSE_CODE "Course Name" "Semester Year"
```

**Example:**
```bash
python course_setup.py create PSYC3100 "Cognitive Psychology" "Fall 2024"
```

## Step 2: Add Course Materials

Navigate to `courses/YOUR_COURSE_CODE/` and add:

- **Textbooks:** `content/textbook/` (PDFs)
- **Lectures:** `content/lectures/` (transcripts, recordings)
- **Materials:** `content/course-materials/` (handouts, notes)

## Step 3: Configure Course Settings

Edit `course_config.json`:

```json
{
  "course_code": "YOUR_COURSE",
  "course_name": "Full Course Name",
  "target_count": 200,
  "clinical_examples": false
}
```

## Step 4: Generate Cards

Use shared tools:

```bash
# Extract content from textbook
python shared/tools/smart_content_fixer.py

# Clean and optimize cards
python shared/tools/css_cleaner.py
python shared/tools/corruption_fixer.py
```

## Step 5: Export Decks

Generated decks will be saved in:
- `courses/YOUR_COURSE/decks/`

## Available Templates

- **Basic Course:** Standard structure for most classes
- **Psychology Course:** Adapted from PSYC2240 with clinical focus
- **Science Course:** STEM-focused with formula cards
- **Humanities Course:** Text-heavy with essay prompts

## Shared Resources

All courses can use:
- `shared/tools/` - Generic Anki management tools
- `shared/scripts/` - PowerShell automation scripts
- `templates/` - Course structure templates

## Example Course Structure

```
courses/PSYC3100/
├── content/
│   ├── textbook/cognitive_psychology.pdf
│   ├── lectures/week1_transcript.txt
│   └── course-materials/syllabus.pdf
├── decks/
│   └── PSYC3100_Complete_Deck.csv
├── tools/
│   └── course_specific_extractor.py
└── course_config.json
```