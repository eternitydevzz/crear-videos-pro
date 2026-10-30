"""Motor del «estilo nuevo»: genera index.html (+ compositions/*.html vía scenes_b.py y textcards.py), 1920x1080 a 30 fps.

Entradas: assets/aroll.mp4 (cámara, sin audio) · assets/voz.m4a · ../trabajo/palabras.json (palabras con su tiempo)
          ../trabajo/spec.txt (subtítulos por frases) · ../trabajo/pausas.json (pausas acortadas, acortar_pausas.py).
Capas, de abajo arriba: cámara (#fs > #frame > #cam, con palabra gigante + recorte detrás) · sombra inferior · escenas ·
motions · subtítulos · voz + efectos. Reglas del estilo: ../../estilo-nuevo.md.
"""
import json
import re
import subprocess
from pathlib import Path

from motions import motions
import scenes
from scenes import build_scenes, tmap
from textcards import text_cards

ROOT = Path(__file__).parent
W, H = 1920, 1080
END = round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(Path(__file__).parent / "assets/voz.m4a")], capture_output=True, text=True).stdout), 3)
PRE = 0.06  # los cortes de escena entran 2 fotogramas antes de su palabra
CUTS = [tmap(x) for x, y in scenes.QUITADO]  # uniones de las pausas acortadas: un cambio de zoom o una escena tapa el salto

WORDS = json.loads((ROOT / "../trabajo/palabras.json").read_text(encoding="utf-8"))
(ROOT / "assets/palabras.json").write_text(json.dumps(WORDS, ensure_ascii=False, indent=0), encoding="utf-8")


def idx(word, n=1):
    """Índice de la n-ésima aparición EXACTA de una palabra."""
    k = 0
    for i, x in enumerate(WORDS):
        if x["w"] == word:
            k += 1
            if k == n:
                return i
    raise SystemExit(f"no encuentro '{word}' #{n}")


wt = lambda word, n=1: WORDS[idx(word, n)]["s"]

# ------------------------------------------------------------------ CONFIGURACIÓN DE ESTE VÍDEO (lo demás es el motor común)
HIDE_EXTRA = []  # tramos extra sin subtítulos [(inicio, fin)] (p. ej. donde un gráfico ya dice la frase)
BEHIND = []  # palabra gigante detrás: [(texto, tamaño px, inicio, fin, recorte.webm sin extensión, inicio del recorte, duración)]
PUSH = []  # aperturas a la derecha
CUTOUTS = []  # recortes del presentador (webm con alfa) para los paneles de cristal DETRÁS de él: [(nombre, inicio, duración)] · ficha §4
wa = lambda word, after: next(x["s"] for x in WORDS if x["w"] == word and x["s"] >= tmap(after) - 1e-6)  # primera aparición desde «after» s (escrito sobre el vídeo sin acortar pausas)

# ------------------------------------------------------------------ subtítulos: trozos separados por «|», destacada entre *asteriscos*
SPEC = (ROOT / "../trabajo/spec.txt").read_text(encoding="utf-8")
chunks, k = [], 0
for part in SPEC.split("|"):
    toks = part.split()
    key = -1
    for j, t in enumerate(toks):
        if t.startswith("*"):
            key = k + j
            toks[j] = t.strip("*")
    assert [x["w"] for x in WORDS[k:k + len(toks)]] == toks, (toks, [x["w"] for x in WORDS[k:k + len(toks)]])
    chunks.append({"a": k, "b": k + len(toks), "key": key})
    k += len(toks)
assert k == len(WORDS), (k, len(WORDS))
strip = lambda w: re.sub(r"^[¿¡]+|[.,:?!…]+$", "", w)
data = {"words": [[strip(x["w"]) if i in {c["key"] for c in chunks} else x["w"], x["s"]] for i, x in enumerate(WORDS)],
        "chunks": chunks, "end": END}

