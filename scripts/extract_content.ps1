# Optimized Textbook Content Parser - Cross-Platform Compatible

param(
    [Parameter(Mandatory=$false)]
    [string]$InputPath = "",
    [Parameter(Mandatory=$false)]
    [string]$OutputPath = "source/textbook_content.txt",
    [Parameter(Mandatory=$false)]
    [switch]$Verbose
)

# Performance optimization: Use streaming for large files
function Write-Progress-Safe {
    param($Activity, $Status, $PercentComplete)
    if ($Verbose) {
        Write-Host "$Activity - $Status ($PercentComplete%)"
    }
}

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

# Memory-efficient XML processing
Write-Progress-Safe "Processing" "Reading XML content" 10
Write-Host "📖 Reading XML content from: $InputPath"

try {
    # Use XmlReader for better memory efficiency with large files
    $xmlSettings = New-Object System.Xml.XmlReaderSettings
    $xmlSettings.IgnoreWhitespace = $true
    $xmlReader = [System.Xml.XmlReader]::Create($InputPath, $xmlSettings)
    
    $extractedContent = [System.Collections.Generic.List[string]]::new()
    
    Write-Progress-Safe "Processing" "Extracting text nodes" 30
    
    while ($xmlReader.Read()) {
        if ($xmlReader.Name -eq "t" -and $xmlReader.NodeType -eq [System.Xml.XmlNodeType]::Element) {
            $text = $xmlReader.ReadElementContentAsString()
            if ($text.Trim()) {
                $extractedContent.Add($text.Trim())
            }
        }
    }
    
    Write-Progress-Safe "Processing" "Joining content" 70
    
    # Efficient string joining
    $fullText = [string]::Join(' ', $extractedContent)
    $fullText = [regex]::Replace($fullText, '\s+', ' ')
    
    # Ensure output directory exists
    $outputDir = Split-Path $OutputPath -Parent
    if ($outputDir -and -not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    }
    
    Write-Progress-Safe "Processing" "Saving to file" 90
    
    # Use StreamWriter for better performance
    [System.IO.File]::WriteAllText($OutputPath, $fullText, [System.Text.Encoding]::UTF8)
    
    Write-Progress-Safe "Processing" "Complete" 100
    
    Write-Host "✅ Content extracted successfully"
    Write-Host "📊 Length: $($fullText.Length) characters"
    Write-Host "📁 Saved to: $OutputPath"
    
    if ($Verbose) {
        Write-Host "🔍 Preview (first 500 chars):"
        Write-Host $fullText.Substring(0, [Math]::Min(500, $fullText.Length))
    }
    
} catch {
    Write-Error "❌ Failed to process XML: $($_.Exception.Message)"
    exit 1
} finally {
    if ($xmlReader) { $xmlReader.Close() }
}
