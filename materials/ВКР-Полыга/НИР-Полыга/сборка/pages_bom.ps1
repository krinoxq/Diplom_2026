$ErrorActionPreference = "Stop"
$path = "C:\Users\iasti\OneDrive\Desktop\НИР-Полыга\Полыга К.Ю. НИР.docx"
$outTsv = "C:\Users\iasti\AppData\Local\Temp\claude\C--Users-iasti--local-bin\f248cfb0-7747-4b8f-bcb4-0e1888feec3c\scratchpad\txt\pages.tsv"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($path)
$doc.Repaginate()
$pages = $doc.ComputeStatistics(2)

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("PAGES`t$pages")
foreach ($p in $doc.Paragraphs) {
    $t = $p.Range.Text.Trim()
    if ($t.Length -gt 0 -and $t.Length -lt 200) {
        $isBold = $p.Range.Bold
        if ($isBold -eq $true -or $isBold -eq -1) {
            $pg = $p.Range.Information(3)
            $lines.Add("$pg`t$t")
        }
    }
}
[System.IO.File]::WriteAllLines($outTsv, $lines, (New-Object System.Text.UTF8Encoding $false))
$pdf = $path -replace "\.docx$", ".pdf"
$doc.SaveAs([ref]$pdf, [ref]17)
$doc.Close($false)
$word.Quit()
Write-Output "pages=$pages"
