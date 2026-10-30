"""Piezas comunes a todas las skills de crear-videos-pro. Mismo código en Mac y en Windows.

Cada script de una skill lo carga así (sin depender de variables de entorno del plugin):
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "_comun"))
    import comun
"""
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# skills/_comun/comun.py -> raíz del plugin (donde están skills/, stock/, estilos/)
RAIZ = Path(__file__).resolve().parents[2]
CONFIG_DIR = Path.home() / ".config" / "crear-videos"
CONFIG = CONFIG_DIR / "config"
ENV = CONFIG_DIR / ".env"
MODELOS_WHISPER = Path.home() / ".cache" / "hyperframes" / "whisper" / "models"
MODELO_WHISPER = MODELOS_WHISPER / "ggml-small.bin"   # multilingüe; small.en solo entiende inglés
FUENTE_MOSAICOS = RAIZ / "stock" / "fuentes" / "comunes" / "Inter-500.ttf"

SO = {"Darwin": "mac", "Windows": "windows"}.get(platform.system(), "linux")


def fallo(msg, codigo=1):
    print(msg, file=sys.stderr)
    sys.exit(codigo)


def leer_config():
    datos = {}
    if CONFIG.is_file():
        for linea in CONFIG.read_text(encoding="utf-8").splitlines():
            if "=" in linea and not linea.lstrip().startswith("#"):
                k, v = linea.split("=", 1)
                datos[k.strip()] = v.strip()
    return datos


def carpeta_usuario():
    """~/crear-videos (o la que diga el config). Ahí van mis-videos/ y mis-estilos/, fuera del plugin,
    porque la carpeta del plugin se sustituye entera en cada actualización."""
    c = leer_config().get("carpeta_usuario")
    return Path(os.path.expanduser(c)) if c else Path.home() / "crear-videos"


def mis_estilos():
    return carpeta_usuario() / "mis-estilos"


def mis_videos():
    return carpeta_usuario() / "mis-videos"


def clave(nombre="SCRAPECREATORS_API_KEY"):
    """Lee la clave del entorno o de ~/.config/crear-videos/.env. Nunca la imprime."""
    if os.environ.get(nombre):
        return os.environ[nombre]
    if ENV.is_file():
        for linea in ENV.read_text(encoding="utf-8").splitlines():
            if linea.startswith(nombre + "="):
                v = linea.split("=", 1)[1].strip().strip("\"'")
                if v:
                    return v
    return None


def aviso_clave():
    return ("No hay clave de ScrapeCreators. Cada persona usa la suya. Guárdala tú, a mano, en el archivo\n"
            f"  {ENV}\n"
            "con una línea así (cambia SU_CLAVE):  SCRAPECREATORS_API_KEY=SU_CLAVE\n"
            "No la escribas en el chat: queda en el historial.")


def herramienta(nombre):
    """Ruta de un programa (ffmpeg, ffprobe, yt-dlp, whisper-cli) o None."""
    if nombre == "whisper-cli":
        env = os.environ.get("HYPERFRAMES_WHISPER_PATH")
        if env and Path(env).is_file():
            return env
        for p in ("/opt/homebrew/bin/whisper-cli", "/usr/local/bin/whisper-cli"):
            if Path(p).is_file():
                return p
    return shutil.which(nombre) or shutil.which(nombre + ".exe")


def pista_instalar(paquete):
    if SO == "mac":
        brew = "brew install whisper-cpp" if paquete == "whisper" else f"brew install {paquete}"
        return f"  -> {brew}" if shutil.which("brew") else f"  -> primero Homebrew (https://brew.sh) y luego: {brew}"
    if SO == "windows":
        ids = {"ffmpeg": "Gyan.FFmpeg", "yt-dlp": "yt-dlp.yt-dlp", "exiftool": "OliverBetz.ExifTool"}
        if paquete == "whisper":
            return "  -> vuelve a ejecutar windows/instalar.cmd (instala whisper.cpp y HYPERFRAMES_WHISPER_PATH)"
        return f"  -> winget install --id {ids.get(paquete, paquete)} -e   (después cierra y abre Claude)"
    return f"  -> instálalo con el gestor de paquetes de tu sistema ({paquete})"


