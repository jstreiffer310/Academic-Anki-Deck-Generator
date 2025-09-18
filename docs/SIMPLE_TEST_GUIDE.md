# 🎯 SIMPLE TESTING STEPS

## What You Need to Do Next:

### 1. ✅ ALREADY DONE:
- AnkiConnect installed (v.6) ✅
- VS Code extension installed ✅ 
- Settings configured ✅
- Test cards created ✅

### 2. 🧪 TEST THE WORKFLOW:

**Step A: Open Anki on your main computer**
- Make sure your PSYC 2240 deck is loaded
- Keep Anki running in the background

**Step B: Test in VS Code**
1. Open the file: `test-cards.md`
2. Put your cursor on the first question
3. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
4. Type "anki" and look for commands like:
   - "Anki: Send note to Anki"
   - "Anki: Send card to deck"
5. Select the send command
6. Check Anki to see if the card appeared!

**Step C: If it works, try the organized cards**
1. Open any file in the `anki-cards/` folder
2. Try sending those cards the same way

### 3. 🎯 WHAT TO EXPECT:

**SUCCESS**: Cards appear in your Anki deck with the question as front, answer as back

**PROBLEMS**: 
- "AnkiConnect not found" → Make sure Anki is running
- "Deck not found" → Check that your deck names match in Anki
- Nothing happens → Try different Anki commands in the command palette

### 4. 📁 YOUR NEW FILES:

```
/workspaces/PSYC2240-Anki-Deck-Generator/
├── test-cards.md           ← Start here for testing
├── anki-cards/
│   ├── high-priority.md    ← Clinical cases, exam-critical  
│   ├── medium-priority.md  ← Important concepts
│   └── low-priority.md     ← Background facts
└── .vscode/settings.json   ← Configuration (done)
```

### 5. ⚡ QUICK REFERENCE:

**Main VS Code Command**: `Ctrl+Shift+P` → search "anki"

**Card Format**:
```markdown
## Question goes here?

Answer goes here.

Tags: priority-level, topic, PSYC2240
```

**Ready to test! Start with `test-cards.md` and see if cards appear in Anki!** 🚀