param(
    [Parameter(Mandatory = $true)][string]$InputDocx,
    [Parameter(Mandatory = $true)][string]$OutputDir
)

$inputPath = (Resolve-Path -LiteralPath $InputDocx).Path
$outputPath = [System.IO.Path]::GetFullPath($OutputDir)
[System.IO.Directory]::CreateDirectory($outputPath) | Out-Null
$pdfPath = Join-Path $outputPath ([System.IO.Path]::GetFileNameWithoutExtension($inputPath) + '.pdf')

$word = $null
$document = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $document = $word.Documents.Open($inputPath, $false, $true)
    $document.ExportAsFixedFormat($pdfPath, 17)
}
finally {
    if ($null -ne $document) {
        $document.Close($false)
    }
    if ($null -ne $word) {
        $word.Quit()
    }
}

$pdftoppm = (Get-Command pdftoppm.exe -ErrorAction Stop).Source
& $pdftoppm -png -r 144 $pdfPath (Join-Path $outputPath 'page')
if ($LASTEXITCODE -ne 0) {
    throw "pdftoppm failed with exit code $LASTEXITCODE"
}

Get-ChildItem -LiteralPath $outputPath -Filter 'page-*.png' | Sort-Object Name | Select-Object Name, Length
