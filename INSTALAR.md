# Instalar crear-videos-pro

Sirve para personas y para Claude. Si le dices a Claude *«instálame esto»*, sigue esta guía y te pide lo que tienes que hacer tú.

## Contenido
- [Antes de empezar](#antes-de-empezar)
- [Mac](#mac)
- [Windows](#windows)
- [Comprobar](#comprobar)
- [Actualizar](#actualizar)
- [Dónde queda cada cosa](#dónde-queda-cada-cosa)
- [Problemas frecuentes](#problemas-frecuentes)

## Antes de empezar

Estos pasos los hace la persona, a mano, una sola vez. El instalador no puede hacerlos por ti.

1. **Cuenta de Claude de pago** (Pro, Max, Team o Enterprise) y **Claude Code** instalado e iniciado.
   - Mac:
     ```bash
     curl -fsSL https://claude.ai/install.sh | bash
     ```
   - Windows (PowerShell):
     ```powershell
     irm https://claude.ai/install.ps1 | iex
     ```
2. **Herramientas base**
   - Mac: **Homebrew** (te pide la contraseña del Mac). Sigue https://brew.sh
   - Windows: **Git for Windows** (obligatorio: Claude Code y las skills usan su Git Bash).
     ```powershell
     winget install --id Git.Git -e
     ```
3. **Acceso al repo.** Acepta la invitación de GitHub que te llegó por email. Después conecta tu ordenador con GitHub:
   - Mac: `brew install gh` · Windows: `winget install --id GitHub.cli -e`
   - Luego, en los dos:
     ```bash
     gh auth login
     ```
     ```bash
     gh auth setup-git
     ```
4. **Tu clave de ScrapeCreators** (opcional, cada persona la suya). Solo se usa para bajar un reel cuando yt-dlp falla. **Escríbela tú, nunca en el chat de Claude** (lo que escribes ahí queda guardado).
   - Mac:
     ```bash
     mkdir -p ~/.config/crear-videos && touch ~/.config/crear-videos/.env && open -e ~/.config/crear-videos/.env
     ```
   - Windows (PowerShell):
     ```powershell
     New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\crear-videos" | Out-Null; notepad "$env:USERPROFILE\.config\crear-videos\.env"
     ```
   En el archivo que se abre, escribe una línea con tu clave y guarda:
   ```
   SCRAPECREATORS_API_KEY=TU_CLAVE
   ```
   Si no la pones, todo se instala igual y el instalador solo avisa.

## Mac

```bash
gh repo clone eternitydevzz/crear-videos-pro ~/crear-videos-pro
```
```bash
bash ~/crear-videos-pro/mac/instalar.sh
```

Instala lo que falte con Homebrew (ffmpeg, exiftool, yt-dlp, Python, Node, whisper-cpp y gh), crea un Python propio con Pillow y numpy, baja el modelo de Whisper (488 MB), crea tu carpeta `~/crear-videos/` y añade a Claude Code los plugins **HyperFrames 0.8.114** y **crear-videos-pro**. Al final dice «Todo listo».

## Windows

En PowerShell:

```powershell
gh repo clone eternitydevzz/crear-videos-pro "$env:USERPROFILE\crear-videos-pro"
```
```powershell
& "$env:USERPROFILE\crear-videos-pro\windows\instalar.cmd"
```

(o doble clic en `windows\instalar.cmd`). Instala con winget lo que falte (ffmpeg de Gyan, ExifTool, yt-dlp, Python 3.13, Node LTS y gh), baja **whisper.cpp** (zip oficial) a `%LOCALAPPDATA%\whisper.cpp` y guarda `HYPERFRAMES_WHISPER_PATH`, crea el Python propio, baja el modelo y añade los dos plugins. Al terminar, **cierra la terminal** y abre una nueva para que se carguen los cambios.

> Si algo falla, copia el error y pásaselo a Claude o al equipo.

## Comprobar

Abre una sesión **nueva** de Claude Code y escribe:

```
/crear-videos-pro:crear-estilo-videos
```

Debe empezar pidiéndote el nombre del estilo y el link del reel. Para ver solo si está todo:

```bash
bash ~/.config/crear-videos/py ~/crear-videos-pro/skills/editar-con-estilo/scripts/comprobar_edicion.py
```

## Actualizar

- Mac: `bash ~/crear-videos-pro/mac/actualizar.sh`
- Windows: `windows\actualizar.cmd`

Baja lo último del repo, actualiza el plugin y las librerías, y comprueba. Después abre una sesión nueva.

Dentro de Claude Code también vale `/plugin marketplace update crear-videos-pro`. Para que se actualice solo: `/plugin` → Marketplaces → crear-videos-pro → **Enable auto-update**.

## Dónde queda cada cosa

| Qué | Dónde |
|---|---|
| Tus vídeos | `~/crear-videos/mis-videos/` |
| Tus estilos nuevos | `~/crear-videos/mis-estilos/` |
| Tu clave y ajustes | `~/.config/crear-videos/` (`.env` y `config`) |
| El Python del equipo | `~/.config/crear-videos/venv/` y el lanzador `~/.config/crear-videos/py` |
| El modelo de Whisper | `~/.cache/hyperframes/whisper/models/ggml-small.bin` |
| El plugin (no lo toques: se sustituye al actualizar) | lo gestiona Claude Code |

En Windows, `~` es tu carpeta de usuario (`C:\Users\<tu usuario>`).

## Problemas frecuentes

- **`Git clone timed out after 120s`** al añadir o actualizar el plugin: el repo pesa ~320 MB. Los instaladores ya dan 300 s; si lo haces a mano, antes ejecuta `export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000` (Mac) o `$env:CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS="300000"` (Windows).
- **No encuentra el repo** (`Repository not found`): acepta la invitación de GitHub y repite `gh auth login` y `gh auth setup-git`.
- **Sin clave SSH de GitHub** y falla `/plugin`: pon `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` antes de abrir Claude Code.
- **`No está el Python de crear-videos-pro`**: vuelve a ejecutar el instalador.
- **La skill no aparece**: abre una sesión **nueva** de Claude Code y mira `/plugin` → Installed.
