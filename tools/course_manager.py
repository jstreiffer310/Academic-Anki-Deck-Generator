#!/usr/bin/env python3
"""
Course Manager - Tool for creating and managing academic courses.

This tool provides a command-line interface for:
- Creating new courses from templates
- Migrating existing courses to new structure
- Managing course configurations
- Validating course structure
"""

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CourseManager:
    """Main class for managing academic courses."""
    
    def __init__(self, repo_root: Optional[Path] = None):
        """Initialize the course manager."""
        self.repo_root = repo_root or Path(__file__).parent
        self.courses_dir = self.repo_root / 'courses'
        self.templates_dir = self.repo_root / 'templates'
        self.config_dir = self.repo_root / 'config'
        
        # Load configurations
        self.templates_config = self._load_templates_config()
        self.default_settings = self._load_default_settings()
    
    def _load_templates_config(self) -> Dict:
        """Load template configurations."""
        config_path = self.config_dir / 'templates.json'
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"Templates config not found at {config_path}")
            return {}
    
    def _load_default_settings(self) -> Dict:
        """Load default settings."""
        settings_path = self.config_dir / 'default_settings.json'
        if settings_path.exists():
            with open(settings_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"Default settings not found at {settings_path}")
            return {}
    
    def list_templates(self) -> List[str]:
        """List available course templates."""
        if 'templates' in self.templates_config:
            return list(self.templates_config['templates'].keys())
        return []
    
    def create_course(self, course_code: str, course_name: str, semester: str, 
                     template: str = 'basic', instructor: str = '') -> bool:
        """
        Create a new course from a template.
        
        Args:
            course_code: Unique course identifier (e.g., 'PSYC2240')
            course_name: Full course name
            semester: Semester information (e.g., 'Fall 2024')
            template: Template to use ('basic', 'psychology', 'science', 'humanities')
            instructor: Instructor name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate inputs
            if not course_code or not course_name:
                logger.error("Course code and name are required")
                return False
            
            # Check if course already exists
            course_path = self.courses_dir / course_code
            if course_path.exists():
                logger.error(f"Course {course_code} already exists at {course_path}")
                return False
            
            # Validate template
            if template not in self.list_templates():
                logger.error(f"Template '{template}' not found. Available: {self.list_templates()}")
                return False
            
            logger.info(f"Creating course {course_code} using template '{template}'")
            
            # Create course directory structure
            self._create_course_structure(course_path, template)
            
            # Create course configuration
            self._create_course_config(course_path, course_code, course_name, 
                                     semester, template, instructor)
            
            # Create additional files
            self._create_course_files(course_path, course_code, course_name)
            
            logger.info(f"Successfully created course {course_code} at {course_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating course {course_code}: {e}")
            return False
    
    def _create_course_structure(self, course_path: Path, template: str) -> None:
        """Create the directory structure for a course."""
        # Get template configuration
        template_config = self.templates_config['templates'][template]
        
        # Create required directories
        required_dirs = self.templates_config['directory_structure']['required_dirs']
        for dir_name in required_dirs:
            dir_path = course_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create optional directories based on template
        optional_dirs = self.templates_config['directory_structure']['optional_dirs']
        template_sources = template_config['config'].get('content_sources', {})
        
        for dir_name in optional_dirs:
            # Only create if relevant to template
            if self._is_dir_relevant_to_template(dir_name, template_sources):
                dir_path = course_path / dir_name
                dir_path.mkdir(parents=True, exist_ok=True)
    
    def _is_dir_relevant_to_template(self, dir_name: str, sources: Dict) -> bool:
        """Check if a directory is relevant to the template's content sources."""
        relevance_map = {
            'content/clinical_cases': sources.get('clinical_cases', False),
            'content/lab_materials': sources.get('lab_materials', False),
            'content/primary_sources': sources.get('primary_sources', False),
            'content/additional_readings': sources.get('additional_readings', False)
        }
        return relevance_map.get(dir_name, False)
    
    def _create_course_config(self, course_path: Path, course_code: str, 
                            course_name: str, semester: str, template: str, instructor: str) -> None:
        """Create the course configuration file."""
        template_config = self.templates_config['templates'][template]['config'].copy()
        
        # Update with provided information
        template_config['course_code'] = course_code
        template_config['course_name'] = course_name
        template_config['semester'] = semester
        template_config['instructor'] = instructor
        template_config['template_used'] = template
        
        # Save configuration
        config_path = course_path / 'config' / 'course_config.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(template_config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created course config at {config_path}")
    
    def _create_course_files(self, course_path: Path, course_code: str, course_name: str) -> None:
        """Create additional course files."""
        # Create README.md
        readme_content = f"""# {course_code}: {course_name}

## Overview
This directory contains all materials and generated content for {course_name}.

## Directory Structure
- `config/` - Course configuration and extraction rules
- `content/` - Source materials (textbooks, lectures, etc.)
- `processing/` - Intermediate processing files and logs
- `decks/` - Generated Anki decks and exports
- `tools/` - Course-specific processing tools

## Usage

### 1. Add Course Materials
Place your course materials in the appropriate directories:
- Textbooks (PDF): `content/textbooks/`
- Lecture notes/transcripts: `content/lectures/`
- Additional materials: `content/materials/`

### 2. Extract Content
Use the shared content extractor:
```python
from shared.core.content_extractor import CourseExtractor

extractor = CourseExtractor('{course_path}')
content = extractor.extract_all_content()
```

### 3. Build Deck
Use the shared deck builder:
```python
from shared.core.deck_builder import CourseDeckBuilder

builder = CourseDeckBuilder('{course_path}')
csv_path, apkg_path = builder.build_complete_deck()
```

### 4. Import to Anki
- Use the `.apkg` file for direct import
- Or import the CSV file with Field mapping: Front→Question, Back→Answer, Tags→Tags

## Generated Files
- `decks/final/{course_code}_Complete_AnkiDeck.csv` - Main deck for import
- `decks/final/{course_code}_Complete_Deck.apkg` - Anki package
- `decks/final/{course_code}_Deck_Summary.md` - Deck statistics and info

## Customization
Edit `config/course_config.json` to customize:
- Card generation settings
- Content extraction rules
- Export options
- Quality filters
"""
        
        readme_path = course_path / 'README.md'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Create extraction rules template
        extraction_rules = {
            "custom_patterns": [],
            "exclude_sections": [],
            "priority_keywords": [],
            "content_markers": []
        }
        
        rules_path = course_path / 'config' / 'extraction_rules.json'
        with open(rules_path, 'w', encoding='utf-8') as f:
            json.dump(extraction_rules, f, indent=2, ensure_ascii=False)
        
        # Create import guide
        import_guide = f"""# {course_code} Anki Import Guide

## Quick Import (Recommended)
1. Download the generated `.apkg` file from `decks/final/`
2. Open Anki
3. File → Import → Select the `.apkg` file
4. Click Import

## CSV Import (Alternative)
1. Download the generated CSV file from `decks/final/`
2. Open Anki
3. File → Import → Select the CSV file
4. Configure import settings:
   - Note Type: Basic
   - Field 1: Front
   - Field 2: Back
   - Field 3: Tags
5. Click Import

## Study Settings (Recommended)
- Enable FSRS algorithm for optimal scheduling
- Set new cards per day: 20-30
- Set maximum reviews: 200-300
- Enable learning steps: 1m 10m

## Deck Organization
Your cards will be tagged with:
- `{course_code}` - Course identifier
- Chapter/section tags
- Priority levels (high/medium/low)
- Content source (textbook/lecture/etc.)

Use Anki's filtered decks to study specific topics or priorities.
"""
        
        import_path = course_path / 'decks' / 'IMPORT_GUIDE.md'
        with open(import_path, 'w', encoding='utf-8') as f:
            f.write(import_guide)
        
        logger.info(f"Created course files for {course_code}")
    
    def migrate_course(self, old_path: Path, course_code: str, template: str = 'basic') -> bool:
        """
        Migrate an existing course to the new structure.
        
        Args:
            old_path: Path to existing course directory
            course_code: Course code for the migrated course
            template: Template to use for migration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not old_path.exists():
                logger.error(f"Source path does not exist: {old_path}")
                return False
            
            new_path = self.courses_dir / course_code
            
            if new_path.exists():
                logger.error(f"Target course already exists: {new_path}")
                return False
            
            logger.info(f"Migrating course from {old_path} to {new_path}")
            
            # Create new structure
            self._create_course_structure(new_path, template)
            
            # Migrate content
            self._migrate_content(old_path, new_path)
            
            # Create configuration based on old structure
            self._create_migration_config(new_path, course_code, template)
            
            logger.info(f"Successfully migrated course to {new_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error migrating course: {e}")
            return False
    
    def _migrate_content(self, old_path: Path, new_path: Path) -> None:
        """Migrate content from old structure to new structure."""
        # Common migration mappings
        migration_map = {
            'content': 'content/materials',
            'decks': 'decks/archives',
            'tools': 'tools',
            '*.pdf': 'content/textbooks',
            '*.txt': 'content/lectures',
            '*.docx': 'content/lectures'
        }
        
        for old_pattern, new_location in migration_map.items():
            if old_pattern.startswith('*'):
                # File pattern
                pattern = old_pattern[1:]  # Remove asterisk
                for file_path in old_path.rglob(f"*{pattern}"):
                    if file_path.is_file():
                        target_dir = new_path / new_location
                        target_dir.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, target_dir / file_path.name)
                        logger.info(f"Migrated file: {file_path.name} → {new_location}")
            else:
                # Directory
                old_dir = old_path / old_pattern
                if old_dir.exists():
                    new_dir = new_path / new_location
                    new_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Copy all files
                    for file_path in old_dir.rglob('*'):
                        if file_path.is_file():
                            relative_path = file_path.relative_to(old_dir)
                            target_path = new_dir / relative_path
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(file_path, target_path)
                    
                    logger.info(f"Migrated directory: {old_pattern} → {new_location}")
    
    def _create_migration_config(self, course_path: Path, course_code: str, template: str) -> None:
        """Create configuration for migrated course."""
        config = self.templates_config['templates'][template]['config'].copy()
        config['course_code'] = course_code
        config['course_name'] = f"Migrated Course {course_code}"
        config['semester'] = "Unknown"
        config['migrated'] = True
        config['migration_date'] = str(Path(__file__).stat().st_mtime)
        
        config_path = course_path / 'config' / 'course_config.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def validate_course(self, course_code: str) -> bool:
        """
        Validate course structure and configuration.
        
        Args:
            course_code: Course code to validate
            
        Returns:
            True if valid, False otherwise
        """
        course_path = self.courses_dir / course_code
        
        if not course_path.exists():
            logger.error(f"Course {course_code} does not exist")
            return False
        
        # Check required directories
        required_dirs = self.templates_config['directory_structure']['required_dirs']
        missing_dirs = []
        
        for dir_name in required_dirs:
            dir_path = course_path / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
        
        if missing_dirs:
            logger.error(f"Missing directories in {course_code}: {missing_dirs}")
            return False
        
        # Check configuration file
        config_path = course_path / 'config' / 'course_config.json'
        if not config_path.exists():
            logger.error(f"Missing course configuration: {config_path}")
            return False
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate required config fields
            required_fields = ['course_code', 'course_name']
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                logger.error(f"Missing config fields in {course_code}: {missing_fields}")
                return False
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in course config: {e}")
            return False
        
        logger.info(f"Course {course_code} validation passed")
        return True
    
    def list_courses(self) -> List[str]:
        """List all existing courses."""
        if not self.courses_dir.exists():
            return []
        
        courses = []
        for item in self.courses_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Check if it has a config file
                config_path = item / 'config' / 'course_config.json'
                if config_path.exists():
                    courses.append(item.name)
        
        return sorted(courses)


def main():
    """Main command-line interface."""
    parser = argparse.ArgumentParser(description='Academic Course Manager')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create course command
    create_parser = subparsers.add_parser('create', help='Create a new course')
    create_parser.add_argument('course_code', help='Course code (e.g., PSYC2240)')
    create_parser.add_argument('course_name', help='Full course name')
    create_parser.add_argument('semester', help='Semester (e.g., Fall 2024)')
    create_parser.add_argument('--template', default='basic', 
                              help='Template to use (basic, psychology, science, humanities)')
    create_parser.add_argument('--instructor', default='', help='Instructor name')
    
    # Migrate course command
    migrate_parser = subparsers.add_parser('migrate', help='Migrate existing course')
    migrate_parser.add_argument('old_path', help='Path to existing course')
    migrate_parser.add_argument('course_code', help='Course code for migrated course')
    migrate_parser.add_argument('--template', default='basic', help='Template to use')
    
    # List commands
    list_parser = subparsers.add_parser('list', help='List available items')
    list_parser.add_argument('type', choices=['courses', 'templates'], 
                           help='What to list')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate course structure')
    validate_parser.add_argument('course_code', help='Course code to validate')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize course manager
    manager = CourseManager()
    
    # Execute command
    if args.command == 'create':
        success = manager.create_course(
            args.course_code, 
            args.course_name, 
            args.semester,
            args.template, 
            args.instructor
        )
        sys.exit(0 if success else 1)
    
    elif args.command == 'migrate':
        success = manager.migrate_course(
            Path(args.old_path), 
            args.course_code, 
            args.template
        )
        sys.exit(0 if success else 1)
    
    elif args.command == 'list':
        if args.type == 'courses':
            courses = manager.list_courses()
            if courses:
                print(f"Available courses ({len(courses)}):")
                for course in courses:
                    print(f"  - {course}")
            else:
                print("No courses found.")
        
        elif args.type == 'templates':
            templates = manager.list_templates()
            if templates:
                print(f"Available templates ({len(templates)}):")
                for template in templates:
                    config = manager.templates_config['templates'][template]
                    print(f"  - {template}: {config['description']}")
            else:
                print("No templates found.")
    
    elif args.command == 'validate':
        success = manager.validate_course(args.course_code)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()