"""Piezas del «estilo nuevo» (ficha: estilos/Estilo Maestria/youtube/estilo.md). Motor único, montado.

Copiadas TAL CUAL del vídeo YouTube 2 (minuto 10, el más completo) + `mini_ruta` del minuto 7 + los iconos que solo
estaban en otros minutos. No se han reescrito: se ven igual que en el vídeo final.

Uso, dentro de `more(root, wt, words, W, H, out)` de scenes_b.py:
    k = kit(root, wt, words, W, H, out)
    k.scene(...), k.ph("frase"), k.gin(...), k.s_card(...), k.stats_card(...), k.broll(...), k.biblio(...) …
"""
import re
import subprocess
from pathlib import Path
from types import SimpleNamespace

from scenes import LEAD, PRE, snaps, write_scene

END = round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(Path(__file__).parent / "assets/voz.m4a")], capture_output=True, text=True).stdout), 3)

TTL = "font-weight:800;color:#101010;letter-spacing:-2px;line-height:1;white-space:nowrap;text-align:center"

# ---- cristal común (mismo vidrio que «Tu sistema» del minuto 2)
GL = """
#ID .gl{position:absolute;border-radius:44px;overflow:hidden;opacity:0;
  background:linear-gradient(135deg,rgba(255,255,255,.34),rgba(190,215,255,.20));
  border:1.5px solid rgba(255,255,255,.55);box-shadow:0 40px 100px rgba(0,20,80,.35),inset 0 1px 0 rgba(255,255,255,.7)}
#ID .gr{zoom:.88;left:1420px;top:260px;width:680px;height:600px}  /* detrás del presentador: su cabeza y hombro tapan el borde (build.py · CUTOUTS) */
#ID .gt{position:absolute;left:0;right:0;top:36px;text-align:center;font-family:'Spline',monospace;font-size:22px;letter-spacing:7px;color:#fff;opacity:.85}
#ID .core{position:absolute;display:flex;align-items:center;justify-content:center;border-radius:46px;background:linear-gradient(160deg,#3b7dff,BLUE);
  box-shadow:0 0 0 10px rgba(255,255,255,.18),0 24px 60px rgba(0,40,160,.55);opacity:0}
#ID .orb{position:absolute;display:flex;align-items:center;justify-content:center;border-radius:50%;background:rgba(255,255,255,.22);
  border:1.5px solid rgba(255,255,255,.65);box-shadow:0 18px 40px rgba(0,20,80,.3),inset 0 1px 0 rgba(255,255,255,.8);opacity:0}
#ID .rg{position:absolute;border-radius:50%;border:3px solid rgba(255,255,255,.7);opacity:0}
#ID .wp{position:absolute;padding:10px 26px;border-radius:999px;background:#fff;color:BLUE;font-size:32px;font-weight:700;white-space:nowrap;opacity:0;box-shadow:0 12px 30px rgba(0,20,80,.3)}
#ID .wt{position:absolute;color:#fff;font-weight:800;letter-spacing:-1px;white-space:nowrap;text-shadow:0 6px 24px rgba(0,20,80,.45);opacity:0}
#ID .gc{left:0;right:0;margin:0 auto}  /* centrado horizontal en blur y b-roll */
"""

# ---- fila fina común a los paneles de cristal (escala única: nada gordo ni diminuto)
RW = """
#ID .rw{position:absolute;left:52px;right:52px;height:76px;border-radius:18px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.28);display:flex;align-items:center;gap:16px;padding:0 18px;opacity:0}
#ID .rw i{flex:none;width:46px;height:46px;border-radius:13px;background:BLUE;display:flex;align-items:center;justify-content:center}
#ID .rw b{font-size:29px;font-weight:600;color:#fff;white-space:nowrap}
#ID .rw s{margin-left:auto;flex:none;width:30px;height:30px;border-radius:50%;background:#16a34a;display:flex;align-items:center;justify-content:center;opacity:0}
"""

