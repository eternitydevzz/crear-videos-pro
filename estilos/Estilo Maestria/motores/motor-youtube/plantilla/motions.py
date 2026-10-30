"""Motions blancos sobre la cara del presentador, ligados a su palabra (build.py llama a motions(wt, wa, END)).

Siempre a la DERECHA (cx 1620, cy 500): nunca encima del micrófono, que entra por la izquierda.
Cada motion: halo + anillo de luz al entrar, flota mientras está y sale hacia arriba. Entra 0,10 s antes de su palabra (LEAD).
"""

LEAD = 0.10
CSS = """
@font-face{font-family:'RobotoYT';src:url(assets/fonts/Roboto-500-latin.woff2) format('woff2');font-weight:100 900}
.fx{position:absolute;width:0;height:0;z-index:30;opacity:0}
.fx .c{position:absolute;left:0;top:0;transform:translate(-50%,-50%)}
.fx .ring{border-radius:50%;border:3px solid rgba(255,255,255,.45);opacity:0}
.fx .glow{border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.22),rgba(255,255,255,0) 65%)}
"""
SW = 'fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round"'
LABEL = "font-family:Hanken,sans-serif;font-weight:700;color:#fff;letter-spacing:6px;font-size:32px;white-space:nowrap"


def box(fid, t, t_out, cx, cy, size, inner, enter=None, k=1.0):
    """Envoltorio común: halo + anillo de luz + entrada y salida. inner va centrado en (0, 0) y escalado ×k."""
    if k != 1.0:
        inner = f'<div style="position:absolute;left:0;top:0;transform:scale({k})">{inner}</div>'
    html = (f'<div class="fx" id="{fid}" style="left:{cx}px;top:{cy}px">'
            f'<div class="c glow" id="{fid}-gl" style="width:{size * 2:.0f}px;height:{size * 2:.0f}px;opacity:0"></div>'
            f'<div class="c ring" id="{fid}-rg" style="width:{size}px;height:{size}px"></div>{inner}</div>')
    t0 = t - LEAD
    js = (f'tl.fromTo("#{fid}", {enter or "{opacity: 0, scale: .35, y: 50}"}, {{opacity: 1, scale: 1, y: 0, rotationX: 0, rotationY: 0, duration: .5, ease: "back.out(1.7)"}}, {t0:.3f});\n'
          f'tl.fromTo("#{fid}-rg", {{scale: .3, opacity: 1}}, {{scale: 1.9, opacity: 0, duration: .8, ease: "power2.out"}}, {t0 + .1:.3f});\n'
          f'tl.fromTo("#{fid}-gl", {{opacity: 0}}, {{opacity: .4, duration: .5, ease: "power2.out"}}, {t0 + .15:.3f});\n'
          f'tl.to("#{fid}", {{opacity: 0, scale: .8, y: -30, duration: .3, ease: "power2.in"}}, {t_out - .3:.3f});\n')
    return html, js, t0


def float_(sel, t0, t_out, amp=10):
    d = (t_out - t0 - .9) / 2  # termina antes de la salida
    return f'tl.to("{sel}", {{y: -{amp}, duration: {d:.3f}, ease: "sine.inOut", yoyo: true, repeat: 1}}, {t0 + .6:.3f});\n' if d > .2 else ""


