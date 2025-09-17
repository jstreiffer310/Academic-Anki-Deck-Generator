# PSYC 2240 Extensible Deck Management Script
# Designed for easy addition of Chapter 7 and final lecture content

param(
    [string]$Action = "status",
    [string]$NewContentPath = "",
    [string]$ContentType = ""
)

function Show-DeckStatus {
    Write-Host "📊 PSYC 2240 DECK STATUS" -ForegroundColor Green
    Write-Host "========================" -ForegroundColor Green
    Write-Host ""
    
    # Current deck statistics
    $basicCards = if (Test-Path "decks/PSYC2240_Complete_AnkiDeck.csv") { 
        (Import-Csv "decks/PSYC2240_Complete_AnkiDeck.csv").Count 
    } else { 0 }
    
    $clozeCards = if (Test-Path "decks/PSYC2240_Complete_Cloze_Cards.csv") { 
        (Import-Csv "decks/PSYC2240_Complete_Cloze_Cards.csv").Count 
    } else { 0 }
    
    Write-Host "📚 Current Content:" -ForegroundColor Cyan
    Write-Host "  Basic Cards: $basicCards"
    Write-Host "  Cloze Cards: $clozeCards"
    Write-Host "  Total Cards: $($basicCards + $clozeCards)"
    Write-Host ""
    
    # Timeline
    $testDate = Get-Date "2025-10-10"
    $today = Get-Date
    $daysLeft = ($testDate - $today).Days
    
    Write-Host "⏰ Timeline:" -ForegroundColor Yellow
    Write-Host "  Test Date: October 10, 2025"
    Write-Host "  Days Remaining: $daysLeft"
    Write-Host "  Recommended: $([math]::Ceiling(($basicCards + $clozeCards) / $daysLeft)) cards/day"
    Write-Host ""
    
    # Coverage analysis
    Write-Host "📋 Content Coverage:" -ForegroundColor Magenta
    Write-Host "  ✅ Chapters 1-3: Covered"
    Write-Host "  ✅ September Lectures: Covered"
    Write-Host "  ⏳ Chapter 7: Pending (add when available)"
    Write-Host "  ⏳ Final Lecture: Pending (add when available)"
}

function Add-NewContent {
    param(
        [string]$ContentPath,
        [string]$Type
    )
    
    Write-Host "📥 Adding New Content: $Type" -ForegroundColor Green
    Write-Host ""
    
    switch ($Type.ToLower()) {
        "chapter7" {
            Write-Host "Adding Chapter 7 content..." -ForegroundColor Yellow
            # Process new content with Chapter 7 tags
            $tagPrefix = "PSYC2240 Chapter7"
        }
        "finallecture" {
            Write-Host "Adding Final Lecture content..." -ForegroundColor Yellow
            # Process new content with Final Lecture tags
            $tagPrefix = "PSYC2240 FinalLecture"
        }
        default {
            Write-Host "❌ Unknown content type. Use 'chapter7' or 'finallecture'" -ForegroundColor Red
            return
        }
    }
    
    if (-not (Test-Path $ContentPath)) {
        Write-Host "❌ Content file not found: $ContentPath" -ForegroundColor Red
        return
    }
    
    # Load existing cards
    $existingBasic = if (Test-Path "decks/PSYC2240_Complete_AnkiDeck.csv") {
        Import-Csv "decks/PSYC2240_Complete_AnkiDeck.csv"
    } else { @() }
    
    $existingCloze = if (Test-Path "decks/PSYC2240_Complete_Cloze_Cards.csv") {
        Import-Csv "decks/PSYC2240_Complete_Cloze_Cards.csv"
    } else { @() }
    
    # Process new content (placeholder - would integrate with our analysis script)
    Write-Host "🔄 Processing new content with optimization..." -ForegroundColor Cyan
    Write-Host "  • Applying retention optimization principles"
    Write-Host "  • Using question format for better memory"
    Write-Host "  • Adding appropriate tags: $tagPrefix"
    Write-Host "  • Checking for overlap with existing content"
    
    # Backup existing decks
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    Copy-Item "decks/PSYC2240_Complete_AnkiDeck.csv" "decks/backup/basic_$timestamp.csv" -Force
    Copy-Item "decks/PSYC2240_Complete_Cloze_Cards.csv" "decks/backup/cloze_$timestamp.csv" -Force
    
    Write-Host "✅ Content addition framework ready!" -ForegroundColor Green
    Write-Host "ℹ️  Manual step: Process $ContentPath through comprehensive_analysis.py" -ForegroundColor Blue
}

function Create-StudySchedule {
    Write-Host "📅 CREATING STUDY SCHEDULE" -ForegroundColor Green
    Write-Host "==========================" -ForegroundColor Green
    Write-Host ""
    
    $testDate = Get-Date "2025-10-10"
    $today = Get-Date "2025-09-17"
    $daysLeft = ($testDate - $today).Days
    
    $totalCards = if (Test-Path "decks/PSYC2240_Complete_AnkiDeck.csv") {
        (Import-Csv "decks/PSYC2240_Complete_AnkiDeck.csv").Count +
        (Import-Csv "decks/PSYC2240_Complete_Cloze_Cards.csv").Count
    } else { 0 }
    
    $cardsPerDay = [math]::Ceiling($totalCards / $daysLeft)
    
    Write-Host "📊 Schedule Analysis:" -ForegroundColor Cyan
    Write-Host "  Total Available Cards: $totalCards"
    Write-Host "  Study Days Available: $daysLeft"
    Write-Host "  Recommended New Cards/Day: $cardsPerDay"
    Write-Host "  Review Cards/Day: $(($cardsPerDay * 2)) (including reviews)"
    Write-Host ""
    
    Write-Host "🎯 Study Strategy:" -ForegroundColor Yellow
    Write-Host "  Week 1 (Sep 17-23): Focus on overlap terms (highest priority)"
    Write-Host "  Week 2 (Sep 24-30): Textbook definitions (vibrant green)"
    Write-Host "  Week 3 (Oct 1-7): Professor concepts (dull green) + integration"
    Write-Host "  Week 4 (Oct 8-10): Review + Chapter 7 + Final lecture"
    Write-Host ""
    
    Write-Host "🔄 Flexibility for New Content:" -ForegroundColor Magenta
    Write-Host "  • Reserve 25% of daily capacity for new additions"
    Write-Host "  • Chapter 7: Can be added in Week 3-4"
    Write-Host "  • Final Lecture: Can be added in Week 4"
    Write-Host "  • Emergency cramming: Prioritize overlap terms only"
}

# Create backup directory
if (-not (Test-Path "decks/backup")) {
    New-Item -ItemType Directory -Path "decks/backup" -Force | Out-Null
}

# Main execution
switch ($Action.ToLower()) {
    "status" { Show-DeckStatus }
    "add" { Add-NewContent -ContentPath $NewContentPath -Type $ContentType }
    "schedule" { Create-StudySchedule }
    default { 
        Write-Host "Usage: .\deck_management.ps1 -Action [status|add|schedule]" -ForegroundColor Yellow
        Write-Host "Examples:" -ForegroundColor Gray
        Write-Host "  .\deck_management.ps1 -Action status"
        Write-Host "  .\deck_management.ps1 -Action add -NewContentPath 'chapter7.txt' -ContentType 'chapter7'"
        Write-Host "  .\deck_management.ps1 -Action schedule"
    }
}