#!/bin/bash
# Cross-platform setup script for PSYC 2240 Anki Deck Generator

echo "🎓 PSYC 2240 Anki Deck Generator"
echo "================================="
echo ""

# Check if PowerShell is available
if command -v pwsh >/dev/null 2>&1; then
    echo "✅ PowerShell Core (pwsh) available"
    POWERSHELL_CMD="pwsh"
elif command -v powershell >/dev/null 2>&1; then
    echo "✅ PowerShell available"
    POWERSHELL_CMD="powershell"
else
    echo "❌ PowerShell not found. Installing..."
    if command -v apt >/dev/null 2>&1; then
        sudo apt update && sudo apt install -y powershell
    elif command -v apk >/dev/null 2>&1; then
        sudo apk add --no-cache powershell
    elif command -v yum >/dev/null 2>&1; then
        sudo yum install -y powershell
    elif command -v brew >/dev/null 2>&1; then
        brew install powershell
    else
        echo "Unable to install PowerShell automatically. Please install manually."
        exit 1
    fi
    POWERSHELL_CMD="pwsh"
fi

# Run the PowerShell setup script
echo ""
echo "🔧 Running PowerShell setup..."
$POWERSHELL_CMD scripts/setup.ps1

echo ""
echo "💡 Available commands:"
echo "   ./setup.sh                    - Run this setup"
echo "   pwsh scripts/setup.ps1        - Check project status"
echo "   pwsh scripts/extract_*.ps1    - Process content (needs path updates)"
echo "   wc -l decks/*.csv             - Count cards in decks"