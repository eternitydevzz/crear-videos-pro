"""Base común de las escenas (estilo nuevo): colores, fuentes, CSS/JS compartidos y escritura de compositions/<id>.html.

- Fondo «light»: #F5F6F8 + cuadrícula 72 px + 2 brillos azules; tarjetas blancas radio 36 px.
- Cada elemento entra 0,10 s antes de su palabra (LEAD); la escena entra 0,06 s antes de la suya (PRE).
- tmap(t): tiempo escrito a mano sobre el vídeo sin acortar pausas -> tiempo actual (../trabajo/pausas.json).
"""
import json
from pathlib import Path

INK, BLUE, BG, RED = "#101010", "#0050E0", "#F5F6F8", "#E5484D"
LEAD, PRE = 0.10, 0.06
CUTS = []  # uniones de las pausas acortadas; build.py las rellena antes de crear escenas
_PZ = Path(__file__).parent / "../trabajo/pausas.json"
QUITADO = json.loads(_PZ.read_text())["quitado"] if _PZ.exists() else []  # pausas acortadas (acortar_pausas.py)


def tmap(t):
    """Tiempo escrito a mano sobre el vídeo SIN acortar pausas -> tiempo actual (las pausas a ~0,12 s)."""
    return round(t - sum(min(y, max(t, x)) - x for x, y in QUITADO), 3)


def snap(t, w=0.4, end=False):
    """Una unión del corte justo antes de que entre una escena (o justo después de que salga) se ve como un salto:
    el inicio se adelanta hasta esa unión y el final se alarga hasta ella (nunca al revés: ningún gráfico entra tarde)."""
    near = [c for c in CUTS if (t <= c <= t + w if end else t - w <= c <= t)]
    return (min(near) if end else max(near)) if near else t


def snaps(s, e):
    return round(snap(s), 3), round(snap(e, end=True), 3)

FONTS = [("Hanken", "HankenGrotesk-normal-500-latin-fe1634.woff2", 500, "normal"),
         ("Hanken", "HankenGrotesk-normal-500-latin-ext-d9a6a0.woff2", 500, "normal"),
         ("Hanken", "HankenGrotesk-normal-700-latin-fe1634.woff2", 700, "normal"),
         ("Hanken", "HankenGrotesk-normal-700-latin-ext-d9a6a0.woff2", 700, "normal"),
         ("News", "Newsreader-italic-500-latin-78bd98.woff2", 500, "italic"),
         ("News", "Newsreader-italic-500-latin-ext-e36b6b.woff2", 500, "italic"),
         ("Spline", "SplineSansMono-normal-500-latin-53329b.woff2", 500, "normal"),
         ("Spline", "SplineSansMono-normal-500-latin-ext-62a811.woff2", 500, "normal")]
UR = {False: "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2212",
      True: "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+2020,U+20A0-20AB,U+20AD-20C0,U+2C60-2C7F,U+A720-A7FF"}
FONT_CSS = "\n".join(f"@font-face{{font-family:'{fam}';src:url(assets/fonts/{f}) format('woff2');font-weight:{w};font-style:{st};unicode-range:{UR['ext' in f]}}}"
                     for fam, f, w, st in FONTS)

COMMON_CSS = """
#ID{position:absolute;inset:0;overflow:hidden;font-family:'Hanken',sans-serif;color:INK}
#ID .bgl{position:absolute;inset:0;background:BG}
#ID .glow{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(0,80,224,.20),rgba(0,80,224,0) 70%)}
#ID .g1{left:-380px;top:-380px;width:1000px;height:1000px}
#ID .g2{right:-420px;bottom:-300px;width:1100px;height:1100px}
#ID .grid{position:absolute;inset:0;background-image:linear-gradient(rgba(16,16,16,.045) 2px,transparent 2px),linear-gradient(90deg,rgba(16,16,16,.045) 2px,transparent 2px);background-size:72px 72px}
#ID .bl{--b:0;filter:blur(calc(var(--b)*1px))}
#ID .card{position:absolute;background:#fff;border-radius:36px;box-shadow:0 30px 80px rgba(16,24,40,.14),0 4px 14px rgba(16,24,40,.06)}
#ID .mono{font-family:'Spline',monospace;font-weight:500;letter-spacing:3px;text-transform:uppercase}
#ID .serif{font-family:'News',serif;font-style:italic;font-weight:500;color:BLUE}
#ID .abs{position:absolute}
#ID .full{position:absolute;inset:0}
#ID .tag{left:0;right:0;margin:0 auto;width:max-content;top:110px;padding:14px 40px;border:4px solid BLUE;border-radius:999px;background:rgba(255,255,255,.92);font-size:44px;letter-spacing:5px;white-space:nowrap;color:#14256B;box-shadow:0 14px 34px rgba(0,80,224,.14)}
#ID .tag b{font-weight:500;color:BLUE}
"""

