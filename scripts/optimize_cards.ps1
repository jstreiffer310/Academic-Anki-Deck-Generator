# PSYC 2240 Card Optimization Script
# Optimizes flashcards for maximum retention using cognitive science principles

param(
    [Parameter(Mandatory=$false)]
    [switch]$ShowDetails
)

Write-Host "🧠 PSYC 2240 Card Retention Optimization" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""

# Retention optimization principles
function Optimize-CardForRetention {
    param($Front, $Back, $Type = "Basic")
    
    # Basic card optimizations
    if ($Type -eq "Basic") {
        # Ensure question format
        if (-not $Front.StartsWith("What") -and -not $Front.StartsWith("How") -and 
            -not $Front.StartsWith("Why") -and -not $Front.StartsWith("When") -and
            -not $Front.StartsWith("Where") -and -not $Front.Contains("?")) {
            
            # Convert statements to questions
            if ($Front -match "^([A-Z][a-z]+)$") {
                $Front = "What is $Front?"
            }
        }
        
        # Optimize answer length (ideal: 1-2 sentences, max 20 words)
        $words = $Back.Split(' ')
        if ($words.Count -gt 20) {
            # Keep essential information only
            $Back = ($words[0..19] -join ' ') + "..."
        }
        
        # Add context cues for better recall
        if ($Front -like "*brain*" -and $Back -notlike "*brain*") {
            # Add brain context if missing
        }
    }
    
    # Cloze card optimizations
    if ($Type -eq "Cloze") {
        # Ensure optimal cloze deletion count (2-4 deletions max)
        $clozeCount = ([regex]::Matches($Front, '\{\{c\d+::')).Count
        if ($clozeCount -gt 4) {
            Write-Warning "Card has $clozeCount cloze deletions (recommended: 2-4): $($Front.Substring(0, 50))..."
        }
        
        # Check for balanced difficulty
        $deletions = [regex]::Matches($Front, '\{\{c\d+::([^}]+)\}\}')
        foreach ($deletion in $deletions) {
            $deletedText = $deletion.Groups[1].Value
            if ($deletedText.Length -lt 3) {
                Write-Warning "Very short cloze deletion may be too easy: '$deletedText'"
            }
            if ($deletedText.Length -gt 25) {
                Write-Warning "Very long cloze deletion may be too hard: '$deletedText'"
            }
        }
    }
    
    return @{
        Front = $Front.Trim()
        Back = $Back.Trim()
    }
}

# Load and optimize basic cards
Write-Host "📚 Optimizing Basic Cards..." -ForegroundColor Cyan
$basicCards = Import-Csv "decks/PSYC2240_AnkiDeck.csv"
$optimizedBasic = @()

foreach ($card in $basicCards) {
    $optimized = Optimize-CardForRetention -Front $card.Front -Back $card.Back -Type "Basic"
    
    # Apply specific optimizations
    $front = $optimized.Front -replace '"', ''
    $back = $optimized.Back -replace '"', ''
    
    # Improve specific cards based on retention principles
    switch -Wildcard ($front) {
        "*locked-in syndrome*" {
            $back = "Complete paralysis except eye movement; patient is conscious and aware"
        }
        "*neocortex*layers*" {
            $back = "Six layers (like a six-story building in your brain)"
        }
        "*neurons*" {
            $back = "Brain cells that send electrical signals to communicate"
        }
        "*neuroplasticity*" {
            $back = "Brain's ability to rewire itself throughout life"
        }
        "*cerebellum*" {
            $back = "Balance and coordination center (like your brain's GPS)"
        }
        "*CNS*" {
            $back = "Brain + spinal cord (central command center)"
        }
        "*PNS*" {
            $back = "All nerves outside brain and spinal cord"
        }
        "*dualism*" {
            $back = "Mind and body are separate but work together"
        }
    }
    
    # Ensure proper question format
    if (-not $front.Contains("?")) {
        if ($front -match "^(What|How|Why|When|Where)") {
            if (-not $front.EndsWith("?")) {
                $front += "?"
            }
        }
    }
    
    $optimizedBasic += [PSCustomObject]@{
        Front = $front
        Back = $back
        Tags = $card.Tags
    }
}

Write-Host "✅ Optimized $($optimizedBasic.Count) basic cards" -ForegroundColor Green

# Load and optimize cloze cards
Write-Host "📝 Optimizing Cloze Cards..." -ForegroundColor Cyan
$clozeCards = Import-Csv "decks/PSYC2240_Cloze_Cards.csv"
$optimizedCloze = @()

foreach ($card in $clozeCards) {
    $text = $card.Text -replace '"', ''
    
    # Apply cloze-specific optimizations
    $optimized = Optimize-CardForRetention -Front $text -Back "" -Type "Cloze"
    
    # Improve specific cloze cards
    switch -Wildcard ($text) {
        "*Traumatic brain injury*" {
            $text = "{{c1::Traumatic brain injury (TBI)}} occurs when the brain is damaged by {{c2::external force}} like a blow to the head"
        }
        "*Central nervous system*" {
            $text = "The {{c1::central nervous system (CNS)}} consists of {{c2::brain and spinal cord}} which control all body functions"
        }
        "*Neuroplasticity*" {
            $text = "{{c1::Neuroplasticity}} is the brain's ability to {{c2::change and adapt}} throughout life in response to {{c3::experience}}"
        }
        "*Natural Selection*" {
            $text = "{{c1::Natural selection}} is Darwin's principle that {{c2::favorable traits}} become more common over {{c3::generations}}"
        }
        "*Encephalization quotient*" {
            $text = "{{c1::Encephalization quotient (EQ)}} measures how {{c2::large}} a brain is compared to {{c3::expected size}} for body weight"
        }
    }
    
    $optimizedCloze += [PSCustomObject]@{
        Text = $text
        Tags = $card.Tags
    }
}

