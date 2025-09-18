# 🏠 Move to Local Setup - Quick Guide

## 🚀 Simple Steps to Work Locally

### 1. Download Repository
**Option A: Download ZIP**
- Go to: https://github.com/jstreiffer310/PSYC2240-Anki-Deck-Generator
- Click green **"Code"** button → **"Download ZIP"**
- Extract to your preferred folder

**Option B: Git Clone** (if you have Git)
```bash
git clone https://github.com/jstreiffer310/PSYC2240-Anki-Deck-Generator.git
```

### 2. Open in Local VS Code
- Open VS Code on your computer
- **File** → **Open Folder** → Select the downloaded folder
- All settings are already configured!

### 3. Verify Anki Integration
- Make sure **Anki is running** with AnkiConnect installed
- Open `test-cards.md`
- **Ctrl+Shift+P** → search "anki" → try "Send to Anki"
- Should work perfectly now!

## 🎯 What You'll Get Locally:

✅ **Direct AnkiConnect access** - no network issues
✅ **Faster performance** - no cloud delays  
✅ **Full VS Code integration** - create cards seamlessly
✅ **Your 829-card deck** ready to import
✅ **FSRS optimization** already configured

## 📁 Your Local Workflow:

1. **Import main deck**: `output/PSYC2240_Consolidated_Deck.apkg`
2. **Use FSRS settings**: Follow `output/FSRS_SETUP_GUIDE.md`
3. **Create supplemental cards**: Use `anki-cards/` templates
4. **Study daily**: Optimized for October 8th exam

## 🔧 Settings Already Configured:

The `.vscode/settings.json` will automatically work with localhost when you're local:
```json
{
    "anki.api.hostname": "127.0.0.1",
    "anki.api.port": 8765,
    "anki.api.schema": "http"
}
```

**Ready to download and work locally? This will solve all the connection issues instantly!** 🎉