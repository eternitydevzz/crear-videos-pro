"""Tira de fotogramas a los fps ORIGINALES del vídeo (30 si es de 30) en una ventana corta, con el segundo escrito.
Sirve para los puntos dudosos de cortes.txt, zooms y animaciones de 1-2 fotogramas.

Uso: py ventana.py --estilo CARPETA --inicio S [--duracion 0.4] [--ancho 130]
Deja ventanas/v_<S>.png. Máximo 12 fotogramas por tira (a 30 fps: 0,4 s); si pides más, enseña los 12 primeros.
"""
import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_comun"))
import comun  # noqa: E402
from PIL import Image  # noqa: E402
from mosaico import etiqueta  # noqa: E402

MAX_FOTOGRAMAS = 12   # más de 12 a 130 px ya no caben legibles en una tira
TAM_LETRA = 14


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--estilo", required=True)
    p.add_argument("--inicio", required=True)
    p.add_argument("--duracion", type=float, default=0.4)
    p.add_argument("--ancho", type=int, default=130)
    a = p.parse_args()
    estilo = Path(a.estilo)
    v = estilo / "video.mp4"
    if not v.is_file():
        comun.fallo(f"No existe {v}")
    fps = float(comun.leer_info(estilo)["fps"])
    n = min(MAX_FOTOGRAMAS, max(1, int(a.duracion * fps + 0.5)))
    inicio = float(a.inicio)

    with tempfile.TemporaryDirectory() as tmp:
        comun.correr(["ffmpeg", "-loglevel", "error", "-y", "-ss", a.inicio, "-t", a.duracion, "-i", v,
                      "-vf", f"scale={a.ancho}:-2", "-fps_mode", "passthrough", "-frames:v", n,
                      Path(tmp) / "f_%03d.png"])
        imgs = sorted(Path(tmp).glob("f_*.png"))
        if not imgs:
            comun.fallo(f"No salió ningún fotograma desde {a.inicio} s")
        celdas = [etiqueta(Image.open(f), f"{inicio + i / fps:.3f}", TAM_LETRA, 3) for i, f in enumerate(imgs)]
    w, h = celdas[0].size
    tira = Image.new("RGB", (w * len(celdas), h))
    for i, c in enumerate(celdas):
        tira.paste(c, (i * w, 0))
    carpeta = estilo / "ventanas"
    carpeta.mkdir(exist_ok=True)
    salida = carpeta / f"v_{a.inicio}.png"
    tira.save(salida)
    print(f"{salida}  ({len(celdas)} fotogramas a {fps:g} fps, desde {a.inicio} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
