import pandas as pd
import requests

def import_excel_edits():
    """Import edited cards from Excel back to Anki"""
    url = "http://127.0.0.1:8765"
    
    try:
        df = pd.read_excel("PSYC2240_Cards_Export_EDITED.xlsx", sheet_name="All_Cards")
        print(f"Importing {len(df)} card edits...")
        
        success_count = 0
        for i, row in df.iterrows():
            if i % 50 == 0:
                print(f"Importing {i}/{len(df)}...")
                
            try:
                note_id = row["Note_ID"]
                result = requests.post(url, json={
                    "action": "updateNoteFields",
                    "version": 6,
                    "params": {
                        "note": {
                            "id": note_id,
                            "fields": {
                                "Question": row["Question_Clean"],
                                "Answer": row["Answer_Clean"],
                                "Priority": row["Priority"],
                                "Source": row["Source"],
                                "Chapter": row["Chapter"],
                                "Clinical": row["Clinical"]
                            }
                        }
                    }
                })
                
                if result.json().get("error") is None:
                    success_count += 1
                    
            except Exception as e:
                print(f"Error processing row {i}: {e}")
        
        print(f"Successfully imported {success_count}/{len(df)} edits")
        
    except FileNotFoundError:
        print("Please save your Excel file as 'PSYC2240_Cards_Export_EDITED.xlsx' first!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import_excel_edits()