def chip(fid, t, t_out, cx, cy):
    """Chip de IA que se dibuja trazo a trazo y se enciende con «AI»."""
    pins = ""
    for k in range(4):
        o = 70 + k * 20
        pins += (f'<path pathLength="1" class="{fid}-p" d="M{o} 40 V10" {SW} stroke-width="7"/><path pathLength="1" class="{fid}-p" d="M{o} 160 V190" {SW} stroke-width="7"/>'
                 f'<path pathLength="1" class="{fid}-p" d="M40 {o} H10" {SW} stroke-width="7"/><path pathLength="1" class="{fid}-p" d="M160 {o} H190" {SW} stroke-width="7"/>')
    svg = (f'<svg class="c" viewBox="0 0 200 200" style="width:230px;height:230px;overflow:visible">'
           f'<rect id="{fid}-b" pathLength="1" x="40" y="40" width="120" height="120" rx="20" {SW} stroke-width="8" style="stroke-dasharray:1;stroke-dashoffset:1"/>'
           f'{pins.replace("/>", " style=\"stroke-dasharray:1;stroke-dashoffset:1\"/>")}'
           f'<text id="{fid}-t" x="100" y="122" text-anchor="middle" style="font-family:Hanken,sans-serif;font-weight:700;font-size:58px;fill:#fff;opacity:0">AI</text></svg>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 250, svg)
    js += (f'tl.fromTo("#{fid}-b", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: .55, ease: "power2.inOut"}}, {t0 + .05:.3f});\n'
           f'tl.fromTo(".{fid}-p", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: .22, ease: "power2.out", stagger: .03}}, {t0 + .45:.3f});\n'
           f'tl.fromTo("#{fid}-t", {{opacity: 0, scale: .4, transformOrigin: "100px 100px"}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(2.5)"}}, {t0 + .75:.3f});\n'
           f'tl.to("#{fid}-gl", {{opacity: .15, duration: .25, ease: "sine.inOut", yoyo: true, repeat: 3}}, {t0 + 1.0:.3f});\n' + float_(f"#{fid}", t0, t_out))
    return html, js


def speed(fid, t, t_out, cx, cy):
    """Flecha que sale disparada en diagonal con líneas de velocidad detrás."""
    lines = "".join(f'<div class="c" id="{fid}-l{i}" style="left:{-60 - (i % 3) * 30}px;top:{-70 + i * 28}px;width:{120 + (i * 37) % 90}px;height:7px;border-radius:4px;'
                    f'background:linear-gradient(90deg,rgba(255,255,255,0),#fff);opacity:0"></div>' for i in range(6))
    arrow = (f'<svg class="c" id="{fid}-a" viewBox="0 0 120 120" style="left:30px;width:150px;height:150px">'
             f'<path d="M15 60 H95 M65 28 L98 60 L65 92" {SW} stroke-width="16"/></svg>')
    inner = f'<div class="c" style="transform:translate(-50%,-50%) rotate(-30deg)"><div style="position:relative">{lines}{arrow}</div></div>'
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, inner, k=1.5)
    js += f'tl.fromTo("#{fid}-a", {{x: -260, opacity: 0, scaleX: 1.6}}, {{x: 0, opacity: 1, scaleX: 1, duration: .45, ease: "expo.out"}}, {t0:.3f});\n'
    n = int((t_out - t0 - .4) / .5)
    for i in range(6):
        js += f'tl.fromTo("#{fid}-l{i}", {{x: -160, opacity: 0}}, {{x: 120, opacity: .9, duration: .5, ease: "power1.in", repeat: {n}}}, {t0 + i * .07:.3f});\n'
    js += f'tl.to("#{fid}-a", {{x: 14, duration: .25, ease: "sine.inOut", yoyo: true, repeat: {max(1, int((t_out - t0 - .6) / .25) | 1)}}}, {t0 + .5:.3f});\n'
    return html, js


def people(fid, t, t_out, cx, cy, label="COMUNIDAD"):
    """Tres avatares blancos que entran en cascada (la comunidad)."""
    av = lambda x, y, s, i: (f'<svg class="c" id="{fid}-a{i}" viewBox="0 0 24 24" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:0">'
                             f'<circle cx="12" cy="8" r="4" fill="#fff"/><path d="M4 21c.6-4.6 3.8-7 8-7s7.4 2.4 8 7z" fill="#fff"/></svg>')
    inner = av(-110, 20, 120, 0) + av(110, 20, 120, 1) + av(0, -10, 160, 2) + f'<div class="c" style="top:185px;{LABEL}">{label}</div>'
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, inner)
    js += "".join(f'tl.fromTo("#{fid}-a{i}", {{opacity: 0, y: 40, scale: .5}}, {{opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2.2)"}}, {t0 + .1 + i * .12:.3f});\n' for i in range(3))
    return html, js + float_(f"#{fid}", t0, t_out)


