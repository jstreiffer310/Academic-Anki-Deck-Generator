# Course Template

This template provides the standard structure for adding new courses to the Multi-Class Anki Deck Generator.

## Directory Structure

```
PSYC2120/
├── content/                   # Course materials
│   ├── textbook/             # Textbook PDFs and extracted content
│   ├── lectures/             # Lecture transcripts and materials
│   └── course-materials/     # Additional course resources
├── decks/                    # Generated Anki decks (CSV/APKG)
├── tools/                    # Course-specific tools and scripts
├── source/                   # Raw extracts and source data
└── output/                   # Generated outputs and exports
```

## Setup Instructions

1. **Copy this template:**
   ```bash
   cp -r templates/course-template courses/YOUR_COURSE_CODE
   ```

2. **Add course materials:**
   - Place textbook PDFs in `content/textbook/`
   - Add lecture transcripts to `content/lectures/`
   - Include any additional course materials in `content/course-materials/`

3. **Configure course-specific tools:**
   - Adapt tools from `shared/tools/` as needed
   - Create course-specific extraction scripts
   - Modify content generation parameters

4. **Generate decks:**
   - Extract content using shared extraction tools
   - Generate cards following established patterns
   - Optimize for memory retention principles

## File Naming Conventions

- **Decks:** `PSYC2120_[DECK_TYPE]_[DATE].csv`
- **Tools:** `[purpose]_[course_code].py`
- **Content:** `[source_type]_content.txt`

## Course Configuration

Create a `course_config.json` file with:

```json
{
  "course_code": "YOUR_COURSE_CODE",
  "course_name": "Full Course Name",
  "semester": "Fall 2024",
  "textbook_title": "Primary Textbook Title",
  "card_generation": {
    "target_count": 100,
    "question_format": "interrogative",
    "answer_length": "concise"
  }
}
```

## Shared Resources

Leverage these shared tools:
- `shared/tools/content_restorer.py` - Fix card content
- `shared/tools/corruption_fixer.py` - Clean malformed cards
- `shared/tools/css_cleaner.py` - Remove formatting issues
- `shared/tools/smart_content_fixer.py` - Generate proper answers
- `shared/tools/validate_clean.py` - Quality assurance

## Best Practices

1. **Content Organization:** Keep source materials separate from generated content
2. **Version Control:** Use descriptive commit messages for course updates
3. **Quality Assurance:** Validate cards before finalizing decks
4. **Documentation:** Update course-specific README with deck statistics
5. **Optimization:** Follow memory retention principles for card design