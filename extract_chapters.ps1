# Read XML content
$xmlPath = "C:\Users\jstre\Desktop\document_content.xml"
$content = Get-Content $xmlPath -Raw

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

# Save full content
$fullContent | Out-File "C:\Users\jstre\Desktop\textbook_full_content.txt" -Encoding UTF8

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
