# PSYC 2240 Anki Deck Generator - Codespace Setup
# Optimized for memory retention and effective learning

Write-Host "🎓 PSYC 2240 Anki Deck Generator" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Check directory structure
$directories = @("decks", "scripts", "source", "docs")
foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host "✅ $dir/ directory ready" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing $dir/ directory" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📚 Available Anki Decks:" -ForegroundColor Cyan

if (Test-Path "decks/PSYC2240_AnkiDeck.csv") {
    $mainCards = (Get-Content "decks/PSYC2240_AnkiDeck.csv" | Measure-Object -Line).Lines - 1
    Write-Host "   🧠 Main Deck: $mainCards optimized cards" -ForegroundColor White
} else {
    Write-Host "   ❌ Main deck not found" -ForegroundColor Red
}

if (Test-Path "decks/PSYC2240_Cloze_Cards.csv") {
    $clozeCards = (Get-Content "decks/PSYC2240_Cloze_Cards.csv" | Measure-Object -Line).Lines - 1
    Write-Host "   🔤 Cloze Deck: $clozeCards fill-in-the-blank cards" -ForegroundColor White
} else {
    Write-Host "   ❌ Cloze deck not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 Quick Actions:" -ForegroundColor Yellow
Write-Host "   📥 Download: Click links in README.md" -ForegroundColor Gray
Write-Host "   📊 View CSV: Open files in VS Code" -ForegroundColor Gray
Write-Host "   ⚙️  Modify: Edit source files and regenerate" -ForegroundColor Gray
Write-Host "   🔄 Update: Run extraction scripts for new content" -ForegroundColor Gray

Write-Host ""
Write-Host "🚀 Ready for Anki import and study!" -ForegroundColor Green
Write-Host "   Total study cards available: $($mainCards + $clozeCards)" -ForegroundColor Cyan

# Function to create new cards (for future use)
function Create-OptimizedCard($front, $back, $chapter, $cardType = "Optimized") {
    $tags = "PSYC2240 Chapter$chapter $cardType"
    return "`"$front`",`"$back`",`"$tags`""
}

Write-Host ""
Write-Host "💡 Codespace ready! Use VS Code to:" -ForegroundColor White
Write-Host "   - View and edit CSV files" -ForegroundColor Gray
Write-Host "   - Run PowerShell scripts" -ForegroundColor Gray
Write-Host "   - Add new content" -ForegroundColor Gray
Write-Host "   - Commit changes to GitHub" -ForegroundColor Gray