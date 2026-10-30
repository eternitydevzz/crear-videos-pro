# Instala crear-videos-pro en Windows 10/11. Antes hay que haber hecho «Antes de empezar» de INSTALAR.md.
# Uso (doble clic o en una terminal):  windows\instalar.cmd          (plugin desde GitHub)
#                                      windows\instalar.cmd -Local   (plugin desde esta carpeta, para probar)
# Se puede repetir: lo que ya está hecho se salta.
param([switch]$Local)
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"   # sin barra de progreso, Invoke-WebRequest va mucho más rápido

$Repo = (Resolve-Path "$PSScriptRoot\..").Path
$Origen = if ($Local) { $Repo } else { "eternitydevzz/crear-videos-pro" }
$Cfg = Join-Path $env:USERPROFILE ".config\crear-videos"
$Venv = Join-Path $Cfg "venv"
$Modelos = Join-Path $env:USERPROFILE ".cache\hyperframes\whisper\models"
$ModeloUrl = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin"
$ModeloBytes = 487601967          # tamaño real de ggml-small.bin; si no coincide, la descarga se cortó
$WhisperUrl = "https://github.com/ggml-org/whisper.cpp/releases/download/b5454/whisper-bin-x64.zip"
$WhisperDir = Join-Path $env:LOCALAPPDATA "whisper.cpp"
$HyperFrames = "heygen-com/hyperframes#v0.8.114"   # versión con la que se probaron los motores
$env:CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS = "300000"   # el repo pesa ~320 MB

