"""Saca de <estilo>/video.mp4: info.txt, Frames/ (unos 15 por segundo, con su segundo exacto en el nombre) y cortes.txt.
Uso: py extraer.py --estilo CARPETA

- Lee los fps REALES del vídeo (no supone 30). Coge 1 de cada K fotogramas, K = fps/15 redondeado
  (30 fps -> 2, 60 fps -> 4, 25 fps -> 2). Cada fotograma se etiqueta con su tiempo real n/fps.
- NO usa el filtro `fps` de ffmpeg: al reducir fps coge el fotograma del medio y desplaza los tiempos.
- Cortes: filtro `scene` a 0,08 con puntuación; 0,25 pierde disolvencias y cortes entre fondos claros.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_comun"))
import comun  # noqa: E402

UMBRAL_ESCENA = 0.08      # por debajo de 0,08 entran movimientos normales; por encima de 0,25 se pierden disolvencias
CORTE_DURO = 0.5          # un solo fotograma con puntuación >= 0,5 es un cambio de plano claro
FPS_VARIABLE_TOL = 0.01   # si el fps medio se aparta más de un 1 % del nominal, los segundos n/fps no son exactos


def cortes(video, fps):
    r = comun.correr(["ffmpeg", "-v", "info", "-i", video, "-vf",
                      f"select='gt(scene,{UMBRAL_ESCENA})',metadata=print:key=lavfi.scene_score",
                      "-an", "-f", "null", "-"], check=False)
    tiempos = re.findall(r"pts_time:([0-9.]+)", r.stderr)
    puntos = re.findall(r"scene_score=([0-9.]+)", r.stderr)
    hueco = 1.5 / fps          # dos detecciones separadas por <= 1,5 fotogramas son el mismo cambio
    grupos = []
    for t, s in zip(map(float, tiempos), map(float, puntos)):
        if grupos and t - grupos[-1]["ultimo"] <= hueco:
            g = grupos[-1]
            g["n"] += 1
            g["max"] = max(g["max"], s)
            g["ultimo"] = t
        else:
            grupos.append({"ini": t, "ultimo": t, "n": 1, "max": s})
    filas = ["segundo\tfotogramas\tpuntuacion\ttipo"]
    for g in grupos:
        if g["n"] >= 2:
            tipo = f"disolvencia ({g['n']} fotogramas)"
        elif g["max"] >= CORTE_DURO:
            tipo = "corte duro"
        else:
            tipo = "dudoso: mirar a 30 fps"
        filas.append(f"{g['ini']:.3f}\t{g['n']}\t{g['max']:.2f}\t{tipo}")
    return "\n".join(filas) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--estilo", required=True)
    a = p.parse_args()
    estilo = Path(a.estilo)
    v = estilo / "video.mp4"
    if not v.is_file() or v.stat().st_size == 0:
        comun.fallo(f"No existe {v}: ejecuta primero descargar.py")

    fps = comun.fraccion(comun.ffprobe(v, "stream=r_frame_rate", "v:0"))
    k = max(1, int(fps / 15 + 0.5))
    rate = fps / k
    dur = comun.ffprobe(v, "format=duration")
    wh = comun.ffprobe(v, "stream=width,height", "v:0")
    tiene_audio = bool(comun.ffprobe(v, "stream=codec_type", "a").splitlines())
    avg = comun.fraccion(comun.ffprobe(v, "stream=avg_frame_rate", "v:0"))
    variable = avg > 0 and abs(avg - fps) / fps > FPS_VARIABLE_TOL

    frames = estilo / "Frames"
    frames.mkdir(exist_ok=True)
    for f in frames.glob("*.jpg"):   # solo esta carpeta: lo de una ejecución anterior no se mezcla
        f.unlink()
    comun.correr(["ffmpeg", "-loglevel", "error", "-y", "-i", v, "-vf", f"select='not(mod(n,{k}))'",
                  "-fps_mode", "passthrough", "-q:v", "3", "-start_number", "0", frames / "_t_%05d.jpg"])
    temporales = sorted(frames.glob("_t_*.jpg"))
    for i, f in enumerate(temporales):
        f.rename(frames / f"{i * k / fps:07.3f}s_{i + 1:05d}.jpg")
    n = len(temporales)

    (estilo / "info.txt").write_text("\n".join([
        f"duracion_s={dur}", f"resolucion={wh}", f"fps={fps:.4f}", f"cada_k_fotogramas={k}",
        f"fotogramas_por_segundo_en_Frames={rate:.4f}", f"fotogramas_en_Frames={n}",
        f"tiene_audio={'si' if tiene_audio else 'no'}", f"fps_medio={avg:.4f}",
        f"fps_variable={'si' if variable else 'no'}"]) + "\n", encoding="utf-8")
    if variable:
        print(f"AVISO: este vídeo parece de fps VARIABLE (nominal {fps:.4f}, medio {avg:.4f}). Los segundos de los "
              "fotogramas pueden desviarse; dilo en la ficha como [SUPOSICIÓN].", file=sys.stderr)

    tabla = cortes(v, fps)
    (estilo / "cortes.txt").write_text(tabla, encoding="utf-8")
    print(f"Vídeo: {dur}s, {wh}, {fps:.4f} fps. Frames: {n} imágenes (1 de cada {k}, ~{rate:.4f}/s) en {frames}")
    print("Cortes (cortes.txt):")
    print(tabla, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
