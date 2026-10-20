# Windows 用ラッパー：音声生成 → 映像レンダリング → video.mp4
# 使い方:  .\render-win.ps1 demos\01-flat-vector [render.mjs への追加オプション]
#   例:    .\render-win.ps1 demos\01-flat-vector --stills '0.5,5,9.5'   (カンマ区切りは必ず引用符で囲む)
#          .\render-win.ps1 demos\01-flat-vector --scale 0.5     (低解像度の試し書き出し)
#          .\render-win.ps1 demos\01-flat-vector -NoAudio        (audio.py を実行しない)
param(
  [Parameter(Mandatory = $true, Position = 0)][string]$Demo,
  [switch]$NoAudio,
  [Parameter(ValueFromRemainingArguments = $true)][string[]]$Rest
)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
Set-Location $root

$env:MG_CHROME = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
# 元の既定値は macOS(Metal) / Linux(EGL) 用。Windows では ANGLE/D3D11 を使う
if (-not $env:MG_GPU_ARGS) { $env:MG_GPU_ARGS = '--use-angle=d3d11' }
# ユーザー名のアポストロフィが ffmpeg の concat リストを壊すため、一時フォルダをリポジトリ内に置く
$tmp = Join-Path $root '.tmp'
New-Item -ItemType Directory -Force $tmp | Out-Null
$env:TMP = $tmp; $env:TEMP = $tmp

$py = Join-Path $root '.venv\Scripts\python.exe'
$audioPy = Join-Path $Demo 'audio.py'
$isStills = $Rest -contains '--stills'
if (-not $NoAudio -and -not $isStills -and (Test-Path $audioPy)) {
  Write-Host "== audio: $audioPy"
  & $py $audioPy
  if ($LASTEXITCODE -ne 0) { throw "audio.py failed ($LASTEXITCODE)" }
}
Write-Host "== render: $Demo"
& node harness/render.mjs $Demo @Rest
if ($LASTEXITCODE -ne 0) { throw "render failed ($LASTEXITCODE)" }
