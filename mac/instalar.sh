#!/usr/bin/env bash
# Instala crear-videos-pro en un Mac. Antes hay que haber hecho «Antes de empezar» de INSTALAR.md.
# Uso:  bash mac/instalar.sh            (instala el plugin desde GitHub)
#       bash mac/instalar.sh --local    (instala el plugin desde esta carpeta, para probar)
# Se puede repetir: lo que ya está hecho se salta.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
ORIGEN="eternitydevzz/crear-videos-pro"
[ "${1:-}" = "--local" ] && ORIGEN="$REPO"
CFG="$HOME/.config/crear-videos"
VENV="$CFG/venv"
MODELOS="$HOME/.cache/hyperframes/whisper/models"
MODELO_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin"
MODELO_BYTES=487601967      # tamaño real de ggml-small.bin (multilingüe); si no coincide, la descarga se cortó
HYPERFRAMES="heygen-com/hyperframes#v0.8.114"   # versión con la que se probaron los motores
# El repo pesa ~320 MB: con conexión lenta, clonarlo pasa de los 120 s que da Claude Code por defecto
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000

paso() { printf '\n== %s\n' "$1"; }
para() { printf '\nNO SE PUEDE SEGUIR: %s\n' "$1" >&2; exit 1; }
mkdir -p "$CFG"

paso "1/8 Tu clave de ScrapeCreators (cada persona la suya)"
if grep -qs '^SCRAPECREATORS_API_KEY=.' "$CFG/.env"; then
  chmod 600 "$CFG/.env"
  echo "Clave encontrada (no se muestra)."
else
  echo "AVISO: no hay clave. Se instala igual; sin clave solo se pierde la descarga de emergencia de reels"
  echo "(cuando yt-dlp falla). Para ponerla, sigue el paso 4 de «Antes de empezar» en INSTALAR.md."
fi

paso "2/8 Homebrew y programas"
command -v brew >/dev/null || para "falta Homebrew. Instálalo tú (pide la contraseña del Mac): https://brew.sh"
faltan=()
for par in ffmpeg:ffmpeg exiftool:exiftool yt-dlp:yt-dlp python3:python node:node whisper-cli:whisper-cpp gh:gh; do
  command -v "${par%%:*}" >/dev/null || faltan+=("${par#*:}")
done
if [ ${#faltan[@]} -gt 0 ]; then
  echo "Instalando: ${faltan[*]}"
  brew install "${faltan[@]}"
else
  echo "Ya están: ffmpeg, exiftool, yt-dlp, python3, node, whisper-cpp y gh."
fi

paso "3/8 Python propio ($VENV)"
[ -x "$VENV/bin/python" ] || python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --quiet --disable-pip-version-check --upgrade pip
"$VENV/bin/python" -m pip install --quiet --disable-pip-version-check -r "$REPO/requirements.txt"
"$VENV/bin/python" -c "import PIL, numpy, pillow_heif; print('Pillow', PIL.__version__, '· numpy', numpy.__version__, '· pillow-heif', pillow_heif.__version__)"

paso "4/8 Lanzador $CFG/py"
cat > "$CFG/py" <<'EOF'
#!/usr/bin/env bash
# Python de crear-videos-pro (con Pillow y numpy). Uso: bash ~/.config/crear-videos/py SCRIPT.py ...
V="$HOME/.config/crear-videos/venv"
if [ -x "$V/bin/python" ]; then exec "$V/bin/python" "$@"
elif [ -x "$V/Scripts/python.exe" ]; then exec "$V/Scripts/python.exe" "$@"
else echo "No está el Python de crear-videos-pro: ejecuta el instalador (INSTALAR.md)." >&2; exit 1; fi
EOF
chmod +x "$CFG/py"
echo "Listo."

paso "5/8 Modelo de Whisper ggml-small.bin (multilingüe, 488 MB)"
mkdir -p "$MODELOS"
if [ "$(stat -f %z "$MODELOS/ggml-small.bin" 2>/dev/null || echo 0)" != "$MODELO_BYTES" ]; then
  curl -L --fail --progress-bar -o "$MODELOS/ggml-small.bin.part" "$MODELO_URL"
  [ "$(stat -f %z "$MODELOS/ggml-small.bin.part")" = "$MODELO_BYTES" ] || para "el modelo no se bajó entero; vuelve a ejecutar el instalador"
  mv "$MODELOS/ggml-small.bin.part" "$MODELOS/ggml-small.bin"
else
  echo "Ya está."
fi

paso "6/8 Tu carpeta (~/crear-videos) y ajustes"
mkdir -p "$HOME/crear-videos/mis-videos" "$HOME/crear-videos/mis-estilos"
[ -f "$CFG/config" ] || printf 'carpeta_usuario=%s\n' "$HOME/crear-videos" > "$CFG/config"
echo "Vídeos: ~/crear-videos/mis-videos · Estilos: ~/crear-videos/mis-estilos"

paso "7/8 Plugins de Claude Code"
command -v claude >/dev/null || para "falta Claude Code. Instálalo: curl -fsSL https://claude.ai/install.sh | bash"
lista="$(claude plugin marketplace list 2>/dev/null || true)"
if echo "$lista" | grep -q 'hyperframes'; then
  echo "HyperFrames ya estaba añadido: no se toca. Versión instalada:"
  claude plugin list 2>/dev/null | grep -A2 'hyperframes@hyperframes' | grep -i version || true
  echo "(los motores se probaron con la 0.8.114)"
else
  claude plugin marketplace add "$HYPERFRAMES"
fi
claude plugin list 2>/dev/null | grep -q 'hyperframes@hyperframes' || claude plugin install hyperframes@hyperframes
if echo "$lista" | grep -q 'crear-videos-pro'; then
  claude plugin marketplace update crear-videos-pro
else
  claude plugin marketplace add "$ORIGEN"
fi
claude plugin list 2>/dev/null | grep -q 'crear-videos-pro@crear-videos-pro' \
  || claude plugin install crear-videos-pro@crear-videos-pro

paso "8/8 Comprobación final"
bash "$CFG/py" "$REPO/skills/editar-con-estilo/scripts/comprobar_edicion.py"
echo
echo "Hecho. Abre una sesión NUEVA de Claude Code y escribe:  /crear-videos-pro:crear-estilo-videos"
