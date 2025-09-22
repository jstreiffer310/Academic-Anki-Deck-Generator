#!/usr/bin/env python3
"""
PSYC2120 Content Extractor - Adapted from PSYC2240 Proven Workflow
Leverages existing comprehensive_content_extractor.py with PSYC2120-specific enhancements:
- Learning Objectives (LOQ) extraction as primary source
- Social psychology terminology focus
- Test 1 content prioritization
- Improved card quality based on lessons learned
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any

# Add PSYC2240 tools to path to leverage existing workflow
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "PSYC2240" / "tools"))
from comprehensive_content_extractor import ContentExtractor

# Import document processing
try:
    from docx import Document
except ImportError:
    print("Installing python-docx...")
    os.system("pip install python-docx")
    from docx import Document

class PSYC2120ContentExtractor(ContentExtractor):
    """Enhanced content extractor specifically for PSYC2120 Social Psychology"""
    
    def __init__(self):
        # Initialize with PSYC2120 paths
        self.base_dir = Path(__file__).parent.parent
        self.source_materials = self.base_dir / "HH-PSYC 2120 C - Social Psychology (Fall 2025-2026)"
        self.content_dir = self.base_dir / "content"
        self.analysis_dir = self.content_dir / "analysis"
        
        # Create necessary directories
        self.content_dir.mkdir(exist_ok=True)
        self.analysis_dir.mkdir(exist_ok=True)
        
        # Course-specific settings
        self.course_code = "PSYC2120"
        self.focus_test = "Test 1"
        
        # Learning objectives priority keywords
        self.priority_keywords = [
            'social psychology', 'stereotype', 'impression', 'social cognition',
            'attribution', 'attitude', 'conformity', 'group', 'relationship',
            'influence', 'behavior', 'perception', 'bias', 'interaction'
        ]
        
    def extract_learning_objectives(self, text: str) -> List[Dict[str, str]]:
        """Extract Learning Objectives with enhanced methodology based on lessons learned"""
        objectives = []
        
        # Enhanced patterns for LOQ detection - more specific to the document format
        loq_patterns = [
            # Pattern 1: Direct LOQ sections
            r'LOQ\s*:?\s*([^.\n]*(?:\n(?!\s*LOQ\s*:)[^.\n]*)*)',
            # Pattern 2: Learning objectives headers
            r'(?:Learning Objectives?|Objectives?)\s*:?\s*\n?(.*?)(?=\n\s*(?:LOQ|Chapter|\d+\.|[A-Z][^a-z])|$)',
            # Pattern 3: After reading patterns
            r'(?:After reading|Upon completion).*?(?:will|should|able to)\s*:?\s*(.*?)(?=\n\s*\n|\n[A-Z][^a-z]|$)',
            # Pattern 4: Numbered objectives
            r'(?:^|\n)\s*\d+\.\s*([A-Z][^.\n]*(?:(?!\n\s*\d+\.)[^.\n]*)*)',
            # Pattern 5: Bullet point objectives
            r'(?:^|\n)\s*[•\-\*]\s*([A-Z][^.\n]*(?:(?!\n\s*[•\-\*])[^.\n]*)*)'
        ]
        
        print(f"🔍 Searching for learning objectives in {len(text)} characters of text...")
        
        for i, pattern in enumerate(loq_patterns):
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL | re.MULTILINE)
            pattern_objectives = []
            
            for match in matches:
                obj_text = match.group(1).strip()
                
                # Clean up the matched text
                obj_text = re.sub(r'\s+', ' ', obj_text).strip()
                
                # Skip if too short or too long
                if len(obj_text) < 10 or len(obj_text) > 300:
                    continue
                
                # Split into individual objectives if needed
                individual_objs = self._parse_objective_list(obj_text)
                for obj in individual_objs:
                    if self._is_valid_objective(obj):
                        pattern_objectives.append({
                            'text': obj,
                            'source': f'pattern_{i+1}',
                            'priority': self._calculate_objective_priority(obj),
                            'chapter': self._extract_chapter_context(text, match.start())
                        })
            
            print(f"  Pattern {i+1}: Found {len(pattern_objectives)} objectives")
            objectives.extend(pattern_objectives)
        
        # Also extract key definitions and concepts as pseudo-objectives
        definition_objectives = self._extract_key_definitions_as_objectives(text)
        objectives.extend(definition_objectives)
        print(f"  Definitions converted to objectives: {len(definition_objectives)}")
        
        deduplicated = self._deduplicate_objectives(objectives)
        print(f"  Final count after deduplication: {len(deduplicated)}")
        
        return deduplicated
    
    def _extract_key_definitions_as_objectives(self, text: str) -> List[Dict[str, str]]:
        """Extract key definitions and convert them to learning objectives"""
        definitions = []
        
        # Look for definition patterns
        definition_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*:\s*([^.\n]{20,200})',  # Term: definition
            r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+is\s+([^.\n]{20,200})',      # Term is definition
            r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+are\s+([^.\n]{20,200})',     # Terms are definition
        ]
        
        for pattern in definition_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                term = match.group(1).strip()
                definition = match.group(2).strip()
                
                # Filter for psychology-relevant terms
                if self._is_psychology_relevant(term) and len(definition) > 15:
                    objective_text = f"Define {term}"
                    definitions.append({
                        'text': objective_text,
                        'source': 'definition_extract',
                        'priority': self._calculate_objective_priority(term),
                        'chapter': 'Extracted',
                        'definition': definition,
                        'term': term
                    })
        
        return definitions
    
    def _is_psychology_relevant(self, term: str) -> bool:
        """Check if a term is relevant to psychology"""
        psychology_indicators = [
            'social', 'psychology', 'behavior', 'behaviour', 'cognitive', 'emotion',
            'personality', 'attitude', 'stereotype', 'bias', 'perception', 'memory',
            'learning', 'motivation', 'group', 'individual', 'research', 'theory',
            'experiment', 'study', 'analysis', 'development', 'interaction'
        ]
        
        term_lower = term.lower()
        return any(indicator in term_lower for indicator in psychology_indicators)
    
    def _parse_objective_list(self, text: str) -> List[str]:
        """Parse a block of text into individual learning objectives"""
        # Clean the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split by common list indicators
        split_patterns = [
            r'\n\s*[•\-\*]\s*',  # Bullet points
            r'\n\s*\d+\.?\s*',    # Numbered lists
            r'\n\s*[a-zA-Z]\.?\s*',  # Lettered lists
            r';\s*',              # Semicolon separated
            r'\.\s+(?=[A-Z])'     # Period + capital letter (new sentence)
        ]
        
        objectives = [text]  # Start with full text
        
        for pattern in split_patterns:
            new_objectives = []
            for obj in objectives:
                parts = re.split(pattern, obj)
                new_objectives.extend([p.strip() for p in parts if p.strip()])
            objectives = new_objectives
        
        return [obj for obj in objectives if len(obj) > 20]  # Filter short fragments
    
    def _is_valid_objective(self, objective: str) -> bool:
        """Validate learning objective quality based on PSYC2240 lessons learned"""
        if len(objective) < 20 or len(objective) > 200:
            return False
        
        # Must contain action verbs
        action_verbs = [
            'define', 'explain', 'describe', 'identify', 'analyze', 'compare',
            'contrast', 'evaluate', 'apply', 'understand', 'recognize',
            'distinguish', 'demonstrate', 'discuss', 'examine', 'interpret'
        ]
        
        if not any(verb in objective.lower() for verb in action_verbs):
            return False
        
        # Avoid personal anecdotes or irrelevant content
        avoid_patterns = [
            r'\bi\s+(think|feel|like|remember)',
            r'professor|instructor|teacher',
            r'homework|assignment|due',
            r'next week|last week|today'
        ]
        
        for pattern in avoid_patterns:
            if re.search(pattern, objective, re.IGNORECASE):
                return False
        
        return True
    
    def _calculate_objective_priority(self, objective: str) -> str:
        """Calculate priority based on social psychology relevance"""
        high_priority_terms = [
            'social psychology', 'stereotype', 'attribution', 'attitude',
            'conformity', 'social influence', 'group behavior', 'prejudice'
        ]
        
        medium_priority_terms = [
            'perception', 'cognition', 'behavior', 'interaction',
            'research', 'theory', 'method'
        ]
        
        obj_lower = objective.lower()
        
        if any(term in obj_lower for term in high_priority_terms):
            return 'high'
        elif any(term in obj_lower for term in medium_priority_terms):
            return 'medium'
        else:
            return 'low'
    
    def _extract_chapter_context(self, text: str, position: int) -> str:
        """Extract chapter context around the objective"""
        # Look backwards for chapter headers
        before_text = text[:position]
        chapter_match = re.search(r'chapter\s+(\d+)', before_text, re.IGNORECASE)
        if chapter_match:
            return f"Chapter {chapter_match.group(1)}"
        return "Unknown"
    
    def _deduplicate_objectives(self, objectives: List[Dict]) -> List[Dict]:
        """Remove duplicate objectives while preserving the best version"""
        seen = set()
        unique_objectives = []
        
        for obj in sorted(objectives, key=lambda x: (x['priority'] == 'high', len(x['text'])), reverse=True):
            # Create a normalized version for comparison
            normalized = re.sub(r'\s+', ' ', obj['text'].lower().strip())
            
            if normalized not in seen:
                seen.add(normalized)
                unique_objectives.append(obj)
        
        return unique_objectives
    
    def read_word_document(self, file_path: Path) -> str:
        """Read Word document content"""
        try:
            doc = Document(file_path)
            content = []
            
            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                if text:
                    content.append(text)
            
            return '\n'.join(content)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def read_lecture_transcript(self, file_path: Path) -> str:
        """Read lecture transcript"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading transcript {file_path}: {e}")
            return ""
    
    def analyze_test_focus(self) -> Dict[str, Any]:
        """Analyze Test 1 focus areas from cue sheet"""
        cue_sheet_path = self.source_materials / "Test 1 - Cue Sheet.docx"
        
        if not cue_sheet_path.exists():
            print("⚠️ Test 1 Cue Sheet not found - using general analysis")
            return {'chapters': [], 'topics': [], 'focus_areas': []}
        
        content = self.read_word_document(cue_sheet_path)
        
        return {
            'chapters': self._extract_chapters_from_text(content),
            'topics': self._extract_topics_from_text(content),
            'focus_areas': self._extract_focus_areas(content),
            'raw_content': content
        }
    
    def _extract_chapters_from_text(self, text: str) -> List[str]:
        """Extract chapter references"""
        chapters = []
        chapter_patterns = [
            r'chapter\s+(\d+)',
            r'ch\.?\s+(\d+)',
            r'section\s+(\d+)'
        ]
        
        for pattern in chapter_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                chapters.append(f"Chapter {match.group(1)}")
        
        return list(set(chapters))
    
    def _extract_topics_from_text(self, text: str) -> List[str]:
        """Extract key topics mentioned"""
        # This would be more sophisticated in practice
        topics = []
        for keyword in self.priority_keywords:
            if keyword.lower() in text.lower():
                topics.append(keyword)
        return topics
    
    def _extract_focus_areas(self, text: str) -> List[str]:
        """Extract specific focus areas for Test 1"""
        focus_patterns = [
            r'focus on\s+([^.!?\n]{10,100})',
            r'emphasis on\s+([^.!?\n]{10,100})',
            r'pay attention to\s+([^.!?\n]{10,100})',
            r'important[:\s]+([^.!?\n]{10,100})'
        ]
        
        focus_areas = []
        for pattern in focus_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                focus_areas.append(match.group(1).strip())
        
        return focus_areas
    
    def generate_improved_cards(self, analysis_data: Dict) -> List[Dict]:
        """Generate cards using LOQ-first methodology with improvements"""
        cards = []
        
        # PRIORITY 1: Learning Objectives (highest quality cards)
        print("🎯 Generating LOQ-based cards...")
        objective_cards = self._create_objective_cards(
            analysis_data.get('learning_objectives', []), 
            analysis_data  # Pass full content data for answer extraction
        )
        cards.extend(objective_cards)
        
        # PRIORITY 2: Cross-validated content
        print("✅ Generating cross-validated concept cards...")
        validated_cards = self._create_validated_concept_cards(analysis_data)
        cards.extend(validated_cards)
        
        # PRIORITY 3: Test-specific content
        print("📝 Generating Test 1 specific cards...")
        test_cards = self._create_test_specific_cards(analysis_data)
        cards.extend(test_cards)
        
        # Apply quality improvements based on PSYC2240 lessons
        cards = self._apply_quality_improvements(cards)
        
        return cards
    
    def _create_objective_cards(self, objectives: List[Dict], content_data: Dict = None) -> List[Dict]:
        """Create cards from learning objectives"""
        cards = []
        
        for obj_data in objectives:
            objective = obj_data['text']
            
            # Convert objective to question format
            question = self._objective_to_question(objective)
            answer = self._extract_answer_for_objective(objective, content_data)
            
            # Skip if answer is still placeholder
            if answer and "Answer to be extracted" not in answer:
                card = {
                    'front': question,
                    'back': answer,
                    'tags': f"PSYC2120 LOQ {obj_data['priority'].title()} {obj_data.get('chapter', '')}",
                    'source': 'Learning Objective',
                    'priority': obj_data['priority'],
                    'card_type': 'objective_based'
                }
                cards.append(card)
        
        return cards
    
    def _objective_to_question(self, objective: str) -> str:
        """Convert learning objective to natural question format"""
        objective = objective.strip()
        
        patterns = [
            (r'^define\s+(.+)', 'What is {}?'),
            (r'^explain\s+(.+)', 'How does {} work?'),
            (r'^describe\s+(.+)', 'What characterizes {}?'),
            (r'^identify\s+(.+)', 'What are {}?'),
            (r'^compare\s+(.+)', 'How do {} compare?'),
            (r'^analyze\s+(.+)', 'How do you analyze {}?'),
            (r'^understand\s+(.+)', 'What is important about {}?')
        ]
        
        for pattern, template in patterns:
            match = re.match(pattern, objective, re.IGNORECASE)
            if match:
                concept = match.group(1).strip()
                return template.format(concept)
        
        # Generic fallback - just clean up the objective
        clean_objective = re.sub(r'^(define|explain|describe|identify|analyze|understand)\s+', '', objective, flags=re.IGNORECASE)
        return f"What should you know about {clean_objective}?"
    
    def _extract_key_terms_from_objective(self, objective: str) -> List[str]:
        """Extract key searchable terms from learning objective"""
        # Remove action verbs and common words
        stop_words = {'define', 'explain', 'describe', 'identify', 'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'what', 'how', 'why', 'when', 'where'}
        
        # Clean up the objective text
        clean_text = re.sub(r'[^\w\s]', ' ', objective.lower())
        words = clean_text.split()
        
        # Filter out stop words and short words
        key_terms = [word for word in words if word not in stop_words and len(word) > 3]
        
        return key_terms[:5]  # Return top 5 key terms

    def _extract_answer_for_objective(self, objective: str, content_data: Dict = None) -> str:
        """Extract or generate answer for the objective using available content"""
        if not content_data:
            return "Answer to be extracted from content analysis"
        
        # Check if this is a definition-based objective
        if 'definition' in objective.lower():
            # Look for definition in extracted definitions
            for obj_data in content_data.get('learning_objectives', []):
                if obj_data.get('definition') and obj_data.get('term'):
                    if obj_data['term'].lower() in objective.lower():
                        return obj_data['definition']
        
        # Search through textbook content for relevant information
        textbook_content = content_data.get('textbook_content', '')
        
        # Extract key terms from the objective
        key_terms = self._extract_key_terms_from_objective(objective)
        
        # Find relevant sentences containing these terms
        sentences = re.split(r'[.!?]+', textbook_content)
        relevant_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Skip very short sentences
                term_matches = sum(1 for term in key_terms if term.lower() in sentence.lower())
                if term_matches >= 1:  # At least one term match
                    relevant_sentences.append(sentence)
        
        if relevant_sentences:
            # Return the most relevant sentence (first match for now)
            answer = relevant_sentences[0].strip()
            # Clean up and limit length
            if len(answer) > 200:
                answer = answer[:197] + '...'
            return answer
        
        return "Answer to be extracted from content analysis"
    
    def _create_validated_concept_cards(self, analysis_data: Dict) -> List[Dict]:
        """Create cards for concepts that appear in multiple sources"""
        # Implementation would cross-reference lecture and textbook content
        return []
    
    def _create_test_specific_cards(self, analysis_data: Dict) -> List[Dict]:
        """Create cards specifically focused on Test 1 content"""
        # Implementation would focus on cue sheet content
        return []
    
    def _apply_quality_improvements(self, cards: List[Dict]) -> List[Dict]:
        """Apply quality improvements based on PSYC2240 lessons learned"""
        improved_cards = []
        
        for card in cards:
            # Skip if answer is placeholder
            if "Answer to be extracted" in card['back']:
                continue
                
            # Ensure question format
            if not card['front'].endswith('?'):
                card['front'] += '?'
            
            # Ensure concise answers
            if len(card['back']) > 200:
                card['back'] = card['back'][:197] + '...'
            
            # Add improved tags
            card['tags'] = card['tags'].replace(' ', ' ').strip() + ' Optimized'
            
            improved_cards.append(card)
        
        return improved_cards
    
    def run_psyc2120_analysis(self):
        """Run complete PSYC2120 content analysis using proven workflow"""
        print("🚀 Starting PSYC2120 Content Analysis (Adapted from PSYC2240 Workflow)")
        
        analysis_data = {}
        
        # Step 1: Analyze test focus
        print("📋 Analyzing Test 1 requirements...")
        test_analysis = self.analyze_test_focus()
        analysis_data['test_focus'] = test_analysis
        
        # Step 2: Extract textbook content and Learning Objectives
        print("📚 Processing textbook content...")
        textbook_path = self.source_materials / "Textbook + Lecture Notes.docx"
        if textbook_path.exists():
            textbook_content = self.read_word_document(textbook_path)
            analysis_data['textbook_content'] = textbook_content
            analysis_data['learning_objectives'] = self.extract_learning_objectives(textbook_content)
            print(f"  📋 Found {len(analysis_data['learning_objectives'])} Learning Objectives")
        
        # Step 3: Process lecture transcripts
        print("🎓 Processing lecture transcripts...")
        lecture_data = []
        lecture_folders = [f for f in self.source_materials.iterdir() 
                          if f.is_dir() and 'Lecture' in f.name]
        
        for folder in sorted(lecture_folders):
            transcript_files = list(folder.glob("*.txt"))
            if transcript_files:
                content = self.read_lecture_transcript(transcript_files[0])
                lecture_data.append({
                    'folder': folder.name,
                    'content': content,
                    'concepts': self.extract_learning_objectives(content)  # Apply same method
                })
                print(f"  🎤 Processed {folder.name}")
        
        analysis_data['lectures'] = lecture_data
        
        # Step 4: Generate improved cards
        print("💳 Generating enhanced cards...")
        cards = self.generate_improved_cards(analysis_data)
        analysis_data['generated_cards'] = cards
        
        # Step 5: Save comprehensive analysis
        analysis_file = self.analysis_dir / "psyc2120_comprehensive_analysis.json"
        analysis_data['generation_date'] = datetime.now().isoformat()
        analysis_data['course_code'] = self.course_code
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Analysis complete!")
        print(f"   📊 Learning Objectives: {len(analysis_data.get('learning_objectives', []))}")
        print(f"   🎓 Lectures Processed: {len(analysis_data.get('lectures', []))}")
        print(f"   💳 Cards Generated: {len(cards)}")
        print(f"   📄 Saved to: {analysis_file}")
        
        return analysis_data

if __name__ == "__main__":
    extractor = PSYC2120ContentExtractor()
    analysis = extractor.run_psyc2120_analysis()