"""Acorta las pausas de la voz a ~0,12 s.
Corta SIEMPRE desde las copias *-sinrecortar: aroll, voz, recortes (webm con alfa) y palabras.json. Guarda los tramos quitados en
../trabajo/pausas.json para que build.py recoloque los tiempos escritos a mano (tmap)."""
import json, math, struct, subprocess
from pathlib import Path

A = Path(__file__).parent / "assets"
TR = Path(__file__).parent / "../trabajo"
FPS, KEEP, MIN_P, TH = 30, 0.06, 0.25, -33.0  # se dejan 0,06 s a cada lado de la pausa


def run(*a):
    subprocess.run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-threads", "4", *a], check=True)


raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(A / "voz-sinrecortar.m4a"), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
n = 800  # 50 ms
lv = [20 * math.log10(math.sqrt(sum(x * x for x in struct.unpack(f"<{n}h", raw[2 * i:2 * (i + n)])) / n) / 32768 + 1e-9) for i in range(0, len(raw) // 2 - n + 1, n)]
dur = len(raw) / 2 / 16000
runs, st = [], None
for k, v in enumerate(lv + [0]):
    if v < TH:
        st = k if st is None else st
    else:
        if st is not None and (k - st) * .05 >= MIN_P:
            runs.append((st * .05, k * .05))
        st = None
runs = [(a, b) for a, b in runs if a > .1 and b < dur - .1]  # ni la pausa inicial (la tapa el recorte de 0,433 s) ni la final
cut = []
for a, b in runs:
    x, y = math.ceil((a + KEEP) * FPS) / FPS, math.floor((b - KEEP) * FPS) / FPS
    if y - x >= 2 / FPS:
        cut.append((round(x, 4), round(y, 4)))
END = round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(A / "voz-sinrecortar.m4a")],
                               capture_output=True, text=True).stdout), 3)
keep, cur = [], 0.0
for x, y in cut:
    keep.append((cur, x))
    cur = y
keep.append((cur, END))
(TR / "pausas.json").write_text(json.dumps({"quitado": cut, "tramos": keep}, indent=1))
print(len(cut), "pausas acortadas, se quitan", round(sum(y - x for x, y in cut), 3), "s; nueva duración", round(sum(b - a for a, b in keep), 3))


def tmap(t):
    return t - sum(min(y, max(t, x)) - x for x, y in cut)


def fc(keep, v=True, a=True):
    p, lab = [], []
    for i, (s, e) in enumerate(keep):
        if v:
            p.append(f"[0:v]trim=start_frame={round(s * FPS)}:end_frame={round(e * FPS)},setpts=PTS-STARTPTS[v{i}];")  # por fotograma: con segundos redondeados se perdían fotogramas
        if a:
            p.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={max(e - s - .008, 0):.4f}:d=0.008[a{i}];")
        lab.append((f"[v{i}]" if v else "") + (f"[a{i}]" if a else ""))
    return "".join(p) + "".join(lab) + f"concat=n={len(keep)}:v={int(v)}:a={int(a)}" + ("[v]" if v else "") + ("[a]" if a else "")


run("-i", str(A / "aroll-sinrecortar.mp4"), "-filter_complex", fc(keep, a=False), "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
    "-pix_fmt", "yuv420p", "-g", "30", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", str(A / "aroll.mp4"))
run("-i", str(A / "voz-sinrecortar.m4a"), "-filter_complex", fc(keep, v=False), "-map", "[a]", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(A / "voz.m4a"))
# recortes de «palabra detrás» (si los hay): cada webm empieza en «t0» del aroll sin recortar y dura «d» (build.py · BEHIND)
RECORTES = []  # p. ej. [("donde", 21.3, 1.9)]
for name, t0, d in RECORTES:
    k2 = [(max(s, t0) - t0, min(e, t0 + d) - t0) for s, e in keep if min(e, t0 + d) > max(s, t0)]
    run("-c:v", "libvpx-vp9", "-i", str(A / f"recorte/{name}-sinrecortar.webm"), "-filter_complex", fc(k2, a=False), "-map", "[v]",
        "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "24", "-row-mt", "1", "-auto-alt-ref", "0", str(A / f"recorte/{name}.webm"))
W = json.loads((TR / "palabras-sinrecortar.json").read_text(encoding="utf-8"))
for w in W:
    w["s"] = round(tmap(w["s"]), 3)
(TR / "palabras.json").write_text(json.dumps(W, ensure_ascii=False, indent=0), encoding="utf-8")
print("listo")
