"""
Base Content Extractor - Core utility for extracting content from various course materials.

This module provides the foundation for course-specific content extractors,
handling common operations like file reading, text processing, and content validation.
"""

import os
import json
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseContentExtractor:
    """Base class for course content extraction."""
    
    def __init__(self, course_path: str, config: Optional[Dict] = None):
        """
        Initialize the content extractor.
        
        Args:
            course_path: Path to the course directory
            config: Optional configuration dictionary
        """
        self.course_path = Path(course_path)
        self.config = config or self._load_default_config()
        self.content_sources = {}
        self.extracted_content = {}
        
        # Validate course structure
        self._validate_course_structure()
    
    def _load_default_config(self) -> Dict:
        """Load default configuration settings."""
        return {
            "extraction_rules": {
                "min_text_length": 10,
                "max_text_length": 500,
                "exclude_patterns": [r'^\s*$', r'^[^a-zA-Z]*$'],
                "content_markers": ['chapter', 'section', 'learning objective', 'definition']
            },
            "quality_filters": {
                "remove_duplicates": True,
                "filter_incomplete": True,
                "validate_format": True
            },
            "output_settings": {
                "question_format": "interrogative",
                "answer_max_length": 200,
                "include_context": True
            }
        }
    
    def _validate_course_structure(self) -> None:
        """Validate that the course has the required directory structure."""
        required_dirs = ['content', 'decks', 'config']
        
        for dir_name in required_dirs:
            dir_path = self.course_path / dir_name
            if not dir_path.exists():
                logger.warning(f"Creating missing directory: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
    
    def load_course_config(self) -> Dict:
        """Load course-specific configuration."""
        config_path = self.course_path / 'config' / 'course_config.json'
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"No course config found at {config_path}")
            return {}
    
    def discover_content_sources(self) -> Dict[str, List[Path]]:
        """
        Discover all available content sources in the course directory.
        
        Returns:
            Dictionary mapping content types to file paths
        """
        content_dir = self.course_path / 'content'
        sources = {
            'textbooks': [],
            'lectures': [],
            'materials': [],
            'transcripts': []
        }
        
        if not content_dir.exists():
            return sources
        
        # Find textbooks (PDFs)
        textbook_dir = content_dir / 'textbooks'
        if textbook_dir.exists():
            sources['textbooks'] = list(textbook_dir.glob('*.pdf'))
        
        # Find lecture materials
        lecture_dir = content_dir / 'lectures'
        if lecture_dir.exists():
            sources['lectures'] = list(lecture_dir.glob('*'))
            # Separate transcripts
            sources['transcripts'] = [f for f in sources['lectures'] 
                                    if f.suffix.lower() in ['.txt', '.docx']]
        
        # Find additional materials
        materials_dir = content_dir / 'materials'
        if materials_dir.exists():
            sources['materials'] = list(materials_dir.glob('*'))
        
        # Also check root content directory
        for file_path in content_dir.glob('*'):
            if file_path.is_file():
                if file_path.suffix.lower() == '.pdf':
                    sources['textbooks'].append(file_path)
                elif file_path.suffix.lower() in ['.txt', '.docx']:
                    sources['transcripts'].append(file_path)
                else:
                    sources['materials'].append(file_path)
        
        # Log discovered sources
        for source_type, files in sources.items():
            if files:
                logger.info(f"Found {len(files)} {source_type}: {[f.name for f in files]}")
        
        return sources
    
    def extract_text_from_file(self, file_path: Path) -> str:
        """
        Extract text content from a file.
        
        Args:
            file_path: Path to the file to extract from
            
        Returns:
            Extracted text content
        """
        try:
            if file_path.suffix.lower() == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_path.suffix.lower() == '.docx':
                return self._extract_from_docx(file_path)
            elif file_path.suffix.lower() == '.txt':
                return self._extract_from_txt(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_path.suffix}")
                return ""
        except Exception as e:
            logger.error(f"Error extracting from {file_path}: {e}")
            return ""
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file."""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except ImportError:
            logger.error("PyMuPDF not installed. Cannot extract from PDF.")
            return ""
    
    def _extract_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file."""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            logger.error("python-docx not installed. Cannot extract from DOCX.")
            return ""
    
    def _extract_from_txt(self, file_path: Path) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove empty lines
        text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
        
        # Apply exclude patterns
        for pattern in self.config['extraction_rules']['exclude_patterns']:
            text = re.sub(pattern, '', text, flags=re.MULTILINE)
        
        return text.strip()
    
    def extract_learning_objectives(self, text: str) -> List[str]:
        """
        Extract learning objectives from text.
        Base implementation - should be overridden by subclasses.
        
        Args:
            text: Text to extract objectives from
            
        Returns:
            List of learning objectives
        """
        objectives = []
        
        # Common patterns for learning objectives
        patterns = [
            r'(?i)learning\s+objective[s]?[:\-]?\s*(.+?)(?=\n\n|\Z)',
            r'(?i)by\s+the\s+end\s+of\s+this\s+chapter[,.]?\s+you\s+will[:\-]?\s*(.+?)(?=\n\n|\Z)',
            r'(?i)students?\s+will\s+be\s+able\s+to[:\-]?\s*(.+?)(?=\n\n|\Z)',
            r'(?i)objectives?[:\-]\s*(.+?)(?=\n\n|\Z)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                # Split on bullet points or line breaks
                obj_lines = re.split(r'[•\-*]\s*|^\s*\d+\.?\s*', match, flags=re.MULTILINE)
                for line in obj_lines:
                    line = line.strip()
                    if len(line) > 10:  # Filter out very short objectives
                        objectives.append(line)
        
        return objectives
    
    def extract_definitions(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract term-definition pairs from text.
        
        Args:
            text: Text to extract definitions from
            
        Returns:
            List of (term, definition) tuples
        """
        definitions = []
        
        # Pattern for explicit definitions
        def_patterns = [
            r'(.+?)\s+is\s+defined\s+as\s+(.+?)(?=\.|;|\n)',
            r'(.+?):\s+(.+?)(?=\n[A-Z]|\n\n|\Z)',
            r'(.+?)\s+refers\s+to\s+(.+?)(?=\.|;|\n)',
        ]
        
        for pattern in def_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for term, definition in matches:
                term = term.strip()
                definition = definition.strip()
                
                # Basic quality filters
                if (len(term) < 50 and len(definition) > 10 and 
                    len(definition) < 300):
                    definitions.append((term, definition))
        
        return definitions
    
    def generate_cards_from_objectives(self, objectives: List[str]) -> List[Dict]:
        """
        Convert learning objectives into flashcard format.
        
        Args:
            objectives: List of learning objectives
            
        Returns:
            List of card dictionaries
        """
        cards = []
        
        for objective in objectives:
            # Convert objective to question format
            question = self._objective_to_question(objective)
            answer = objective.strip()
            
            if question and answer:
                card = {
                    'front': question,
                    'back': answer,
                    'tags': self._generate_tags('objective'),
                    'type': 'basic',
                    'source': 'learning_objective'
                }
                cards.append(card)
        
        return cards
    
    def _objective_to_question(self, objective: str) -> str:
        """Convert a learning objective to a question format."""
        # Remove common objective prefixes
        objective = re.sub(r'^(?:students?\s+will\s+|you\s+will\s+|learners?\s+will\s+)', '', objective, flags=re.IGNORECASE)
        objective = re.sub(r'^(?:be\s+able\s+to\s+|understand\s+|learn\s+|know\s+)', '', objective, flags=re.IGNORECASE)
        
        # Convert to question
        if objective.lower().startswith('identify'):
            return f"What should you be able to identify regarding {objective[8:].strip()}?"
        elif objective.lower().startswith('explain'):
            return f"How would you explain {objective[7:].strip()}?"
        elif objective.lower().startswith('describe'):
            return f"How would you describe {objective[8:].strip()}?"
        elif objective.lower().startswith('analyze'):
            return f"How would you analyze {objective[7:].strip()}?"
        else:
            return f"What do you need to know about {objective.strip()}?"
    
    def _generate_tags(self, card_type: str) -> str:
        """Generate tags for a card based on course and type."""
        course_code = self.course_path.name
        return f"{course_code} {card_type}"
    
    def save_extracted_content(self, content: Dict, filename: str = "extracted_content.json") -> None:
        """Save extracted content to a JSON file."""
        output_path = self.course_path / 'processing' / 'extracted' / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Extracted content saved to {output_path}")
    
    def load_extracted_content(self, filename: str = "extracted_content.json") -> Dict:
        """Load previously extracted content from a JSON file."""
        content_path = self.course_path / 'processing' / 'extracted' / filename
        
        if content_path.exists():
            with open(content_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"No extracted content found at {content_path}")
            return {}


class CourseExtractor(BaseContentExtractor):
    """
    Course-specific content extractor.
    Inherits from BaseContentExtractor and adds course-specific functionality.
    """
    
    def __init__(self, course_path: str):
        super().__init__(course_path)
        self.course_config = self.load_course_config()
        self.content_sources = self.discover_content_sources()
    
    def extract_all_content(self) -> Dict:
        """
        Extract content from all available sources.
        
        Returns:
            Dictionary containing all extracted content
        """
        extracted = {
            'learning_objectives': [],
            'definitions': [],
            'key_concepts': [],
            'cards': [],
            'source_files': []
        }
        
        # Process each content source
        for source_type, files in self.content_sources.items():
            logger.info(f"Processing {len(files)} {source_type} files...")
            
            for file_path in files:
                logger.info(f"Extracting from: {file_path.name}")
                
                # Extract text
                text = self.extract_text_from_file(file_path)
                if not text:
                    continue
                
                # Clean text
                clean_text = self.clean_text(text)
                
                # Extract learning objectives
                objectives = self.extract_learning_objectives(clean_text)
                extracted['learning_objectives'].extend(objectives)
                
                # Extract definitions
                definitions = self.extract_definitions(clean_text)
                extracted['definitions'].extend(definitions)
                
                # Track source file
                extracted['source_files'].append({
                    'path': str(file_path),
                    'type': source_type,
                    'text_length': len(clean_text),
                    'objectives_found': len(objectives),
                    'definitions_found': len(definitions)
                })
        
        # Generate cards from objectives
        objective_cards = self.generate_cards_from_objectives(extracted['learning_objectives'])
        extracted['cards'].extend(objective_cards)
        
        # Generate cards from definitions
        definition_cards = self.generate_cards_from_definitions(extracted['definitions'])
        extracted['cards'].extend(definition_cards)
        
        # Save extracted content
        self.save_extracted_content(extracted)
        
        logger.info(f"Extraction complete: {len(extracted['cards'])} cards generated")
        return extracted
    
    def generate_cards_from_definitions(self, definitions: List[Tuple[str, str]]) -> List[Dict]:
        """Generate flashcards from term-definition pairs."""
        cards = []
        
        for term, definition in definitions:
            card = {
                'front': f"What is {term}?",
                'back': definition,
                'tags': self._generate_tags('definition'),
                'type': 'basic',
                'source': 'definition'
            }
            cards.append(card)
        
        return cards