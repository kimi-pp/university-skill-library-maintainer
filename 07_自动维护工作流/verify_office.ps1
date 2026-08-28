[CmdletBinding()]
param(
    [string]$Excel,
    [ValidateSet('ledger', 'daily')]
    [string]$ExcelRole = 'ledger',
    [string]$Word,
    [string]$RenderDirectory,
    [string]$StableFileProbe,
    [ValidateRange(100, 30000)]
    [int]$StableTimeoutMilliseconds = 10000,
    [ValidateRange(10, 1000)]
    [int]$StablePollMilliseconds = 100
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
        if ($count -eq $Baseline) { return $count }
        Start-Sleep -Milliseconds 200
    } while ([DateTime]::UtcNow -lt $deadline)
    return (Get-ProcessCount $Name)
}

function Wait-ForStableFile([string]$Path, [int]$TimeoutMilliseconds, [int]$PollMilliseconds) {
    $deadline = [DateTime]::UtcNow.AddMilliseconds($TimeoutMilliseconds)
    [long]$lastSize = -1
    [int]$stableObservations = 0
    do {
        if ([IO.File]::Exists($Path)) {
            [long]$size = (Get-Item -LiteralPath $Path).Length
            if ($size -gt 0) {
                if ($size -eq $lastSize) {
                    $stableObservations += 1
                } else {
                    $lastSize = $size
                    $stableObservations = 1
                }
                if ($stableObservations -ge 2) {
                    return @{ size = $size; stable_observations = $stableObservations }
                }
            } else {
                $lastSize = -1
                $stableObservations = 0
            }
        } else {
            $lastSize = -1
            $stableObservations = 0
        }
        Start-Sleep -Milliseconds $PollMilliseconds
    } while ([DateTime]::UtcNow -lt $deadline)
    throw 'word-pdf-stability-timeout'
}

function Write-Result([hashtable]$Result) {
    [Console]::Out.WriteLine(($Result | ConvertTo-Json -Compress -Depth 6))
}

if (-not [string]::IsNullOrWhiteSpace($StableFileProbe)) {
    $probeResult = @{ passed = $false; observed_size = 0; stable_observations = 0; error = $null }
    try {
        $probe = Wait-ForStableFile ([IO.Path]::GetFullPath($StableFileProbe)) $StableTimeoutMilliseconds $StablePollMilliseconds
        $probeResult.observed_size = [long]$probe.size
        $probeResult.stable_observations = [int]$probe.stable_observations
        $probeResult.passed = $true
    } catch {
        $probeResult.error = $_.Exception.Message
    }
    Write-Result $probeResult
    exit 0
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
        $runRecord = -join ([char[]](0x8FD0,0x884C,0x8BB0,0x5F55))
        $executionOverview = -join ([char[]](0x6267,0x884C,0x6982,0x89C8))
        $preferred = if ($ExcelRole -eq 'daily') { @($executionOverview) } else { @($currentSkill, $runRecord) }
        $selectedExtent = $null
        $selectedHasData = $false
        $firstExisting = $null
        $firstExistingExtent = $null
        foreach ($name in $preferred) {
            $candidate = $null
            $candidateCells = $null
            $candidateLast = $null
            $candidateColumns = $null
            $candidateKeyColumn = $null
            $candidateKeyLast = $null
            try {
                $candidate = $worksheets.Item($name)
                if ($null -ne $candidate) {
                    $candidateCells = $candidate.Cells
                    $candidateLast = $candidateCells.Find('*', [Type]::Missing, -4163, 2, 1, 2, $false, $false, $false)
                    $candidateLastRow = if ($null -eq $candidateLast) { 0 } else { [int]$candidateLast.Row }
                    $candidateLastColumn = if ($null -eq $candidateLast) { 0 } else { [int]$candidateLast.Column }
                    $candidateLastValue = if ($null -eq $candidateLast -or $null -eq $candidateLast.Value2) { $null } else { [string]$candidateLast.Value2 }
                    $candidateHasData = $candidateLastRow -ge 2 -and -not [string]::IsNullOrWhiteSpace([string]$candidateLastValue)
                    if ($ExcelRole -eq 'ledger' -and $name -eq $currentSkill) {
                        $candidateColumns = $candidate.Columns
                        $candidateKeyColumn = $candidateColumns.Item(1)
                        $candidateKeyLast = $candidateKeyColumn.Find('*', [Type]::Missing, -4163, 2, 1, 2, $false, $false, $false)
                        $candidateHasData = $null -ne $candidateKeyLast -and [int]$candidateKeyLast.Row -ge 2 -and -not [string]::IsNullOrWhiteSpace([string]$candidateKeyLast.Value2)
                    }
                    if ($candidateHasData) {
                        Release-ComObject $firstExisting
                        $firstExisting = $null
                        $sheet = $candidate
                        $candidate = $null
                        $selectedExtent = @($candidateLastRow, $candidateLastColumn, $candidateLastValue)
                        $selectedHasData = $true
                    } elseif ($null -eq $firstExisting) {
                        $firstExisting = $candidate
                        $candidate = $null
                        $firstExistingExtent = @($candidateLastRow, $candidateLastColumn, $candidateLastValue)
                    }
                }
            } catch { } finally {
                Release-ComObject $candidateKeyLast
                Release-ComObject $candidateKeyColumn
                Release-ComObject $candidateColumns
                Release-ComObject $candidateLast
                Release-ComObject $candidateCells
                Release-ComObject $candidate
            }
            if ($null -ne $sheet) { break }
        }
        if ($null -eq $sheet -and $null -ne $firstExisting) {
            $sheet = $firstExisting
            $firstExisting = $null
            $selectedExtent = $firstExistingExtent
            $selectedHasData = $false
        }
        if ($null -eq $sheet) { throw 'excel-key-sheet-missing' }
        $result.key_sheet = [string]$sheet.Name
        $lastRow = [int]$selectedExtent[0]
        $lastColumn = [int]$selectedExtent[1]
        $lastValue = $selectedExtent[2]
        $result.last_row = $lastRow
        $result.last_column = $lastColumn
        $result.last_value = if ($null -eq $lastValue) { $null } else { [string]$lastValue }
        if (-not $result.read_only) { throw 'excel-not-read-only' }
        if (-not $selectedHasData -or $lastRow -lt 2 -or [string]::IsNullOrWhiteSpace([string]$lastValue)) {
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
        Release-ComObject $firstExisting
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
        if ($result.process_count_after -ne $before) {
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
    $null = Wait-ForStableFile $pdf $StableTimeoutMilliseconds $StablePollMilliseconds
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
    if ($result.process_count_after -ne $before) {
        $result.passed = $false
        $result.error = 'word-process-leak'
    }
}
Write-Result $result
exit 0