# ---- iconos blancos de trazo (24×24)
SW = 'fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
ICON = {
    "target": f'<circle cx="12" cy="12" r="9" {SW}/><circle cx="12" cy="12" r="5" {SW}/><circle cx="12" cy="12" r="1.5" fill="#fff"/>',
    "chart": f'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2" {SW}/>',
    "play": '<path d="M8 5l11 7-11 7z" fill="#fff"/>',
    "crown": f'<path d="M3 8l4 4 5-7 5 7 4-4-2 11H5z" {SW}/>',
    "heart": '<path d="M12 21s-8-5.2-8-11a4.6 4.6 0 0 1 8-3 4.6 4.6 0 0 1 8 3c0 5.8-8 11-8 11z" fill="#fff"/>',
    "bulb": f'<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.9.7 1.6 1.7 1.6 2.9V17h4v-.3c0-1.2.7-2.2 1.6-2.9A6 6 0 0 0 12 3z" {SW}/>',
    "person": '<circle cx="12" cy="8" r="4" fill="#fff"/><path d="M4 21c.6-4.6 3.8-7 8-7s7.4 2.4 8 7z" fill="#fff"/>',
    "alert": f'<path d="M12 3l10 18H2z" {SW}/><path d="M12 10v5" {SW}/><circle cx="12" cy="18" r="1" fill="#fff"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z" fill="#fff"/>',
    "check": f'<path d="M5 12.5l4.5 4.5L19 7" {SW} stroke-width="3"/>',
    "cam": f'<rect x="2" y="7" width="14" height="11" rx="3" {SW}/><path d="M16 11l6-3v9l-6-3" {SW}/>',
    "clock": f'<circle cx="12" cy="12" r="9" {SW}/>',
    "clockh": f'<circle cx="12" cy="12" r="9" {SW}/><path d="M12 7v5l3.5 2" {SW}/>',
    "gear": f'<circle cx="12" cy="12" r="3.5" {SW}/><path d="M19.4 13.5a7.6 7.6 0 0 0 0-3l2-1.6-2-3.4-2.4 1a7.7 7.7 0 0 0-2.6-1.5L14 2.5h-4l-.4 2.5A7.7 7.7 0 0 0 7 6.5l-2.4-1-2 3.4 2 1.6a7.6 7.6 0 0 0 0 3l-2 1.6 2 3.4 2.4-1a7.7 7.7 0 0 0 2.6 1.5l.4 2.5h4l.4-2.5a7.7 7.7 0 0 0 2.6-1.5l2.4 1 2-3.4z" {SW}/>',
    "puzzle": f'<path d="M4 8h4a2 2 0 1 1 4 0h4v4a2 2 0 1 1 0 4v4H4z" {SW}/>',
    "globe": f'<circle cx="12" cy="12" r="9" {SW}/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18" {SW}/>',
    "chat": f'<path d="M4 5h16v11H9l-5 4z" {SW}/>',
    "pen": f'<path d="M4 20l4-1 11-11-3-3L5 16z M14 6l3 3" {SW}/>',
    "layers": f'<path d="M12 3l9 5-9 5-9-5z M3 13l9 5 9-5" {SW}/>',
    "mega": f'<path d="M3 10v4h4l7 4V6L7 10z M17 9a4 4 0 0 1 0 6" {SW}/>',
    "mail": f'<rect x="3" y="5" width="18" height="14" rx="3" {SW}/><path d="M3 7l9 6 9-6" {SW}/>',
    "bot": f'<rect x="5" y="8" width="14" height="11" rx="3" {SW}/><path d="M12 4v4M9 13h.01M15 13h.01M9 16h6" {SW}/>',
    "x": f'<path d="M6 6l12 12M18 6L6 18" {SW} stroke-width="3"/>',
    "app": f'<rect x="3" y="4" width="18" height="16" rx="3" {SW}/><path d="M3 9h18M9 9v11" {SW}/><circle cx="6" cy="6.5" r=".6" fill="#fff"/>',
    "dollar": f'<path d="M12 2.5v19M16.5 7c-.7-1.4-2.4-2.3-4.5-2.3-2.6 0-4.5 1.3-4.5 3.2 0 4.6 9.5 2.3 9.5 7.2 0 2-2 3.4-5 3.4-2.4 0-4.4-1-5.1-2.7" {SW}/>',
    "camig": f'<rect x="3" y="3" width="18" height="18" rx="5" {SW}/><circle cx="12" cy="12" r="4" {SW}/><circle cx="17.3" cy="6.7" r="1" fill="#fff"/>',
    "magnet": f'<path d="M6 3v8a6 6 0 0 0 12 0V3h-4v8a2 2 0 0 1-4 0V3z" {SW}/>',
}


