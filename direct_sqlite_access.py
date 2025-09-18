# Direct Anki Database Access
# Find your Anki profile folder and access collection.anki2 directly

import sqlite3
import os
from pathlib import Path

def find_anki_database():
    """Find Anki collection database"""
    # Common Anki profile locations
    possible_paths = [
        Path.home() / "AppData" / "Roaming" / "Anki2" / "User 1" / "collection.anki2",  # Windows
        Path.home() / "Documents" / "Anki2" / "User 1" / "collection.anki2",  # Windows alt
        Path.home() / "Library" / "Application Support" / "Anki2" / "User 1" / "collection.anki2",  # macOS
        Path.home() / ".local" / "share" / "Anki2" / "User 1" / "collection.anki2",  # Linux
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    print("Anki database not found. Please locate your collection.anki2 file manually.")
    return None

def direct_edit_cards():
    """Edit cards directly in SQLite database"""
    db_path = find_anki_database()
    if not db_path:
        return
    
    # BACKUP FIRST!
    backup_path = db_path.replace(".anki2", "_backup.anki2")
    import shutil
    shutil.copy2(db_path, backup_path)
    print(f"Backup created: {backup_path}")
    
    # Connect and edit
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Example: Fix common issues
    cursor.execute("""
        UPDATE notes 
        SET flds = REPLACE(flds, '  ', ' ')  -- Remove double spaces
        WHERE flds LIKE '%PSYC2240%'
    """)
    
    conn.commit()
    conn.close()
    print("Direct database edits completed!")

if __name__ == "__main__":
    direct_edit_cards()