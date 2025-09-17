#!/usr/bin/env python3
"""
PSYC 2240 Audio-Transcript Analysis Tool
Compares audio files with existing transcripts to:
1. Verify transcript accuracy
2. Extract missed content  
3. Identify emphasis and context
4. Generate enhanced Anki cards with verified content
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import difflib

class AudioTranscriptAnalyzer:
    def __init__(self, workspace_path: str = "/workspaces/PSYC2240-Anki-Deck-Generator"):
        self.workspace_path = Path(workspace_path)
        self.audio_transcript_pairs = []
        self.analysis_results = {}
        
    def find_audio_transcript_pairs(self) -> List[Dict]:
        """Find all audio files and their corresponding transcripts"""
        pairs = []
        
        # Primary transcript location
        transcript_dir = self.workspace_path / "source" / "transcripts"
        
        # Course materials location  
        course_dir = self.workspace_path / "HH PSYC 2240 B - Biological Basis of Behaviour (Fall 2025-2026)"
        
        # Search both locations
        for directory in [transcript_dir, course_dir]:
            if directory.exists():
                for audio_file in directory.rglob("*.m4a"):
                    # Find corresponding transcript
                    txt_file = audio_file.with_suffix('.txt')
                    if txt_file.exists():
                        pairs.append({
                            'audio_path': str(audio_file),
                            'transcript_path': str(txt_file),
                            'filename': audio_file.stem,
                            'location': str(directory)
                        })
        
        self.audio_transcript_pairs = pairs
        return pairs
    
    def analyze_transcript_quality(self, transcript_path: str) -> Dict:
        """Analyze existing transcript for potential issues"""
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = {
            'total_length': len(content),
            'word_count': len(content.split()),
            'potential_errors': [],
            'technical_terms': [],
            'unclear_sections': [],
            'timestamps_present': bool(re.search(r'\d{1,2}:\d{2}', content)),
        }
        
        # Look for signs of transcription errors
        error_patterns = [
            (r'\b[A-Z]{2,}\b', 'ALL_CAPS_WORDS'),  # Often transcription errors
            (r'\b\w{1,2}\b\.', 'SINGLE_LETTERS'),   # Single letters often wrong
            (r'[^\w\s\.\,\?\!\:\;]', 'SPECIAL_CHARS'), # Unusual characters
            (r'\b(um|uh|like|you know)\b', 'FILLER_WORDS'),
        ]
        
        for pattern, error_type in error_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                analysis['potential_errors'].append({
                    'type': error_type,
                    'count': len(matches),
                    'examples': matches[:5]  # First 5 examples
                })
        
        # Identify neuroscience technical terms that need verification
        neuro_terms = [
            'neuron', 'synapse', 'neurotransmitter', 'dopamine', 'serotonin',
            'cortex', 'hippocampus', 'amygdala', 'cerebellum', 'brainstem',
            'action potential', 'myelin', 'axon', 'dendrite', 'plasticity',
            'GABA', 'acetylcholine', 'norepinephrine', 'vestibular'
        ]
        
        found_terms = []
        for term in neuro_terms:
            if re.search(r'\b' + re.escape(term) + r'\b', content, re.IGNORECASE):
                found_terms.append(term)
        analysis['technical_terms'] = found_terms
        
        # Look for unclear sections (multiple question marks, incomplete sentences)
        unclear_patterns = [
            r'[^\.\!\?]{50,}$',  # Long sentences without punctuation
            r'\?\?\?+',          # Multiple question marks
            r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b',  # Potential proper nouns that might be wrong
        ]
        
        for pattern in unclear_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                analysis['unclear_sections'].extend(matches[:3])
        
        return analysis
    
    def generate_verification_prompts(self, pair: Dict) -> List[str]:
        """Generate specific prompts for audio verification"""
        analysis = self.analyze_transcript_quality(pair['transcript_path'])
        
        prompts = [
            f"Please analyze the audio file '{pair['filename']}' and compare it with the existing transcript.",
            "Focus on:",
            "1. Technical neuroscience terminology accuracy",
            "2. Any content missed in the original transcription", 
            "3. Context and emphasis that affects meaning",
            "4. Proper names, citations, or references mentioned",
        ]
        
        if analysis['potential_errors']:
            prompts.append("5. Verification of flagged potential transcription errors:")
            for error in analysis['potential_errors'][:3]:
                prompts.append(f"   - {error['type']}: {error['examples'][:3]}")
        
        if analysis['technical_terms']:
            prompts.append(f"6. Verify these technical terms were transcribed correctly: {', '.join(analysis['technical_terms'][:10])}")
        
        return prompts
    
    def extract_key_concepts_from_transcript(self, transcript_path: str) -> List[Dict]:
        """Extract key concepts that should become Anki cards"""
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        concepts = []
        
        # Look for definition patterns
        definition_patterns = [
            r'(\w+(?:\s+\w+){0,2})\s+is\s+([^\.]{10,100})',
            r'(\w+(?:\s+\w+){0,2})\s+refers to\s+([^\.]{10,100})',
            r'(\w+(?:\s+\w+){0,2})\s+means\s+([^\.]{10,100})',
            r'(\w+(?:\s+\w+){0,2})\s+are\s+([^\.]{10,100})',
        ]
        
        for pattern in definition_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for term, definition in matches:
                concepts.append({
                    'type': 'definition',
                    'term': term.strip(),
                    'definition': definition.strip(),
                    'source': transcript_path
                })
        
        # Look for process descriptions
        process_patterns = [
            r'(when|if|during)\s+([^\.]{20,150})',
            r'(the process of|how)\s+([^\.]{20,150})',
        ]
        
        for pattern in process_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for trigger, process in matches:
                concepts.append({
                    'type': 'process',
                    'trigger': trigger.strip(),
                    'process': process.strip(),
                    'source': transcript_path
                })
        
        return concepts
    
    def run_analysis(self) -> Dict:
        """Run complete audio-transcript analysis"""
        print("🎧 Starting Audio-Transcript Analysis...")
        
        pairs = self.find_audio_transcript_pairs()
        print(f"📁 Found {len(pairs)} audio-transcript pairs")
        
        results = {
            'pairs_analyzed': len(pairs),
            'transcript_analyses': {},
            'verification_prompts': {},
            'extracted_concepts': {},
            'recommended_actions': []
        }
        
        for pair in pairs:
            filename = pair['filename']
            print(f"🔍 Analyzing: {filename}")
            
            # Analyze transcript quality
            transcript_analysis = self.analyze_transcript_quality(pair['transcript_path'])
            results['transcript_analyses'][filename] = transcript_analysis
            
            # Generate verification prompts
            verification_prompts = self.generate_verification_prompts(pair)
            results['verification_prompts'][filename] = verification_prompts
            
            # Extract concepts for Anki cards
            concepts = self.extract_key_concepts_from_transcript(pair['transcript_path'])
            results['extracted_concepts'][filename] = concepts
            
            print(f"   ✅ Found {len(concepts)} potential concepts")
            print(f"   ⚠️  {len(transcript_analysis['potential_errors'])} potential issues flagged")
        
        # Generate recommendations
        results['recommended_actions'] = self._generate_recommendations(results)
        
        return results
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        total_concepts = sum(len(concepts) for concepts in results['extracted_concepts'].values())
        total_errors = sum(len(analysis['potential_errors']) for analysis in results['transcript_analyses'].values())
        
        recommendations.append(f"📊 ANALYSIS SUMMARY:")
        recommendations.append(f"   • {results['pairs_analyzed']} audio files analyzed")
        recommendations.append(f"   • {total_concepts} potential concepts extracted")
        recommendations.append(f"   • {total_errors} potential transcription issues flagged")
        recommendations.append("")
        
        recommendations.append("🎯 RECOMMENDED ACTIONS:")
        recommendations.append("1. Listen to audio files to verify flagged transcription errors")
        recommendations.append("2. Cross-reference technical terms with audio for accuracy")
        recommendations.append("3. Extract any missed content that could become Anki cards")
        recommendations.append("4. Note professor emphasis for prioritizing card creation")
        recommendations.append("5. Identify clinical examples or case studies mentioned")
        
        if total_concepts > 50:
            recommendations.append("6. ⚠️  High concept density - prioritize overlap analysis")
        
        return recommendations
    
    def save_results(self, results: Dict, output_path: str = None):
        """Save analysis results to JSON file"""
        if output_path is None:
            output_path = self.workspace_path / "source" / "audio_transcript_analysis.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Analysis results saved to: {output_path}")

def main():
    """Run the audio-transcript analysis"""
    analyzer = AudioTranscriptAnalyzer()
    results = analyzer.run_analysis()
    analyzer.save_results(results)
    
    print("\n" + "="*60)
    print("🎧 AUDIO-TRANSCRIPT ANALYSIS COMPLETE")
    print("="*60)
    
    for recommendation in results['recommended_actions']:
        print(recommendation)
    
    print("\n📋 NEXT STEPS:")
    print("1. Review the generated analysis file")
    print("2. Use verification prompts to analyze audio files")
    print("3. Create enhanced Anki cards from verified content")
    print("4. Update comprehensive deck with audio-verified concepts")

if __name__ == "__main__":
    main()