COMMON_JS = r"""
const F = 1/30;
const sn = t => Math.round(t*30)/30;
const IN = (sel, t, o) => {const r = (o&&o.rot)||0; const f = Object.assign({y: 90, scale: .92, "--b": 14, opacity: 0}, o||{}); delete f.rot; return tl.fromTo(sel, f, {y: 0, x: 0, scale: 1, rotation: r, "--b": 0, opacity: 1, duration: .32, ease: "power3.out"}, sn(t));};
const POP = (sel, t, r) => tl.fromTo(sel, {scale: 0, opacity: 0, rotation: (r||0) - 12}, {scale: 1, opacity: 1, rotation: r||0, duration: .3, ease: "back.out(2.4)"}, sn(t));
const SHAKE = (sel, t, px) => tl.fromTo(sel, {x: 0}, {x: px, duration: .05, yoyo: true, repeat: 3, ease: "none"}, sn(t));
const fmt = (v, dec) => {const p = v.toFixed(dec||0).split("."); return p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".") + (p[1] ? "," + p[1] : "");};
const CNT = (sel, t, a, b, d, pre, suf, dec) => {const o = {v: a}, el = document.querySelector(sel); tl.fromTo(o, {v: a}, {v: b, duration: d, ease: "power2.out", onUpdate: () => { el.textContent = pre + fmt(o.v, dec) + suf; }}, sn(t));};
const SCENE_IN = () => tl.fromTo("#ID-wrap", {scale: 1.12, "--b": 18, opacity: 1}, {scale: 1, "--b": 0, opacity: 1, duration: .22, ease: "power3.out"}, 0);
"""


# Fondos: «light» = gráfico claro · «blue» = pantalla azul (#1157df → #003fab) · «none» = transparente (se ve la cámara o un b-roll)
BACKS = {"none": "",
         "light": '<div class="bgl"></div><div class="grid"></div><div class="glow g1"></div><div class="glow g2"></div>\n',
         "blue": '<div class="full" style="background:radial-gradient(ellipse at 50% 38%,#2f74ff 0%,#1157df 45%,#003fab 100%)"></div>\n'}


def write_scene(root, cid, dur, w, h, css, body, js, bg="light"):
    css = FONT_CSS + (COMMON_CSS + css).replace("#ID", "#" + cid).replace("INK", INK).replace("BLUE", BLUE).replace("BG", BG)
    js = (COMMON_JS + js).replace("#ID", "#" + cid).replace("BLUE", BLUE)
    body = body.replace('"ID-', f'"{cid}-')
    html = (f'<!doctype html>\n<html><head><meta charset="UTF-8"></head><body>\n<template>\n<style>{css}</style>\n'
            f'<div id="{cid}" data-composition-id="{cid}" data-width="{w}" data-height="{h}">\n'
            + BACKS[bg] +
            f'<div id="{cid}-wrap" class="full bl">\n{body}\n</div>\n</div>\n<script>\n(function(){{\n'
            f'const tl = gsap.timeline({{paused: true}});\n{js}\ntl.set({{}}, {{}}, {dur:.3f});\n'
            f'window.__timelines["{cid}"] = tl;\n}})();\n</script>\n</template></body></html>\n')
    (root / "compositions").mkdir(exist_ok=True)
    (root / "compositions" / f"{cid}.html").write_text(html, encoding="utf-8")


def build_scenes(root: Path, wt, W, H, words):
    """Escribe las escenas del vídeo (scenes_b.py) y devuelve [(id, inicio, fin, [(sfx, t, vol)])] en tiempo global."""
    from scenes_b import more
    out = []
    more(root, wt, words, W, H, out)
    return out
