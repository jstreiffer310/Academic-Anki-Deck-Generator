# Create Perfect Anki Deck from Scratch
import genanki
import pandas as pd
import hashlib

def create_clean_deck():
    """Create a new, clean PSYC2240 deck"""
    
    # Read our cleaned data
    df = pd.read_excel("PSYC2240_Cards_Export.xlsx", sheet_name="All_Cards")
    
    # Create clean note type (no CSS bloat)
    note_type = genanki.Model(
        1607392319,  # Unique ID
        'PSYC2240 Clean',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
            {'name': 'Priority'},
            {'name': 'Source'},
            {'name': 'Chapter'},
            {'name': 'Clinical'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '''
                <div class="question">{{Question}}</div>
                <div class="meta">{{#Priority}}Priority: {{Priority}} | {{/Priority}}Chapter {{Chapter}}</div>
                ''',
                'afmt': '''
                <div class="question">{{Question}}</div>
                <hr>
                <div class="answer">{{Answer}}</div>
                <div class="meta">
                    {{#Priority}}Priority: {{Priority}} | {{/Priority}}
                    Chapter {{Chapter}}
                    {{#Clinical}} | Clinical{{/Clinical}}
                    {{#Source}} | {{Source}}{{/Source}}
                </div>
                ''',
            },
        ],
        css="""
        .card { font-family: arial; font-size: 16px; }
        .question { font-weight: bold; margin-bottom: 10px; }
        .answer { margin: 10px 0; }
        .meta { font-size: 12px; color: #666; border-top: 1px solid #ddd; padding-top: 5px; }
        """
    )
    
    # Create deck
    deck = genanki.Deck(
        2059400110,  # Unique ID
        'PSYC2240 - Clean Rebuild'
    )
    
    # Add cards
    for _, row in df.iterrows():
        note = genanki.Note(
            model=note_type,
            fields=[
                row['Question_Clean'],
                row['Answer_Clean'], 
                row['Priority'],
                row['Source'],
                row['Chapter'],
                row['Clinical']
            ]
        )
        deck.add_note(note)
    
    # Export
    genanki.Package(deck).write_to_file('PSYC2240_Clean_Rebuild.apkg')
    print(f"Created clean deck: PSYC2240_Clean_Rebuild.apkg ({len(df)} cards)")

if __name__ == "__main__":
    create_clean_deck()