def ico(name, size, color=None, cls=""):
    svg = f'<svg class="{cls}" viewBox="0 0 24 24" width="{size}" height="{size}" style="display:block;overflow:visible">{ICON[name]}</svg>'
    return svg.replace("#fff", color) if color else svg

ICON.update({
    "doc": f'<path d="M6 3h8l4 4v14H6z M14 3v4h4 M9 12h6 M9 16h6" {SW}/>',
    "map": f'<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z M9 4v14 M15 6v14" {SW}/>',
    "pin": f'<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z" {SW}/><circle cx="12" cy="9" r="2.5" {SW}/>',
    "stop": f'<circle cx="12" cy="12" r="9" {SW}/><path d="M8 12h8" {SW}/>',
    "thumb": f'<path d="M7 11v9H4v-9z M7 11l4-7a2 2 0 0 1 3 2l-1 4h6a2 2 0 0 1 2 2l-2 7a2 2 0 0 1-2 1H7" {SW}/>',
    "share": f'<circle cx="6" cy="12" r="2.5" {SW}/><circle cx="18" cy="6" r="2.5" {SW}/><circle cx="18" cy="18" r="2.5" {SW}/><path d="M8.2 11l7.6-4M8.2 13l7.6 4" {SW}/>',
    "up": f'<path d="M3 17l6-6 4 4 8-8" {SW}/><path d="M15 7h6v6" {SW}/>',
    "bars": f'<path d="M5 20V12M12 20V7M19 20V4M3 20h18" {SW}/>',
    "store": f'<path d="M3 9l1.5-5h15L21 9M3 9h18v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0zM5 13v7h14v-7M10 20v-4h4v4" {SW}/>',
    "bolt": f'<path d="M13 2L4 14h7l-1 8 9-12h-7z" {SW}/>',
    "bell": f'<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z M10 20a2 2 0 0 0 4 0" {SW}/>',
    "cal": f'<rect x="3" y="5" width="18" height="16" rx="3" {SW}/><path d="M3 10h18M8 3v4M16 3v4" {SW}/>',
    "copy": f'<rect x="8" y="8" width="12" height="12" rx="2" {SW}/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3" {SW}/>',
    "db": f'<ellipse cx="12" cy="5" rx="8" ry="3" {SW}/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5 M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" {SW}/>',
    "send": f'<path d="M4 12l16-8-6 16-3-6z M11 14l9-10" {SW}/>',
    "pixel": f'<rect x="4" y="4" width="16" height="16" rx="4" {SW}/><circle cx="12" cy="12" r="3" {SW}/>',
    "form": f'<rect x="4" y="3" width="16" height="18" rx="3" {SW}/><path d="M8 8h8M8 12h8M8 16h5" {SW}/>',
    "coin": f'<circle cx="12" cy="12" r="9" {SW}/><path d="M12 7v10M15 9.5c-.4-.9-1.5-1.5-3-1.5-1.7 0-3 .8-3 2 0 3 6 1.5 6 4.5 0 1.2-1.3 2-3 2-1.6 0-2.8-.7-3.2-1.7" {SW}/>',
    "tag": f'<path d="M3 12V4h8l10 10-8 8z" {SW}/><circle cx="7.5" cy="8.5" r="1.5" fill="#fff"/>',
    "laptop": f'<rect x="4" y="5" width="16" height="11" rx="2" {SW}/><path d="M2 19h20" {SW}/>',
    "box": f'<path d="M3 8l9-5 9 5v8l-9 5-9-5z M3 8l9 5 9-5 M12 13v8" {SW}/>',
    "star": f'<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1.1 6.2L12 17.4 6.4 20.3l1.1-6.2L3 9.7l6.2-.9z" {SW}/>',
    "wrench": f'<path d="M14 6a4 4 0 0 0 5 5l-9 9-3-3 9-9a4 4 0 0 0-2-2z" {SW}/>',
})


