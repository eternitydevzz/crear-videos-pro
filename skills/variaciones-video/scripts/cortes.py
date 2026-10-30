"""Elige 5 puntos de inicio, uno por variación, en pausas de la voz.

Uso: python3 cortes.py <palabras.json>  -> imprime 5 segundos, uno por línea.
v1 empieza en 0; v2-v5 empiezan cerca de 1.0, 1.7, 2.4 y 3.1 s, siempre al
principio de una palabra, prefiriendo inicios de frase y palabras tras una pausa.
Sin transcripción usa cortes fijos.
"""
import json
import sys

OBJETIVOS = [1.0, 1.7, 2.4, 3.1]
FIJOS = [0.0, 1.0, 1.7, 2.4, 3.1]
PAUSA_MIN = 0.12
SEPARACION_MIN = 0.4
MARGEN = 0.08


def cargar_palabras(ruta):
    try:
        with open(ruta) as f:
            datos = json.load(f)
    except (OSError, ValueError):
        return []
    return [w for w in datos.get("words", []) if w.get("type") == "word"]


def candidatos(palabras):
    """(inicio_de_corte, bonus) para cada palabra de los primeros 5 s.

    El bonus premia empezar tras un signo de puntuación (inicio de frase) y,
    en menor medida, tras una pausa de la voz.
    """
    salida = []
    for i, w in enumerate(palabras[1:], start=1):
        if w["start"] > 5.0:
            break
        previa = palabras[i - 1]
        pausa = w["start"] - previa["end"]
        bonus = (1.0 if previa["text"].rstrip()[-1:] in ".,;:?!" else 0) + (0.5 if pausa >= PAUSA_MIN else 0)
        salida.append((max(0.0, w["start"] - min(MARGEN, max(pausa, 0) / 2)), bonus))
    return salida


def elegir(palabras):
    cands = candidatos(palabras)
    if len(cands) < 4:
        return FIJOS
    elegidos = [0.0]
    for objetivo in OBJETIVOS:
        libres = [c for c in cands if all(abs(c[0] - e) >= SEPARACION_MIN for e in elegidos)]
        if not libres:
            return FIJOS
        # Cerca del objetivo; un inicio de frase o una pausa cuentan como si estuvieran más cerca
        mejor = min(libres, key=lambda c: abs(c[0] - objetivo) - c[1])
        elegidos.append(mejor[0])
    return elegidos


if __name__ == "__main__":
    for s in elegir(cargar_palabras(sys.argv[1])):
        print(f"{s:.2f}")