# ------------------------------------------------------------------ escenas a pantalla completa (scenes.py)
scenes.CUTS[:] = CUTS
SC = build_scenes(ROOT, wt, W, H, WORDS)
text_cards(ROOT, wt, wa, W, H, SC)  # pantallas azules de texto
SC.sort(key=lambda x: x[1])
FR = lambda t: round(round(t * 30) / 30, 3)  # todo cambio cae en un fotograma exacto
SC = [(c, FR(s0), FR(e0), fx) for c, s0, e0, fx in SC]
import math
FRU = lambda t: round(math.ceil(t * 30 - 1e-6) / 30, 3)  # el recorte (webm cortado con -ss s0) empieza en el fotograma ≥ s0: así va clavado a la cámara
CUTOUTS = [(n, FRU(s0), round(FR(s0 + d) - FRU(s0), 3)) for n, s0, d in CUTOUTS]
# Dos escenas seguidas: si la segunda se adelantó hasta una unión del corte, la primera se recorta ahí (sin solapes).
for i in range(len(SC) - 1):
    if SC[i + 1][1] < SC[i][2]:
        SC[i] = (SC[i][0], SC[i][1], SC[i + 1][1], SC[i][3])  # [(id, inicio, fin, sfx[])]
hosts = "\n".join(
    f'      <div id="h-{c}" class="scene clip" data-composition-id="{c}" data-composition-src="compositions/{c}.html" '
    f'data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="2" data-width="{W}" data-height="{H}"></div>'
    for c, s, e, _ in SC)
# ------------------------------------------------------------------ subtítulos «Selección Figma», por FRASES
# Solo cuando se ve al presentador hablando a pantalla completa: fuera en pantallas azules (t), blur (b), gráficos (g), b-rolls (v),
# cámara reducida (c), palabra gigante detrás de él y donde el gráfico ya dice lo mismo.
# Cada frase se ve entera o no se ve: se oculta si choca más de 0,25 s con un tramo oculto (nunca media palabra).
SUBPOS = {"derecha": "left: 40, right: 720", "izquierda": "left: 720, right: 40", "circulo": "left: 40, right: 560"}
HIDE = [(s, e) for c, s, e, _ in SC if c[0] in "tbgvc"]
HIDE += HIDE_EXTRA
CH = [(WORDS[c["a"]]["s"], WORDS[chunks[i + 1]["a"]]["s"] if i + 1 < len(chunks) else END) for i, c in enumerate(chunks)]
ov = lambda a, b: sum(max(0, min(b, e) - max(a, s)) for s, e in HIDE)
vis = [ov(a, b) <= .1 and b - a >= 1.0 for a, b in CH]  # SOLO frases enteras sobre la cara y de ≥1 s
sub_js = 'tl.set("#subs", {opacity: 0}, 0);\n'
for (a, b), v, pv in zip(CH, vis, [None] + vis[:-1]):
    if v != pv:
        sub_js += f'tl.set("#subs", {{opacity: {1 if v else 0}}}, {(a + 0.07 if v else a - 0.04):.3f});\n'  # +2 fotogramas: la frase anterior ya se apagó
# al entrar una escena sin subtítulos (b-roll, blur, tarjeta…) el subtítulo se apaga EN ESE fotograma, aunque la frase siga
_on = []
for (a, b), v, pv in zip(CH, vis, [None] + vis[:-1]):
    if v != pv:
        _on.append((a + 0.07 if v else a - 0.04, v))
for hs, he in HIDE:
    st = next((v for t, v in reversed(_on) if t <= hs + 1e-6), False)
    if st:
        sub_js += f'tl.set("#subs", {{opacity: 0}}, {hs:.3f});\n'
        print("apago subtítulo al entrar escena en", hs)
print("frases con subtítulo:", sum(vis), "de", len(vis))
for c, s0, e0, _ in SC:  # cámara reducida: subtítulo en tinta (fondo claro) y centrado en la zona del gráfico
    for k, pos in SUBPOS.items():
        if k in c:
            fin = e0 >= END - .05
            sub_js += (f'tl.set("#subsw", {{opacity: 0}}, {s0:.3f});\n'
                       f'tl.set("#subs", {{{pos}, "--fg": "#101010", "--sh": "none"}}, {s0 + .5:.3f});\n'
                       f'tl.set("#subsw", {{opacity: 1}}, {s0 + .55:.3f});\n')
            if not fin:
                sub_js += (f'tl.set("#subsw", {{opacity: 0}}, {e0 - .45:.3f});\n'
                           f'tl.set("#subs", {{left: 100, right: 100, top: 905, "--fg": "#fff", "--sh": "0 2px 8px rgba(0,0,0,.75), 0 0 2px rgba(0,0,0,.4)"}}, {e0:.3f});\n'
                           f'tl.set("#subsw", {{opacity: 1}}, {e0:.3f});\n')
