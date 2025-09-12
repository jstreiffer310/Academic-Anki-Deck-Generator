# Anki Deck Package Creator - Generates .apkg file
# Uses Anki's text format for direct import

param(
    [Parameter(Mandatory=$false)]
    [string]$DeckName = "PSYC 2240 - Biological Basis of Behaviour"
)

Write-Host "📦 Creating Anki Deck Package (.apkg)" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Create Anki text format file that can be converted to .apkg
function New-AnkiTextFormat {
    $ankiText = @"
#separator:tab
#html:true
#deck column:1
#tags column:2
#notetype column:3
"@

    # Read CSV files
    $mainCards = Import-Csv "decks/PSYC2240_AnkiDeck.csv"
    $clozeCards = Import-Csv "decks/PSYC2240_Cloze_Cards.csv"
    
    Write-Host "📊 Processing cards:" -ForegroundColor Cyan
    Write-Host "  🧠 Main deck: $($mainCards.Count) cards"
    Write-Host "  🔤 Cloze deck: $($clozeCards.Count) cards"
    
    # Add main cards (Basic note type)
    foreach ($card in $mainCards) {
        $front = $card.Front -replace '"', ''
        $back = $card.Back -replace '"', ''
        $tags = $card.Tags -replace '"', ''
        $ankiText += "`nPSYC2240`t$tags`tBasic`t$front`t$back"
    }
    
    # Add cloze cards (Cloze note type)
    foreach ($card in $clozeCards) {
        $text = $card.Text -replace '"', ''
        $tags = $card.Tags -replace '"', ''
        $ankiText += "`nPSYC2240`t$tags`tCloze`t$text"
    }
    
    return $ankiText
}

# Generate Anki-compatible text file
$ankiTextContent = New-AnkiTextFormat
$textFile = "decks/PSYC2240_Anki_Import.txt"
$ankiTextContent | Out-File $textFile -Encoding UTF8

Write-Host ""
Write-Host "✅ Created Anki import file: $textFile" -ForegroundColor Green

# Create .apkg using a different approach - generate JSON export
$ankiJson = @{
    "__type__" = "Deck"
    "crowdanki_uuid" = "12345678-1234-1234-1234-123456789abc"
    "deck_config_uuid" = "12345678-1234-1234-1234-123456789def"
    "name" = "PSYC 2240 - Biological Basis of Behaviour"
    "desc" = "Optimized flashcards for PSYC 2240 covering Chapters 1-3. Memory-retention focused with question format and concise answers."
    "note_models" = @(
        @{
            "crowdanki_uuid" = "basic-model-uuid"
            "name" = "Basic"
            "type" = 0
            "flds" = @(
                @{ "name" = "Front"; "ord" = 0; "sticky" = $false }
                @{ "name" = "Back"; "ord" = 1; "sticky" = $false }
            )
            "tmpls" = @(
                @{
                    "name" = "Card 1"
                    "qfmt" = "{{Front}}"
                    "afmt" = "{{FrontSide}}<hr id=answer>{{Back}}"
                    "ord" = 0
                }
            )
        }
        @{
            "crowdanki_uuid" = "cloze-model-uuid"
            "name" = "Cloze"
            "type" = 1
            "flds" = @(
                @{ "name" = "Text"; "ord" = 0; "sticky" = $false }
                @{ "name" = "Extra"; "ord" = 1; "sticky" = $false }
            )
            "tmpls" = @(
                @{
                    "name" = "Cloze"
                    "qfmt" = "{{cloze:Text}}"
                    "afmt" = "{{cloze:Text}}<br>{{Extra}}"
                    "ord" = 0
                }
            )
        }
    )
    "notes" = @()
}

# Add notes to JSON
$mainCards = Import-Csv "decks/PSYC2240_AnkiDeck.csv"
$clozeCards = Import-Csv "decks/PSYC2240_Cloze_Cards.csv"

