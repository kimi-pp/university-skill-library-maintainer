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

function Assert-OrdinaryPathChain {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LiteralPath
    )

    $current = [System.IO.Path]::GetFullPath($LiteralPath)
    while (-not [string]::IsNullOrWhiteSpace($current)) {
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
            if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Links and reparse points are not allowed in the path chain: $current"
            }
        }
        $parent = [System.IO.Directory]::GetParent($current)
        if ($null -eq $parent) {
            break
        }
        $current = $parent.FullName
    }
}

function Get-OrdinaryPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LiteralPath,

        [Parameter(Mandatory = $true)]
        [ValidateSet("File", "Directory")]
        [string]$Kind
    )

    Assert-OrdinaryPathChain -LiteralPath $LiteralPath
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

    & $Executable -I @Arguments
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

function Assert-OwnedOrAbsent {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LiteralPath,

        [Parameter(Mandatory = $true)]
        [string]$OwnershipMarker
    )

    if (-not (Test-Path -LiteralPath $LiteralPath)) {
        return
    }
    $fullName = Get-OrdinaryPath -LiteralPath $LiteralPath -Kind File
    $strictUtf8 = New-Object System.Text.UTF8Encoding($false, $true)
    $content = [System.IO.File]::ReadAllText($fullName, $strictUtf8)
    if (-not $content.StartsWith($OwnershipMarker, [System.StringComparison]::Ordinal)) {
        throw "Refusing to overwrite a file not owned by this installer: $LiteralPath"
    }
}

function Write-AtomicOwnedText {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LiteralPath,

        [Parameter(Mandatory = $true)]
        [string]$Content,

        [Parameter(Mandatory = $true)]
        [string]$OwnershipMarker
    )

    Assert-OwnedOrAbsent -LiteralPath $LiteralPath -OwnershipMarker $OwnershipMarker
    $parent = Split-Path -Parent $LiteralPath
    [void](Get-OrdinaryPath -LiteralPath $parent -Kind Directory)
    $temporary = Join-Path $parent ("." + [System.IO.Path]::GetFileName($LiteralPath) + "." + [guid]::NewGuid().ToString("N") + ".pending")
    $previous = Join-Path $parent ("." + [System.IO.Path]::GetFileName($LiteralPath) + "." + [guid]::NewGuid().ToString("N") + ".previous")
    $strictUtf8 = New-Object System.Text.UTF8Encoding($false, $true)
    try {
        $stream = New-Object System.IO.FileStream(
            $temporary,
            [System.IO.FileMode]::CreateNew,
            [System.IO.FileAccess]::Write,
            [System.IO.FileShare]::None
        )
        try {
            $writer = New-Object System.IO.StreamWriter($stream, $strictUtf8)
            try {
                $writer.Write($Content)
                $writer.Flush()
                $stream.Flush($true)
            }
            finally {
                $writer.Dispose()
            }
        }
        finally {
            if ($null -ne $stream) {
                $stream.Dispose()
            }
        }
        Assert-OwnedOrAbsent -LiteralPath $LiteralPath -OwnershipMarker $OwnershipMarker
        if (Test-Path -LiteralPath $LiteralPath) {
            [System.IO.File]::Replace($temporary, $LiteralPath, $previous)
        }
        else {
            [System.IO.File]::Move($temporary, $LiteralPath)
        }
    }
    finally {
        if (Test-Path -LiteralPath $temporary) {
            Remove-Item -LiteralPath $temporary -Force
        }
        if (Test-Path -LiteralPath $previous) {
            Remove-Item -LiteralPath $previous -Force
        }
    }
}

