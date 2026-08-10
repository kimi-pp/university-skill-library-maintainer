param([string[]]$Keys = @())

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$deliveryBase = Get-ChildItem -LiteralPath $projectRoot -Directory | Where-Object { $_.Name.StartsWith("05_") } | Select-Object -First 1
$deliveryRoot = (Get-ChildItem -LiteralPath $deliveryBase.FullName -Directory | Where-Object { $_.Name.StartsWith("06_") } | Select-Object -First 1).FullName
$shortRoot = Join-Path $PSScriptRoot "fd06_artifacts"
$artifactRoot = Join-Path $shortRoot "docx_renders"
$pdftoppm = "C:\Users\34927\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe"
New-Item -ItemType Directory -Path $artifactRoot -Force | Out-Null

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$word.ScreenUpdating = $false
$word.Options.SaveInterval = 0
$word.Options.BackgroundSave = $false
$word.Options.CheckSpellingAsYouType = $false
$word.Options.CheckGrammarAsYouType = $false
$word.Options.UpdateLinksAtOpen = $false
try {
    $documents = Get-ChildItem -LiteralPath $deliveryRoot -Recurse -Filter "*.docx" | Sort-Object @{ Expression = { if ($_.BaseName.StartsWith("00_")) { 1 } else { 0 } } }, FullName
    if ($Keys.Count -gt 0) {
        $documents = $documents | Where-Object {
            $candidate = if ($_.BaseName.StartsWith("00_")) { "00" } else { $_.BaseName.Substring(0, 5).Replace("-", "_") }
            $Keys -contains $candidate
        }
    }
    foreach ($inputFile in $documents) {
        $key = if ($inputFile.BaseName.StartsWith("00_")) { "00" } else { $inputFile.BaseName.Substring(0, 5).Replace("-", "_") }
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        $outputDir = Join-Path $artifactRoot $key
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        Get-ChildItem -LiteralPath $outputDir -Filter "page-*.png" -ErrorAction SilentlyContinue | Remove-Item -Force
        [string]$pdfPath = Join-Path $shortRoot ("render_" + $key + ".pdf")
        $tempPrefixName = "render_" + $key + "_page"
        $prefix = Join-Path $shortRoot $tempPrefixName
        if (Test-Path -LiteralPath $pdfPath) { Remove-Item -LiteralPath $pdfPath -Force }
        Get-ChildItem -LiteralPath $shortRoot -Filter ($tempPrefixName + "-*.png") -ErrorAction SilentlyContinue | Remove-Item -Force

        $document = $null
        try {
            Write-Output "START`t$key`tinput_length=$($inputFile.FullName.Length)`toutput=$pdfPath"
            $document = $word.Documents.OpenNoRepairDialog($inputFile.FullName, $false, $true)
            Write-Output "OPEN`t$key`t$([math]::Round($stopwatch.Elapsed.TotalSeconds, 1))s"
            [int]$pdfFormat = 17
            $document.SaveAs([ref]$pdfPath, [ref]$pdfFormat)
            Write-Output "PDF`t$key`t$([math]::Round($stopwatch.Elapsed.TotalSeconds, 1))s"
        }
        finally {
            if ($null -ne $document) { $document.Close(0) }
        }

        & $pdftoppm -png -r 180 $pdfPath $prefix
        if ($LASTEXITCODE -ne 0) { throw "PDF page rendering failed: $pdfPath" }
        Get-ChildItem -LiteralPath $shortRoot -Filter ($tempPrefixName + "-*.png") | Sort-Object Name | ForEach-Object {
            $pageNumber = $_.BaseName.Substring($tempPrefixName.Length + 1)
            Move-Item -LiteralPath $_.FullName -Destination (Join-Path $outputDir ("page-" + $pageNumber + ".png")) -Force
        }
        Remove-Item -LiteralPath $pdfPath -Force
        $pageCount = (Get-ChildItem -LiteralPath $outputDir -Filter "page-*.png").Count
        Write-Output "$key`t$pageCount pages"
    }
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null
}
