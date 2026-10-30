"""Comprobación final: marcas C2PA/AI en las variaciones y caracteres invisibles en los textos.

Uso: python3 comprobar.py <carpeta_variaciones> [--limpiar]

- Videos (*_v?.mp4): recorre las cajas del MP4 sin entrar en los datos de imagen
  y audio (mdat), así no da falsos positivos. Marca cajas `jumb` (C2PA), cajas
  `uuid` con el identificador de C2PA y cualquier etiqueta con c2pa, jumbf,
  contentauth o los códigos IPTC de contenido generado por AI.
- Textos (ganchos.txt, descripciones.md): marca caracteres invisibles y espacios raros.
- Con --limpiar, reempaqueta los videos marcados sin metadatos (sin recodificar)
  y quita los caracteres invisibles de los textos; luego vuelve a comprobar.

Sale con 0 si todo queda limpio, 1 si queda algo.
"""
import subprocess
import sys
import unicodedata
from pathlib import Path

C2PA_UUID = bytes.fromhex("d8fec3d61b0e483c92975828877ec481")
PALABRAS = [b"c2pa", b"jumbf", b"contentauth", b"trainedalgorithmicmedia", b"made with ai"]
CONTENEDORES = {b"moov", b"trak", b"mdia", b"minf", b"stbl", b"udta", b"edts", b"dinf", b"ilst", b"meta"}
TEXTOS = ["ganchos.txt", "descripciones.md"]


def cajas(datos, inicio, fin, ruta=""):
    """Recorre cajas ISO BMFF y devuelve (ruta, tipo, contenido) sin abrir mdat."""
    pos = inicio
    while pos + 8 <= fin:
        tam = int.from_bytes(datos[pos:pos + 4], "big")
        tipo = datos[pos + 4:pos + 8]
        cab = 8
        if tam == 1:
            tam = int.from_bytes(datos[pos + 8:pos + 16], "big")
            cab = 16
        elif tam == 0:
            tam = fin - pos
        if tam < cab or pos + tam > fin:
            break
        nombre = f"{ruta}/{tipo.decode('latin-1')}"
        if tipo != b"mdat":
            cuerpo = datos[pos + cab:pos + tam]
            yield nombre, tipo, cuerpo
            if tipo in CONTENEDORES:
                salto = 4 if tipo == b"meta" else 0  # meta lleva versión y flags
                yield from cajas(datos, pos + cab + salto, pos + tam, nombre)
        pos += tam


def marcas_video(ruta):
    datos = ruta.read_bytes()
    hallazgos = []
    for nombre, tipo, cuerpo in cajas(datos, 0, len(datos)):
        if tipo == b"jumb":
            hallazgos.append(f"caja C2PA {nombre}")
        elif tipo == b"uuid" and cuerpo[:16] == C2PA_UUID:
            hallazgos.append(f"caja uuid de C2PA {nombre}")
        elif tipo not in CONTENEDORES:
            bajo = cuerpo.lower()
            hallazgos += [f"'{p.decode()}' en {nombre}" for p in PALABRAS if p in bajo]
    return hallazgos


def invisible(c):
    cat = unicodedata.category(c)
    return cat in ("Cf", "Co", "Cn") or (cat == "Zs" and c != " ")


def limpiar_video(ruta):
    tmp = ruta.with_suffix(".limpio.mp4")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(ruta), "-map", "0:v:0", "-map", "0:a:0?",
         "-map_metadata", "-1", "-c", "copy", "-movflags", "+faststart", str(tmp)],
        check=True,
    )
    tmp.replace(ruta)


def comprobar(carpeta, arreglar):
    pendientes = 0
    for video in sorted(carpeta.glob("*_v[0-9].mp4")):
        hallazgos = marcas_video(video)
        if hallazgos and arreglar:
            limpiar_video(video)
            print(f"LIMPIADO {video.name}: {', '.join(hallazgos)}")
            hallazgos = marcas_video(video)
        if hallazgos:
            pendientes += 1
            print(f"MARCAS   {video.name}: {', '.join(hallazgos)}")
        else:
            print(f"ok       {video.name}: sin C2PA ni etiquetas de AI")

    for nombre in TEXTOS:
        ruta = carpeta / nombre
        if not ruta.exists():
            continue
        texto = ruta.read_text(encoding="utf-8")
        raros = [c for c in texto if invisible(c)]
        if raros and arreglar:
            ruta.write_text("".join(" " if unicodedata.category(c) == "Zs" else "" if invisible(c) else c
                                    for c in texto), encoding="utf-8")
            print(f"LIMPIADO {nombre}: {len(raros)} caracteres invisibles")
            raros = [c for c in ruta.read_text(encoding="utf-8") if invisible(c)]
        if raros:
            pendientes += 1
            print(f"MARCAS   {nombre}: {len(raros)} caracteres invisibles")
        else:
            print(f"ok       {nombre}: sin caracteres invisibles")
    return pendientes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 comprobar.py <carpeta_variaciones> [--limpiar]")
    sys.exit(1 if comprobar(Path(sys.argv[1]), "--limpiar" in sys.argv[2:]) else 0)