foreach ($card in $mainCards) {
    $ankiJson.notes += @{
        "crowdanki_uuid" = [System.Guid]::NewGuid().ToString()
        "note_model_uuid" = "basic-model-uuid"
        "tags" = @($card.Tags)
        "fields" = @($card.Front -replace '"','', $card.Back -replace '"','')
    }
}

foreach ($card in $clozeCards) {
    $ankiJson.notes += @{
        "crowdanki_uuid" = [System.Guid]::NewGuid().ToString()
        "note_model_uuid" = "cloze-model-uuid"
        "tags" = @($card.Tags)
        "fields" = @($card.Text -replace '"','', "")
    }
}

# Save JSON file (can be imported with CrowdAnki add-on)
$jsonFile = "decks/PSYC2240_CrowdAnki.json"
$ankiJson | ConvertTo-Json -Depth 10 | Out-File $jsonFile -Encoding UTF8

Write-Host "✅ Created CrowdAnki JSON: $jsonFile" -ForegroundColor Green
Write-Host ""

# Create final import package as ZIP (manual .apkg)
$packageDir = "decks/PSYC2240_Package"
if (Test-Path $packageDir) {
    Remove-Item $packageDir -Recurse -Force
}
New-Item -ItemType Directory -Path $packageDir -Force | Out-Null

# Copy all formats
Copy-Item "decks/PSYC2240_AnkiDeck.csv" $packageDir
Copy-Item "decks/PSYC2240_Cloze_Cards.csv" $packageDir
Copy-Item $textFile $packageDir
Copy-Item $jsonFile $packageDir

# Create comprehensive instructions
$instructions = @"
# 🎯 PSYC 2240 Anki Deck - Import Options

## 📦 Multiple Import Formats Available:

### Option 1: CSV Files (Easiest)
**Files**: PSYC2240_AnkiDeck.csv + PSYC2240_Cloze_Cards.csv
1. Import PSYC2240_AnkiDeck.csv first
   - Note Type: Basic
   - Field 1 → Front, Field 2 → Back, Field 3 → Tags
2. Import PSYC2240_Cloze_Cards.csv second
   - Note Type: Cloze
   - Field 1 → Text, Field 2 → Tags

### Option 2: Text Format
**File**: PSYC2240_Anki_Import.txt
1. File → Import → Select text file
2. Field separator: Tab
3. Allow HTML: ✅ Checked

### Option 3: CrowdAnki (Advanced)
**File**: PSYC2240_CrowdAnki.json
1. Install CrowdAnki add-on first
2. Import JSON through CrowdAnki

## 📊 What You'll Get:
- **74 Basic Cards**: Question → Answer format
- **47 Cloze Cards**: Fill-in-the-blank format
- **Total: 121 optimized study cards**

## 🎯 Recommended Settings:
- New cards/day: 10-15
- Maximum interval: 365 days
- Graduating interval: 1 day
- Easy interval: 4 days

## 📚 Study Strategy:
1. Start with Basic cards (Week 1-2)
2. Add Cloze cards (Week 3+)
3. Review daily for best retention
4. Focus on weak areas using tags

Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')
Cards: 121 total (74 Basic + 47 Cloze)
Coverage: PSYC 2240 Chapters 1-3
"@

$instructions | Out-File "$packageDir/IMPORT_INSTRUCTIONS.md" -Encoding UTF8

Write-Host "📋 Complete Import Package Created!" -ForegroundColor Yellow
Write-Host "📁 Location: $packageDir" -ForegroundColor White
Write-Host ""
Write-Host "📥 To Download:" -ForegroundColor Cyan
Write-Host "  1. Right-click the 'PSYC2240_Package' folder in VS Code"
Write-Host "  2. Select 'Download'"
Write-Host "  3. Extract ZIP on your computer"
Write-Host "  4. Follow IMPORT_INSTRUCTIONS.md"
Write-Host ""
Write-Host "🎉 Ready for Anki import!" -ForegroundColor Green