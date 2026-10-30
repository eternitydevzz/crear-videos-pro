"""Crea <estilo>/transcripcion.md con lo que se dice, transcrito con Whisper EN LOCAL (sin red ni créditos).
Uso: py transcribir.py --estilo CARPETA [--idioma auto|es|en|pt…]

El archivo tiene 3 secciones. Este script deja hecha la primera; Claude rellena las otras dos:
  1. Lo que se dice (Whisper local)              <- este script
  2. Subtítulos leídos de los fotogramas         <- Claude, leyendo los mosaicos
  3. Comparación de las dos                      <- Claude: así ninguna queda sin revisar
Si Whisper falla o el vídeo no tiene voz, el archivo lo dice: no se inventa texto.
"""
import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_comun"))
import comun  # noqa: E402


def transcribir(video, idioma):
    whisper = comun.herramienta("whisper-cli")
    if not whisper:
        return None, "no está whisper-cli"
    if not comun.MODELO_WHISPER.is_file():
        return None, f"falta el modelo {comun.MODELO_WHISPER}"
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "voz16k.wav"
        # Whisper trabaja a 16 kHz mono
        r = comun.correr(["ffmpeg", "-loglevel", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav],
                         check=False)
        if r.returncode != 0:
            return None, "el vídeo no tiene audio que se pueda leer"
        base = Path(tmp) / "texto"
        r = comun.correr([whisper, "-m", comun.MODELO_WHISPER, "-l", idioma, "-np", "-otxt", "-of", base, "-f", wav],
                         check=False)
        txt = base.with_suffix(".txt")
        if r.returncode != 0 or not txt.is_file():
            return None, f"whisper-cli falló: {(r.stderr or '').strip()[-300:]}"
        texto = " ".join(l.strip() for l in txt.read_text(encoding="utf-8", errors="replace").splitlines()).strip()
        return texto, None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--estilo", required=True)
    p.add_argument("--idioma", default="auto")
    a = p.parse_args()
    estilo = Path(a.estilo)
    v = estilo / "video.mp4"
    if not v.is_file():
        comun.fallo(f"No existe {v}")

    texto, error = transcribir(v, a.idioma)
    partes = ["# Transcripción", "", "## 1. Lo que se dice (Whisper local, modelo ggml-small)", ""]
    if texto:
        partes += ["Transcripción automática, sin tiempos: puede tener errores.", "", texto]
    else:
        partes += [f"No disponible: {error or 'Whisper no devolvió texto (¿el vídeo no tiene voz?)'}."]
    partes += ["", "## 2. Subtítulos leídos de los fotogramas", "",
               "(Pendiente: Claude lo rellena leyendo los mosaicos. Es lo que se VE escrito, no necesariamente lo que "
               "se dice.)", "", "## 3. Comparación de las dos", "",
               "(Pendiente: Claude anota aquí las diferencias entre 1 y 2: palabras que se dicen y no se ven escritas, "
               "palabras escritas que no se dicen y posibles errores de la transcripción. Si falta una de las dos, "
               "lo dice.)"]
    salida = estilo / "transcripcion.md"
    salida.write_text("\n".join(partes) + "\n", encoding="utf-8")
    print(f"Escrito: {salida} ({'con texto de Whisper' if texto else 'SIN texto: ' + (error or 'sin voz')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
