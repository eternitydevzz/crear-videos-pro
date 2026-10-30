#!/usr/bin/env bash
# Actualiza crear-videos-pro en un Mac: baja lo último del repo, actualiza el plugin y las librerías de Python.
# Uso: bash mac/actualizar.sh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000   # el repo pesa ~320 MB

echo "== 1/3 Repo"
git -C "$REPO" pull --ff-only
echo "== 2/3 Plugin"
claude plugin marketplace update crear-videos-pro
claude plugin update crear-videos-pro@crear-videos-pro || true   # sale con error si ya estaba al día
echo "== 3/3 Librerías de Python"
"$HOME/.config/crear-videos/venv/bin/python" -m pip install --quiet --disable-pip-version-check -r "$REPO/requirements.txt"
bash "$HOME/.config/crear-videos/py" "$REPO/skills/_comun/comprobar.py"
echo "Hecho. Abre una sesión NUEVA de Claude Code para usar la versión nueva."
