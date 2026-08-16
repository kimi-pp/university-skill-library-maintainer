$ErrorActionPreference = 'Stop'

$root = $PSScriptRoot
$manifestPath = Join-Path $root 'source_manifest.json'
$manifest = Get-Content -Raw -Encoding utf8 $manifestPath | ConvertFrom-Json

foreach ($source in $manifest.sources) {
    $uri = [Uri]$source.url
    if ($uri.Scheme -ne 'https' -or $uri.Host -notmatch '(^|\.)moe\.gov\.cn$') {
        throw "Official source must use an moe.gov.cn HTTPS host: $($source.url)"
    }

    $destination = Join-Path $root $source.local_path
    $destinationDirectory = Split-Path -Parent $destination
    New-Item -ItemType Directory -Force $destinationDirectory | Out-Null
    Invoke-WebRequest -Uri $source.url -OutFile $destination
    $source.sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $destination).Hash.ToLowerInvariant()
}

$manifest | ConvertTo-Json -Depth 5 | Set-Content -Encoding utf8 $manifestPath

# Windows PowerShell's UTF-8 encoding adds a BOM, while the consumer reads the
# manifest as strict UTF-8. Preserve the required Set-Content write and remove
# that legacy-only marker afterwards.
if ($PSVersionTable.PSEdition -eq 'Desktop') {
    $bytes = [System.IO.File]::ReadAllBytes($manifestPath)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        [System.IO.File]::WriteAllBytes($manifestPath, $bytes[3..($bytes.Length - 1)])
    }
}
