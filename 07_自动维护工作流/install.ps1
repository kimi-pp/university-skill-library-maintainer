[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,

    [Parameter(Mandatory = $true)]
    [string]$PythonExe,

    [Parameter(Mandatory = $false)]
    [string]$CodexSkillsRoot
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Get-OrdinaryPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LiteralPath,

        [Parameter(Mandatory = $true)]
        [ValidateSet("File", "Directory")]
        [string]$Kind
    )

    $item = Get-Item -LiteralPath $LiteralPath -Force -ErrorAction Stop
    if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw "Links and reparse points are not allowed: $LiteralPath"
    }
    if ($Kind -eq "File" -and -not $item.PSIsContainer) {
        return $item.FullName
    }
    if ($Kind -eq "Directory" -and $item.PSIsContainer) {
        return $item.FullName
    }
    throw "Unexpected path type (expected $Kind): $LiteralPath"
}

function Invoke-CheckedPython {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code $LASTEXITCODE."
    }
}

function Assert-RequiredTextFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LiteralPath
    )

    $fullName = Get-OrdinaryPath -LiteralPath $LiteralPath -Kind File
    $strictUtf8 = New-Object System.Text.UTF8Encoding($false, $true)
    $text = [System.IO.File]::ReadAllText($fullName, $strictUtf8)
    if ([string]::IsNullOrWhiteSpace($text)) {
        throw "Required authority file is empty: $LiteralPath"
    }
}

$resolvedProject = Get-OrdinaryPath -LiteralPath $ProjectRoot -Kind Directory
$resolvedPython = Get-OrdinaryPath -LiteralPath $PythonExe -Kind File
$scriptRoot = Get-OrdinaryPath -LiteralPath $PSScriptRoot -Kind Directory
$workflowParent = Split-Path -Parent $scriptRoot
if (-not [string]::Equals($resolvedProject, $workflowParent, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "install.ps1 must run from the workflow directory directly below ProjectRoot."
}
$resolvedWorkflow = $scriptRoot

$rulesDirectoryName = "01_" + [char]0x89C4 + [char]0x5219
$rulesRoot = Join-Path $resolvedProject $rulesDirectoryName
Assert-RequiredTextFile -LiteralPath (Join-Path $resolvedProject "AGENTS.md")
foreach ($ruleName in @(
    "SKILL_RESEARCH_WORKFLOW.md",
    "SECURITY_REVIEW_PROTOCOL.md",
    "DATA_DICTIONARY.md",
    "REPORTING_STANDARD.md"
)) {
    Assert-RequiredTextFile -LiteralPath (Join-Path $rulesRoot $ruleName)
}

$requirements = Get-OrdinaryPath -LiteralPath (Join-Path $resolvedWorkflow "requirements.txt") -Kind File
$projectMetadata = Get-OrdinaryPath -LiteralPath (Join-Path $resolvedWorkflow "pyproject.toml") -Kind File
if (-not $projectMetadata) {
    throw "pyproject.toml is missing."
}

if ([string]::IsNullOrWhiteSpace($CodexSkillsRoot)) {
    if (-not [string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
        $CodexSkillsRoot = Join-Path $env:CODEX_HOME "skills"
    }
    else {
        $profileRoot = [Environment]::GetFolderPath([Environment+SpecialFolder]::UserProfile)
        if ([string]::IsNullOrWhiteSpace($profileRoot)) {
            throw "Cannot determine the Codex Skills directory; pass -CodexSkillsRoot explicitly."
        }
        $CodexSkillsRoot = Join-Path (Join-Path $profileRoot ".codex") "skills"
    }
}
$resolvedSkillsParent = [System.IO.Path]::GetFullPath($CodexSkillsRoot)

Invoke-CheckedPython -Executable $resolvedPython -Arguments @("--version")

$venvRoot = Join-Path $resolvedWorkflow ".venv"
if (Test-Path -LiteralPath $venvRoot) {
    [void](Get-OrdinaryPath -LiteralPath $venvRoot -Kind Directory)
}
else {
    Invoke-CheckedPython -Executable $resolvedPython -Arguments @("-m", "venv", "--system-site-packages", $venvRoot)
}

$venvPython = Get-OrdinaryPath -LiteralPath (Join-Path $venvRoot "Scripts\python.exe") -Kind File
Invoke-CheckedPython -Executable $venvPython -Arguments @(
    "-m", "pip", "install", "--disable-pip-version-check", "--requirement", $requirements
)
Invoke-CheckedPython -Executable $venvPython -Arguments @(
    "-m", "pip", "install", "--disable-pip-version-check", "--no-deps", "--no-build-isolation", "--editable", $resolvedWorkflow
)

Invoke-CheckedPython -Executable $venvPython -Arguments @(
    "-m", "skill_maintainer.cli", "setup", "--project-root", $resolvedProject,
    "--codex-skills-root", $resolvedSkillsParent
)
Invoke-CheckedPython -Executable $venvPython -Arguments @(
    "-m", "skill_maintainer.cli", "doctor", "--project-root", $resolvedProject
)

Write-Output "Installation checks completed. No automation was created; settings remain disabled/manual."
