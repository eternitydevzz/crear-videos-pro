"""Quita las pausas largas de un vídeo a cámara, con silencedetect + select/aselect (un solo paso de ffmpeg).

Uso: py cortar_silencios.py --video VIDEO --salida CARPETA/trabajo [--pausa 0.3] [--margen 0.05] [--umbral -35]
  --pausa   duración mínima (s) de un silencio para cortarlo
  --margen  aire (s) que se deja a cada lado del corte
  --umbral  nivel (dB) por debajo del cual se considera silencio
Deja en la carpeta de salida: cortado.mp4 (vídeo sin pausas), voz.wav (su audio, sin tocar el volumen)
y cortes.json (qué tramos del original se conservan y dónde caen en el nuevo).
"""
import argparse, json, os, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--video", required=True)
ap.add_argument("--salida", required=True)
ap.add_argument("--pausa", type=float, default=0.3)
ap.add_argument("--margen", type=float, default=0.05)
ap.add_argument("--umbral", type=float, default=-35.0)
a = ap.parse_args()

if not os.path.isfile(a.video):
    sys.exit(f"No existe el vídeo: {a.video}")
os.makedirs(a.salida, exist_ok=True)

def duracion(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True)
    return float(r.stdout.strip())

tiene_audio = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "csv=p=0", a.video],
                             capture_output=True, text=True).stdout.strip()
if not tiene_audio:
    sys.exit("El vídeo no tiene audio: no hay silencios que cortar.")

total = duracion(a.video)
det = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.video, "-vn", "-af", f"silencedetect=n={a.umbral}dB:d={a.pausa}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
inicios = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", det)]
finales = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", det)]
if len(finales) < len(inicios):
    finales.append(total)  # el vídeo termina en silencio

# Tramos que se quitan: el silencio menos el margen a cada lado.
quitar = []
for s, e in zip(inicios, finales):
    s2, e2 = max(0.0, s) + a.margen, min(total, e) - a.margen
    if s <= 0: s2 = 0.0            # silencio al principio: se quita entero
    if e >= total - 1e-3: e2 = total  # silencio al final: se quita entero
    if e2 - s2 > 0.01:
        quitar.append((s2, e2))

conservar, t = [], 0.0
for s, e in quitar:
    if s > t: conservar.append((t, s))
    t = e
if t < total: conservar.append((t, total))
if not conservar:
    sys.exit("Todo el vídeo es silencio con ese umbral: prueba con --umbral -45.")

expr = "+".join(f"between(t,{s:.3f},{e:.3f})" for s, e in conservar)
salida = os.path.join(a.salida, "cortado.mp4")
voz = os.path.join(a.salida, "voz.wav")
grafo = f"[0:v]select='{expr}',setpts=N/FRAME_RATE/TB[v];[0:a]aselect='{expr}',asetpts=N/SR/TB[a]"
r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.video, "-filter_complex", grafo,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", os.path.join(a.salida, "_tmp.mov")])
if r.returncode != 0:
    sys.exit("ffmpeg falló al cortar (mira el mensaje de arriba).")
tmp = os.path.join(a.salida, "_tmp.mov")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", tmp, "-map", "0:v", "-c:v", "copy", "-map", "0:a", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", salida], check=True)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", tmp, "-vn", "-c:a", "copy", voz], check=True)
os.unlink(tmp)

nuevo, acum, tramos = duracion(salida), 0.0, []
for s, e in conservar:
    tramos.append({"original_inicio": round(s, 3), "original_fin": round(e, 3), "nuevo_inicio": round(acum, 3), "nuevo_fin": round(acum + e - s, 3)})
    acum += e - s
json.dump({"video_original": os.path.abspath(a.video), "duracion_original": round(total, 3), "duracion_nueva": round(nuevo, 3),
           "parametros": {"pausa": a.pausa, "margen": a.margen, "umbral_db": a.umbral}, "tramos": tramos},
          open(os.path.join(a.salida, "cortes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"Antes: {total:.2f} s · después: {nuevo:.2f} s · se quitaron {total - nuevo:.2f} s en {len(quitar)} pausas.")
print(f"Escrito: {salida}, {voz} y cortes.json")
