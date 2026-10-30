"""Motor MaestrIA (reconstruido desde Leccion 5 / Módulos). Genera index.html + compositions/*.html (1920x1080, 30 fps).

Base copiada del proyecto «LM 1» (pasada 3, aprobada por el presentador). Cambio pedido: las pantallas de texto van
todas en AZUL con letra blanca (los gráficos de fondo claro se mantienen).
- assets/aroll.mp4 (brillo medio +37 % solo en la persona) / assets/voz.m4a: pausas >0,3 s cortadas (97,6 s).
- ../trabajo/palabras.json: guion_final.txt (lo que dice el audio, aprobado por el presentador) con tiempos de Whisper.
"""
import json
import re
import subprocess
from pathlib import Path

from motions import motions
import scenes
from scenes import build_scenes
from textcards import text_cards

ROOT = Path(__file__).parent
W, H = 1920, 1080
END = round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(Path(__file__).parent / "assets/voz.m4a")], capture_output=True, text=True).stdout), 3)
PRE = 0.06  # los cortes de escena entran 2 fotogramas antes de su palabra
TRAMOS = json.loads((ROOT / "../trabajo/tramos.json").read_text())["tramos"]
CUTS = []
_acc = 0.0
for a, b in TRAMOS[:-1]:
    _acc += b - a
    CUTS.append(round(_acc, 3))

WORDS = json.loads((ROOT / "../trabajo/palabras.json").read_text(encoding="utf-8"))
(ROOT / "assets/palabras.json").write_text(json.dumps(WORDS, ensure_ascii=False, indent=0), encoding="utf-8")


def idx(word, n=1):
    """Índice de la n-ésima aparición EXACTA de una palabra (error 3 de estilo.md: nada de buscar sin distinguir)."""
    k = 0
    for i, x in enumerate(WORDS):
        if x["w"] == word:
            k += 1
            if k == n:
                return i
    raise SystemExit(f"no encuentro '{word}' #{n}")


wt = lambda word, n=1: WORDS[idx(word, n)]["s"]
wa = lambda word, after: next(x["s"] for x in WORDS if x["w"] == word and x["s"] >= after - 1e-6)  # primera aparición desde «after» s

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
import textcards
textcards.END = END
text_cards(ROOT, wt, wa, W, H, SC)  # pantallas de texto blancas/azules
SC.sort(key=lambda x: x[1])
# Dos escenas seguidas: si la segunda se adelantó hasta una unión del corte, la primera se recorta ahí (sin solapes).
for i in range(len(SC) - 1):
    if SC[i + 1][1] < SC[i][2]:
        SC[i] = (SC[i][0], SC[i][1], SC[i + 1][1], SC[i][3])  # [(id, inicio, fin, sfx[])]
hosts = "\n".join(
    f'      <div id="h-{c}" class="scene clip" data-composition-id="{c}" data-composition-src="compositions/{c}.html" '
    f'data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="2" data-width="{W}" data-height="{H}"></div>'
    for c, s, e, _ in SC)
# subtítulos: blancos sobre la persona, tinta + destacada azul sobre los gráficos claros
sub_js = "".join(f'tl.set("#subs", {{"--fg": "#101010", "--key": "#0050E0", "--sh": "none"}}, {s:.3f});\n'
                 f'tl.set("#subs", {{"--fg": "#fff", "--key": "#fff", "--sh": "0 4px 24px rgba(0,0,0,.55)"}}, {e:.3f});\n'
                 for _, s, e, _ in SC)
# Sobre las pantallas de texto no hay subtítulos (como en las dos referencias del presentador): el texto ya está en grande.
sub_js += "".join(f'tl.set("#subs", {{opacity: 0}}, {s:.3f});\ntl.set("#subs", {{opacity: 1}}, {e:.3f});\n' for c, s, e, _ in SC if c.startswith("t"))

# ------------------------------------------------------------------ planos de A-roll (zoom alterno 100/116 %)
# Cambio de zoom: al volver de un gráfico y en las uniones del corte de pausas (lo tapa), sin planos de menos de 2 s.
bounds = sorted({0.0} | {s for _, s, _, _ in SC} | {e for _, _, e, _ in SC})
cands = sorted(set(CUTS) | set(bounds))
starts, last = [0.0], 0.0
inside = lambda t: any(s < t < e for _, s, e, _ in SC)
for c in cands:  # pasada 3: TODAS las uniones fuera de gráficos cambian de zoom (si no, se ve el tirón)
    if c in bounds or (c - last >= 0.3 and not inside(c)):
        if c - last > 0.3 and c not in starts:
            starts.append(c)
            last = c