def flag(fid, t, t_out, cx, cy):
    """Bandera de EE. UU. en blanco: las franjas se dibujan, las estrellas aparecen y ondea."""
    W_, H_ = 300, 180
    stripes = "".join(f'<div class="{fid}-st" style="position:absolute;left:0;top:{i * H_ / 7:.1f}px;width:100%;height:{H_ / 7:.1f}px;background:#fff;transform-origin:0 50%"></div>'
                      for i in range(0, 7, 2))
    stars = "".join(f'<div class="{fid}-sr" style="position:absolute;left:{16 + c * 24 + (r % 2) * 12}px;top:{12 + r * 18}px;width:7px;height:7px;border-radius:50%;background:#0050E0"></div>'
                    for r in range(5) for c in range(5 - (r % 2)))
    inner = (f'<div class="c" style="width:{W_}px;height:{H_}px"><div id="{fid}-f" style="position:relative;width:{W_}px;height:{H_}px;border:4px solid #fff;border-radius:8px;overflow:hidden">'
             f'{stripes}<div id="{fid}-cn" style="position:absolute;left:0;top:0;width:{W_ * .42:.0f}px;height:{H_ * 4 / 7:.0f}px;background:#fff">{stars}</div></div></div>'
             f'<div class="c" id="{fid}-lb" style="top:{H_ / 2 + 50:.0f}px;{LABEL};opacity:0">ESTADOS UNIDOS</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 320, inner)
    js += (f'tl.fromTo(".{fid}-st", {{scaleX: 0}}, {{scaleX: 1, duration: .35, ease: "power3.out", stagger: .06}}, {t0 + .1:.3f});\n'
           f'tl.fromTo("#{fid}-cn", {{scale: 0, transformOrigin: "0 0"}}, {{scale: 1, duration: .3, ease: "back.out(2)"}}, {t0 + .3:.3f});\n'
           f'tl.fromTo(".{fid}-sr", {{scale: 0}}, {{scale: 1, duration: .15, ease: "back.out(3)", stagger: .015}}, {t0 + .45:.3f});\n'
           f'tl.fromTo("#{fid}-lb", {{opacity: 0, y: 16}}, {{opacity: 1, y: 0, duration: .3, ease: "power3.out"}}, {t0 + .4:.3f});\n' + float_(f"#{fid}", t0, t_out))
    return html, js


def bubble(fid, t, t_out, cx, cy, text):
    """Bocadillo de pregunta del espectador (cristal claro, texto oscuro)."""
    inner = (f'<div class="c" id="{fid}-b" style="padding:26px 40px;border-radius:40px 40px 40px 8px;background:rgba(255,255,255,.92);box-shadow:0 24px 60px rgba(0,10,40,.35);'
             f'font-family:Hanken,sans-serif;font-weight:700;font-size:52px;color:#101010;white-space:nowrap">{text}</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, inner, "{opacity: 0, scale: .5, y: 60, rotation: -6}")
    return html, js + float_(f"#{fid}", t0, t_out, 8)


def bulb(fid, t, t_out, cx, cy, label):
    """Bombilla blanca que se enciende (trucos / ideas)."""
    svg = (f'<svg class="c" viewBox="0 0 200 220" style="width:200px;height:220px;overflow:visible"><g id="{fid}-g" opacity=".35">'
           f'<path d="M100 20a62 62 0 0 0-36 112c8 6 12 14 12 22v8h48v-8c0-8 4-16 12-22A62 62 0 0 0 100 20z" fill="#fff"/></g>'
           f'<path d="M100 20a62 62 0 0 0-36 112c8 6 12 14 12 22v8h48v-8c0-8 4-16 12-22A62 62 0 0 0 100 20z" {SW} stroke-width="8"/>'
           f'<path d="M78 182h44M84 200h32" {SW} stroke-width="8"/></svg>'
           f'<div class="c" style="top:150px;{LABEL}">{label}</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, svg)
    js += (f'tl.to("#{fid}-g", {{opacity: 1, duration: .15, yoyo: true, repeat: 3}}, {t0 + .35:.3f});\n'
           f'tl.to("#{fid}-gl", {{opacity: .9, duration: .3}}, {t0 + .6:.3f});\n' + float_(f"#{fid}", t0, t_out))
    return html, js


def flags(fid, t, t_out, cx, cy, items, label):
    """Fila de banderas en círculos blancos que saltan una a una."""
    n = len(items)
    inner = "".join(f'<div class="c" id="{fid}-f{i}" style="left:{(i - (n - 1) / 2) * 104:.0f}px;width:92px;height:92px;border-radius:50%;background:#fff;'
                    f'display:flex;align-items:center;justify-content:center;font-size:54px;box-shadow:0 14px 34px rgba(0,10,40,.35);opacity:0">{f}</div>' for i, f in enumerate(items))
    inner += f'<div class="c" style="top:90px;{LABEL}">{label}</div>'
    html, js, t0 = box(fid, t, t_out, cx, cy, 360, inner)
    js += "".join(f'tl.fromTo("#{fid}-f{i}", {{opacity: 0, scale: 0, y: 30}}, {{opacity: 1, scale: 1, y: 0, duration: .3, ease: "back.out(2.6)"}}, {t0 + .1 + i * .08:.3f});\n' for i in range(n))
    return html, js + float_(f"#{fid}", t0, t_out, 8)


import json as _json
from pathlib import Path as _Path

_W = _json.loads((_Path(__file__).parent / "../trabajo/palabras.json").read_text(encoding="utf-8"))
_T = [x["w"] for x in _W]


def ph(text, n=1):
    """Tiempo de la primera palabra de la n-ésima aparición EXACTA de la frase."""
    q, k = text.split(), 0
    for i in range(len(_T) - len(q) + 1):
        if _T[i:i + len(q)] == q:
            k += 1
            if k == n:
                return _W[i]["s"]
    raise SystemExit(f"no encuentro «{text}» #{n}")


def panel(fid, t, t_out, cx, cy, title, items, strike=None, foot=None, big=None):
    """Panel de cristal claro a la DERECHA de la cara: título mono + filas (emoji, texto, t) que entran en su palabra.
    strike = (t, texto) tacha las filas y enseña un pie rojo; foot = (t, texto, color) pie final; big = texto grande bajo el título."""
    rows = "".join(f'<div class="pr" id="{fid}-r{i}" style="display:flex;align-items:center;gap:16px;font-size:38px;font-weight:700;color:#101010;opacity:0;position:relative">'
                   f'<span style="font-size:42px">{em}</span><span style="position:relative">{tx}<i id="{fid}-s{i}" style="position:absolute;left:-6px;right:-6px;top:52%;height:5px;margin-top:-2px;border-radius:3px;background:#E5484D;transform:scaleX(0);transform-origin:0 50%"></i></span></div>' for i, (em, tx, _) in enumerate(items))
    inner = (f'<div class="c" id="{fid}-p" style="width:560px;padding:34px 40px;border-radius:40px;background:rgba(255,255,255,.93);box-shadow:0 30px 70px rgba(0,10,40,.35);'
             f'font-family:Hanken,sans-serif;display:flex;flex-direction:column;gap:20px">'
             f'<div style="font-family:Spline,monospace;font-size:26px;letter-spacing:6px;color:#0050E0">{title}</div>'
             + (f'<div style="font-size:64px;font-weight:800;letter-spacing:-2px;line-height:1;color:#101010">{big}</div>' if big else "")
             + f'<div style="position:relative;display:flex;flex-direction:column;gap:16px">{rows}'
             + '</div>'
             + (f'<div id="{fid}-sf" style="font-size:40px;font-weight:800;color:#E5484D;opacity:0">{strike[1]}</div>' if strike else "")
             + (f'<div id="{fid}-ft" style="font-size:40px;font-weight:800;color:{foot[2]};opacity:0">{foot[1]}</div>' if foot else "")
             + '</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 420, inner, "{opacity: 0, scale: .6, y: 60}")
    js += "".join(f'tl.fromTo("#{fid}-r{i}", {{opacity: 0, x: 40}}, {{opacity: 1, x: 0, duration: .3, ease: "power3.out"}}, {max(ti - LEAD, t0 + .2):.3f});\n' for i, (_, _, ti) in enumerate(items))
    if strike:
        js += "".join(f'tl.fromTo("#{fid}-s{i}", {{scaleX: 0}}, {{scaleX: 1, duration: .18, ease: "power3.out"}}, {strike[0] - LEAD + i * .08:.3f});\n' for i in range(len(items)))
        js += (f'tl.to("#{fid}-r0, #{fid}-r1, #{fid}-r2, #{fid}-r3", {{opacity: .45, duration: .2}}, {strike[0] - LEAD + .25:.3f});\n'
               f'tl.fromTo("#{fid}-sf", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: .3, ease: "back.out(2)"}}, {strike[0] - LEAD + .15:.3f});\n')
    if foot:
        js += f'tl.fromTo("#{fid}-ft", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: .3, ease: "back.out(2)"}}, {foot[0] - LEAD:.3f});\n'
    return html, js + float_(f"#{fid}", t0, t_out, 6)


def subs(fid, t, t_out, cx, cy):
    """Banner de suscripción estilo YouTube claro (ref. videoeffects «Subscribe Banner 5 Light», hecho desde cero):
    foto → se abre el banner → «Suscribirse» se pulsa → «Suscrito» → entra la campana y el botón se aparta. Dura t … t_out (3 s).
    Proporción de la referencia medida: 590 × 119 (4,96 : 1); aquí 612 × 124."""
    W, W2, H, P, B = 534, 569, 124, 18, 56   # ancho con «Suscribirse» / con «Suscrito»+campana (16 px tras el ✔, medido), alto, margen, botón
    bell = ('<svg viewBox="0 0 24 24" style="width:26px;height:26px"><path d="M12 22a2.4 2.4 0 0 0 2.4-2.4H9.6A2.4 2.4 0 0 0 12 22zm7-5.2V11a7 7 0 0 0-5.6-6.9V3.4a1.4 1.4 0 0 0-2.8 0v.7A7 7 0 0 0 5 11v5.8L3 18.6v1h18v-1z" fill="currentColor"/></svg>')
    btn = f"position:absolute;top:{(H - B) / 2:.0f}px;height:{B}px"
    html = (f'<div class="fx" id="{fid}" style="left:{cx}px;top:{cy}px;z-index:31">'
            f'<div class="c" id="{fid}-bn" style="width:{W}px;height:{H}px;border-radius:24px;background:#fff;box-shadow:0 24px 60px rgba(0,10,40,.35);overflow:hidden">'
            f'<div id="{fid}-tx" style="position:absolute;left:124px;top:33px;font-family:RobotoYT,Roboto,sans-serif;white-space:nowrap;opacity:0">'
            f'<div style="font-weight:700;font-size:26px;color:#0f0f0f;display:flex;align-items:center;gap:7px">@TuCanal'
            f'<svg viewBox="0 0 24 24" style="width:20px;height:20px"><circle cx="12" cy="12" r="10" fill="#8a8a8a"/><path d="M7.5 12.2l3 3 6-6.2" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
            f'<div style="font-weight:400;font-size:21px;color:#606060;margin-top:3px">10K suscriptores</div></div>'
            f'<div id="{fid}-sb" style="{btn};right:{P}px;padding:0 20px;border-radius:{B / 2:.0f}px;background:#0f0f0f;color:#fff;'
            f'font-family:RobotoYT,Roboto,sans-serif;font-weight:500;font-size:21px;display:flex;align-items:center;opacity:0">'
            f'<span id="{fid}-s1">Suscribirse</span><span id="{fid}-s2" style="display:none">Suscrito</span></div>'
            f'<div id="{fid}-bl" style="{btn};right:{P}px;width:{B}px;border-radius:50%;background:#0f0f0f;color:#fff;'
            f'display:flex;align-items:center;justify-content:center;opacity:0">{bell}</div></div>'
            f'<img class="c" id="{fid}-av" src="assets/img/avatar.jpg" style="width:92px;height:92px;border-radius:50%;object-fit:cover;object-position:50% 30%"></div>')
    t0, L = t - LEAD, -W / 2 + P + 46   # L = centro de la foto ya abierta (respecto al centro del banner)
    js = (f'tl.set("#{fid}", {{opacity: 1}}, {t0:.3f});\n'
          f'tl.fromTo("#{fid}-av", {{scale: 0}}, {{scale: 1, duration: .3, ease: "back.out(2)"}}, {t0:.3f});\n'
          f'tl.fromTo("#{fid}-bn", {{width: {H}, scale: 0}}, {{scale: 1, duration: .25, ease: "back.out(2)"}}, {t0 + .05:.3f});\n'
          f'tl.to("#{fid}-bn", {{width: {W}, duration: .4, ease: "power3.inOut"}}, {t0 + .3:.3f});\n'
          f'tl.to("#{fid}-av", {{x: {L:.0f}, duration: .4, ease: "power3.inOut"}}, {t0 + .3:.3f});\n'
          f'tl.fromTo("#{fid}-tx", {{opacity: 0, x: -14}}, {{opacity: 1, x: 0, duration: .3, ease: "power2.out"}}, {t0 + .55:.3f});\n'
          f'tl.fromTo("#{fid}-sb", {{opacity: 0, scale: .7}}, {{opacity: 1, scale: 1, duration: .25, ease: "back.out(2)"}}, {t0 + .6:.3f});\n'
          f'tl.to("#{fid}-sb", {{scale: .9, duration: .1, yoyo: true, repeat: 1}}, {t0 + 1.2:.3f});\n'
          f'tl.set("#{fid}-s1", {{display: "none"}}, {t0 + 1.3:.3f});\ntl.set("#{fid}-s2", {{display: "inline"}}, {t0 + 1.3:.3f});\n'
          f'tl.to("#{fid}-sb", {{background: "#f2f2f2", color: "#0f0f0f", duration: .15}}, {t0 + 1.3:.3f});\n'
          f'tl.to("#{fid}-bn", {{width: {W2}, x: {(W2 - W) / 2:.1f}, duration: .3, ease: "power3.out"}}, {t0 + 1.5:.3f});\n'   # crece solo hacia la derecha
          f'tl.to("#{fid}-sb", {{right: {P + B + 10}, duration: .3, ease: "power3.out"}}, {t0 + 1.5:.3f});\n'
          f'tl.fromTo("#{fid}-bl", {{opacity: 0, scale: .4}}, {{opacity: 1, scale: 1, duration: .25, ease: "back.out(2.4)"}}, {t0 + 1.6:.3f});\n'
          f'tl.to("#{fid}-bl", {{scale: .88, duration: .1, yoyo: true, repeat: 1}}, {t0 + 2.0:.3f});\n'
          f'tl.to("#{fid}-bl", {{background: "#f2f2f2", color: "#0f0f0f", duration: .15}}, {t0 + 2.1:.3f});\n'
          f'tl.to("#{fid}", {{opacity: 0, scale: .9, y: -20, duration: .3, ease: "power2.in"}}, {t_out - .3:.3f});\n')
    return html, js


def motions(wt, wa, END):
    """Los motions de este vídeo: (pieza, [(sfx, t, vol)]). Siempre a la DERECHA (cx 1500–1620, cy ≈ 500) · ficha §4.
    Ejemplos:
        (flag("m01-usa", wt("Unidos"), wt("Y", 2) - .1, 1560, 520), [("pop.mp3", wt("Unidos") - LEAD, 0.24)]),
        (subs("m02-subs", wt("trucos") + .1, wt("trucos") + .1 - LEAD + 3, 1568, 500),            # banner de suscripción, 3 s
         [("pop.mp3", wt("trucos"), 0.24), ("mouse-click.mp3", wt("trucos") + 1.2, 0.3), ("mouse-click.mp3", wt("trucos") + 2.0, 0.3)]),
    """
    items = []
    return CSS, "\n".join(h for (h, _), _ in items), "".join(j for (_, j), _ in items), [x for _, sf in items for x in sf]