def correr(args, **kw):
    """subprocess.run con texto y sin abrir consola; lanza error si falla (salvo check=False)."""
    kw.setdefault("check", True)
    kw.setdefault("capture_output", True)
    kw.setdefault("text", True)
    return subprocess.run([str(a) for a in args], **kw)


def ffprobe(ruta, entradas, stream=None):
    args = ["ffprobe", "-v", "error"]
    if stream:
        args += ["-select_streams", stream]
    args += ["-show_entries", entradas, "-of", "csv=p=0", ruta]
    return correr(args).stdout.strip()


def fraccion(txt):
    a, _, b = txt.partition("/")
    return float(a) / float(b) if b and float(b) != 0 else (float(a) if not b else 0.0)


def scrapecreators(ruta_api, url, timeout=60):
    """GET a la API de ScrapeCreators con la clave del usuario. Devuelve el JSON."""
    k = clave()
    if not k:
        raise RuntimeError(aviso_clave())
    req = urllib.request.Request(
        f"https://api.scrapecreators.com{ruta_api}?url=" + urllib.parse.quote(url, safe=""),
        headers={"x-api-key": k})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def leer_info(estilo):
    datos = {}
    f = Path(estilo) / "info.txt"
    if not f.is_file():
        fallo(f"No hay {f}: ejecuta primero extraer.py")
    for linea in f.read_text(encoding="utf-8").splitlines():
        if "=" in linea:
            k, v = linea.split("=", 1)
            datos[k] = v
    return datos


def palabras_whisper(audio, idioma="auto"):
    """Transcribe con whisper.cpp en local y devuelve (palabras, idioma). Cada palabra: {texto, inicio, fin} en s.
    Une los tokens en palabras (un token que empieza con espacio abre una palabra nueva)."""
    import tempfile
    whisper = herramienta("whisper-cli")
    if not whisper:
        raise RuntimeError("no está whisper-cli (ejecuta comprobar.py)")
    if not MODELO_WHISPER.is_file():
        raise RuntimeError(f"falta el modelo {MODELO_WHISPER}")
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "voz16k.wav"
        correr(["ffmpeg", "-loglevel", "error", "-y", "-i", audio, "-vn", "-ac", "1", "-ar", "16000", wav])
        base = Path(tmp) / "salida"
        r = correr([whisper, "-m", MODELO_WHISPER, "-f", wav, "-l", idioma, "-ojf", "-of", base, "-np"], check=False)
        js = base.with_suffix(".json")
        if r.returncode != 0 or not js.is_file():
            raise RuntimeError(f"whisper-cli falló: {(r.stderr or '')[-300:]}")
        datos = json.loads(js.read_text(encoding="utf-8", errors="replace"))
    palabras = []
    for seg in datos.get("transcription", []):
        for tok in seg.get("tokens", []):
            t = tok.get("text", "")
            if not t or t.startswith("[_") or t.startswith("<|"):
                continue
            ini, fin = tok["offsets"]["from"] / 1000, tok["offsets"]["to"] / 1000
            if t.startswith(" ") or not palabras:
                palabras.append({"texto": t.strip(), "inicio": ini, "fin": fin})
            else:
                palabras[-1]["texto"] += t
                palabras[-1]["fin"] = fin
    palabras = [p for p in palabras if p["texto"]]
    return palabras, datos.get("result", {}).get("language", idioma)


def fuente(tam):
    """Fuente de los mosaicos: va dentro del repo, así es igual en Mac y en Windows."""
    from PIL import ImageFont
    if not FUENTE_MOSAICOS.is_file():
        fallo(f"Falta la fuente {FUENTE_MOSAICOS} (el plugin está incompleto: reinstálalo)")
    return ImageFont.truetype(str(FUENTE_MOSAICOS), tam)