starts = sorted(set(starts))
# Tramos largos sin uniones: cambio de zoom en la palabra que abre trozo (−PRE), un plano cada ~3 s (estilobasico.md: 3,6 s de media).
chunk_t = [WORDS[c["a"]]["s"] - PRE for c in chunks]
filled = []
for i, s in enumerate(starts):
    e = starts[i + 1] if i + 1 < len(starts) else END
    filled.append(s)
    last = s
    for t in chunk_t:
        if t - last >= 2.6 and e - t >= 2.0 and s < t < e:
            filled.append(round(t, 3))
            last = t
starts = sorted(set(filled))
SHOTS = []
for i, s in enumerate(starts):
    e = starts[i + 1] if i + 1 < len(starts) else END
    SHOTS.append((s, e, 1.0 if len(SHOTS) % 2 == 0 else 1.16))
zoom_js = "".join(f'tl.fromTo("#cam", {{scale: {z}}}, {{scale: {z + 0.04:.2f}, duration: {e - s - 0.002:.3f}, ease: "none", immediateRender: false}}, {s:.3f});\n'
                  for s, e, z in SHOTS)

# ------------------------------------------------------------------ efectos (volúmenes aprobados en estilo.md §9.3)
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
      #cam {{ position: absolute; inset: 0; transform-origin: 920px 640px; }}
      #av {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #shade {{ position: absolute; left: 0; right: 0; bottom: 0; height: 380px; z-index: 5;
                background: linear-gradient(to top, rgba(0,0,0,.38), rgba(0,0,0,0)); }}
      .scene {{ position: absolute; inset: 0; z-index: 10; }}
      #subs {{ position: absolute; left: 260px; right: 260px; top: 800px; z-index: 50; --fg: #fff; --key: #fff; --sh: 0 4px 24px rgba(0,0,0,.55); }}
      .chunk {{ position: absolute; left: 0; right: 0; top: 0; display: flex; flex-wrap: wrap; justify-content: center; align-items: baseline; column-gap: 18px; opacity: 0; }}
      .word {{ display: none; font-size: 64px; line-height: 1.2; font-weight: 700; color: var(--fg); text-shadow: var(--sh);
               opacity: 0; --b: 0; filter: blur(calc(var(--b) * 1px)); }}
      .word.key {{ flex-basis: 100%; text-align: center; text-transform: uppercase; font-size: 112px; line-height: 1.05; letter-spacing: -3px; color: var(--key); }}
      {mo_css}
      #blk {{ position: absolute; inset: 0; background: #000; opacity: 0; z-index: 90; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="{W}" data-height="{H}">
      <div id="cam"><video id="av" class="clip" src="assets/aroll.mp4" data-start="0" data-duration="{END}" data-track-index="1" muted playsinline></video></div>
      <div id="shade"></div>
{hosts}
      {mo_html}
      <div id="subs"></div>
      <div id="blk"></div>
      <audio id="voz" src="assets/voz.m4a" data-start="0" data-duration="{END}" data-track-index="10" data-volume="1"></audio>
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
          sp.className = "word" + (k === c.key ? " key" : ""); sp.id = "w" + k;
          sp.textContent = D.words[k][0];
          el.appendChild(sp);
        }}
        subs.appendChild(el);
        tl.set(el, {{ opacity: 1 }}, sn(t0));
        for (let k = c.a; k < c.b; k++) {{
          const t = sn(D.words[k][1]);
          const sel = "#w" + k;
          tl.set(sel, {{ display: "block" }}, t);
          if (k === c.key) tl.fromTo(sel, {{ opacity: 0, "--b": 14, scale: .7 }}, {{ opacity: 1, "--b": 0, scale: 1, duration: .16, ease: "back.out(2.5)" }}, t);
          else tl.fromTo(sel, {{ opacity: 0, "--b": 10, y: 14 }}, {{ opacity: 1, "--b": 0, y: 0, duration: .12, ease: "power2.out" }}, t);
        }}
        const next = ci + 1 < D.chunks.length ? D.words[D.chunks[ci + 1].a][1] : D.end;
        tl.to(el, {{ opacity: 0, duration: 2 * F, ease: "none" }}, sn(Math.max(next - 2 * F, t0 + F)));
      }});
{sub_js}
{zoom_js}
{mo_js}
      tl.to("#blk", {{ opacity: 1, duration: .3, ease: "none" }}, {END - 0.3:.2f});
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
