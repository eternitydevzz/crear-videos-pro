"""5 variaciones de un vídeo, cada una con su gancho, encuadre, velocidad, color e inicio, y sin metadatos.

Uso:
  py variar.py analizar  <video>   -> transcripción (Whisper local) + hoja de fotogramas en <nombre>_variaciones/
  py variar.py generar   <video>   -> 5 variaciones con el gancho de cada línea de ganchos.txt (y comprueba)
  py variar.py comprobar <video>   -> solo la comprobación final
"""
import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "_comun"))
import comun  # noqa: E402

SEGUNDOS_GANCHO = 3.5
LETRAS_POR_RENGLON = 22
# Arial Bold existe igual en Mac y en Windows; si no está, la del repo.
FUENTES = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "C:/Windows/Fonts/arialbd.ttf",
           str(comun.RAIZ / "stock" / "fuentes" / "comunes" / "Inter-600.ttf")]
# nombre  zoom  ancla_x  ancla_y  velocidad  brillo  contraste  saturación  volumen
VARIANTES = [
    ("v1", 1.03, 0.50, 0.50, 1.00, 0.02, 1.00, 1.04, 1.00),
    ("v2", 1.08, 0.00, 0.30, 1.03, 0.00, 1.03, 1.06, 1.03),
    ("v3", 1.10, 1.00, 0.50, 0.98, -0.01, 1.04, 1.00, 0.98),
    ("v4", 1.06, 0.50, 0.00, 1.02, 0.01, 1.00, 0.96, 1.02),
    ("v5", 1.09, 0.30, 1.00, 0.97, -0.02, 1.02, 1.03, 0.97),
]


def carpeta(video):
    out = video.parent / f"{video.stem}_variaciones"
    out.mkdir(exist_ok=True)
    return out


def tiene_audio(video):
    return bool(comun.ffprobe(video, "stream=index", "a"))


def analizar(video, out):
    dur = float(comun.ffprobe(video, "format=duration"))
    fps = 12 / max(dur, 1)   # 12 cuadros repartidos por todo el vídeo
    comun.correr(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", f"fps={fps},scale=320:-2,tile=4x3",
                  "-frames:v", "1", out / "fotogramas.jpg"])
    if not tiene_audio(video):
        (out / "transcripcion.txt").write_text("(el video no tiene audio)\n", encoding="utf-8")
    else:
        try:
            palabras, idioma = comun.palabras_whisper(video)
        except RuntimeError as e:
            (out / "transcripcion.txt").write_text(f"Sin transcripción: {e}\n", encoding="utf-8")
        else:
            texto = " ".join(p["texto"] for p in palabras)
            (out / "transcripcion.txt").write_text(texto + "\n", encoding="utf-8")
            # Mismo formato que usaba Scribe, para que cortes.py no cambie
            words = [{"type": "word", "text": p["texto"], "start": p["inicio"], "end": p["fin"]} for p in palabras]
            (out / "palabras.json").write_text(json.dumps({"language": idioma, "words": words}, ensure_ascii=False,
                                                          indent=1), encoding="utf-8")
    print("ok transcripcion.txt y fotogramas.jpg")
    print(f"CARPETA={out}")


def fuente():
    for f in FUENTES:
        if Path(f).is_file():
            return Path(f)
    comun.fallo("No encontré ninguna fuente para el gancho.")


def generar(video, out):
    ganchos = out / "ganchos.txt"
    if not ganchos.is_file():
        comun.fallo(f"Falta {ganchos} (5 líneas, una por variación)")
    lineas = ganchos.read_text(encoding="utf-8").splitlines()
    w, h = (int(x) // 2 * 2 for x in comun.ffprobe(video, "stream=width,height", "v:0").split(","))
    tam, interlineado, margen = h * 36 // 1000, h * 8 // 1000, h * 14 // 1000
    inicios = comun.correr([sys.executable, AQUI / "cortes.py", out / "palabras.json"]).stdout.split()
    audio = tiene_audio(video)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # ffmpeg corre DENTRO de tmp y la fuente y los textos se nombran sin ruta: así no hay que escapar «C:» en Windows
        shutil.copy(fuente(), tmp / "fuente.ttf")
        procesos = []
        for i, (n, z, ax, ay, s, b, c, sat, vol) in enumerate(VARIANTES):
            t = inicios[i]
            print(f"{n}: empieza en {t}s, zoom {z}, ancla {ax},{ay}")
            gancho = lineas[i].strip() if i < len(lineas) else ""
            (tmp / f"g{i + 1}.txt").write_text("\n".join(textwrap.wrap(gancho, LETRAS_POR_RENGLON)), encoding="utf-8")
            vf = (f"scale=trunc(iw*{z}/2)*2:trunc(ih*{z}/2)*2,crop={w}:{h}:(in_w-{w})*{ax}:(in_h-{h})*{ay},"
                  f"setpts=PTS/{s},eq=brightness={b}:contrast={c}:saturation={sat},noise=alls=2:allf=t")
            if gancho:
                vf += (f",drawtext=fontfile=fuente.ttf:textfile=g{i + 1}.txt:fontsize={tam}:fontcolor=black:"
                       f"line_spacing={interlineado}:text_align=center:box=1:boxcolor=white:boxborderw={margen}:"
                       f"x=(w-text_w)/2:y=h*0.13:enable='lt(t,{SEGUNDOS_GANCHO})'")
            vf += ",format=yuv420p"
            aud = ["-af", f"atempo={s},volume={vol}", "-c:a", "aac", "-b:a", "160k", "-ar", "48000"] if audio else ["-an"]
            args = ["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", video.resolve(), "-map_metadata", "-1",
                    "-map", "0:v:0", "-map", "0:a:0?", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "20", "-profile:v", "high", "-r", "30", *aud, "-movflags", "+faststart",
                    (out / f"{video.stem}_{n}.mp4").resolve()]
            procesos.append(subprocess.Popen([str(x) for x in args], cwd=tmp))
        fallos = sum(1 for p in procesos if p.wait() != 0)
    if fallos:
        comun.fallo(f"Fallaron {fallos} variaciones")
    for f in sorted(out.glob("*_v?.mp4")):
        print(f)
    print(f"CARPETA={out}")


def comprobar(out):
    return comun.correr([sys.executable, AQUI / "comprobar.py", out, "--limpiar"], capture_output=False,
                        check=False).returncode


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("analizar", "generar", "comprobar"):
        comun.fallo("Uso: py variar.py analizar|generar|comprobar <video>")
    video = Path(sys.argv[2])
    if not video.is_file():
        comun.fallo(f"No existe: {video}")
    out = carpeta(video)
    if sys.argv[1] == "analizar":
        analizar(video, out)
        return 0
    if sys.argv[1] == "generar":
        generar(video, out)
    return comprobar(out)


if __name__ == "__main__":
    sys.exit(main())
