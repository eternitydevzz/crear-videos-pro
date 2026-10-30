# Actualiza crear-videos-pro en Windows: baja lo último del repo, actualiza el plugin y las librerías de Python.
# Uso: windows\actualizar.cmd
$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path "$PSScriptRoot\..").Path
$Py = Join-Path $env:USERPROFILE ".config\crear-videos\venv\Scripts\python.exe"
$env:CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS = "300000"   # el repo pesa ~320 MB

Write-Host "== 1/3 Repo"
git -C $Repo pull --ff-only
Write-Host "== 2/3 Plugin"
claude plugin marketplace update crear-videos-pro
claude plugin update crear-videos-pro@crear-videos-pro   # da error si ya estaba al día: no pasa nada
Write-Host "== 3/3 Librerías de Python"
& $Py -m pip install --quiet --disable-pip-version-check -r (Join-Path $Repo "requirements.txt")
& $Py (Join-Path $Repo "skills\_comun\comprobar.py")
Write-Host "Hecho. Abre una sesión NUEVA de Claude Code para usar la versión nueva."
