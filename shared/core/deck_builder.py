"""
Base Deck Builder - Core utility for generating Anki decks from extracted content.

This module provides the foundation for creating high-quality Anki decks with
standardized formats, quality validation, and multiple export options.
"""

import os
import json
import csv
import uuid
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import genanki
    GENANKI_AVAILABLE = True
except ImportError:
    logger.warning("genanki not available. .apkg export will be disabled.")
    GENANKI_AVAILABLE = False


class BaseDeckBuilder:
    """Base class for Anki deck generation."""
    
    def __init__(self, course_path: str, config: Optional[Dict] = None):
        """
        Initialize the deck builder.
        
        Args:
            course_path: Path to the course directory
            config: Optional configuration dictionary
        """
        self.course_path = Path(course_path)
        self.config = config or self._load_default_config()
        self.course_config = self._load_course_config()
        self.cards = []
        self.deck_stats = {}
    
    def _load_default_config(self) -> Dict:
        """Load default deck generation settings."""
        return {
            "deck_settings": {
                "model_id": 1607392319,  # Basic model ID
                "deck_id": None,  # Will be auto-generated
                "css_styling": True,
                "enable_cloze": True
            },
            "card_quality": {
                "min_front_length": 10,
                "max_front_length": 200,
                "min_back_length": 5,
                "max_back_length": 500,
                "remove_duplicates": True,
                "validate_format": True
            },
            "export_options": {
                "csv_export": True,
                "apkg_export": True,
                "include_metadata": True,
                "split_by_type": False
            },
            "tagging": {
                "include_course_code": True,
                "include_source": True,
                "include_priority": True,
                "format": "{course_code} {chapter} {priority}"
            }
        }
    
    def _load_course_config(self) -> Dict:
        """Load course-specific configuration."""
        config_path = self.course_path / 'config' / 'course_config.json'
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "course_code": self.course_path.name,
                "course_name": f"Course {self.course_path.name}",
                "target_count": 100
            }
    
    def load_extracted_content(self, filename: str = "extracted_content.json") -> Dict:
        """Load extracted content from JSON file."""
        content_path = self.course_path / 'processing' / 'extracted' / filename
        
        if content_path.exists():
            with open(content_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.error(f"No extracted content found at {content_path}")
            return {}
    
    def validate_card(self, card: Dict) -> bool:
        """
        Validate a single card for quality and format.
        
        Args:
            card: Card dictionary to validate
            
        Returns:
            True if card is valid, False otherwise
        """
        required_fields = ['front', 'back']
        
        # Check required fields
        for field in required_fields:
            if field not in card or not card[field]:
                logger.warning(f"Card missing required field: {field}")
                return False
        
        # Check length constraints
        front_len = len(card['front'])
        back_len = len(card['back'])
        
        if (front_len < self.config['card_quality']['min_front_length'] or
            front_len > self.config['card_quality']['max_front_length']):
            logger.warning(f"Card front length invalid: {front_len}")
            return False
        
        if (back_len < self.config['card_quality']['min_back_length'] or
            back_len > self.config['card_quality']['max_back_length']):
            logger.warning(f"Card back length invalid: {back_len}")
            return False
        
        return True
    
    def clean_card_text(self, text: str) -> str:
        """Clean and format card text."""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove problematic characters
        text = text.replace('"', "'")
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
        
        # Ensure proper punctuation
        if text and not text.endswith(('.', '?', '!')):
            if '?' in text or text.lower().startswith(('what', 'how', 'why', 'when', 'where')):
                text += '?'
            else:
                text += '.'
        
        return text.strip()
    
    def standardize_tags(self, card: Dict) -> str:
        """Generate standardized tags for a card."""
        course_code = self.course_config.get('course_code', self.course_path.name)
        
        tags = [course_code]
        
        # Add source-based tags
        if 'source' in card:
            tags.append(card['source'])
        
        # Add type-based tags
        if 'type' in card:
            tags.append(card['type'])
        
        # Add priority if available
        if 'priority' in card:
            tags.append(card['priority'])
        
        # Add chapter/topic if available
        if 'chapter' in card:
            tags.append(f"Chapter{card['chapter']}")
        
        return ' '.join(tags)
    
    def process_cards(self, cards: List[Dict]) -> List[Dict]:
        """
        Process and clean a list of cards.
        
        Args:
            cards: List of raw card dictionaries
            
        Returns:
            List of processed and validated cards
        """
        processed_cards = []
        
        for card in cards:
            # Clean text
            if 'front' in card:
                card['front'] = self.clean_card_text(card['front'])
            if 'back' in card:
                card['back'] = self.clean_card_text(card['back'])
            
            # Standardize tags
            card['tags'] = self.standardize_tags(card)
            
            # Validate card
            if self.validate_card(card):
                processed_cards.append(card)
            else:
                logger.warning(f"Skipping invalid card: {card.get('front', 'Unknown')}")
        
        # Remove duplicates if configured
        if self.config['card_quality']['remove_duplicates']:
            processed_cards = self.remove_duplicate_cards(processed_cards)
        
        logger.info(f"Processed {len(processed_cards)} valid cards from {len(cards)} input cards")
        return processed_cards
    
    def remove_duplicate_cards(self, cards: List[Dict]) -> List[Dict]:
        """Remove duplicate cards based on front text."""
        seen_fronts = set()
        unique_cards = []
        
        for card in cards:
            front_text = card['front'].lower().strip()
            if front_text not in seen_fronts:
                seen_fronts.add(front_text)
                unique_cards.append(card)
            else:
                logger.debug(f"Removing duplicate card: {card['front']}")
        
        logger.info(f"Removed {len(cards) - len(unique_cards)} duplicate cards")
        return unique_cards
    
    def categorize_cards_by_priority(self, cards: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize cards by priority level."""
        categories = {
            'high': [],
            'medium': [],
            'low': []
        }
        
        for card in cards:
            priority = card.get('priority', 'medium').lower()
            if priority in categories:
                categories[priority].append(card)
            else:
                categories['medium'].append(card)
        
        return categories
    
    def export_to_csv(self, cards: List[Dict], filename: str = None) -> Path:
        """
        Export cards to CSV format for Anki import.
        
        Args:
            cards: List of card dictionaries
            filename: Optional custom filename
            
        Returns:
            Path to the created CSV file
        """
        if not filename:
            course_code = self.course_config.get('course_code', 'UNKNOWN')
            filename = f"{course_code}_Complete_AnkiDeck.csv"
        
        output_path = self.course_path / 'decks' / 'final' / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Front', 'Back', 'Tags'])
            
            # Write cards
            for card in cards:
                front = card.get('front', '')
                back = card.get('back', '')
                tags = card.get('tags', '')
                
                writer.writerow([front, back, tags])
        
        logger.info(f"Exported {len(cards)} cards to {output_path}")
        return output_path
    
    def export_to_apkg(self, cards: List[Dict], filename: str = None) -> Optional[Path]:
        """
        Export cards to Anki package (.apkg) format.
        
        Args:
            cards: List of card dictionaries
            filename: Optional custom filename
            
        Returns:
            Path to the created .apkg file, or None if genanki unavailable
        """
        if not GENANKI_AVAILABLE:
            logger.warning("genanki not available. Skipping .apkg export.")
            return None
        
        if not filename:
            course_code = self.course_config.get('course_code', 'UNKNOWN')
            filename = f"{course_code}_Complete_Deck.apkg"
        
        output_path = self.course_path / 'decks' / 'final' / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create Anki model
        model = genanki.Model(
            self.config['deck_settings']['model_id'],
            'Basic Card Model',
            fields=[
                {'name': 'Front'},
                {'name': 'Back'},
                {'name': 'Tags'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Front}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
                },
            ],
            css=self._get_card_css() if self.config['deck_settings']['css_styling'] else ''
        )
        
        # Create deck
        deck_id = self.config['deck_settings']['deck_id'] or self._generate_deck_id()
        deck_name = self.course_config.get('course_name', f"Course {self.course_path.name}")
        
        deck = genanki.Deck(deck_id, deck_name)
        
        # Add cards to deck
        for card_data in cards:
            note = genanki.Note(
                model=model,
                fields=[
                    card_data.get('front', ''),
                    card_data.get('back', ''),
                    card_data.get('tags', '')
                ],
                tags=card_data.get('tags', '').split()
            )
            deck.add_note(note)
        
        # Create package
        package = genanki.Package(deck)
        package.write_to_file(str(output_path))
        
        logger.info(f"Exported {len(cards)} cards to {output_path}")
        return output_path
    
    def _generate_deck_id(self) -> int:
        """Generate a unique deck ID."""
        return abs(hash(self.course_path.name)) % (10**8)
    
    def _get_card_css(self) -> str:
        """Get CSS styling for cards."""
        return """
        .card {
            font-family: Arial, sans-serif;
            font-size: 16px;
            line-height: 1.5;
            color: #333;
            background-color: #fff;
            padding: 20px;
            text-align: left;
        }
        
        .front {
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .back {
            margin-top: 10px;
        }
        
        .tags {
            font-size: 12px;
            color: #666;
            margin-top: 15px;
        }
        
        .highlight {
            background-color: #ffff99;
            padding: 2px 4px;
        }
        
        .definition {
            font-style: italic;
        }
        
        .example {
            background-color: #f0f8ff;
            padding: 10px;
            border-left: 4px solid #007acc;
            margin: 10px 0;
        }
        """
    
    def generate_deck_statistics(self, cards: List[Dict]) -> Dict:
        """Generate statistics about the deck."""
        stats = {
            'total_cards': len(cards),
            'card_types': {},
            'source_breakdown': {},
            'priority_breakdown': {},
            'avg_front_length': 0,
            'avg_back_length': 0
        }
        
        if not cards:
            return stats
        
        # Calculate averages
        total_front_length = sum(len(card.get('front', '')) for card in cards)
        total_back_length = sum(len(card.get('back', '')) for card in cards)
        
        stats['avg_front_length'] = round(total_front_length / len(cards), 1)
        stats['avg_back_length'] = round(total_back_length / len(cards), 1)
        
        # Count by type
        for card in cards:
            card_type = card.get('type', 'unknown')
            stats['card_types'][card_type] = stats['card_types'].get(card_type, 0) + 1
            
            source = card.get('source', 'unknown')
            stats['source_breakdown'][source] = stats['source_breakdown'].get(source, 0) + 1
            
            priority = card.get('priority', 'medium')
            stats['priority_breakdown'][priority] = stats['priority_breakdown'].get(priority, 0) + 1
        
        return stats
    
    def save_deck_metadata(self, cards: List[Dict], stats: Dict) -> None:
        """Save deck metadata and statistics."""
        metadata = {
            'course_config': self.course_config,
            'deck_config': self.config,
            'generation_timestamp': str(Path(__file__).stat().st_mtime),
            'statistics': stats,
            'card_count': len(cards)
        }
        
        metadata_path = self.course_path / 'decks' / 'final' / 'deck_metadata.json'
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Deck metadata saved to {metadata_path}")


class CourseDeckBuilder(BaseDeckBuilder):
    """
    Course-specific deck builder.
    Inherits from BaseDeckBuilder and adds course-specific functionality.
    """
    
    def __init__(self, course_path: str):
        super().__init__(course_path)
    
    def build_complete_deck(self, content_filename: str = "extracted_content.json") -> Tuple[Path, Optional[Path]]:
        """
        Build a complete deck from extracted content.
        
        Args:
            content_filename: Name of the extracted content file
            
        Returns:
            Tuple of (CSV path, APKG path)
        """
        # Load extracted content
        content = self.load_extracted_content(content_filename)
        
        if not content or 'cards' not in content:
            logger.error("No cards found in extracted content")
            return None, None
        
        # Process cards
        cards = self.process_cards(content['cards'])
        
        if not cards:
            logger.error("No valid cards after processing")
            return None, None
        
        # Generate statistics
        stats = self.generate_deck_statistics(cards)
        
        # Save metadata
        self.save_deck_metadata(cards, stats)
        
        # Export to CSV
        csv_path = self.export_to_csv(cards)
        
        # Export to APKG
        apkg_path = self.export_to_apkg(cards)
        
        # Log results
        logger.info(f"Deck building complete:")
        logger.info(f"  Total cards: {stats['total_cards']}")
        logger.info(f"  CSV export: {csv_path}")
        if apkg_path:
            logger.info(f"  APKG export: {apkg_path}")
        
        # Generate summary
        self._generate_deck_summary(cards, stats)
        
        return csv_path, apkg_path
    
    def build_priority_decks(self, content_filename: str = "extracted_content.json") -> Dict[str, Tuple[Path, Optional[Path]]]:
        """
        Build separate decks for different priority levels.
        
        Args:
            content_filename: Name of the extracted content file
            
        Returns:
            Dictionary mapping priority levels to (CSV path, APKG path) tuples
        """
        # Load and process cards
        content = self.load_extracted_content(content_filename)
        cards = self.process_cards(content.get('cards', []))
        
        if not cards:
            logger.error("No valid cards to build priority decks")
            return {}
        
        # Categorize by priority
        priority_cards = self.categorize_cards_by_priority(cards)
        
        results = {}
        
        for priority, priority_card_list in priority_cards.items():
            if not priority_card_list:
                continue
            
            logger.info(f"Building {priority} priority deck with {len(priority_card_list)} cards")
            
            # Export with priority-specific filename
            course_code = self.course_config.get('course_code', 'UNKNOWN')
            csv_filename = f"{course_code}_{priority.title()}_Priority_Deck.csv"
            apkg_filename = f"{course_code}_{priority.title()}_Priority_Deck.apkg"
            
            csv_path = self.export_to_csv(priority_card_list, csv_filename)
            apkg_path = self.export_to_apkg(priority_card_list, apkg_filename)
            
            results[priority] = (csv_path, apkg_path)
        
        return results
    
    def _generate_deck_summary(self, cards: List[Dict], stats: Dict) -> None:
        """Generate a summary report of the deck."""
        course_code = self.course_config.get('course_code', 'UNKNOWN')
        summary_path = self.course_path / 'decks' / 'final' / f"{course_code}_Deck_Summary.md"
        
        summary_content = f"""# {course_code} Anki Deck Summary

## Overview
- **Course**: {self.course_config.get('course_name', 'Unknown')}
- **Total Cards**: {stats['total_cards']}
- **Average Front Length**: {stats['avg_front_length']} characters
- **Average Back Length**: {stats['avg_back_length']} characters

## Card Type Breakdown
"""
        
        for card_type, count in stats['card_types'].items():
            percentage = round((count / stats['total_cards']) * 100, 1)
            summary_content += f"- **{card_type.title()}**: {count} cards ({percentage}%)\n"
        
        summary_content += "\n## Source Breakdown\n"
        
        for source, count in stats['source_breakdown'].items():
            percentage = round((count / stats['total_cards']) * 100, 1)
            summary_content += f"- **{source.title()}**: {count} cards ({percentage}%)\n"
        
        summary_content += "\n## Priority Breakdown\n"
        
        for priority, count in stats['priority_breakdown'].items():
            percentage = round((count / stats['total_cards']) * 100, 1)
            summary_content += f"- **{priority.title()}**: {count} cards ({percentage}%)\n"
        
        summary_content += f"""
## Files Generated
- **CSV Deck**: `{course_code}_Complete_AnkiDeck.csv`
- **Anki Package**: `{course_code}_Complete_Deck.apkg`
- **Metadata**: `deck_metadata.json`

## Import Instructions
1. Import the `.apkg` file directly into Anki for immediate use
2. Or import the CSV file using Anki's import feature:
   - Select "Basic" note type
   - Map Field 1 → Front, Field 2 → Back, Field 3 → Tags

## Study Recommendations
- Focus on high-priority cards first
- Use spaced repetition for optimal retention
- Review clinical examples and definitions regularly
"""
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        logger.info(f"Deck summary saved to {summary_path}")