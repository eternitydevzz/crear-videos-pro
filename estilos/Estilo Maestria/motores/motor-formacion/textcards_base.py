"""Pantallas de texto grande a partir de dos referencias suyas:
- Blanca: «Video YT/Intro - primeros 10 s - pasada 11.mp4» (3,30–4,87 s): fondo blanco liso, etiqueta mono azul,
  palabra gigante azul y línea que se dibuja.
- Azul: vídeo de WhatsApp del 2026-10-14: degradado #1157df → #003fab, texto blanco grueso, tachados y letra a letra.
Sin subtítulos encima (build.py los oculta en los ids «t..»). Ids: tNN-palabra.
"""
from scenes import BLUE, LEAD, PRE, RED, snap, snaps, write_scene

CSS = f"""
#ID .box{{position:absolute;inset:0;justify-content:center;display:flex;flex-direction:column;align-items:center;gap:26px}}
#ID .lab{{font-family:'Spline',monospace;font-weight:500;font-size:46px;letter-spacing:14px;text-transform:uppercase;opacity:0}}
#ID .big{{font-weight:700;font-size:220px;line-height:.95;letter-spacing:-6px;text-transform:uppercase;white-space:nowrap;position:relative;opacity:0}}
#ID .big i{{font-style:normal;display:inline-block}}
#ID .ul{{width:420px;height:10px;border-radius:5px;transform-origin:50% 50%}}
#ID .strike{{position:absolute;left:-20px;right:-20px;top:52%;height:22px;margin-top:-11px;border-radius:11px;background:{RED};transform-origin:0 50%}}
#ID .w .lab{{color:{BLUE}}} #ID .w .big{{color:{BLUE}}} #ID .w .ul{{background:{BLUE}}}
#ID .b .lab{{color:rgba(255,255,255,.8)}} #ID .b .big{{color:#fff;text-shadow:0 10px 50px rgba(0,20,80,.35)}} #ID .b .ul{{background:#fff}}
"""


def card(root, W, H, out, c, s, e, bg, label, big, t_lab, t_big, letters=False, ul=False, strike=None, extra_body="", extra_js="", sfx=(), size=None):
    """Etiqueta + palabra gigante. Tiempos globales; se pasan a locales con LEAD."""
    s, e = snaps(s, e)
    L = lambda t: 0.0 if t is None else round(max(t - s - LEAD, 0), 3)  # None = al entrar la pantalla
    fs = size or min(220, int(1650 / (0.64 * len(big))))  # que la palabra gigante quepa en una línea (≤ ~1650 px)
    word = "".join(f"<i>{ch}</i>" if ch != " " else " " for ch in big) if letters else big
    body = (f'<div class="box {"w" if bg == "white" else "b"}">'
            + (f'<div class="lab" id="ID-lab">{label}</div>' if label else "")
            + f'<div class="big" id="ID-big" style="font-size:{fs}px;letter-spacing:{-fs / 36:.1f}px">{word}' + ('<span class="strike" id="ID-st"></span>' if strike else "") + "</div>"
            + ('<div class="ul" id="ID-ul"></div>' if ul else "") + extra_body + "</div>")
    js = ""
    if label:
        js += f'tl.fromTo("#ID-lab", {{opacity: 0, y: 30, "--b": 10}}, {{opacity: 1, y: 0, "--b": 0, duration: .25, ease: "power3.out"}}, sn({L(t_lab)}));\n'
    if letters:
        js += (f'tl.set("#ID-big", {{opacity: 1}}, sn({L(t_big)}));\n'
               f'tl.fromTo("#ID-big i", {{opacity: 0, y: 60, filter: "blur(14px)"}}, {{opacity: 1, y: 0, filter: "blur(0px)", duration: .22, ease: "power3.out", stagger: .035}}, sn({L(t_big)}));\n')
    else:
        js += f'tl.fromTo("#ID-big", {{scale: 1.7, opacity: 0, filter: "blur(16px)"}}, {{scale: 1, opacity: 1, filter: "blur(0px)", duration: .28, ease: "back.out(1.8)"}}, sn({L(t_big)}));\n'
    if ul:
        js += f'tl.fromTo("#ID-ul", {{scaleX: 0}}, {{scaleX: 1, duration: .3, ease: "power3.out"}}, sn({L(t_big) + .15}));\n'
    if strike:
        js += (f'tl.fromTo("#ID-st", {{scaleX: 0}}, {{scaleX: 1, duration: .14, ease: "power3.out"}}, sn({L(strike)}));\n'
               f'SHAKE("#ID-big", {L(strike)} + .05, 18);\n'
               f'tl.to("#ID-big", {{color: "{"rgba(0,80,224,.45)" if bg == "white" else "rgba(255,255,255,.45)"}", duration: .2}}, sn({L(strike)} + .2));\n')
    js += f'tl.to("#ID-wrap", {{scale: 1.04, duration: {max(e - s - .22, .1):.3f}, ease: "none"}}, .22);\n' + extra_js  # empuje lento, como el A-roll
    write_scene(root, c, e - s, W, H, CSS, body, js, bg=bg)
    out.append((c, round(s, 3), round(e, 3), [(n, round(s + L(t), 3), v) for n, t, v in sfx]))


END = 0.0  # build.py lo fija


