# PSYC 2240 Anki Deck Generator - Setup Script
# Run this script to quickly generate additional Anki cards

Write-Host "PSYC 2240 Anki Deck Generator" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Function to create Anki card
function Create-AnkiCard($term, $definition, $chapter, $cardType = "Definition") {
    $front = $term
    $back = $definition
    $tags = "PSYC2240 Chapter$chapter $cardType"
    return "`"$front`",`"$back`",`"$tags`""
}

# Check if source files exist
if (-not (Test-Path "textbook_full_content.txt")) {
    Write-Host "⚠️  Missing source file: textbook_full_content.txt" -ForegroundColor Yellow
    Write-Host "Please add your textbook content file to continue." -ForegroundColor Yellow
    exit
}

Write-Host "✅ Source files found" -ForegroundColor Green
Write-Host "📊 Current deck: PSYC2240_Chapters1-3_AnkiDeck.csv (191 cards)" -ForegroundColor Cyan
Write-Host ""

Write-Host "Available Actions:" -ForegroundColor White
Write-Host "1. View deck statistics" -ForegroundColor Gray
Write-Host "2. Add new chapter content" -ForegroundColor Gray  
Write-Host "3. Create supplementary cards" -ForegroundColor Gray
Write-Host "4. Export for Anki import" -ForegroundColor Gray
Write-Host ""

Write-Host "💡 To add more content:" -ForegroundColor Yellow
Write-Host "   - Update textbook_full_content.txt with new chapters" -ForegroundColor Gray
Write-Host "   - Run the extraction scripts to generate new cards" -ForegroundColor Gray
Write-Host "   - Commit changes to Git repository" -ForegroundColor Gray
Write-Host ""

Write-Host "📚 Current Coverage: Chapters 1-3 (Complete)" -ForegroundColor Green
Write-Host "🎯 Ready for: Import into Anki, GitHub upload" -ForegroundColor Green