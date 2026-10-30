"""Auditoría de tirones (uniones del corte de pausas sin tapar). Uso: bash ~/.config/crear-videos/py auditar.py <carpeta del vídeo> [mp4 final]
Sin mp4: revisa proyecto/index.html. Con mp4: además detecta cambios de imagen inesperados en el render."""
import json, re, subprocess, sys
B = sys.argv[1]
html = open(f"{B}/proyecto/index.html").read()
scenes = sorted((float(a), float(a) + float(b)) for a, b in re.findall(r'class="scene clip"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', html))
shots = [(float(s), float(d)) for d, s in re.findall(r'tl\.fromTo\("#cam", \{scale: [\d.]+\}, \{scale: [\d.]+, duration: ([\d.]+), ease: "none", immediateRender: false\}, ([\d.]+)\)', html)]
tr = json.load(open(f"{B}/trabajo/tramos.json"))["tramos"]; cuts, acc = [], 0
for a, b in tr[:-1]:
    acc += b - a; cuts.append(round(acc, 3))
ins = lambda c: any(s - 0.006 < c < e + 0.006 for s, e in scenes)
ok = True
for name, val in [("uniones sin tapar", [c for c in cuts if not ins(c) and not any(abs(c - x) < 0.005 for x, _ in shots)]),
                  ("planos visibles < 0,3 s", [(x, d) for x, d in shots if d < 0.3 and not any(s - 0.01 <= x and x + d <= e + 0.01 for s, e in scenes)]),
                  ("solapes de escenas", [(a, b) for a, b in zip(scenes, scenes[1:]) if b[0] < a[1] - 0.001]),
                  ("unión visible a <0,4 s de un borde", [c for c in cuts if not ins(c) and any(0.006 < abs(c - b) < 0.4 for s, e in scenes for b in (s, e))])]:
    print(f"{name}: {val}"); ok &= not val
if len(sys.argv) > 2:
    log = subprocess.run(["ffmpeg", "-i", sys.argv[2], "-vf", "scale=480:-1,select='gt(scene,0.08)',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    det = [float(x) for x in re.findall(r"pts_time:([\d.]+)", log)]
    exp = sorted(set([x for s, e in scenes for x in (s, e)] + [x for x, _ in shots]))
    odd = [t for t in det if not any(s + 0.1 < t < e - 0.05 for s, e in scenes) and min(abs(t - x) for x in exp) > 0.07]
    print(f"render: {len(det)} cambios de imagen; inesperados: {odd}"); ok &= not odd
print("OK" if ok else "FALLA")