# ------------------------------------------------------------------ cámara reducida (lateral o círculo)
# Se recorta #frame y se mueve; queda por encima del gráfico (z 20). Sin zoom en la cara mientras está reducida.
GEOM = {"derecha": ("inset(70px 730px 70px 570px round 44px)", 670, 0, "inset(0px 0px 0px 0px round 0px)"),
        "izquierda": ("inset(70px 730px 70px 570px round 44px)", -500, 0, "inset(0px 0px 0px 0px round 0px)"),
        "circulo": ("circle(470px at 915px 500px)", 785, -270, "circle(1400px at 915px 500px)")}  # círculo arriba a la derecha, cabeza y hombros (×0,4)
lay_js = ""
for c, s, e, _ in SC:
    for k, (g, dx, dy, full) in GEOM.items():
        if k in c:
            lay_js += (f'tl.set("#fs", {{zIndex: 20}}, {s:.3f});\ntl.set("#frame", {{clipPath: "{full}"}}, {s:.3f});\n'
                       f'tl.to("#frame", {{clipPath: "{g}", x: {dx}, y: {dy}, scale: {.4 if k == "circulo" else 1}, transformOrigin: "915px 500px", duration: .55, ease: "power3.inOut"}}, {s:.3f});\n')
            if e < END - .05:  # la última escena (círculo) se queda quieta hasta el final
                # vuelta a pantalla completa de golpe
                lay_js += (f'tl.set("#frame", {{clipPath: "none", x: 0, y: 0, scale: 1}}, {e:.3f});\n'
                           f'tl.set("#fs", {{zIndex: 1}}, {e:.3f});\n')
# ------------------------------------------------------------------ blur de la cámara (escenas «b»): desenfocada y un 28 % más oscura
BL = []
for c, s, e, _ in SC:
    if c[0] == "b":
        if BL and s - BL[-1][1] < .05:
            BL[-1][1] = e
        else:
            BL.append([s, e])
blur_js = 'tl.set("#cam", {filter: "blur(0px) brightness(1)"}, 0);\n' + "".join(
    f'tl.to("#cam", {{filter: "blur(34px) brightness(0.72)", duration: .3, ease: "power2.out"}}, {max(s - .3, 0):.3f});\n'
    f'tl.to("#cam", {{filter: "blur(0px) brightness(1)", duration: .35, ease: "power2.inOut"}}, {e - .1:.3f});\n' for s, e in BL)
# ------------------------------------------------------------------ palabra gigante DETRÁS del presentador: vídeo → palabra → recorte (webm con alfa)
bw_html, bw_js = "", ""
twin_html = "".join(f'<video id="tw{i}" class="clip" src="assets/recorte/{n}.webm" data-start="{s0:.3f}" data-duration="{d:.3f}" data-track-index="{12 + i}" muted playsinline></video>'
                    for i, (n, s0, d) in enumerate(CUTOUTS))
if CUTOUTS:  # el micro de encima (mic.png) también va delante, igual que en #cam
    twin_html += '<img src="assets/mic.png" style="position:absolute;left:0;top:80px;width:100%;height:100%;z-index:3;pointer-events:none;opacity:0" id="twmic">'
    twin_html_js = "".join(f'tl.set("#twmic", {{opacity: 1}}, {s0:.3f});\ntl.set("#twmic", {{opacity: 0}}, {s0 + d:.3f});\n' for _, s0, d in CUTOUTS)
else:
    twin_html_js = ""
for i, (txt, fs, s0, e0, src, cs, cd) in enumerate(BEHIND):
    bw_html += (f'<div class="bw" id="bw{i}" style="font-size:{fs}px">{txt}</div>'
                f'<video id="cut{i}" class="clip cut" src="assets/recorte/{src}.webm" data-start="{cs}" data-duration="{cd}" data-track-index="{6 + i}" muted playsinline></video>')
    bw_js += (f'tl.fromTo("#bw{i}", {{opacity: 0, scale: 1.25, y: 40}}, {{opacity: 1, scale: 1, y: 0, duration: .4, ease: "power3.out"}}, {s0:.3f});\n'
              f'tl.to("#bw{i}", {{scale: 1.05, duration: {e0 - s0 - .6:.3f}, ease: "none"}}, {s0 + .4:.3f});\n'
              f'tl.to("#bw{i}", {{opacity: 0, duration: .2}}, {e0 - .2:.3f});\n')