def kit(root, wt, words, W, H, out):
    def scene(c, s, e, css, body, js, sfx, bg="light"):
        # panel de cristal (#ID-g) nunca vacío: entra 0,4 s antes de su primer contenido
        G = 'tl.fromTo("#ID-g", {opacity: 0, scale: .88, y: 40, filter: "blur(18px)"}, {opacity: 1, scale: 1, y: 0, filter: "blur(0px)", duration: .4, ease: "power3.out"}, sn(0.02));\n'
        T = 'IN("#ID-g .gt", .15, {y: 20});\n'
        if js.startswith(G + T):
            rest = js[len(G + T):]
            ts = [float(x) for x in re.findall(r'(?:sn\(|CNT\("[^"]+", )([0-9.]+)', rest)]
            first = min(ts) if ts else .3
            t0 = round(max(.02, first - .4), 2)
            js = G.replace("sn(0.02)", f"sn({t0})") + f'IN("#ID-g .gt", {t0 + .13:.2f}, {{y: 20}});\n' + rest
            sfx = [(n, (t0 if (n == "whoosh.m4a" and abs(tt) < .1) else tt), v) for n, tt, v in sfx]
        write_scene(root, c, e - s, W, H, css, body, js, bg=bg)
        out.append((c, round(s, 3), round(e, 3), [(n, round(s + t, 3), v) for n, t, v in sfx]))

    toks = [x["w"] for x in words]

    def ph(text, n=1):
        """Tiempo de la primera palabra de la n-ésima aparición EXACTA de la frase."""
        q, k = text.split(), 0
        for i in range(len(toks) - len(q) + 1):
            if toks[i:i + len(q)] == q:
                k += 1
                if k == n:
                    return words[i]["s"]
        raise SystemExit(f"no encuentro «{text}» #{n}")

    def logo(name, size):
        svg = (root / f"assets/logos/{name}.svg").read_text(encoding="utf-8")
        svg = re.sub(r"<title>.*?</title>", "", svg)
        return svg.replace("<svg ", f'<svg width="{size}" height="{size}" style="display:block;flex:none" ', 1)

    def gin(sel, t):
        """Entrada del cristal: aparece desenfocado y se asienta."""
        return f'tl.fromTo("{sel}", {{opacity: 0, scale: .88, y: 40, filter: "blur(18px)"}}, {{opacity: 1, scale: 1, y: 0, filter: "blur(0px)", duration: .4, ease: "power3.out"}}, sn({t:.2f}));\n'

    def gout(sel, d):
        return f'tl.to("{sel}", {{opacity: 0, scale: .94, y: -30, filter: "blur(10px)", duration: .28, ease: "power2.in"}}, sn({d - .3:.2f}));\n'

    def blur_at(t):
        """B-roll limpio hasta t y luego blur fuerte: los motions van encima del blur."""
        return f'tl.fromTo("#ID .bv", {{filter: "blur(0px) brightness(1) saturate(1)"}}, {{filter: "blur(30px) brightness(.7) saturate(1.15)", duration: .45, ease: "power2.inOut", immediateRender: false}}, sn({t:.2f}));\n'

    def gin_slow(sel, t):
        return f'tl.fromTo("{sel}", {{opacity: 0, scale: .94, y: 50, filter: "blur(18px)"}}, {{opacity: 1, scale: 1, y: 0, filter: "blur(0px)", duration: .8, ease: "power2.out"}}, sn({t:.2f}));\n'

    def pulse(sel, t, n=2, k=2.2, d=.9):
        return f'tl.fromTo("{sel}", {{opacity: .9, scale: 1}}, {{opacity: 0, scale: {k}, duration: {d}, ease: "power2.out", repeat: {n - 1}}}, sn({t:.2f}));\n'

    def floaty(sel, t, d, amp=8, per=1.8):
        n = max(1, int(d / per))
        return f'tl.fromTo("{sel}", {{y: 0}}, {{y: -{amp}, duration: {per / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: {n * 2 - 1}}}, {t:.3f});\n'

    # ================================================================== S · apertura a la derecha (build.py · PUSH): icono de cristal + nombre + barra
    S_CSS = """
#ID .wr{right:90px;top:330px;display:flex;flex-direction:column;align-items:flex-start;gap:34px}
#ID .hd{position:relative;display:flex;align-items:center;gap:6px;perspective:900px}
#ID .ico{position:relative;z-index:2;width:140px;height:140px;border-radius:36px;display:flex;align-items:center;justify-content:center;flex:none;font-size:76px;font-weight:800;color:#fff;
  background:linear-gradient(135deg,rgba(255,255,255,.34),rgba(170,200,255,.16));
  border:1.5px solid rgba(255,255,255,.65);box-shadow:0 24px 50px rgba(0,25,90,.35),inset 0 1px 0 rgba(255,255,255,.8);opacity:0}
#ID .ico .rg{position:absolute;inset:-2px;border-radius:38px;border:3px solid rgba(255,255,255,.8);opacity:0}
#ID .nmw{position:relative;z-index:1;overflow:hidden;margin-left:-30px;padding:10px 10px 16px 58px}
#ID .nm{font-size:80px;font-weight:700;letter-spacing:-3px;color:#fff;white-space:nowrap;line-height:1;text-shadow:0 6px 30px rgba(0,20,80,.45)}
#ID .bar{position:relative;margin-left:8px;height:86px;padding:0 30px;display:flex;align-items:center;opacity:0}
#ID .bar .bg{position:absolute;inset:0;background:BLUE;transform:skewX(-12deg) scaleX(0);transform-origin:0 50%;box-shadow:0 16px 40px rgba(0,25,90,.4)}
#ID .bar .tx{position:relative;font-size:46px;font-weight:700;font-style:italic;letter-spacing:-1px;color:#fff;padding-right:10px;clip-path:inset(0 100% 0 0);white-space:nowrap}
"""

    def s_card(c, s, e, icon, name, bar, t_bar, extra_sfx=()):
        L = lambda t: round(max(t - s - LEAD, 0), 3)
        body = (f'<div class="abs wr"><div class="hd"><div class="ico" id="ID-ic">{icon}<i class="rg" id="ID-rg"></i></div><div class="nmw"><div class="nm" id="ID-nm">{name}</div></div></div>'
                f'<div class="bar" id="ID-bar"><span class="bg" id="ID-bg"></span><span class="tx" id="ID-tx">{bar}</span></div></div>')
        tb = L(t_bar)
        js = ('tl.fromTo("#ID-ic", {opacity: 0, scale: .08, rotationX: 55, rotationY: -70, rotation: -35, filter: "blur(16px)"}, {opacity: 1, scale: 1, rotationX: 0, rotationY: 0, rotation: 0, filter: "blur(0px)", duration: .6, ease: "power3.out"}, .1);\n'
              + pulse("#ID-rg", .45, 2, 1.6, .7)
              + 'tl.fromTo("#ID-nm", {xPercent: -105, filter: "blur(12px)"}, {xPercent: 0, filter: "blur(0px)", duration: .6, ease: "power3.out"}, sn(.35));\n'
              f'tl.fromTo("#ID-bg", {{scaleX: .03}}, {{scaleX: 1, duration: .45, ease: "power3.inOut"}}, sn({tb:.2f}));\n'
              f'tl.fromTo("#ID-bar", {{opacity: 0}}, {{opacity: 1, duration: .05}}, sn({tb:.2f}));\n'
              f'tl.fromTo("#ID-tx", {{clipPath: "inset(0 100% 0 0)"}}, {{clipPath: "inset(0 0% 0 0)", duration: .45, ease: "power3.inOut"}}, sn({tb + .04:.2f}));\n'
              f'tl.to("#ID-ic", {{scale: 1.08, duration: .5, yoyo: true, repeat: 3, ease: "sine.inOut"}}, sn({tb + .5:.2f}));\n')
        scene(c, s, e, S_CSS, body, js, [("whoosh.m4a", 0, 0.22), ("pop.mp3", .45, 0.26), ("whoosh-slide.mp3", .35, 0.16), ("ding.m4a", tb, 0.15), *extra_sfx], bg="none")


    # ---- b-roll a pantalla completa (Mixkit, 1080p30): vídeo + degradado inferior + empuje lento
    def broll(src, t0, d, track=3, ms=0.0, blur=False):
        return ('<div style="position:absolute;inset:0;background:#0d1730"></div>'  # fondo bajo el b-roll: el blur deja los bordes translúcidos
                f'<video class="clip bv" src="assets/broll/{src}.mp4" data-start="{t0:.3f}" data-duration="{d + .2:.3f}"' + (f' data-media-start="{ms:.3f}"' if ms else '') + f' data-track-index="{track}" muted playsinline '
                f'style="position:absolute;left:-90px;top:-90px;width:2100px;height:1260px;object-fit:cover' + (';filter:blur(30px) brightness(.7) saturate(1.15)' if blur else '') + '"></video>')

    BV = """
#ID .bv{transform-origin:50% 50%}
#ID .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,15,60,.15) 0%,rgba(0,15,60,.05) 45%,rgba(0,15,60,.55) 100%)}
#ID .gc{left:0;right:0;margin:0 auto}
#ID .gl{background:linear-gradient(135deg,rgba(10,30,90,.62),rgba(10,30,90,.40));border-color:rgba(255,255,255,.45)}
"""

    def stats_card(c, s, e, title, stats, side, zone):
        """Cámara reducida + título grande + tarjetas de datos con contador (como «Cómo lo hicimos» del minuto 5)."""
        L = lambda t: round(max(t - s - LEAD, 0), 3)
        x0, wz = zone
        n = len(stats)
        cw = 340 if n == 3 else 400
        gap = 30
        left = x0 + (wz - (n * cw + (n - 1) * gap)) // 2
        body = (f'<div class="abs ttl" id="ID-t">{title}</div>'
                + "".join(f'<div class="card st bl" id="ID-s{i}" style="left:{left + i * (cw + gap)}px;width:{cw}px"><div class="ic">{ico(icn, 40, "#0050E0")}</div><b id="ID-v{i}">{v0}</b><span class="lb">{lb}</span></div>'
                          for i, (icn, v0, lb, *_r) in enumerate(stats)))
        css = f"""
#ID .ttl{{left:{x0}px;width:{wz}px;top:350px;font-size:56px;{TTL};opacity:0}}
#ID .st{{top:450px;height:250px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;opacity:0}}
#ID .st .ic{{width:72px;height:72px;border-radius:20px;background:#eef4ff;display:flex;align-items:center;justify-content:center}}
#ID .st b{{font-size:46px;font-weight:700;color:BLUE;letter-spacing:-1px;white-space:nowrap;font-variant-numeric:tabular-nums}}
#ID .st .lb{{font-size:24px;font-weight:500;color:#4b5263;text-align:center;line-height:1.15}}
"""
        js = 'SCENE_IN();\nIN("#ID-t", .05, {y: 30});\n'
        sfx = [("swish.mp3", 0, 0.24)]
        for i, (icn, v0, lb, t, cnt) in enumerate(stats):
            js += f'tl.fromTo("#ID-s{i}", {{opacity: 0, y: 60, scale: .8}}, {{opacity: 1, y: 0, scale: 1, duration: .4, ease: "back.out(2)"}}, sn({L(t):.2f}));\n'
            if cnt:
                a, b, pre, suf = cnt
                js += f'CNT("#ID-v{i}", {L(t) + .1}, {a}, {b}, .8, "{pre}", "{suf}", 0);\n'
            sfx += [("pop.mp3", L(t), 0.24)] + ([("moneda.wav", L(t) + .6, 0.16)] if "$" in v0 else [])
        js += f'tl.to("#ID-s{n - 1}", {{scale: 1.06, boxShadow: "0 0 0 2px #0050E0, 0 24px 60px rgba(0,80,224,.22)", duration: .3}}, sn({L(stats[-1][3]) + .8:.2f}));\n'
        scene(c, s, e, css, body, js, sfx + [("ding.m4a", L(stats[-1][3]) + .8, 0.14)])

    ICON.update({
        "doc": f'<path d="M6 3h8l4 4v14H6z M14 3v4h4 M9 12h6 M9 16h6" {SW}/>',
        "map": f'<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z M9 4v14 M15 6v14" {SW}/>',
        "pin": f'<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z" {SW}/><circle cx="12" cy="9" r="2.5" {SW}/>',
        "stop": f'<circle cx="12" cy="12" r="9" {SW}/><path d="M8 12h8" {SW}/>',
        "thumb": f'<path d="M7 11v9H4v-9z M7 11l4-7a2 2 0 0 1 3 2l-1 4h6a2 2 0 0 1 2 2l-2 7a2 2 0 0 1-2 1H7" {SW}/>',
        "share": f'<circle cx="6" cy="12" r="2.5" {SW}/><circle cx="18" cy="6" r="2.5" {SW}/><circle cx="18" cy="18" r="2.5" {SW}/><path d="M8.2 11l7.6-4M8.2 13l7.6 4" {SW}/>',
    })

    # ================================================================== V·BIBLIO · grabación real de la biblioteca (biblioteca.codigomaestria.com/recursos) en una ventana · «biblioteca de recursos»
    def biblio(c, s, e, ms=0.0, chips=()):
        """Ventana de navegador con la grabación de la biblioteca + rótulo «link en la descripción ↓» + chips opcionales [(texto, t global)]."""
        L = lambda t: round(max(t - s - LEAD, 0), 3)
        body = ('<div class="win" id="ID-w"><div class="bar"><i></i><i></i><i></i><span>biblioteca.codigomaestria.com/recursos</span></div>'
                f'<video class="clip" src="assets/broll/biblioteca.mp4" data-start="0" data-duration="{e - s:.3f}"' + (f' data-media-start="{ms:.3f}"' if ms else '')
                + ' data-track-index="3" muted playsinline style="position:absolute;left:0;top:44px;width:1440px;height:810px;object-fit:cover"></video></div>'
                '<div class="pill" id="ID-p">Link en la descripción ↓</div>'
                + "".join(f'<div class="chp" id="ID-c{k}" style="top:{330 + k * 96}px">{t}</div>' for k, (t, _) in enumerate(chips)))
        css = """
#ID .win{position:absolute;left:240px;top:150px;width:1440px;height:854px;border-radius:22px;overflow:hidden;background:#060b1a;box-shadow:0 50px 120px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.15);opacity:0}
#ID .win .bar{position:absolute;left:0;right:0;top:0;height:44px;background:#141b2e;display:flex;align-items:center;gap:8px;padding:0 18px;z-index:2}
#ID .win .bar i{width:12px;height:12px;border-radius:50%;background:#3a4560}
#ID .win .bar span{margin-left:18px;font-family:'Spline',monospace;font-size:17px;color:#9aa6c4}
#ID .pill{position:absolute;left:0;right:0;margin:0 auto;width:max-content;top:66px;padding:16px 36px;border-radius:999px;background:BLUE;color:#fff;font-size:34px;font-weight:800;box-shadow:0 20px 50px rgba(0,40,160,.5);opacity:0;z-index:3}
#ID .chp{position:absolute;right:110px;width:300px;height:76px;border-radius:999px;background:rgba(255,255,255,.97);color:BLUE;font-size:32px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 16px 40px rgba(0,10,40,.35);opacity:0;z-index:3}
"""
        js = ('tl.fromTo("#ID-w", {opacity: 0, y: 60, scale: .92}, {opacity: 1, y: 0, scale: 1, duration: .55, ease: "power3.out"}, 0);\n'
              + f'tl.to("#ID-w", {{scale: 1.05, duration: {e - s - .55:.2f}, ease: "none"}}, .55);\n'
              + 'tl.fromTo("#ID-p", {opacity: 0, y: -30, scale: .8}, {opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2)"}, sn(.5));\n'
              + "".join(f'tl.fromTo("#ID-c{k}", {{opacity: 0, x: 60}}, {{opacity: 1, x: 0, duration: .3, ease: "back.out(1.8)"}}, sn({max(L(t) - .1, .7 + k * .2):.2f}));\n' for k, (_, t) in enumerate(chips)))
        scene(c, s, e, css, body, js, [("whoosh.m4a", 0, 0.22), ("pop.mp3", .5, 0.2)] + [("pop.mp3", max(L(t) - .1, .7 + k * .2), 0.18) for k, (_, t) in enumerate(chips)], bg="none")

    WINCSS = """
#ID .win{position:absolute;left:240px;top:150px;width:1440px;height:854px;border-radius:22px;overflow:hidden;background:#060b1a;box-shadow:0 50px 120px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.15);opacity:0}
#ID .win .bar{position:absolute;left:0;right:0;top:0;height:44px;background:#141b2e;display:flex;align-items:center;gap:8px;padding:0 18px;z-index:2}
#ID .win .bar i{width:12px;height:12px;border-radius:50%;background:#3a4560}
#ID .win .bar span{margin-left:18px;font-family:'Spline',monospace;font-size:17px;color:#9aa6c4}
"""
    def win(src, dur, url):
        return (f'<div class="win" id="ID-w"><div class="bar"><i></i><i></i><i></i><span>{url}</span></div>'
                f'<video class="clip" src="assets/broll/{src}.mp4" data-start="0" data-duration="{dur:.3f}" data-track-index="3" muted playsinline style="position:absolute;left:0;top:44px;width:1440px;height:810px;object-fit:cover"></video></div>')
    WIN_IN = 'tl.fromTo("#ID-w", {opacity: 0, y: 60, scale: .92}, {opacity: 1, y: 0, scale: 1, duration: .5, ease: "power3.out"}, 0);\n'

    def mini_ruta(k):
        """Ruta numerada 01–05 (hechos en blanco, actual en azul con halo): los 5 motions de los pasos se leen como un solo roadmap."""
        return ('<div class="mr">' + "".join(f'<i class="{"on" if i < k else ("cur" if i == k else "")}">0{i + 1}</i>' + (f'<b class="{"on" if i < k else ""}"></b>' if i < 4 else '') for i in range(5)) + '</div>')
    MR = """
#ID .mr{position:absolute;left:0;right:0;top:84px;display:flex;align-items:center;justify-content:center}
#ID .mr i{font-style:normal;width:34px;height:34px;border-radius:50%;border:2px solid rgba(255,255,255,.5);display:flex;align-items:center;justify-content:center;font-family:'Spline',monospace;font-size:13px;color:rgba(255,255,255,.75)}
#ID .mr i.on{background:#fff;border-color:#fff;color:BLUE}
#ID .mr i.cur{width:42px;height:42px;font-size:15px;background:BLUE;border-color:#fff;color:#fff;box-shadow:0 0 0 7px rgba(255,255,255,.22),0 0 24px rgba(80,140,255,.8)}
#ID .mr b{width:34px;height:3px;background:rgba(255,255,255,.3)}
#ID .mr b.on{background:#fff}
"""

    return SimpleNamespace(**{k: v for k, v in locals().items() if k not in ('root', 'wt', 'words', 'W', 'H', 'out')})
