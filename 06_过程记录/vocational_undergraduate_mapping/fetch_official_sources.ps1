[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$mappingRoot = $PSScriptRoot
$snapshotRoot = Join-Path $mappingRoot 'source_snapshots'
$inputPath = 'D:\高校AI工作台\高职高专Skills领域分类表.xlsx'

if (-not (Test-Path -LiteralPath $inputPath -PathType Leaf)) {
    throw "Missing external input workbook: $inputPath"
}

New-Item -ItemType Directory -Path $snapshotRoot -Force | Out-Null

$sources = @(
    [ordered]@{
        id = 'vocational_2021_base'
        kind = 'docx'
        title = '职业教育专业目录（2021年）'
        publisher = '教育部'
        publication_date = '2021-03-17'
        url = 'https://www.moe.gov.cn/srcsite/A07/moe_953/202103/W020210319595911145604.docx'
        local_path = 'source_snapshots/vocational_2021_base.docx'
        applies_to = '职业教育专业基础目录'
    },
    [ordered]@{
        id = 'vocational_2025_supplement'
        kind = 'doc'
        title = '2025年职业教育专业目录增补清单'
        publisher = '教育部办公厅'
        publication_date = '2025-12-01'
        url = 'https://www.moe.gov.cn/srcsite/A07/moe_737/s3876_qt/202601/W020260106393908779349.doc'
        local_path = 'source_snapshots/vocational_2025_supplement.doc'
        applies_to = '2025年职业教育专业目录增补沿革'
    },
    [ordered]@{
        id = 'vocational_effective_2026_07'
        kind = 'docx'
        title = '职业教育专业目录（2021年）（更新时间：2026年7月）'
        publisher = '教育部'
        publication_date = '2026-07-16'
        url = 'https://www.moe.gov.cn/s78/A07/zcs_ztzl/2017_zt06/17zt06_bznr/zhijiao/202607/P020260714589584937536.docx'
        local_path = 'source_snapshots/vocational_effective_2026_07.docx'
        applies_to = '截至2026年7月的现行职业教育专业完整目录'
    },
    [ordered]@{
        id = 'vocational_2021_notice'
        kind = 'html'
        title = '教育部关于印发《职业教育专业目录（2021年）》的通知'
        publisher = '教育部'
        publication_date = '2021-03-19'
        url = 'https://www.moe.gov.cn/srcsite/A07/moe_953/202103/t20210319_521135.html'
        local_path = 'source_snapshots/vocational_2021_notice.html'
        applies_to = '基础目录发布说明与744个高职专科专业基线'
    },
    [ordered]@{
        id = 'vocational_2025_notice'
        kind = 'html'
        title = '教育部办公厅关于做好2026年职业教育拟招生专业设置管理工作的通知'
        publisher = '教育部办公厅'
        publication_date = '2025-12-01'
        url = 'https://www.moe.gov.cn/srcsite/A07/moe_737/s3876_qt/202601/t20260105_1425685.html'
        local_path = 'source_snapshots/vocational_2025_notice.html'
        applies_to = '2025年增补清单发布依据'
    },
    [ordered]@{
        id = 'vocational_2026_release'
        kind = 'html'
        title = '《职业教育专业目录》增补27个新专业'
        publisher = '教育部'
        publication_date = '2026-07-16'
        url = 'https://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/202607/t20260715_1443823.html'
        local_path = 'source_snapshots/vocational_2026_release.html'
        applies_to = '2026年新增9个高职专科专业及执行时间说明'
    },
    [ordered]@{
        id = 'vocational_2026_qa'
        kind = 'html'
        title = '教育部职业教育与成人教育司负责人就2026年《职业教育专业目录》专业增补答记者问'
        publisher = '教育部'
        publication_date = '2026-07-16'
        url = 'https://www.moe.gov.cn/jyb_xwfb/s271/202607/t20260715_1443829.html'
        local_path = 'source_snapshots/vocational_2026_qa.html'
        applies_to = '2026年增补口径说明'
    }
)

foreach ($source in $sources) {
    $uri = [Uri]$source.url
    if ($uri.Scheme -ne 'https' -or -not ($uri.Host -eq 'moe.gov.cn' -or $uri.Host.EndsWith('.moe.gov.cn'))) {
        throw "Rejected non-official source URL: $($source.url)"
    }

    $target = Join-Path $mappingRoot ($source.local_path -replace '/', '\')
    Invoke-WebRequest -Uri $source.url -UseBasicParsing -OutFile $target
    $item = Get-Item -LiteralPath $target
    if ($item.Length -le 1000) {
        throw "Downloaded source is unexpectedly small: $($source.id)"
    }
    $source.sha256 = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
    $source.size_bytes = $item.Length
}

$sourceManifest = [ordered]@{
    accessed_at = '2026-08-17'
    sources = $sources
}
$sourceManifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $mappingRoot 'source_manifest.json') -Encoding utf8

$inputManifest = [ordered]@{
    absolute_path = 'D:/高校AI工作台/高职高专Skills领域分类表.xlsx'
    sha256 = (Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash.ToLowerInvariant()
    size_bytes = (Get-Item -LiteralPath $inputPath).Length
    accessed_at = '2026-08-17'
    sheets = [ordered]@{
        'Skills领域分类总表' = 'A1:E61'
        '领域分类-专业反向索引' = 'A1:F15'
        '专业大类-领域分类矩阵' = 'A1:R20'
        '专业类-领域分类明细' = 'A1:F389'
    }
}
$inputManifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $mappingRoot 'input_manifest.json') -Encoding utf8

Write-Output "Frozen $($sources.Count) official sources and one external input workbook."
