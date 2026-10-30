"""Comprueba lo que hace falta y dice qué falta, con el comando para arreglarlo.
Uso: py comprobar.py
Sale con 1 si falta algo imprescindible. La clave de ScrapeCreators solo avisa (es el plan B de descarga).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comun  # noqa: E402

FILTROS = ["select", "metadata", "showspectrumpic", "ebur128", "silencedetect", "astats", "volumedetect",
           "pan", "lowpass"]


def main():
    falta = []

    if sys.version_info < (3, 10):
        falta.append(f"Python {sys.version.split()[0]} es viejo: hace falta 3.10 o más.")
    try:
        import PIL  # noqa: F401
        import numpy  # noqa: F401
    except ImportError as e:
        falta.append(f"Falta la librería {e.name} en el entorno de Python: vuelve a ejecutar el instalador.")

    for prog, paquete in (("ffmpeg", "ffmpeg"), ("ffprobe", "ffmpeg"), ("yt-dlp", "yt-dlp"),
                          ("whisper-cli", "whisper")):
        if not comun.herramienta(prog):
            falta.append(f"FALTA {prog}\n{comun.pista_instalar(paquete)}")

    if comun.herramienta("ffmpeg"):
        filtros = comun.correr(["ffmpeg", "-hide_banner", "-filters"], check=False).stdout
        for f in FILTROS:
            if f" {f} " not in filtros:
                falta.append(f"A este ffmpeg le falta el filtro '{f}'.\n{comun.pista_instalar('ffmpeg')}")
        ayuda = comun.correr(["ffmpeg", "-hide_banner", "-h", "full"], check=False).stdout
        if "-fps_mode" not in ayuda:
            falta.append("Este ffmpeg es demasiado viejo (falta -fps_mode, llegó en la 5.1). Actualízalo.")

    if not comun.MODELO_WHISPER.is_file():
        falta.append(f"Falta el modelo de Whisper {comun.MODELO_WHISPER}: vuelve a ejecutar el instalador.")
    if not comun.FUENTE_MOSAICOS.is_file():
        falta.append(f"Falta la fuente {comun.FUENTE_MOSAICOS}: el plugin está incompleto, reinstálalo.")

    for f in falta:
        print(f, file=sys.stderr)
    if not comun.clave():
        print("AVISO: " + comun.aviso_clave(), file=sys.stderr)

    if falta:
        return 1
    print(f"Todo listo ({comun.SO}): Python {sys.version.split()[0]}, Pillow y numpy, ffmpeg con sus filtros, "
          f"yt-dlp, whisper-cli y el modelo ggml-small.bin. Tus estilos se guardan en {comun.mis_estilos()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