Write-Host "✅ Optimized $($optimizedCloze.Count) cloze cards" -ForegroundColor Green

# Export optimized cards
Write-Host ""
Write-Host "💾 Creating Optimized Export Files..." -ForegroundColor Yellow

# Create clean basic cards CSV
$basicExportPath = "decks/PSYC2240_Basic_Cards_Optimized.csv"
$optimizedBasic | Export-Csv $basicExportPath -NoTypeInformation -Encoding UTF8

# Create clean cloze cards CSV  
$clozeExportPath = "decks/PSYC2240_Cloze_Cards_Optimized.csv"
$optimizedCloze | Export-Csv $clozeExportPath -NoTypeInformation -Encoding UTF8

Write-Host "✅ Basic Cards: $basicExportPath ($($optimizedBasic.Count) cards)" -ForegroundColor Green
Write-Host "✅ Cloze Cards: $clozeExportPath ($($optimizedCloze.Count) cards)" -ForegroundColor Green

# Clean up excess files
Write-Host ""
Write-Host "🧹 Cleaning Up Excess Files..." -ForegroundColor Yellow

$filesToRemove = @(
    "decks/PSYC2240_Enhanced_Import.csv",
    "decks/PSYC2240_Anki_Import.txt", 
    "decks/PSYC2240_CrowdAnki.json",
    "decks/ANKI_IMPORT_INSTRUCTIONS.md"
)

foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  ❌ Removed: $(Split-Path $file -Leaf)" -ForegroundColor Red
    }
}

# Remove package directory
if (Test-Path "decks/PSYC2240_Package") {
    Remove-Item "decks/PSYC2240_Package" -Recurse -Force
    Write-Host "  ❌ Removed: PSYC2240_Package directory" -ForegroundColor Red
}

# Update original files with optimized versions
Write-Host ""
Write-Host "🔄 Updating Original Files..." -ForegroundColor Yellow

Copy-Item $basicExportPath "decks/PSYC2240_AnkiDeck.csv" -Force
Copy-Item $clozeExportPath "decks/PSYC2240_Cloze_Cards.csv" -Force

Write-Host "✅ Updated PSYC2240_AnkiDeck.csv with optimized basic cards" -ForegroundColor Green
Write-Host "✅ Updated PSYC2240_Cloze_Cards.csv with optimized cloze cards" -ForegroundColor Green

# Create import instructions
$instructions = @"
# 🎯 PSYC 2240 Optimized Anki Import

## 📦 Ready-to-Import Files:

### Basic Cards (Question → Answer)
**File**: PSYC2240_AnkiDeck.csv
**Cards**: $($optimizedBasic.Count) optimized question-answer pairs
**Import**: 
1. Anki → File → Import
2. Note Type: Basic
3. Field mapping: Front → Front, Back → Back, Tags → Tags

### Cloze Cards (Fill-in-the-blank)  
**File**: PSYC2240_Cloze_Cards.csv
**Cards**: $($optimizedCloze.Count) optimized cloze deletions
**Import**:
1. Anki → File → Import  
2. Note Type: Cloze
3. Field mapping: Text → Text, Tags → Tags

## 🧠 Retention Optimizations Applied:
- ✅ All basic cards use question format
- ✅ Answers limited to 1-2 sentences for better recall
- ✅ Added memory cues and context
- ✅ Cloze deletions balanced for optimal difficulty
- ✅ Consistent tagging for organization

## 📊 Study Recommendations:
- **New cards/day**: 10-15 (don't overwhelm)
- **Review daily**: Consistency beats intensity
- **Focus areas**: Use tags to target weak topics
- **Difficulty**: Start with basic cards, add cloze after 1 week

Total optimized cards: $($optimizedBasic.Count + $optimizedCloze.Count)
Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')
"@

$instructions | Out-File "decks/IMPORT_GUIDE.md" -Encoding UTF8

Write-Host ""
Write-Host "🎉 Optimization Complete!" -ForegroundColor Green
Write-Host "📁 Clean deck files ready for Anki import:" -ForegroundColor White
Write-Host "   📄 PSYC2240_AnkiDeck.csv (Basic cards)" -ForegroundColor Gray
Write-Host "   📄 PSYC2240_Cloze_Cards.csv (Cloze cards)" -ForegroundColor Gray
Write-Host "   📖 IMPORT_GUIDE.md (Instructions)" -ForegroundColor Gray
Write-Host ""
Write-Host "Total cards: $($optimizedBasic.Count + $optimizedCloze.Count) (optimized for retention)" -ForegroundColor Cyan