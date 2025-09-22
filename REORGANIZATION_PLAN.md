# Repository Reorganization Plan

## Current Structure Issues
- Course-specific tools scattered in multiple locations
- Shared utilities not properly organized
- Template system partially implemented
- Documentation spread across multiple files

## New Flexible Structure

```
Academic-Anki-Deck-Generator/
├── 📁 courses/                    # ALL COURSE CONTENT
│   ├── PSYC2120/                 # Social Psychology (existing)
│   ├── PSYC2240/                 # Biological Psychology (existing)
│   ├── [ANY_COURSE]/             # Template for new courses
│   └── _template/                # Master course template
│
├── 📁 shared/                     # SHARED UTILITIES
│   ├── core/                     # Core Anki generation tools
│   │   ├── content_extractor.py  # Base content extraction
│   │   ├── deck_builder.py       # Base deck generation
│   │   ├── card_optimizer.py     # Card quality optimization
│   │   └── anki_exporter.py      # CSV/APKG export
│   ├── utils/                    # Utility functions
│   │   ├── text_processor.py     # Text cleaning and processing
│   │   ├── file_manager.py       # File operations
│   │   └── validation.py         # Quality assurance
│   └── scripts/                  # PowerShell automation
│       ├── setup_course.ps1      # New course setup
│       ├── build_deck.ps1        # Deck generation
│       └── maintenance.ps1       # Cleanup and validation
│
├── 📁 templates/                  # COURSE TEMPLATES
│   ├── basic/                    # Standard academic course
│   ├── psychology/               # Psychology-specific template
│   ├── science/                  # STEM course template
│   └── humanities/               # Text-heavy course template
│
├── 📁 config/                     # GLOBAL CONFIGURATION
│   ├── default_settings.json     # Default card generation settings
│   ├── templates.json            # Template configurations
│   └── export_formats.json       # Output format definitions
│
├── 📁 docs/                       # DOCUMENTATION
│   ├── user_guide.md             # Complete user documentation
│   ├── developer_guide.md        # Development and customization
│   ├── course_setup.md           # Adding new courses
│   └── api_reference.md          # Tool and function reference
│
├── 📁 tools/                      # MANAGEMENT TOOLS
│   ├── course_manager.py         # Create/manage courses
│   ├── deck_analyzer.py          # Analyze deck quality
│   └── migration_tool.py         # Upgrade existing courses
│
└── 📁 examples/                   # EXAMPLE IMPLEMENTATIONS
    ├── psychology_cards.csv      # Sample psychology cards
    ├── science_cards.csv         # Sample science cards
    └── import_examples/          # Anki import examples
```

## Standardized Course Structure

Each course follows this exact structure:

```
courses/COURSE_CODE/
├── config/
│   ├── course_config.json        # Course-specific settings
│   └── extraction_rules.json    # Content extraction rules
├── content/
│   ├── textbooks/               # PDF textbooks
│   ├── lectures/                # Transcripts, recordings
│   ├── materials/               # Additional course materials
│   └── raw/                     # Unprocessed source files
├── processing/
│   ├── extracted/               # Processed content
│   ├── analysis/                # Content analysis results
│   └── logs/                    # Processing logs
├── decks/
│   ├── drafts/                  # Work-in-progress decks
│   ├── final/                   # Ready-for-use decks
│   └── archives/                # Previous versions
├── tools/
│   ├── course_extractor.py      # Course-specific extraction
│   └── custom_processors.py    # Any custom processing
└── README.md                    # Course-specific documentation
```

## Migration Strategy

1. **Phase 1**: Create new structure alongside existing
2. **Phase 2**: Migrate PSYC2240 and PSYC2120 to new structure
3. **Phase 3**: Update all tools to use new paths
4. **Phase 4**: Remove old structure and update documentation

## Benefits

- **Scalability**: Easy to add unlimited courses
- **Consistency**: Standardized structure across all courses
- **Maintainability**: Shared tools, course-specific customization
- **Documentation**: Clear guides for each component
- **Template System**: Multiple templates for different course types
- **Quality Assurance**: Built-in validation and testing