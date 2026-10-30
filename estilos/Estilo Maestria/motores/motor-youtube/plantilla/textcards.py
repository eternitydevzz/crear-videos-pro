"""Pantallas azules de texto grande (ids «t..», sin subtítulos encima): degradado #1157df → #003fab, texto blanco grueso.
card(): etiqueta mono opcional + frase gigante que entra con desenfoque; opcional, un tachado blanco que se dibuja en su palabra.
"""
from scenes import LEAD, PRE, snaps, tmap, write_scene

CSS = f"""
#ID .box{{position:absolute;inset:0;justify-content:center;display:flex;flex-direction:column;align-items:center;gap:26px}}
#ID .lab{{font-family:'Spline',monospace;font-weight:500;font-size:46px;letter-spacing:14px;text-transform:uppercase;opacity:0}}
#ID .big{{font-weight:700;font-size:220px;line-height:.95;letter-spacing:-6px;text-transform:uppercase;white-space:nowrap;position:relative;opacity:0}}
#ID .strike{{position:absolute;left:-20px;right:-20px;top:52%;height:19.8px;margin-top:-9.9px;border-radius:9.9px;background:#fff;transform-origin:0 50%}}
#ID .then{{font-weight:700;font-size:120px;line-height:1;letter-spacing:-3px;color:#fff;text-transform:uppercase;white-space:nowrap;margin-top:16px;opacity:0;text-shadow:0 10px 50px rgba(0,20,80,.35)}}
#ID .b .lab{{color:rgba(255,255,255,.8)}} #ID .b .big{{color:#fff;text-shadow:0 10px 50px rgba(0,20,80,.35)}}
"""


def card(root, W, H, out, c, s, e, label, big, t_lab, t_big, strike=None, extra_js="", sfx=(), size=None, then=None):
    """Etiqueta + palabra gigante. Tiempos globales; se pasan a locales con LEAD."""
    s, e = snaps(s, e)
    L = lambda t: 0.0 if t is None else round(max(t - s - LEAD, 0), 3)  # None = al entrar la pantalla
    fs = size or min(220, int(1650 / (0.64 * len(big))))  # que la palabra gigante quepa en una línea (≤ ~1650 px)
    body = (f'<div class="box b">'
            + (f'<div class="lab" id="ID-lab">{label}</div>' if label else "")
            + f'<div class="big" id="ID-big" style="font-size:{fs}px;letter-spacing:{-fs / 36:.1f}px">{big}' + ('<span class="strike" id="ID-st"></span>' if strike else "") + "</div>"
            + (f'<div class="then" id="ID-th">{then[0]}</div>' if then else "") + "</div>")
    js = ""
    if label:
        js += f'tl.fromTo("#ID-lab", {{opacity: 0, y: 30, "--b": 10}}, {{opacity: 1, y: 0, "--b": 0, duration: .25, ease: "power3.out"}}, sn({L(t_lab)}));\n'
    js += f'tl.fromTo("#ID-big", {{scale: 1.7, opacity: 0, filter: "blur(16px)"}}, {{scale: 1, opacity: 1, filter: "blur(0px)", duration: .28, ease: "back.out(1.8)"}}, sn({L(t_big)}));\n'
    if strike:
        js += (f'tl.fromTo("#ID-st", {{scaleX: 0}}, {{scaleX: 1, duration: .14, ease: "power3.out"}}, sn({L(strike)}));\n'
               f'SHAKE("#ID-big", {L(strike)} + .05, 18);\n'
               f'tl.to("#ID-big", {{color: "rgba(255,255,255,.45)", duration: .2}}, sn({L(strike)} + .2));\n')
    if then:  # segunda línea que entra después (p. ej. tras el tachado)
        js += f'tl.fromTo("#ID-th", {{opacity: 0, y: 40, "--b": 12}}, {{opacity: 1, y: 0, "--b": 0, duration: .3, ease: "power3.out"}}, sn({L(then[1])}));\n'
    js += f'tl.to("#ID-wrap", {{scale: 1.04, duration: {max(e - s - .22, .1):.3f}, ease: "none"}}, .22);\n' + extra_js  # empuje lento, como el A-roll
    write_scene(root, c, e - s, W, H, CSS, body, js, bg="blue")
    out.append((c, round(s, 3), round(e, 3), [(n, round(s + L(t), 3), v) for n, t, v in sfx]))


def text_cards(root, wt, wa, W, H, out):
    """Las pantallas azules de este vídeo (títulos de bloque y preguntas) · ficha §5.
    Ejemplo:
        A("t03-dificil", wt("Lo") - PRE, wt("porque") - PRE, "Lo difícil es", "Venderlo", 0.0, wt("venderlo,"), size=200,
          sfx=[("whoosh.m4a", None, 0.26), ("impacto.m4a", wt("venderlo,"), 0.08)])   # (de YouTube 2, minuto 10)
    """
    A = lambda c, s, e, *a, **k: card(root, W, H, out, c, s, e, *a, **k)
