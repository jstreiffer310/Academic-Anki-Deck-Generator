#!/usr/bin/env python3
"""
Academic Anki Deck Generator - Course Setup Tool
Creates new course structure from template for multi-class support
"""

import os
import shutil
import json
import sys
from pathlib import Path

def create_new_course(course_code, course_name, semester="", textbook=""):
    """Create new course directory structure"""
    
    # Validate course code
    if not course_code or not course_code.isalnum():
        print("❌ Course code must be alphanumeric (e.g., PSYC2240, MATH101)")
        return False
    
    # Paths
    repo_root = Path(__file__).parent
    template_path = repo_root / "templates" / "course-template"
    course_path = repo_root / "courses" / course_code
    
    # Check if course already exists
    if course_path.exists():
        print(f"❌ Course {course_code} already exists!")
        return False
    
    # Check if template exists
    if not template_path.exists():
        print("❌ Course template not found!")
        return False
    
    try:
        # Copy template
        print(f"📂 Creating course structure for {course_code}...")
        shutil.copytree(template_path, course_path)
        
        # Update course configuration
        config_path = course_path / "course_config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Update with provided information
            config["course_code"] = course_code
            config["course_name"] = course_name or f"{course_code} Course"
            config["semester"] = semester or "Term Year"
            config["textbook_title"] = textbook or "Primary Textbook"
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
        
        # Create course-specific README
        readme_path = course_path / "README.md"
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                readme_content = f.read()
            
            # Replace template placeholders
            readme_content = readme_content.replace("[COURSE_CODE]", course_code)
            readme_content = readme_content.replace("Template Course Name", course_name or f"{course_code} Course")
            
            with open(readme_path, 'w') as f:
                f.write(readme_content)
        
        print(f"✅ Course {course_code} created successfully!")
        print(f"📁 Location: {course_path}")
        print(f"📖 Next steps:")
        print(f"   1. Add textbook PDFs to courses/{course_code}/content/textbook/")
        print(f"   2. Add lecture materials to courses/{course_code}/content/lectures/")
        print(f"   3. Configure course_config.json with specific settings")
        print(f"   4. Use shared tools to generate cards")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating course: {e}")
        return False

def list_courses():
    """List all existing courses"""
    repo_root = Path(__file__).parent
    courses_path = repo_root / "courses"
    
    if not courses_path.exists():
        print("❌ No courses directory found!")
        return
    
    courses = [d for d in courses_path.iterdir() if d.is_dir()]
    
    if not courses:
        print("📚 No courses found.")
        return
    
    print("📚 Existing Courses:")
    for course_dir in sorted(courses):
        config_path = course_dir / "course_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                course_name = config.get("course_name", "Unknown")
                semester = config.get("semester", "")
                print(f"   • {course_dir.name}: {course_name} ({semester})")
            except:
                print(f"   • {course_dir.name}: Configuration error")
        else:
            print(f"   • {course_dir.name}: No configuration found")

def main():
    """Main execution"""
    if len(sys.argv) < 2:
        print("🎓 ACADEMIC ANKI DECK GENERATOR - COURSE SETUP")
        print("=" * 55)
        print("Create optimized flashcard decks for any academic course")
        print()
        print("Usage:")
        print("  python course_setup.py create COURSE_CODE [COURSE_NAME] [SEMESTER] [TEXTBOOK]")
        print("  python course_setup.py list")
        print()
        print("Examples:")
        print("  python course_setup.py create PSYC3100 'Cognitive Psychology' 'Fall 2024'")
        print("  python course_setup.py create MATH201 'Calculus II'")
        print("  python course_setup.py create HIST150 'World History'")
        print("  python course_setup.py list")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_courses()
    elif command == "create":
        if len(sys.argv) < 3:
            print("❌ Course code required!")
            return
        
        course_code = sys.argv[2]
        course_name = sys.argv[3] if len(sys.argv) > 3 else ""
        semester = sys.argv[4] if len(sys.argv) > 4 else ""
        textbook = sys.argv[5] if len(sys.argv) > 5 else ""
        
        create_new_course(course_code, course_name, semester, textbook)
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'create' or 'list'")

if __name__ == "__main__":
    main()