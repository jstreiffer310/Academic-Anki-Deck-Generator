"""
Targeted fixer for:
- 'What characterizes Parkinson disease is enigmatic?' -> fix grammar
- Remove stray figure caption sentences like 'Figure 16-21 illustrates the extent of this system.'

Cards identified:
- PD_enigmatic: 1758156037338
- Figure sentence: 1758156037338, 1758156038224
"""

import requests
import re

ANKI_URL = 'http://127.0.0.1:8765'

PD_CARD_IDS = [1758156037338]
FIGURE_CARD_IDS = [1758156037338, 1758156038224]

PD_FIXES = [
    # Exact bad phrasing -> good phrasing
    (
        'What characterizes Parkinson disease is enigmatic?',
        'Why is Parkinson disease considered enigmatic?'
    ),
    # More general safety net
    (
        re.compile(r'^\s*What characterizes\s+(.+?)\s+is\s+enigmatic\?$', re.IGNORECASE),
        lambda m: f"Why is {m.group(1).strip()} considered enigmatic?"
    )
]

FIGURE_SENTENCE_PATTERNS = [
    re.compile(r'\bFigure\s*\d+[-–]\d+[^.]*\.', re.IGNORECASE),
    re.compile(r'\bFig\.?\s*\d+[-–]\d+[^.]*\.', re.IGNORECASE)
]


def anki(action, params=None):
    payload = {"action": action, "version": 6, "params": params or {}}
    r = requests.post(ANKI_URL, json=payload, timeout=20)
    return r.json()


def get_note_fields(card_id):
    ci = anki('cardsInfo', {"cards": [card_id]})['result'][0]
    ni = anki('notesInfo', {"notes": [ci['note']]})['result'][0]
    return ci['note'], ni['fields']


def fix_pd_enigmatic(card_id):
    note_id, fields = get_note_fields(card_id)
    q = fields['Question']['value']

    # Extract plain text for question for matching
    plain = re.sub(r'<[^>]+>', ' ', q)
    plain = re.sub(r'\s+', ' ', plain).strip()

    new_q = q
    for pat, repl in PD_FIXES:
        if isinstance(pat, str):
            if pat in plain:
                new_plain = plain.replace(pat, repl)
                new_q = q.replace(pat, repl)
                break
        else:
            m = pat.match(plain)
            if m:
                replacement = repl(m) if callable(repl) else repl
                # Replace the matched substring in the HTML too, best-effort
                new_q = q.replace(m.group(0), replacement)
                break

    if new_q == q:
        return False, 'no-change'

    res = anki('updateNoteFields', {
        'note': {
            'id': note_id,
            'fields': {
                'Question': new_q,
                'Answer': fields['Answer']['value'],
                'Priority': fields.get('Priority', {}).get('value', ''),
                'Source': fields.get('Source', {}).get('value', ''),
                'Chapter': fields.get('Chapter', {}).get('value', ''),
                'Clinical': fields.get('Clinical', {}).get('value', ''),
            }
        }
    })
    return (res.get('error') is None), res


def strip_figure_sentences(text_html):
    # Work on a plain-text proxy for detection
    plain = re.sub(r'<[^>]+>', ' ', text_html)
    plain = re.sub(r'\s+', ' ', plain)

    to_strip = []
    for pat in FIGURE_SENTENCE_PATTERNS:
        for m in pat.finditer(plain):
            to_strip.append(m.group(0))

    new_html = text_html
    for s in to_strip:
        new_html = new_html.replace(s, '')

    # Normalize extra spaces that may remain
    new_html = re.sub(r'\s{2,}', ' ', new_html)
    return new_html, len(to_strip)


def fix_figure_captions(card_id):
    note_id, fields = get_note_fields(card_id)
    q = fields['Question']['value']
    a = fields['Answer']['value']

    new_q, q_count = strip_figure_sentences(q)
    new_a, a_count = strip_figure_sentences(a)

    if q_count == 0 and a_count == 0:
        return False, 'no-figure-sentences'

    res = anki('updateNoteFields', {
        'note': {
            'id': note_id,
            'fields': {
                'Question': new_q,
                'Answer': new_a,
                'Priority': fields.get('Priority', {}).get('value', ''),
                'Source': fields.get('Source', {}).get('value', ''),
                'Chapter': fields.get('Chapter', {}).get('value', ''),
                'Clinical': fields.get('Clinical', {}).get('value', ''),
            }
        }
    })
    return (res.get('error') is None), {'q_removed': q_count, 'a_removed': a_count, 'raw': res}


def main():
    print('Fixing PD enigmatic question...')
    for cid in PD_CARD_IDS:
        ok, info = fix_pd_enigmatic(cid)
        print('  ', cid, '->', 'OK' if ok else 'NO-CHANGE', info)

    print('\nStripping figure captions...')
    for cid in FIGURE_CARD_IDS:
        ok, info = fix_figure_captions(cid)
        print('  ', cid, '->', 'OK' if ok else 'NO-CHANGE', info)

if __name__ == '__main__':
    main()
