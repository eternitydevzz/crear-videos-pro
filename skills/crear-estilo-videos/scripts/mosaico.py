"""Mosaicos de fotogramas con el segundo REAL escrito encima, leyendo <estilo>/Frames/ (nombres con el segundo).

Uso: py mosaico.py --estilo CARPETA --todo [--rejilla 8x4] [--ancho 160]
       -> recorre todo el reel y deja mosaicos/m_00.jpg, m_01.jpg…
     py mosaico.py --estilo CARPETA --inicio S --salida ARCHIVO.jpg [--rejilla 8x4] [--ancho 160] [--recorte W:H:X:Y]
       -> un solo mosaico que empieza en el segundo S.
--recorte limita a una zona del fotograma original (píxeles), por ejemplo 720:250:0:100 = banda de subtítulos.

Elige los fotogramas por su número (no usa el filtro `fps`, que desplaza los tiempos). Dibuja con Pillow y la
fuente del repo, así sale igual en Mac y en Windows. El segundo se escribe con 2 decimales.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_comun"))
import comun  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

TAM_LETRA = 18
AMARILLO = (255, 255, 0)
CAJA = (0, 0, 0, 179)   # negro al 70 %


def etiqueta(img, texto, tam, margen):
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    f = comun.fuente(tam)
    x0, y0, x1, y1 = d.textbbox((margen, margen), texto, font=f)
    d.rectangle((x0 - 2, y0 - 2, x1 + 2, y1 + 2), fill=CAJA)
    d.text((margen, margen), texto, font=f, fill=AMARILLO)
    return Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB")


def un_mosaico(frames, inicio, rate, cols, filas, ancho, recorte, salida):
    trozo = frames[inicio:inicio + cols * filas]
    if not trozo:
        comun.fallo(f"No hay fotogramas desde el número {inicio}")
    celdas = []
    for i, f in enumerate(trozo):
        img = Image.open(f).convert("RGB")
        if recorte:
            w, h, x, y = recorte
            img = img.crop((x, y, x + w, y + h))
        alto = round(img.height * ancho / img.width)
        img = img.resize((ancho, alto), Image.LANCZOS)
        segundo = int((inicio + i) * 100 / rate) / 100   # truncado a centésimas, como antes
        celdas.append(etiqueta(img, f"{segundo:.2f}", TAM_LETRA, 4))
    alto = celdas[0].height
    lienzo = Image.new("RGB", (cols * ancho, filas * alto), (0, 0, 0))
    for i, c in enumerate(celdas):
        lienzo.paste(c, ((i % cols) * ancho, (i // cols) * alto))
    lienzo.save(salida, quality=90)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--estilo", required=True)
    p.add_argument("--todo", action="store_true")
    p.add_argument("--inicio", type=float, default=0.0)
    p.add_argument("--salida")
    p.add_argument("--rejilla", default="8x4")
    p.add_argument("--ancho", type=int, default=160)
    p.add_argument("--recorte", help="W:H:X:Y en píxeles del fotograma original")
    a = p.parse_args()
    estilo = Path(a.estilo)
    info = comun.leer_info(estilo)
    rate = float(info["fotogramas_por_segundo_en_Frames"])
    frames = sorted((estilo / "Frames").glob("*.jpg"))
    cols, filas = (int(x) for x in a.rejilla.lower().split("x"))
    recorte = tuple(int(x) for x in a.recorte.split(":")) if a.recorte else None
    por = cols * filas

    if a.todo:
        carpeta = estilo / "mosaicos"
        carpeta.mkdir(exist_ok=True)
        for k, s in enumerate(range(0, len(frames), por)):
            out = carpeta / f"m_{k:02d}.jpg"
            un_mosaico(frames, s, rate, cols, filas, a.ancho, recorte, out)
            print(f"{out}  (desde {s / rate:.2f} s)")
    else:
        if not a.salida:
            comun.fallo("Falta --salida (o usa --todo)")
        s = int(a.inicio * rate + 0.5)
        un_mosaico(frames, s, rate, cols, filas, a.ancho, recorte, a.salida)
        print(a.salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