# ------------------------------------------------------------------ planos de la cámara (zoom alterno 100 / 116 % con empuje lento +4 %)
# El zoom cambia: al volver de una escena, en las uniones de pausas que caen sobre la cara (tapa el salto) y,
# en tramos largos, SOLO al empezar una frase nueva (tras punto; nunca a mitad de frase).
bounds = sorted({0.0} | {s for _, s, _, _ in SC} | {e for _, _, e, _ in SC})
cands = sorted(set(CUTS) | set(bounds))
starts, last = [0.0], 0.0
inside = lambda t: any(s < t < e for _, s, e, _ in SC)
for c in cands:
    if c in bounds or (c - last >= 0.3 and not inside(c)):
        if c - last > 0.3 and c not in starts:
            starts.append(c)
            last = c
starts = sorted(set(starts))
chunk_t = [WORDS[i + 1]["s"] - PRE for i, w in enumerate(WORDS[:-1]) if w["w"].rstrip()[-1:] in ".?!"]
filled = []
for i, s in enumerate(starts):
    e = starts[i + 1] if i + 1 < len(starts) else END
    filled.append(s)
    last = s
    for t in chunk_t:
        if t - last >= 1.5 and e - t >= 1.0 and s < t < e:
            filled.append(round(t, 3))
            last = t
starts = sorted(set(filled))
SHOTS = []
for i, s in enumerate(starts):
    e = starts[i + 1] if i + 1 < len(starts) else END
    SHOTS.append((s, e, 1.0 if len(SHOTS) % 2 == 0 else 1.16))
RED = [(s, e) for c, s, e, _ in SC if c[0] == "c"]  # cámara reducida: zoom 1,0 y sin empuje
cuts = sorted({0.0, END} | {x for s, e, _ in SHOTS for x in (s, e)} | {x for a, b in RED for x in (a, b)})
inred = lambda t: any(a - .001 <= t < b - .001 for a, b in RED)
z_at = lambda t: next((z for s, e, z in SHOTS if s <= t < e), 1.0)
SHOTS = [(a, b, 1.0 if inred(a) else z_at(a)) for a, b in zip(cuts, cuts[1:]) if b - a > .01]
zoom_js = "".join(f'tl.fromTo("#cam, #twin", {{scale: {z}}}, {{scale: {z + (0 if inred(s) else 0.04):.2f}, duration: {e - s - 0.002:.3f}, ease: "none", immediateRender: false}}, {s:.3f});\n'
                  for s, e, z in SHOTS)

# ------------------------------------------------------------------ apertura a la derecha (ref «animiation.mp4»; va con una escena «s»)
# Sin zoom: el plano se desplaza 320 px a la izquierda en 0,5 s con desenfoque de movimiento; la pared se prolonga con la franja
# derecha del vídeo EN ESPEJO Y DESENFOCADA, solapada 120 px con fundido (sin rayas ni costura). Empieza y acaba en inicio de frase.
ext_html = ""
for i, (s0, e0) in enumerate(PUSH):  # extensión de la pared: 120 px del borde + espejo de los 360 px derechos, con desenfoque
    ext = ROOT / f"assets/recorte/ext{i}.mp4"
    if not ext.exists() or ext.stat().st_mtime < Path(__file__).stat().st_mtime:
        ext.parent.mkdir(exist_ok=True)
        subprocess.run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-ss", f"{max(s0 - .1, 0):.3f}", "-i", str(ROOT / "assets/aroll.mp4"), "-t", f"{e0 - s0 + .3:.3f}",
                        "-filter_complex", "[0:v]split[a][b];[a]crop=120:1080:1800:0[e];[b]crop=360:1080:1560:0,hflip[m];[e][m]hstack,gblur=sigma=18,format=yuv420p", "-an", "-c:v", "libx264", "-crf", "14", str(ext)], check=True)
    ext_html += f'<video id="ext{i}" class="clip ext" src="assets/recorte/ext{i}.mp4" data-start="{max(s0 - .1, 0):.3f}" data-duration="{e0 - s0 + .3:.3f}" data-track-index="{16 + i}" muted playsinline></video>'
push_js = "".join(
    f'tl.fromTo("#fs", {{x: 0, scale: 1}}, {{x: -320, scale: 1, duration: .5, ease: "power3.out", immediateRender: false}}, {s:.3f});\n'
    f'tl.to("#cam", {{filter: "blur(9px) brightness(1)", duration: .18, ease: "power2.in"}}, {s:.3f});\n'
    f'tl.to("#cam", {{filter: "blur(0px) brightness(1)", duration: .32, ease: "power2.out"}}, {s + .18:.3f});\n'
    f'tl.set("#fs", {{x: 0, scale: 1}}, {e:.3f});\n' for s, e in PUSH)

