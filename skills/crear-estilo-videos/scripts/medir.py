"""Mide texto y encuadre en fotogramas. Solo librería estándar de Python + ffmpeg/ffprobe.

  medir.py texto FOTOGRAMA [FOTOGRAMA ...] [--y 90:330] [--color blanco|oscuro|azul | --rgb R,G,B [--tol 60]]
      Busca líneas de texto del color indicado dentro de la franja vertical --y y da, por línea:
      y0-y1, alto, x0-x1, ancho, centro x y color medio. Detecta las líneas por perfil de filas,
      sin bandas fijas (una banda mal puesta recorta el texto). Precisión: ±2 px.
      Para cualquier otro color (el acento de otra marca) usa --rgb con el color aproximado y --tol
      (diferencia máxima por canal, 60 por defecto). Pon siempre --y: sin franja, una camiseta o
      una pared blanca cuentan como texto.

  medir.py encuadre FOTOGRAMA [FOTOGRAMA ...]
      Caja de piel (percentil 5-95 %) en la parte media del cuadro: sirve para comparar el
      acercamiento de la cara entre tomas, NO es detección de caras. Aproximado. Los umbrales de
      color de piel se ajustaron con una sola persona y una sola luz: con otra piel u otra luz puede
      no encontrar nada o medir otra cosa. Si pasa, compara a ojo la posición de la cabeza en dos
      fotogramas y dilo en la ficha como [SUPOSICIÓN].

Cuidado: un fotograma con el subtítulo a medio animar (desenfocado o creciendo) da tamaños falsos;
mide en fotogramas donde el texto ya esté quieto y nítido.
"""
import argparse
import subprocess
import sys

COLORES = {
    "blanco": lambda r, g, b: r > 228 and g > 228 and b > 228,
    "oscuro": lambda r, g, b: r < 70 and g < 70 and b < 80,
    "azul": lambda r, g, b: b > 170 and r < 70 and g < 140,
}
PIEL = lambda r, g, b: r > 150 and 90 < g < 190 and 70 < b < 170 and r > g + 15 and g > b


def dimensiones(ruta):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "csv=p=0", ruta],
                         capture_output=True, text=True, check=True).stdout.strip()
    w, h = out.split(",")
    return int(w), int(h)


def pixeles(ruta):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", ruta, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, check=True)
    return r.stdout


def lineas_de_texto(ruta, ya, yb, pred):
    w, h = dimensiones(ruta)
    d = pixeles(ruta)
    yb = min(yb, h)
    filas = []
    for y in range(ya, yb):
        base = y * w * 3
        xs = [x for x in range(0, w, 1) if pred(d[base + x * 3], d[base + x * 3 + 1], d[base + x * 3 + 2])]
        filas.append((y, xs))
    lineas, actual = [], None
    for y, xs in filas:
        if len(xs) >= 6:
            if actual is None:
                actual = {"y0": y, "y1": y, "xs": []}
            actual["y1"] = y
            actual["xs"] += [xs[0], xs[-1]]
        elif actual is not None:
            lineas.append(actual)
            actual = None
    if actual is not None:
        lineas.append(actual)
    salida = []
    for l in lineas:
        if l["y1"] - l["y0"] < 8:   # menos de 9 px de alto: ruido
            continue
        sr = sg = sb = n = 0
        for y in range(l["y0"], l["y1"] + 1):
            base = y * w * 3
            for x in range(min(l["xs"]), max(l["xs"]) + 1, 2):
                r_, g_, b_ = d[base + x * 3], d[base + x * 3 + 1], d[base + x * 3 + 2]
                if pred(r_, g_, b_):
                    sr, sg, sb, n = sr + r_, sg + g_, sb + b_, n + 1
        x0, x1 = min(l["xs"]), max(l["xs"])
        color = "#%02X%02X%02X" % (sr // n, sg // n, sb // n) if n else "?"
        salida.append({"y0": l["y0"], "y1": l["y1"], "alto": l["y1"] - l["y0"] + 1, "x0": x0, "x1": x1,
                       "ancho": x1 - x0 + 1, "centro_x": (x0 + x1) // 2, "color_medio": color, "frame_w": w, "frame_h": h})
    return salida


def encuadre(ruta):
    w, h = dimensiones(ruta)
    d = pixeles(ruta)
    xs, ys = [], []
    for y in range(int(h * 0.23), int(h * 0.70), 2):
        base = y * w * 3
        for x in range(0, w, 2):
            if PIEL(d[base + x * 3], d[base + x * 3 + 1], d[base + x * 3 + 2]):
                xs.append(x)
                ys.append(y)
    if len(xs) < 50:
        return None
    xs.sort()
    ys.sort()
    k = len(xs)
    a, b = xs[int(k * 0.05)], xs[int(k * 0.95)]
    c, e = ys[int(k * 0.05)], ys[int(k * 0.95)]
    return {"x": f"{a}-{b}", "ancho": b - a, "y": f"{c}-{e}", "pixeles_de_piel": k, "frame": f"{w}x{h}"}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="orden", required=True)
    t = sub.add_parser("texto")
    t.add_argument("frames", nargs="+")
    t.add_argument("--y", default="0:9999", help="franja vertical ya:yb en píxeles")
    t.add_argument("--color", choices=sorted(COLORES), default="blanco")
    t.add_argument("--rgb", help="color propio R,G,B (sustituye a --color)")
    t.add_argument("--tol", type=int, default=60, help="tolerancia por canal con --rgb")
    e = sub.add_parser("encuadre")
    e.add_argument("frames", nargs="+")
    a = p.parse_args()

    for f in a.frames:
        print(f"== {f}")
        if a.orden == "texto":
            ya, yb = (int(v) for v in a.y.split(":"))
            if a.rgb:
                cr, cg, cb = (int(v) for v in a.rgb.split(","))
                pred = lambda r, g, b: abs(r - cr) <= a.tol and abs(g - cg) <= a.tol and abs(b - cb) <= a.tol
            else:
                pred = COLORES[a.color]
            res = lineas_de_texto(f, ya, yb, pred)
            if not res:
                print("   (no se encontró texto de ese color en esa franja)")
            for l in res:
                print(f"   y {l['y0']}-{l['y1']} (alto {l['alto']}) | x {l['x0']}-{l['x1']} (ancho {l['ancho']}, centro {l['centro_x']} de {l['frame_w']}) | color medio {l['color_medio']}")
        else:
            r = encuadre(f)
            print("   " + (f"caja de piel x {r['x']} (ancho {r['ancho']}), y {r['y']}, {r['pixeles_de_piel']} px, cuadro {r['frame']}" if r
                           else "no se encontró piel suficiente"))


if __name__ == "__main__":
    sys.exit(main())
