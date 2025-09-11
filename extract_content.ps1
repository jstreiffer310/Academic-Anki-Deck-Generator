# Textbook Content Parser

# Read the XML content
$xmlPath = "C:\Users\jstre\Desktop\document_content.xml"
$xml = [xml](Get-Content $xmlPath)

# Extract all text content
$allTextNodes = $xml.SelectNodes("//w:t")
$extractedContent = @()

foreach ($node in $allTextNodes) {
    if ($node.'#text') {
        $extractedContent += $node.'#text'
    }
}

# Join and clean up the content
$fullText = $extractedContent -join ' '
$fullText = $fullText -replace '\s+', ' '

# Save to file for easier processing
$fullText | Out-File "C:\Users\jstre\Desktop\textbook_content.txt" -Encoding UTF8

Write-Output "Content extracted and saved. Length: $($fullText.Length) characters"
Write-Output "First 1000 characters:"
Write-Output $fullText.Substring(0, [Math]::Min(1000, $fullText.Length))
