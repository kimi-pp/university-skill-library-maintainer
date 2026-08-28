[CmdletBinding()]
param(
    [string]$Excel,
    [string]$Word,
    [string]$RenderDirectory
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

function Get-ProcessCount([string]$Name) {
    return @((Get-Process -Name $Name -ErrorAction SilentlyContinue)).Count
}

function Release-ComObject([object]$Value) {
    if ($null -ne $Value -and [System.Runtime.InteropServices.Marshal]::IsComObject($Value)) {
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($Value)
    }
}

function Wait-ForProcessBaseline([string]$Name, [int]$Baseline) {
    $deadline = [DateTime]::UtcNow.AddSeconds(15)
    do {
        $count = Get-ProcessCount $Name
        if ($count -le $Baseline) { return $count }
        Start-Sleep -Milliseconds 200
    } while ([DateTime]::UtcNow -lt $deadline)
    return (Get-ProcessCount $Name)
}

function Write-Result([hashtable]$Result) {
    [Console]::Out.WriteLine(($Result | ConvertTo-Json -Compress -Depth 6))
}

if ([string]::IsNullOrWhiteSpace($Excel) -eq [string]::IsNullOrWhiteSpace($Word)) {
    Write-Result @{ passed = $false; error = 'select-exactly-one-office-input' }
    exit 0
}

if (-not [string]::IsNullOrWhiteSpace($Excel)) {
    $application = $null
    $workbooks = $null
    $workbook = $null
    $worksheets = $null
    $sheet = $null
    $used = $null
    $usedRows = $null
    $usedColumns = $null
    $cells = $null
    $lastCell = $null
    $before = Get-ProcessCount 'EXCEL'
    $result = @{
        kind = 'excel'; passed = $false; office_opened = $false; read_only = $false
        key_sheet = $null; last_row = 0; last_column = 0; last_value = $null
        process_count_before = $before; process_count_after = $before; error = $null
    }
    try {
        $absolute = [IO.Path]::GetFullPath($Excel)
        if (-not [IO.File]::Exists($absolute)) { throw "excel-file-missing:$absolute" }
        $application = New-Object -ComObject Excel.Application
        $application.Visible = $false
        $application.DisplayAlerts = $false
        $application.AskToUpdateLinks = $false
        $application.AlertBeforeOverwriting = $false
        $application.EnableEvents = $false
        $application.AutomationSecurity = 3
        $workbooks = $application.Workbooks
        $workbook = $workbooks.Open($absolute, 0, $true)
        $result.office_opened = $true
        $result.read_only = [bool]$workbook.ReadOnly
        $worksheets = $workbook.Worksheets
        $currentSkill = -join ([char[]](0x5F53,0x524D,0x0053,0x006B,0x0069,0x006C,0x006C))
        $runOverview = -join ([char[]](0x6267,0x884C,0x6982,0x89C8))
        $preferred = @($currentSkill, $runOverview)
        foreach ($name in $preferred) {
            try {
                $candidate = $worksheets.Item($name)
                if ($null -ne $candidate) { $sheet = $candidate; break }
            } catch { }
        }
        if ($null -eq $sheet) { $sheet = $worksheets.Item(1) }
        $result.key_sheet = [string]$sheet.Name
        $used = $sheet.UsedRange
        $usedRows = $used.Rows
        $usedColumns = $used.Columns
        $lastRow = [int]($used.Row + $usedRows.Count - 1)
        $lastColumn = [int]($used.Column + $usedColumns.Count - 1)
        $cells = $sheet.Cells
        $lastCell = $cells.Item($lastRow, $lastColumn)
        $lastValue = $lastCell.Value2
        $result.last_row = $lastRow
        $result.last_column = $lastColumn
        $result.last_value = if ($null -eq $lastValue) { $null } else { [string]$lastValue }
        if (-not $result.read_only) { throw 'excel-not-read-only' }
        if ($lastRow -lt 2 -or [string]::IsNullOrWhiteSpace([string]$lastValue)) {
            throw 'excel-no-data-row'
        }
        $result.passed = $true
    } catch {
        $result.error = $_.Exception.Message
    } finally {
        if ($null -ne $workbook) {
            try { $workbook.Close($false) } catch { if (-not $result.error) { $result.error = $_.Exception.Message } }
        }
        Release-ComObject $lastCell
        Release-ComObject $cells
        Release-ComObject $usedColumns
        Release-ComObject $usedRows
        Release-ComObject $used
        Release-ComObject $sheet
        Release-ComObject $worksheets
        Release-ComObject $workbook
        Release-ComObject $workbooks
        if ($null -ne $application) {
            try { $application.Quit() } catch { if (-not $result.error) { $result.error = $_.Exception.Message } }
        }
        Release-ComObject $application
        [GC]::Collect()
        [GC]::WaitForPendingFinalizers()
        [GC]::Collect()
        $result.process_count_after = Wait-ForProcessBaseline 'EXCEL' $before
        if ($result.process_count_after -gt $before) {
            $result.passed = $false
            $result.error = 'excel-process-leak'
        }
    }
    Write-Result $result
    exit 0
}

$application = $null
$documents = $null
$document = $null
$before = Get-ProcessCount 'WINWORD'
$result = @{
    kind = 'word'; passed = $false; office_opened = $false; read_only = $false
    page_count = 0; pdf_path = $null
    process_count_before = $before; process_count_after = $before; error = $null
}
try {
    $absolute = [IO.Path]::GetFullPath($Word)
    if (-not [IO.File]::Exists($absolute)) { throw "word-file-missing:$absolute" }
    if ([string]::IsNullOrWhiteSpace($RenderDirectory)) { throw 'word-render-directory-required' }
    $renderAbsolute = [IO.Path]::GetFullPath($RenderDirectory)
    [IO.Directory]::CreateDirectory($renderAbsolute) | Out-Null
    $pdf = [IO.Path]::Combine($renderAbsolute, ([IO.Path]::GetFileNameWithoutExtension($absolute) + '.office.pdf'))
    if ([IO.File]::Exists($pdf)) { throw 'word-pdf-target-exists' }
    $application = New-Object -ComObject Word.Application
    $application.Visible = $false
    $application.DisplayAlerts = 0
    $application.AutomationSecurity = 3
    $documents = $application.Documents
    $document = $documents.Open($absolute, $false, $true)
    $result.office_opened = $true
    $result.read_only = [bool]$document.ReadOnly
    if (-not $result.read_only) { throw 'word-not-read-only' }
    $result.page_count = [int]$document.ComputeStatistics(2)
    $document.ExportAsFixedFormat($pdf, 17)
    if (-not [IO.File]::Exists($pdf) -or (Get-Item -LiteralPath $pdf).Length -le 0) {
        throw 'word-pdf-empty-or-missing'
    }
    $result.pdf_path = $pdf
    $result.passed = $true
} catch {
    $result.error = $_.Exception.Message
} finally {
    if ($null -ne $document) {
        try { $document.Close(0) } catch { if (-not $result.error) { $result.error = $_.Exception.Message } }
    }
    Release-ComObject $document
    Release-ComObject $documents
    if ($null -ne $application) {
        try { $application.Quit() } catch { if (-not $result.error) { $result.error = $_.Exception.Message } }
    }
    Release-ComObject $application
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
    [GC]::Collect()
    $result.process_count_after = Wait-ForProcessBaseline 'WINWORD' $before
    if ($result.process_count_after -gt $before) {
        $result.passed = $false
        $result.error = 'word-process-leak'
    }
}
Write-Result $result
exit 0
