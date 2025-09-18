#!/bin/bash#!/bin/bash

# Cross-platform setup script for PSYC 2240 Anki Deck Generator

# PSYC 2240 Anki Integration - Quick Setup

# ========================================echo "🎓 PSYC 2240 Anki Deck Generator"

echo "================================="

echo "🧠 PSYC 2240 Anki Deck Generator"echo ""

echo "================================"

echo ""# Check if PowerShell is available

if command -v pwsh >/dev/null 2>&1; then

# Check what user wants to do    echo "✅ PowerShell Core (pwsh) available"

echo "What would you like to do?"    POWERSHELL_CMD="pwsh"

echo ""elif command -v powershell >/dev/null 2>&1; then

echo "1) 📚 Use the main study deck (829 cards)"    echo "✅ PowerShell available"

echo "2) 🔗 Set up VS Code → Anki integration"     POWERSHELL_CMD="powershell"

echo "3) 🧪 Test existing connection"else

echo "4) 📖 View documentation"    echo "❌ PowerShell not found. Installing..."

echo ""    if command -v apt >/dev/null 2>&1; then

        sudo apt update && sudo apt install -y powershell

read -p "Enter choice (1-4): " choice    elif command -v apk >/dev/null 2>&1; then

        sudo apk add --no-cache powershell

case $choice in    elif command -v yum >/dev/null 2>&1; then

    1)        sudo yum install -y powershell

        echo ""    elif command -v brew >/dev/null 2>&1; then

        echo "📦 MAIN STUDY DECK SETUP"        brew install powershell

        echo "========================"    else

        echo ""        echo "Unable to install PowerShell automatically. Please install manually."

        echo "Your 829-card PSYC 2240 deck is ready!"        exit 1

        echo ""    fi

        echo "📍 Location: output/PSYC2240_Consolidated_Deck.apkg"    POWERSHELL_CMD="pwsh"

        echo "📖 Setup Guide: output/FSRS_SETUP_GUIDE.md"fi

        echo ""

        echo "🚀 Next steps:"# Run the PowerShell setup script

        echo "   1. Download the .apkg file to your computer"echo ""

        echo "   2. Import to Anki: File → Import"echo "🔧 Running PowerShell setup..."

        echo "   3. Configure FSRS using the setup guide"$POWERSHELL_CMD scripts/setup.ps1

        echo "   4. Start studying!"

        echo ""echo ""

        ;;echo "💡 Available commands:"

    2)echo "   ./setup.sh                    - Run this setup"

        echo ""echo "   pwsh scripts/setup.ps1        - Check project status"

        echo "🔗 VS CODE INTEGRATION SETUP"echo "   pwsh scripts/extract_*.ps1    - Process content (needs path updates)"

        echo "============================"echo "   wc -l decks/*.csv             - Count cards in decks"
        echo ""
        echo "Setting up live card creation from VS Code..."
        cd setup && ./connect_to_anki.sh
        ;;
    3)
        echo ""
        echo "🧪 TESTING CONNECTION"
        echo "===================="
        echo ""
        cd setup && ./test_connection.sh
        ;;
    4)
        echo ""
        echo "📖 DOCUMENTATION"
        echo "================"
        echo ""
        echo "Available guides:"
        echo "• docs/SIMPLE_TEST_GUIDE.md - Quick VS Code setup"
        echo "• docs/ANKI_VSCODE_INTEGRATION.md - Detailed integration guide"
        echo "• docs/CODESPACE_ANKI_SETUP.md - Codespace-specific setup"
        echo "• output/FSRS_SETUP_GUIDE.md - Deck optimization"
        echo ""
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        ;;
esac

echo ""
echo "💡 For more help, check the README.md or docs/ directory"
echo "🎯 Goal: Ace your October 8th PSYC 2240 exam!"