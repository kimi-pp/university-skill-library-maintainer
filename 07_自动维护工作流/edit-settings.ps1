[CmdletBinding()]
param(
    [string]$SettingsPath = (Join-Path $PSScriptRoot 'workflow-settings.toml')
)

$ErrorActionPreference = 'Stop'
$projectPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $projectPython -PathType Leaf)) {
    throw '未找到安装程序创建的项目 Python 环境；请先运行 install.ps1。'
}

$absoluteSettings = [IO.Path]::GetFullPath($SettingsPath)
& $projectPython -m skill_maintainer.settings_editor --settings $absoluteSettings
exit $LASTEXITCODE
