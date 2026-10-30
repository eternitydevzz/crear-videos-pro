# CLAUDE.md — manual del repo para Claude

Repo privado del equipo: un **plugin de Claude Code** con 5 skills de edición de vídeo, el Estilo Maestria, estilos de otros creadores y el stock. Responde siempre en español.

## Si te piden «instálame esto»
1. Lee [INSTALAR.md](INSTALAR.md) y detecta el sistema (Mac o Windows).
2. Comprueba «Antes de empezar» y **pide a la persona** lo que solo puede hacer ella: instalar Homebrew (pide su contraseña), Git for Windows, `gh auth login`, aceptar la invitación al repo.
3. **La clave de ScrapeCreators nunca se escribe en el chat.** Si la persona quiere ponerla, dale el comando que abre el archivo `~/.config/crear-videos/.env` y que la escriba ella.
4. Ejecuta el instalador (`bash mac/instalar.sh` o `windows\instalar.cmd`) y cuenta lo que imprime. Si falla, di en qué paso y qué quedó hecho.
5. Termina pidiéndole que abra una sesión nueva y escriba `/crear-videos-pro:crear-estilo-videos`.

## Dónde está cada cosa
- `skills/<skill>/SKILL.md`: las 5 skills. `skills/_comun/`: código común (`comun.py`) y `comprobar.py`.
- `estilos/Estilo Maestria/`: 4 fichas (`youtube/`, `formacion/`, `whatsapp-comunidad/`, `edicion-claude/`), `motores/` y `herramientas/`.
- `estilos/creadores/`: 6 fichas de otros creadores con sus mosaicos.
- `stock/`: ver [STOCK.md](STOCK.md).
- Lo de cada usuario vive **fuera del repo**: `~/crear-videos/mis-videos/`, `~/crear-videos/mis-estilos/` y `~/.config/crear-videos/` (config, `.env`, `venv/` y el lanzador `py`).

## Reglas para trabajar aquí
- **Python siempre con el lanzador**: `bash ~/.config/crear-videos/py SCRIPT.py …`. Nunca `python` o `python3` a secas (en el Mac `python` no existe y el del sistema no tiene Pillow).
- **Un solo código para Mac y Windows.** Rutas con `/`; en Windows los comandos van por Git Bash. Nada de herramientas que solo hay en el Mac (`sips`, `mdls`, `xattr`, `/System/Library`) salvo con su alternativa para Windows.
- **Nunca escribas dentro de la carpeta del plugin instalado**: se sustituye entera al actualizar. Lo nuevo va a `~/crear-videos/`.
- **Los scripts encuentran la raíz del plugin solos** (`comun.RAIZ`); no guardes rutas del plugin en archivos: cambian en cada versión.
- **Nada personal en el repo**: ni nombres, ni emails, ni rutas de un ordenador, ni caras (salvo las excepciones del README). Antes de cada versión: `revisar_repo.sh` de la skill crear-repos y `gitleaks`.
- **Versiones:** cada cambio que deba llegar al equipo sube `version` en `.claude-plugin/plugin.json`. Si no, nadie lo recibe.
- Si cambias un `.md`, pasa `bash ~/.config/crear-videos/py pruebas/enlaces.py`.

## Lo que no hay que hacer
- Fijar o cambiar la versión de HyperFrames sin avisar: los motores se probaron con la 0.8.114.
- Normalizar el volumen al entregar: el vídeo sale tal cual del render (decisión del equipo).
- Copiar archivos de trabajo de los reels de otros creadores (vídeos, audio, fotogramas) al repo: solo `estilo.md` y mosaicos.
