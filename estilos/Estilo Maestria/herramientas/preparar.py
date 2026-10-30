"""Prepara un vídeo del estilo de formación: corta silencios, transcribe con Whisper (DTW) y deja los assets del proyecto.
Uso: bash ~/.config/crear-videos/py preparar.py <vídeo origen> <carpeta destino>
Deja: trabajo/ (cortado.mp4, tramos.json, cortado16k.wav, cortado_dtw.json, whisper.log)
      proyecto/assets/ (aroll-original.mp4, aroll.mp4 con el brillo de color.fc.txt, voz.m4a)
Antes era preparar.sh (zsh, solo Mac). Mismo resultado en Mac y en Windows.
"""
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2] / "skills" / "_comun"))
import comun  # noqa: E402


def main():
    if len(sys.argv) != 3:
        comun.fallo("Uso: py preparar.py <vídeo origen> <carpeta destino>")
    src, base = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    trabajo, assets = base / "trabajo", base / "proyecto" / "assets"
    trabajo.mkdir(parents=True, exist_ok=True)
    assets.mkdir(parents=True, exist_ok=True)

    r = subprocess.run([sys.executable, str(AQUI / "cortar.py"), str(src), str(trabajo / "cortado.mp4")])
    if r.returncode:
        comun.fallo("cortar.py falló (mira el mensaje de arriba)")

    whisper = comun.herramienta("whisper-cli")
    if not whisper:
        comun.fallo("No encuentro whisper-cli: ejecuta comprobar.py")
    comun.correr(["ffmpeg", "-v", "error", "-y", "-i", trabajo / "cortado.mp4", "-vn", "-ac", "1", "-ar", "16000",
                  trabajo / "cortado16k.wav"])
    with open(trabajo / "whisper.log", "w", encoding="utf-8") as log:
        r = subprocess.run([whisper, "-m", str(comun.MODELO_WHISPER), "-l", "es", "-ojf", "-dtw", "small", "-nfa",
                            "-f", "cortado16k.wav", "-of", "cortado_dtw"], cwd=trabajo, stdout=log, stderr=log)
    if r.returncode:
        comun.fallo(f"whisper-cli falló: mira {trabajo / 'whisper.log'}")

    shutil.copy(trabajo / "cortado.mp4", assets / "aroll-original.mp4")
    # color.fc.txt se lee desde su carpeta y con nombre relativo: así la ruta no lleva «C:» en Windows
    comun.correr(["ffmpeg", "-v", "error", "-y", "-i", assets / "aroll-original.mp4", "-/filter_complex", "color.fc.txt",
                  "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium", assets / "aroll.mp4"],
                 cwd=AQUI)
    comun.correr(["ffmpeg", "-v", "error", "-y", "-i", trabajo / "cortado.mp4", "-vn", "-c:a", "copy",
                  assets / "voz.m4a"])
    print(f"LISTO {base} {comun.ffprobe(assets / 'aroll.mp4', 'format=duration')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