function Paso($t) { Write-Host "`n== $t" -ForegroundColor Cyan }
function Para($t) { Write-Host "`nNO SE PUEDE SEGUIR: $t" -ForegroundColor Red; exit 1 }
function Hay($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function RecargarPath {
  $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
}
New-Item -ItemType Directory -Force -Path $Cfg | Out-Null

Paso "1/9 Tu clave de ScrapeCreators (cada persona la suya)"
$Env = Join-Path $Cfg ".env"
if ((Test-Path $Env) -and (Select-String -Path $Env -Pattern '^SCRAPECREATORS_API_KEY=.' -Quiet)) {
  Write-Host "Clave encontrada (no se muestra)."
} else {
  Write-Host "AVISO: no hay clave. Se instala igual; sin clave solo se pierde la descarga de emergencia de reels" -ForegroundColor Yellow
  Write-Host "(cuando yt-dlp falla). Para ponerla, sigue el paso 4 de «Antes de empezar» en INSTALAR.md." -ForegroundColor Yellow
}

Paso "2/9 Programas (winget)"
if (-not (Hay "winget")) { Para "falta winget. Actualiza «Instalador de aplicación» desde Microsoft Store." }
if (-not (Hay "git")) { Para "falta Git for Windows (obligatorio). Instálalo: winget install --id Git.Git -e  y vuelve a abrir la terminal." }
$paquetes = @(
  @{cmd = "ffmpeg";   id = "Gyan.FFmpeg"},
  @{cmd = "exiftool"; id = "OliverBetz.ExifTool"},
  @{cmd = "yt-dlp";   id = "yt-dlp.yt-dlp"},
  @{cmd = "py";       id = "Python.Python.3.13"},
  @{cmd = "node";     id = "OpenJS.NodeJS.LTS"},
  @{cmd = "gh";       id = "GitHub.cli"}
)
foreach ($p in $paquetes) {
  if (Hay $p.cmd) { Write-Host "Ya está: $($p.cmd)" }
  else {
    Write-Host "Instalando $($p.id)…"
    winget install --id $p.id -e --silent --accept-package-agreements --accept-source-agreements
    RecargarPath
  }
}

Paso "3/9 whisper.cpp ($WhisperDir)"
$WhisperExe = Join-Path $WhisperDir "Release\whisper-cli.exe"
if (-not (Test-Path $WhisperExe)) {
  $zip = Join-Path $env:TEMP "whisper-bin-x64.zip"
  Invoke-WebRequest -Uri $WhisperUrl -OutFile $zip
  Expand-Archive -Path $zip -DestinationPath $WhisperDir -Force
  Remove-Item $zip
}
if (-not (Test-Path $WhisperExe)) { Para "no encuentro $WhisperExe dentro del zip de whisper.cpp" }
# Guardada para siempre: HyperFrames y las skills buscan whisper aquí
setx HYPERFRAMES_WHISPER_PATH "$WhisperExe" | Out-Null
$env:HYPERFRAMES_WHISPER_PATH = $WhisperExe
Write-Host "whisper-cli: $WhisperExe"

Paso "4/9 Python propio ($Venv)"
$Py = Join-Path $Venv "Scripts\python.exe"
if (-not (Test-Path $Py)) { py -3.13 -m venv $Venv; if (-not $?) { py -3 -m venv $Venv } }
& $Py -m pip install --quiet --disable-pip-version-check --upgrade pip
& $Py -m pip install --quiet --disable-pip-version-check -r (Join-Path $Repo "requirements.txt")
& $Py -c "import PIL, numpy, pillow_heif; print('Pillow', PIL.__version__, '· numpy', numpy.__version__)"

Paso "5/9 Lanzador $Cfg\py (Git Bash)"
$lanzador = @'
#!/usr/bin/env bash
# Python de crear-videos-pro (con Pillow y numpy). Uso: bash ~/.config/crear-videos/py SCRIPT.py ...
V="$HOME/.config/crear-videos/venv"
if [ -x "$V/bin/python" ]; then exec "$V/bin/python" "$@"
elif [ -x "$V/Scripts/python.exe" ]; then exec "$V/Scripts/python.exe" "$@"
else echo "No está el Python de crear-videos-pro: ejecuta el instalador (INSTALAR.md)." >&2; exit 1; fi
'@
# Finales de línea LF: con CRLF, Git Bash falla con «\r»
[IO.File]::WriteAllText((Join-Path $Cfg "py"), ($lanzador -replace "`r`n", "`n") + "`n", (New-Object Text.UTF8Encoding $false))
Write-Host "Listo."

Paso "6/9 Modelo de Whisper ggml-small.bin (multilingüe, 488 MB)"
New-Item -ItemType Directory -Force -Path $Modelos | Out-Null
$Modelo = Join-Path $Modelos "ggml-small.bin"
if (-not ((Test-Path $Modelo) -and ((Get-Item $Modelo).Length -eq $ModeloBytes))) {
  Invoke-WebRequest -Uri $ModeloUrl -OutFile "$Modelo.part"
  if ((Get-Item "$Modelo.part").Length -ne $ModeloBytes) { Para "el modelo no se bajó entero; vuelve a ejecutar el instalador" }
  Move-Item -Force "$Modelo.part" $Modelo
} else { Write-Host "Ya está." }

Paso "7/9 Tu carpeta (crear-videos) y ajustes"
$Usuario = Join-Path $env:USERPROFILE "crear-videos"
New-Item -ItemType Directory -Force -Path (Join-Path $Usuario "mis-videos"), (Join-Path $Usuario "mis-estilos") | Out-Null
$Config = Join-Path $Cfg "config"
if (-not (Test-Path $Config)) { [IO.File]::WriteAllText($Config, "carpeta_usuario=$Usuario`n", (New-Object Text.UTF8Encoding $false)) }
Write-Host "Vídeos: $Usuario\mis-videos · Estilos: $Usuario\mis-estilos"

Paso "8/9 Plugins de Claude Code"
if (-not (Hay "claude")) { Para "falta Claude Code. Instálalo: irm https://claude.ai/install.ps1 | iex" }
$lista = (claude plugin marketplace list 2>$null) -join "`n"
if ($lista -match "hyperframes") { Write-Host "HyperFrames ya estaba añadido: no se toca (los motores se probaron con la 0.8.114)." }
else { claude plugin marketplace add $HyperFrames }
if (-not ((claude plugin list 2>$null) -join "`n" -match "hyperframes@hyperframes")) { claude plugin install hyperframes@hyperframes }
if ($lista -match "crear-videos-pro") { claude plugin marketplace update crear-videos-pro }
else { claude plugin marketplace add $Origen }
if (-not ((claude plugin list 2>$null) -join "`n" -match "crear-videos-pro@crear-videos-pro")) { claude plugin install crear-videos-pro@crear-videos-pro }

Paso "9/9 Comprobación final"
& $Py (Join-Path $Repo "skills\editar-con-estilo\scripts\comprobar_edicion.py")
Write-Host "`nHecho. Cierra esta terminal, abre una sesión NUEVA de Claude Code y escribe:  /crear-videos-pro:crear-estilo-videos"
