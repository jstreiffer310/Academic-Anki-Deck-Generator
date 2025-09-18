# 🚀 PSYC 2240 Local Project Setup Script
# Run this script on your local computer to create a clean study workspace

param(
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = "$env:USERPROFILE\Documents\PSYC2240-Study"
)

Write-Host "🎯 Setting up PSYC 2240 Study Workspace..." -ForegroundColor Green
Write-Host "📁 Location: $ProjectPath" -ForegroundColor Cyan

# Create project directory
if (Test-Path $ProjectPath) {
    Write-Host "⚠️  Directory already exists. Contents will be overwritten." -ForegroundColor Yellow
    $response = Read-Host "Continue? (y/N)"
    if ($response -ne 'y' -and $response -ne 'Y') {
        Write-Host "❌ Setup cancelled." -ForegroundColor Red
        exit
    }
}

New-Item -ItemType Directory -Path $ProjectPath -Force | Out-Null
Set-Location $ProjectPath

Write-Host "📦 Cloning repository..." -ForegroundColor Yellow
git clone https://github.com/jstreiffer310/PSYC2240-Anki-Deck-Generator.git temp-repo

Write-Host "📋 Extracting essential files..." -ForegroundColor Yellow

# Create clean project structure
$folders = @(
    ".vscode",
    "anki-cards", 
    "study-deck",
    "docs"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
}

# Copy essential files
Write-Host "📁 Copying VS Code settings..." -ForegroundColor Cyan
Copy-Item "temp-repo\.vscode\settings.json" ".vscode\" -Force

Write-Host "🃏 Copying card templates..." -ForegroundColor Cyan
Copy-Item "temp-repo\anki-cards\*" "anki-cards\" -Recurse -Force

Write-Host "📚 Copying study deck..." -ForegroundColor Cyan
Copy-Item "temp-repo\output\PSYC2240_Consolidated_Deck.apkg" "study-deck\" -Force
Copy-Item "temp-repo\output\FSRS_SETUP_GUIDE.md" "study-deck\" -Force

Write-Host "📖 Copying documentation..." -ForegroundColor Cyan
Copy-Item "temp-repo\README.md" "." -Force
Copy-Item "temp-repo\CREATE_LOCAL_PROJECT.md" "docs\" -Force

# Create workspace file
Write-Host "⚙️  Creating VS Code workspace..." -ForegroundColor Yellow
$workspaceConfig = @{
    folders = @(
        @{ path = "." }
    )
    settings = @{
        "anki.api.hostname" = "127.0.0.1"
        "anki.api.port" = 8765
    }
    extensions = @{
        recommendations = @(
            "jasew.anki"
        )
    }
} | ConvertTo-Json -Depth 10

$workspaceConfig | Out-File -FilePath "PSYC2240-Study.code-workspace" -Encoding utf8

# Cleanup
Write-Host "🧹 Cleaning up..." -ForegroundColor Yellow
Remove-Item "temp-repo" -Recurse -Force

# Create quick start script
$quickStart = @"
# 🚀 Quick Start Guide

## What You Have:
- **📚 Main Study Deck**: ``study-deck/PSYC2240_Consolidated_Deck.apkg`` (829 cards)
- **⚙️  FSRS Settings**: ``study-deck/FSRS_SETUP_GUIDE.md`` (Exam optimization)
- **🃏 Card Templates**: ``anki-cards/`` (For creating new cards)
- **🔧 VS Code Integration**: Pre-configured AnkiConnect settings

## Next Steps:
1. **Import Deck**: Double-click ``study-deck/PSYC2240_Consolidated_Deck.apkg``
2. **Configure FSRS**: Follow ``study-deck/FSRS_SETUP_GUIDE.md``
3. **Open VS Code**: Double-click ``PSYC2240-Study.code-workspace``
4. **Install Anki Extension**: VS Code will prompt to install recommended extensions

## Creating New Cards:
- Open any ``.md`` file in ``anki-cards/``
- Use Ctrl+Shift+P → "Anki: Send to Anki"
- Cards automatically sync to your deck!

**🎯 Ready for October 8th exam prep!**
"@

$quickStart | Out-File -FilePath "QUICK_START.md" -Encoding utf8

Write-Host ""
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "📍 Project Location: $ProjectPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Import study-deck/PSYC2240_Consolidated_Deck.apkg into Anki"
Write-Host "   2. Open PSYC2240-Study.code-workspace in VS Code"
Write-Host "   3. Follow QUICK_START.md instructions"
Write-Host ""
Write-Host "🚀 Happy studying for your October 8th exam!" -ForegroundColor Green