# Chapter Extraction Script - Cross-Platform Compatible

param(
    [Parameter(Mandatory=$false)]
    [string]$InputPath = "",
    [Parameter(Mandatory=$false)]
    [string]$OutputPath = "source/textbook_full_content.txt"
)

# Use default path if not provided
if ([string]::IsNullOrEmpty($InputPath)) {
    # Try common locations for the XML file
    $possiblePaths = @(
        "source/document_content.xml",
        "document_content.xml",
        "../document_content.xml"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $InputPath = $path
            break
        }
    }
    
    if ([string]::IsNullOrEmpty($InputPath)) {
        Write-Error "XML file not found. Please specify -InputPath parameter or place document_content.xml in the source/ directory."
        exit 1
    }
}

if (-not (Test-Path $InputPath)) {
    Write-Error "Input file not found: $InputPath"
    exit 1
}

# Read XML content
Write-Host "Processing XML content from: $InputPath"
$content = Get-Content $InputPath -Raw

# Extract all text nodes more carefully
$textPattern = '<w:t xml:space="preserve">(.*?)</w:t>'
$allMatches = [regex]::Matches($content, $textPattern)

$extractedText = @()
foreach ($match in $allMatches) {
    $text = $match.Groups[1].Value
    if ($text.Trim()) {
        $extractedText += $text.Trim()
    }
}

# Join text and clean up
$fullContent = $extractedText -join ' '
$fullContent = $fullContent -replace '\s+', ' '

# Ensure output directory exists
$outputDir = Split-Path $OutputPath -Parent
if ($outputDir -and -not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Save full content
$fullContent | Out-File $OutputPath -Encoding UTF8

# Extract chapter structure
$chapters = @()
if ($fullContent -match 'CHAPTER 1.*?(?=CHAPTER [2-9]|$)') {
    $chapters += @{Number=1; Content=$matches[0]}
}
if ($fullContent -match 'CHAPTER 2.*?(?=CHAPTER [3-9]|$)') {
    $chapters += @{Number=2; Content=$matches[0]}
}
if ($fullContent -match 'CHAPTER 3.*?(?=CHAPTER [4-9]|$)') {
    $chapters += @{Number=3; Content=$matches[0]}
}

Write-Output "Extracted content length: $($fullContent.Length)"
Write-Output "Found chapters: $($chapters.Count)"
Write-Output "`nFirst 1000 characters:"
Write-Output $fullContent.Substring(0, [Math]::Min(1000, $fullContent.Length))
