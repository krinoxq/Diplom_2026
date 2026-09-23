$s = "C:\Users\iasti\AppData\Local\Temp\claude\C--Users-iasti--local-bin\418611ba-2e03-4e5b-9038-2e3ec53bc34c\scratchpad"
$w = New-Object -ComObject Word.Application; $w.Visible = $false
$d = $w.Documents.Open("$s\nirs2_raw.docx")
$d.TablesOfContents(1).Update(); $d.Fields.Update() | Out-Null; $d.Repaginate()
"pages=" + $d.ComputeStatistics(2)
$i = 0
foreach ($t in $d.Tables) { $i++; $split = @(); for ($r=2; $r -le $t.Rows.Count; $r++) { if ($t.Rows($r).Range.Information(3) -ne $t.Rows($r-1).Range.Information(3)) { $split += $r } }; "table $i : pages $($t.Rows(1).Range.Information(3))-$($t.Rows($t.Rows.Count).Range.Information(3)) split=$($split -join ',')" }
$d.SaveAs2("$s\nirs2_toc.docx", 16)
$d.ExportAsFixedFormat("$s\nirs2.pdf", 17)
$d.Close($false); $w.Quit()