$pythonEnvironmentNames = @("PYTHONPATH", "PYTHONHOME", "PYTHONUSERBASE")
$originalPythonEnvironment = @{}
foreach ($environmentName in $pythonEnvironmentNames) {
    $originalPythonEnvironment[$environmentName] = [Environment]::GetEnvironmentVariable($environmentName, "Process")
}
try {
foreach ($environmentName in $pythonEnvironmentNames) {
    [Environment]::SetEnvironmentVariable($environmentName, $null, "Process")
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
Assert-OrdinaryPathChain -LiteralPath $resolvedSkillsParent

Invoke-CheckedPython -Executable $resolvedPython -Arguments @("--version")

$venvRoot = Join-Path $resolvedWorkflow ".venv"
Assert-OrdinaryPathChain -LiteralPath $venvRoot
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

$sitePackages = Get-OrdinaryPath -LiteralPath (Join-Path $venvRoot "Lib\site-packages") -Kind Directory
$scriptsRoot = Get-OrdinaryPath -LiteralPath (Join-Path $venvRoot "Scripts") -Kind Directory
$editableSource = Get-OrdinaryPath -LiteralPath (Join-Path $resolvedWorkflow "src") -Kind Directory
$ownershipMarker = "# university-skill-library-maintainer installer-owned"
$editableLink = Join-Path $sitePackages "university_skill_library_maintainer.pth"
$commandLauncher = Join-Path $scriptsRoot "skill-maintainer.cmd"
$nonIsolatedLauncher = Join-Path $scriptsRoot "skill-maintainer.exe"
Assert-OwnedOrAbsent -LiteralPath $commandLauncher -OwnershipMarker "@rem university-skill-library-maintainer installer-owned"

& $venvPython -I -c "import importlib.util; raise SystemExit(0 if importlib.util.find_spec('wheel') else 1)"
$wheelProbe = $LASTEXITCODE
if ($wheelProbe -eq 0) {
    if (Test-Path -LiteralPath $nonIsolatedLauncher) {
        throw "Refusing to overwrite an existing non-isolated skill-maintainer.exe launcher."
    }
    Invoke-CheckedPython -Executable $venvPython -Arguments @(
        "-m", "pip", "install", "--disable-pip-version-check", "--no-deps", "--no-build-isolation", "--editable", $resolvedWorkflow
    )
    if (Test-Path -LiteralPath $nonIsolatedLauncher) {
        [void](Get-OrdinaryPath -LiteralPath $nonIsolatedLauncher -Kind File)
        Remove-Item -LiteralPath $nonIsolatedLauncher -Force
    }
}
elseif ($wheelProbe -eq 1) {
    # Do not round-trip a Unicode path through native stdout: Windows PowerShell
    # 5.1 can decode Python's output with a different code page.
    Assert-OwnedOrAbsent -LiteralPath $editableLink -OwnershipMarker $ownershipMarker
    $sourceBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($editableSource))
    Write-AtomicOwnedText -LiteralPath $editableLink -OwnershipMarker $ownershipMarker -Content (
        $ownershipMarker + [Environment]::NewLine +
        "import base64,sys;sys.path.insert(0,base64.b64decode('$sourceBase64').decode('utf-8'))" +
        [Environment]::NewLine
    )
}
else {
    throw "Cannot determine whether the target virtual environment provides wheel."
}

Write-AtomicOwnedText -LiteralPath $commandLauncher -OwnershipMarker "@rem university-skill-library-maintainer installer-owned" -Content (
    "@rem university-skill-library-maintainer installer-owned" + [Environment]::NewLine +
    "@`"%~dp0python.exe`" -I -m skill_maintainer.cli %*" + [Environment]::NewLine
)

$expectedSource = Get-OrdinaryPath -LiteralPath (Join-Path $resolvedWorkflow "src") -Kind Directory
Invoke-CheckedPython -Executable $venvPython -Arguments @(
    "-c",
    "from pathlib import Path; import skill_maintainer; actual=Path(skill_maintainer.__file__).resolve(); expected=Path(__import__('sys').argv[1]).resolve(); raise SystemExit(0 if actual.is_relative_to(expected) else 1)",
    $expectedSource
)
$consoleCommand = Get-OrdinaryPath -LiteralPath $commandLauncher -Kind File
& $consoleCommand --help | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Installed skill-maintainer command failed with exit code $LASTEXITCODE."
}

Invoke-CheckedPython -Executable $venvPython -Arguments @(
    "-m", "skill_maintainer.cli", "setup", "--project-root", $resolvedProject,
    "--codex-skills-root", $resolvedSkillsParent
)
Invoke-CheckedPython -Executable $venvPython -Arguments @(
    "-m", "skill_maintainer.cli", "doctor", "--project-root", $resolvedProject
)

Write-Output "Installation checks completed. No automation was created; settings remain disabled/manual."
}
finally {
    foreach ($environmentName in $pythonEnvironmentNames) {
        [Environment]::SetEnvironmentVariable(
            $environmentName,
            $originalPythonEnvironment[$environmentName],
            "Process"
        )
    }
}