# ------------------------------------------------------------------ efectos de sonido: cada uno en la primera pista libre
mo_css, mo_html, mo_js, mo_sfx = motions(wt, wa, END)
SFX = sorted([x for *_, sf in SC for x in sf] + [(n, round(t, 3), v) for n, t, v in mo_sfx], key=lambda x: x[1])
DUR = {f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ROOT / "assets/sfx" / f)],
                               capture_output=True, text=True).stdout) for f in {x[0] for x in SFX}}
track_end, rows = [], []  # cada efecto en la primera pista libre (sin solapes en la misma pista)
for k, (n, t, v) in enumerate(SFX):
    d = min(DUR[n], END - t)
    tr = next((i for i, x in enumerate(track_end) if x <= t), None)
    if tr is None:
        track_end.append(0)
        tr = len(track_end) - 1
    track_end[tr] = t + d
    rows.append(f'      <audio id="sfx{k:02d}" src="assets/sfx/{n}" data-start="{t:.3f}" data-duration="{d:.3f}" data-track-index="{20 + tr}" data-volume="{v}"></audio>')
sfx_html = "\n".join(rows)

FONT_CSS = "\n".join(
    f"@font-face{{font-family:'Hanken';src:url(assets/fonts/{f}) format('woff2');font-weight:700;unicode-range:{ur}}}"
    for f, ur in [("HankenGrotesk-normal-700-latin-fe1634.woff2", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2212"),
                  ("HankenGrotesk-normal-700-latin-ext-d9a6a0.woff2", "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+2020,U+20A0-20AB,U+20AD-20C0,U+2C60-2C7F,U+A720-A7FF")])

index = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>{ROOT.parent.name}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      {FONT_CSS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: 'Hanken', sans-serif; }}
      #fs {{ position: absolute; inset: 0; z-index: 1; filter: drop-shadow(0 30px 60px rgba(0,0,0,.35)); }}
      #frame {{ position: absolute; inset: 0; z-index: 1; }}
      #cam {{ position: absolute; inset: 0; transform-origin: 920px 640px; }}
      .ext {{ position: absolute; left: 1800px; top: 0; width: 480px; height: 100%; object-fit: fill; -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 120px); mask-image: linear-gradient(90deg, transparent 0, #000 120px); }}
      #twin {{ position: absolute; inset: 0; z-index: 11; transform-origin: 920px 640px; pointer-events: none; }}
      #twin video {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
      .bw {{ position: absolute; left: 0; right: 0; top: 140px; text-align: center; font-weight: 700; color: #fff; letter-spacing: -0.03em; line-height: 1; opacity: 0; z-index: 1;
             text-shadow: 0 10px 60px rgba(0,30,90,.35); }}
      .cut {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 2; }}
      #av {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #shade {{ position: absolute; left: 0; right: 0; bottom: 0; height: 380px; z-index: 5;
                background: linear-gradient(to top, rgba(0,0,0,.38), rgba(0,0,0,0)); }}
      .scene {{ position: absolute; inset: 0; z-index: 10; }}
      @font-face {{ font-family: 'NYI'; src: url(assets/fonts/NewYorkItalic.ttf); font-style: italic; }}
      #subs {{ position: absolute; left: 100px; right: 100px; top: 905px; height: 110px; z-index: 50; }}
      .chunk {{ position: absolute; left: 0; right: 0; bottom: 0; display: flex; flex-wrap: wrap; row-gap: 4px; justify-content: center; align-items: baseline; opacity: 0; }}
      .word {{ display: inline-block; white-space: nowrap; overflow: hidden; padding: 14px 0 16px; margin: -14px 0 -16px; font-family: 'Helvetica Neue', Helvetica, sans-serif;
               font-size: 67px; line-height: 1.1; font-weight: 400; color: var(--fg, #fff); text-shadow: var(--sh, 0 2px 8px rgba(0,0,0,.75), 0 0 2px rgba(0,0,0,.4));
               opacity: 0; --b: 0; filter: blur(calc(var(--b) * 1px)); }}
      .word .in {{ padding-right: .28em; }}
      .word.num {{ font-weight: 700; }}
      .word.key {{ filter: none !important; }}  /* en el render, el desenfoque de entrada deja invisible la palabra con recuadro */
      .word.key .in {{ position: relative; display: inline-block; font-family: 'NYI', Georgia, serif; font-style: italic; font-size: 1.08em; text-shadow: none; color: #fff;
               padding: 0 12px; margin-right: .28em; background: rgba(32,72,152,.55); border: 2px solid #5888E0; border-radius: 3px; }}
      .word.key .in::before, .word.key .in::after {{ content: ""; position: absolute; width: 12px; height: 12px; border-radius: 50%; background: #5888E0; border: 2px solid #ebf0ff; }}
      .word.key .in::before {{ left: -8px; top: -8px; }}
      .word.key .in::after {{ right: -8px; bottom: -8px; }}
      {mo_css}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="{W}" data-height="{H}">
      <div id="fs"><div id="frame"><div id="cam"><video id="av" class="clip" src="assets/aroll.mp4" data-start="0" data-duration="{END}" data-track-index="1" muted playsinline></video>{bw_html}{ext_html}<img id="mic" src="assets/mic.png" style="position:absolute;left:0;top:80px;width:100%;height:100%;z-index:3;pointer-events:none"></div></div></div>
      <div id="shade"></div>
{hosts}
      <div id="twin">{twin_html}</div>
      {mo_html}
      <div id="subsw" style="position:absolute;inset:0;z-index:50;pointer-events:none"><div id="subs"></div></div>
      <audio id="voz" src="assets/voz.m4a" data-start="0" data-duration="{END}" data-track-index="10" data-volume="0.8"></audio>
{sfx_html}
    </div>
    <script>
      const D = {json.dumps(data, ensure_ascii=False)};
      const F = 1 / 30;
      const sn = (t) => Math.round(t * 30) / 30;
      const tl = gsap.timeline({{ paused: true }});
      const subs = document.getElementById("subs");
      D.chunks.forEach((c, ci) => {{
        const t0 = D.words[c.a][1];
        const el = document.createElement("div");
        el.className = "chunk"; el.id = "ch" + ci;
        for (let k = c.a; k < c.b; k++) {{
          const sp = document.createElement("span");
          sp.className = "word" + (k === c.key ? " key" : (/[0-9]/.test(D.words[k][0]) ? " num" : "")); sp.id = "w" + k;
          const inn = document.createElement("span"); inn.className = "in"; inn.textContent = D.words[k][0];
          sp.appendChild(inn);
          el.appendChild(sp);
        }}
        subs.appendChild(el);
        el.querySelectorAll(".word").forEach((w) => {{ w.dataset.w = w.scrollWidth; w.style.maxWidth = "0px"; }});
        tl.set(el, {{ opacity: 1 }}, sn(t0));
        for (let k = c.a; k < c.b; k++) {{
          const t = sn(D.words[k][1]);
          const sel = "#w" + k;
          const wpx = +document.getElementById("w" + k).dataset.w + 2;
          // la línea crece y se recentra con suavidad; la palabra entra desenfocada y se enfoca en 0,2 s
          tl.fromTo(sel, {{ maxWidth: 0 }}, {{ maxWidth: wpx, duration: .2, ease: "power2.out" }}, t);
          tl.set(sel, {{ maxWidth: "none" }}, t + .2);  // ancho natural en cuanto entra (la medida puede ser de antes de cargar la fuente)
          tl.fromTo(sel, {{ opacity: 0, "--b": 12 }}, {{ opacity: 1, "--b": 0, duration: .2, ease: "power2.out" }}, t);
        }}
        const next = ci + 1 < D.chunks.length ? D.words[D.chunks[ci + 1].a][1] : D.end;
        tl.to(el, {{ opacity: 0, duration: 2 * F, ease: "none" }}, sn(Math.max(next - 2 * F, t0 + F)));
      }});
{sub_js}
{zoom_js}
{lay_js}
{blur_js}
{push_js}
{twin_html_js}
{bw_js}
{mo_js}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(index, encoding="utf-8")
print("escenas:", [(c, s, round(e - s, 2)) for c, s, e, _ in SC])
print("planos:", len(SHOTS), [(round(s, 2), round(e - s, 2), z) for s, e, z in SHOTS[:8]], "…")
print("sfx:", [(n, round(t, 2)) for n, t, _ in SFX])
print("trozos:", len(chunks), "| destacadas:", sum(c["key"] >= 0 for c in chunks))
