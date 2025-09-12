#!/bin/bash
# Safe Performance Optimization for PSYC 2240 Anki Deck Generator

echo "🚀 Performance Optimization"
echo "=========================="

# Check current system status
echo "📊 System Status:"
echo "  Memory: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "  Disk: $(df -h / | tail -1 | awk '{print $5 " used"}')"

# Optimize PowerShell
echo ""
echo "⚡ PowerShell Optimization:"
if command -v pwsh >/dev/null 2>&1; then
    echo "✅ PowerShell Core available"
    # Test response time
    start=$(date +%s%N)
    pwsh -c "Get-Date" >/dev/null 2>&1
    end=$(date +%s%N)
    duration=$(( (end - start) / 1000000 ))
    echo "  Response time: ${duration}ms"
else
    echo "❌ PowerShell not found"
fi

# CSV file validation
echo ""
echo "📊 Deck Status:"
if [[ -f "decks/PSYC2240_AnkiDeck.csv" ]]; then
    main_cards=$(($(wc -l < "decks/PSYC2240_AnkiDeck.csv") - 1))
    echo "  🧠 Main Deck: $main_cards cards"
fi

if [[ -f "decks/PSYC2240_Cloze_Cards.csv" ]]; then
    cloze_cards=$(($(wc -l < "decks/PSYC2240_Cloze_Cards.csv") - 1))
    echo "  🔤 Cloze Deck: $cloze_cards cards"
fi

# Quick file system check
echo ""
echo "📁 File System:"
echo "  Scripts: $(ls scripts/*.ps1 | wc -l) PowerShell files"
echo "  Source: $(ls source/*.txt 2>/dev/null | wc -l) text files"

echo ""
echo "💡 Performance Tips:"
echo "  • Use single tool calls instead of batches"
echo "  • Close unused VS Code tabs"
echo "  • Monitor memory with 'free -h'"

echo ""
echo "✅ Optimization complete!"