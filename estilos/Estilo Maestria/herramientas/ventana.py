"""Renderiza SOLO una ventana [A, B] de un proyecto HyperFrames del «estilo nuevo».

HyperFrames siempre renderiza desde 0, así que se crea index-ventana.html desplazado: el segundo 0 es A.
- Clips (<video>, <audio>, escenas) con data-start: se desplazan −A; los que acaban antes de A o empiezan después de B se quitan;
  los vídeos/audios que ya estaban sonando en A se recortan con data-media-start (offset en la fuente).
- El timeline principal (zoom, subtítulos, cámara reducida…) se reproduce de A a B con tl.tweenFromTo(A, B): así se aplica también lo que pasó antes de A.
- A no puede caer DENTRO de una escena (su timeline interno no se puede recortar): elegir A en un hueco entre escenas.

Uso: bash ~/.config/crear-videos/py ventana.py <carpeta proyecto> <A> <B> <salida.mp4>   (render con 2 trabajadores; deja index.html intacto)
Luego se pega sobre el render base con trim/concat en el fotograma A·30 … B·30 (comprobar PSNR en los bordes).
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

proj, A, B, out = Path(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
D = round(B - A, 3)
html = (proj / "index.html").read_text(encoding="utf-8")


def fix(m):
    tag = m.group(0)
    s = float(re.search(r'data-start="([0-9.]+)"', tag).group(1))
    d = float(re.search(r'data-duration="([0-9.]+)"', tag).group(1))
    if 'id="root"' in tag:
        return re.sub(r'data-duration="[0-9.]+"', f'data-duration="{D}"', tag, 1)
    e = s + d
    if e <= A + 1e-3 or s >= B - 1e-3:
        return ""  # fuera de la ventana
    is_media = tag.startswith("<video") or tag.startswith("<audio")
    if s < A:
        if not is_media:
            raise SystemExit(f"A={A} cae dentro de una escena: {tag[:120]}")
        ms = re.search(r'data-media-start="([0-9.]+)"', tag)
        off = (float(ms.group(1)) if ms else 0.0) + (A - s)
        tag = re.sub(r' data-media-start="[0-9.]+"', "", tag)
        tag = tag.replace(" data-start=", f' data-media-start="{off:.3f}" data-start=', 1)
        ns, nd = 0.0, min(e, B) - A
    else:
        ns, nd = s - A, min(e, B) - s
    tag = re.sub(r'data-start="[0-9.]+"', f'data-start="{ns:.3f}"', tag, 1)
    return re.sub(r'data-duration="[0-9.]+"', f'data-duration="{nd:.3f}"', tag, 1)


# etiquetas de apertura con data-start (las de cierre se quedan: si se quita la apertura de un clip vacío, quitamos también su cierre)
def clip(m):
    new = fix(re.match(r"<[^>]*>", m.group(0)))
    return new + (m.group(2) or "") if new else ""


out_html = re.sub(r'<(video|audio|div)\b[^>]*data-start="[0-9.]+"[^>]*>(</video>|</audio>|</div>)?', clip, html)
out_html = out_html.replace('window.__timelines["main"] = tl;',
                            f'const __w = gsap.timeline({{ paused: true }}); __w.add(tl.tweenFromTo({A}, {B}, {{ ease: "none" }}), 0);\n'
                            '      window.__timelines["main"] = __w;')  # el timeline original se «reproduce» de A a B (incluye lo que pasó antes de A)
assert "tweenFromTo(" in out_html, "no encuentro el timeline principal"
bak = proj / ".index-completo.html"
shutil.copy(proj / "index.html", bak)
try:
    (proj / "index.html").write_text(out_html, encoding="utf-8")
    r = subprocess.run(([shutil.which("nice"), "-n", "10"] if shutil.which("nice") else []) + [shutil.which("npx") or "npx", "--yes", "hyperframes@0.8.114", "render", "-o", out, "--workers", "2"], cwd=proj,
                       env={**__import__("os").environ, "HF_VIDEO_COVERAGE_THRESHOLD": "0"})
finally:
    shutil.copy(bak, proj / "index.html")
    bak.unlink()
sys.exit(r.returncode)
