"""Motions blancos a los lados del presentador (estilobasico.md §5), ligados a su palabra. build.py llama a motions(wt, wa, END).

Izquierda cx ≈ 300 y derecha cx ≈ 1620, por encima de los subtítulos (y < 760). Se alterna el lado.
Las piezas aprobadas (box, coin, chip, big, sparks) vienen de fxlib.py, copia de «Bienvenida comunidad/fx.py».
"""
import re
from pathlib import Path

from fxlib import CSS, LABEL, LEAD, SW, big, box, chip, coin, flag, float_, logo, rain, sparks, speed

RED = "#E5484D"
SL = Path(__file__).parent / "assets/descargas"


def clock(fid, t, t_out, cx, cy):
    """Reloj blanco cuyas agujas giran rápido (ahorrar tiempo)."""
    ticks = "".join(f'<path d="M100 18 V32" {SW} stroke-width="6" transform="rotate({k * 30} 100 100)"/>' for k in range(12))
    svg = (f'<svg class="c" viewBox="0 0 200 200" style="width:230px;height:230px;overflow:visible"><circle cx="100" cy="100" r="88" {SW} stroke-width="10"/>{ticks}'
           f'<path id="{fid}-h" d="M100 100 V55" {SW} stroke-width="11"/><path id="{fid}-m" d="M100 100 V30" {SW} stroke-width="7"/>'
           f'<circle cx="100" cy="100" r="9" fill="#0050E0"/></svg>'
           f'<div class="c" style="top:160px;{LABEL}">AHORRA TIEMPO</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 260, svg)
    js += (f'tl.fromTo("#{fid}-m", {{rotation: 0, svgOrigin: "100 100"}}, {{rotation: 1080, svgOrigin: "100 100", duration: {t_out - t0 - .3:.3f}, ease: "power2.out"}}, {t0:.3f});\n'
           f'tl.fromTo("#{fid}-h", {{rotation: 0, svgOrigin: "100 100"}}, {{rotation: 90, svgOrigin: "100 100", duration: {t_out - t0 - .3:.3f}, ease: "power2.out"}}, {t0:.3f});\n'
           + float_(f"#{fid}", t0, t_out))
    return html, js


def donut(fid, t, t_out, cx, cy, pct, label):
    """Anillo blanco que se llena solo hasta pct % con la cifra en medio."""
    svg = (f'<svg class="c" viewBox="0 0 200 200" style="width:260px;height:260px;overflow:visible;transform:translate(-50%,-50%) rotate(-90deg)">'
           f'<circle cx="100" cy="100" r="80" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="22"/>'
           f'<circle id="{fid}-a" pathLength="100" cx="100" cy="100" r="80" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round" '
           f'style="stroke-dasharray:100;stroke-dashoffset:100"/></svg>'
           f'<div class="c num" id="{fid}-n" style="font-size:84px">0%</div>'
           f'<div class="c" style="top:175px;{LABEL};font-size:28px">{label}</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, svg)
    js += (f'tl.fromTo("#{fid}-a", {{strokeDashoffset: 100}}, {{strokeDashoffset: {100 - pct}, duration: .7, ease: "power2.out"}}, {t0 + .15:.3f});\n'
           f'(() => {{ const o = {{v: 0}}, el = document.getElementById("{fid}-n");\n'
           f'  tl.fromTo(o, {{v: 0}}, {{v: {pct}, duration: .7, ease: "power2.out", onUpdate: () => {{ el.textContent = Math.round(o.v) + "%"; }} }}, {t0 + .15:.3f}); }})();\n'
           f'tl.to("#{fid}-n", {{scale: 1.18, duration: .12, ease: "power2.out", yoyo: true, repeat: 1}}, {t0 + .85:.3f});\n' + float_(f"#{fid}", t0, t_out, 8))
    return html, js


def loss(fid, t, t_out, cx, cy):
    """«−$» de golpe con flecha roja hacia abajo y billetes que caen (pierden miles de dólares)."""
    bills = "".join(f'<div class="c" id="{fid}-b{i}" style="left:{x}px;top:-40px;width:90px;height:48px;border:4px solid #fff;border-radius:8px;'
                    f'background:rgba(255,255,255,.12);opacity:0"><div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);'
                    f'font-family:Hanken,sans-serif;font-weight:700;font-size:28px;color:#fff">$</div></div>' for i, x in enumerate([-120, 10, 125]))
    inner = (bills + f'<div class="c num" id="{fid}-n" style="font-size:200px;line-height:1">−$</div>'
             f'<svg class="c" id="{fid}-ar" viewBox="0 0 60 80" style="left:150px;top:-30px;width:70px;height:94px;opacity:0">'
             f'<path d="M30 6 V66 M8 46 L30 70 L52 46" fill="none" stroke="{RED}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>'
             f'<div class="c" style="top:140px;{LABEL}">CADA DÍA</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 280, inner, "{opacity: 0}")
    js += (f'tl.fromTo("#{fid}-n", {{scale: 2.6, opacity: 0}}, {{scale: 1, opacity: 1, duration: .3, ease: "back.out(1.8)"}}, {t0:.3f});\n'
           + "".join(f'tl.to("#{fid}", {{x: {x}, duration: .05, ease: "none"}}, {t0 + .28 + i * .05:.3f});\n' for i, x in enumerate([14, -12, 8, 0]))
           + f'tl.fromTo("#{fid}-ar", {{opacity: 0, y: -40}}, {{opacity: 1, y: 0, duration: .35, ease: "back.out(2)"}}, {t0 + .35:.3f});\n'
           + f'tl.to("#{fid}-ar", {{y: 14, duration: .3, ease: "sine.inOut", yoyo: true, repeat: {max(1, int((t_out - t0 - 1) / .3) | 1)}}}, {t0 + .7:.3f});\n'
           + "".join(f'tl.fromTo("#{fid}-b{i}", {{y: -160, opacity: 0, rotation: {(-1) ** i * 20}}}, {{y: 260, opacity: .9, rotation: {(-1) ** i * -25}, duration: 1.1, ease: "power1.in"}}, {t0 + .5 + i * .18:.3f});\n'
                     f'tl.to("#{fid}-b{i}", {{opacity: 0, duration: .25}}, {t0 + 1.6 + i * .18:.3f});\n' for i in range(3)))
    return html, js


def counter(fid, t, t_out, cx, cy, target, pre, label):
    """Cifra que cuenta de 0 a target con destellos al llegar."""
    k_html, k_js = sparks(fid, t + .9, [(-170, -110), (170, -100), (180, 60)])
    inner = (f'<div class="c num" id="{fid}-n" style="font-size:120px;line-height:1">{pre}0</div>'
             f'<div class="c" style="top:100px;{LABEL}">{label}</div>' + k_html)
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, inner, "{opacity: 0, scale: .5, y: 40}")
    js += (f'(() => {{ const o = {{v: 0}}, el = document.getElementById("{fid}-n");\n'
           f'  tl.fromTo(o, {{v: 0}}, {{v: {target}, duration: .9, ease: "power2.out", onUpdate: () => {{ el.textContent = "{pre}" + Math.round(o.v).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, "."); }} }}, {t0 + .1:.3f}); }})();\n'
           f'tl.to("#{fid}-n", {{scale: 1.15, duration: .12, ease: "power2.out", yoyo: true, repeat: 1}}, {t0 + 1.0:.3f});\n' + k_js)
    return html, js


def gears(fid, t, t_out, cx, cy):
    """Dos engranajes blancos que giran engranados (automatizan)."""
    def gear(r, teeth):
        tooth = "".join(f'<rect x="-9" y="{-r - 16}" width="18" height="22" rx="4" fill="#fff" transform="rotate({k * 360 / teeth})"/>' for k in range(teeth))
        return f'{tooth}<circle r="{r}" fill="#fff"/><circle r="{r * .38:.0f}" fill="#0050E0"/>'
    svg = (f'<svg class="c" viewBox="-160 -120 320 240" style="width:330px;height:250px;overflow:visible">'
           f'<g transform="translate(-55 0)"><g id="{fid}-g1">{gear(62, 10)}</g></g>'
           f'<g transform="translate(70 -55)"><g id="{fid}-g2">{gear(40, 7)}</g></g></svg>'
           f'<div class="c" style="top:150px;{LABEL}">AUTOMATIZA</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, svg)
    d = t_out - t0
    js += (f'tl.fromTo("#{fid}-g1", {{rotation: 0, svgOrigin: "0 0"}}, {{rotation: {int(d * 120)}, svgOrigin: "0 0", duration: {d:.3f}, ease: "none"}}, {t0:.3f});\n'
           f'tl.fromTo("#{fid}-g2", {{rotation: 0, svgOrigin: "0 0"}}, {{rotation: {-int(d * 120 * 10 / 7)}, svgOrigin: "0 0", duration: {d:.3f}, ease: "none"}}, {t0:.3f});\n'
           + float_(f"#{fid}", t0, t_out))
    return html, js


def portrait(fid, t, t_out, cx, cy, img, label):
    """Retrato en marco blanco que entra girando 180° en 3D."""
    inner = (f'<div class="c p3" style="width:250px;height:310px"><div class="s3" id="{fid}-s" style="width:250px;height:310px;border:8px solid #fff;border-radius:22px;overflow:hidden;'
             f'box-shadow:0 20px 60px rgba(0,0,0,.35);backface-visibility:hidden"><img src="{img}" style="width:100%;height:100%;object-fit:cover;display:block"></div></div>'
             f'<div class="c" style="top:200px;{LABEL};font-size:28px">{label}</div>')
    k_html, k_js = sparks(fid, t + .4, [(-150, -150), (150, -130), (160, 110)])
    html, js, t0 = box(fid, t, t_out, cx, cy, 330, inner + k_html, "{opacity: 0, scale: .5}")
    js += (f'tl.fromTo("#{fid}-s", {{rotationY: -180}}, {{rotationY: 0, duration: .8, ease: "power3.out"}}, {t0:.3f});\n' + k_js
           + f'tl.to("#{fid}-s", {{rotationY: 12, duration: {(t_out - t0 - 1.1) / 2:.3f}, ease: "sine.inOut", yoyo: true, repeat: 1}}, {t0 + .8:.3f});\n')
    return html, js


def checklist(fid, t, t_out, cx, cy, items):
    """Lista blanca: cada fila se marca ✓ con su palabra [(texto, t)]."""
    rows = ""
    for i, (txt, _) in enumerate(items):
        rows += (f'<div class="c" id="{fid}-r{i}" style="left:0;top:{(i - 1) * 96}px;width:460px;display:flex;align-items:center;gap:22px;opacity:0;transform:translate(-50%,-50%)">'
                 f'<svg viewBox="0 0 100 100" width="70" height="70" style="flex:none"><circle cx="50" cy="50" r="44" fill="none" stroke="#fff" stroke-width="7"/>'
                 f'<circle id="{fid}-o{i}" cx="50" cy="50" r="44" fill="#fff" style="opacity:0"/>'
                 f'<path id="{fid}-k{i}" pathLength="1" d="M28 52 L44 67 L73 36" fill="none" stroke="#0050E0" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:1;stroke-dashoffset:1"/></svg>'
                 f'<span style="{LABEL};font-size:40px;letter-spacing:2px">{txt}</span></div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 360, rows, "{opacity: 0, scale: .6}")
    for i, (_, ti) in enumerate(items):
        js += (f'tl.fromTo("#{fid}-r{i}", {{opacity: 0, x: -40}}, {{opacity: 1, x: 0, duration: .3, ease: "power3.out"}}, {t0 + i * .1:.3f});\n'
               f'tl.to("#{fid}-o{i}", {{opacity: 1, duration: .08}}, {ti - LEAD:.3f});\n'
               f'tl.to("#{fid}-k{i}", {{strokeDashoffset: 0, duration: .22, ease: "power2.out"}}, {ti - LEAD:.3f});\n'
               f'tl.to("#{fid}-r{i}", {{scale: 1.08, duration: .1, yoyo: true, repeat: 1}}, {ti - LEAD:.3f});\n')
    return html, js + float_(f"#{fid}", t0, t_out, 8)


def tiktok(fid, t, t_out, cx, cy):
    """Logo de TikTok en blanco que se apaga a gris con «PERDER EL TIEMPO»."""
    d = re.search(r'<path d="([^"]+)"', (SL / "tiktok.svg").read_text()).group(1)
    inner = (f'<svg class="c" id="{fid}-l" viewBox="0 0 24 24" style="width:200px;height:200px"><path d="{d}" fill="#fff"/></svg>'
             f'<div class="c" style="top:150px;{LABEL}">TIKTOK</div>'
             f'<div class="c" id="{fid}-p" style="top:200px;padding:8px 22px;border-radius:30px;background:{RED};{LABEL};font-size:24px;letter-spacing:3px;opacity:0">PERDER EL TIEMPO</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 280, inner, "{opacity: 0, scale: .4, rotationY: -90}")
    js += (f'tl.to("#{fid}-l", {{rotation: -8, duration: .15, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {t0 + .5:.3f});\n'
           f'tl.fromTo("#{fid}-p", {{opacity: 0, scale: 0}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(2.5)"}}, {t0 + .5:.3f});\n'
           f'tl.to("#{fid}-l", {{opacity: .45, duration: .6}}, {t0 + 1.4:.3f});\n' + float_(f"#{fid}", t0, t_out, 8))
    return html, js


def people(fid, t, t_out, cx, cy, label="COMUNIDAD"):
    """Tres avatares blancos que entran en cascada (la comunidad)."""
    av = lambda x, y, s, i: (f'<svg class="c" id="{fid}-a{i}" viewBox="0 0 24 24" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:0">'
                             f'<circle cx="12" cy="8" r="4" fill="#fff"/><path d="M4 21c.6-4.6 3.8-7 8-7s7.4 2.4 8 7z" fill="#fff"/></svg>')
    inner = av(-110, 20, 120, 0) + av(110, 20, 120, 1) + av(0, -10, 160, 2) + f'<div class="c" style="top:185px;{LABEL}">{label}</div>'
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, inner)
    js += "".join(f'tl.fromTo("#{fid}-a{i}", {{opacity: 0, y: 40, scale: .5}}, {{opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2.2)"}}, {t0 + .1 + i * .12:.3f});\n' for i in range(3))
    return html, js + float_(f"#{fid}", t0, t_out)


def nobubble(fid, t, t_out, cx, cy, label):
    """Bocadillo blanco con «#@!» que se tacha con una ✕ roja."""
    svg = (f'<svg class="c" viewBox="0 0 200 170" style="width:230px;height:195px;overflow:visible"><path d="M20 15 H180 V120 H80 L40 155 V120 H20 Z" fill="#fff"/>'
           f'<text x="100" y="85" text-anchor="middle" style="font-family:Hanken,sans-serif;font-weight:700;font-size:56px;fill:#9aa3b5">#@!</text></svg>'
           f'<div class="c" id="{fid}-x" style="left:95px;top:-80px;width:90px;height:90px;border-radius:50%;background:{RED};display:flex;align-items:center;justify-content:center;'
           f'color:#fff;font-family:Hanken,sans-serif;font-weight:700;font-size:52px;opacity:0">✕</div>'
           f'<div class="c" style="top:140px;{LABEL}">{label}</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 280, svg)
    js += (f'tl.fromTo("#{fid}-x", {{opacity: 0, scale: 0, rotation: -40}}, {{opacity: 1, scale: 1, rotation: 0, duration: .3, ease: "back.out(3)"}}, {t0 + .45:.3f});\n'
           + "".join(f'tl.to("#{fid}", {{x: {x}, duration: .05, ease: "none"}}, {t0 + .6 + i * .05:.3f});\n' for i, x in enumerate([12, -10, 6, 0])) + float_(f"#{fid}", t0, t_out))
    return html, js


def dm(fid, t, t_out, cx, cy):
    """Sobre de mensaje privado con «OFERTA» tachado (spam por privado)."""
    svg = (f'<svg class="c" viewBox="0 0 220 160" style="width:240px;height:175px;overflow:visible"><rect x="10" y="10" width="200" height="140" rx="16" fill="#fff"/>'
           f'<path d="M14 18 L110 88 L206 18" fill="none" stroke="#c9d3ea" stroke-width="8" stroke-linejoin="round"/></svg>'
           f'<div class="c" id="{fid}-o" style="top:-110px;padding:8px 22px;border-radius:30px;background:#fff;color:#0050E0;font-family:Hanken,sans-serif;font-weight:700;font-size:30px;opacity:0">OFERTA'
           f'<i id="{fid}-s" style="position:absolute;left:10px;right:10px;top:50%;height:6px;margin-top:-3px;background:{RED};border-radius:3px;transform-origin:0 50%"></i></div>'
           f'<div class="c" style="top:135px;{LABEL}">MENSAJES PRIVADOS</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 280, svg)
    js += (f'tl.fromTo("#{fid}-o", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: .3, ease: "back.out(2)"}}, {t0 + .3:.3f});\n'
           f'tl.fromTo("#{fid}-s", {{scaleX: 0}}, {{scaleX: 1, duration: .18, ease: "power3.out"}}, {t0 + .8:.3f});\n' + float_(f"#{fid}", t0, t_out))
    return html, js


def shield(fid, t, t_out, cx, cy, label):
    """Escudo blanco con ✓ que se dibuja (privacidad/confidencialidad)."""
    svg = (f'<svg class="c" viewBox="0 0 200 230" style="width:200px;height:230px;overflow:visible"><path d="M100 10 L180 40 V110 C180 165 140 200 100 220 C60 200 20 165 20 110 V40 Z" fill="#fff"/>'
           f'<path id="{fid}-k" pathLength="1" d="M62 115 L90 143 L142 88" fill="none" stroke="#0050E0" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:1;stroke-dashoffset:1"/></svg>'
           f'<div class="c" style="top:155px;{LABEL}">{label}</div>')
    k_html, k_js = sparks(fid, t + .5, [(-140, -110), (135, -100), (145, 60)])
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, svg + k_html, "{opacity: 0, scale: .4, rotationY: -180}")
    js += f'tl.fromTo("#{fid}-k", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: .35, ease: "power2.out"}}, {t0 + .4:.3f});\n' + k_js + float_(f"#{fid}", t0, t_out)
    return html, js


def share(fid, t, t_out, cx, cy):
    """Caja con flecha que sale hacia arriba (compártelo)."""
    svg = (f'<svg class="c" viewBox="0 0 200 200" style="width:210px;height:210px;overflow:visible"><path d="M40 90 V170 H160 V90" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'
           f'<g id="{fid}-ar"><path d="M100 130 V25 M65 58 L100 22 L135 58" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></g></svg>'
           f'<div class="c" style="top:140px;{LABEL}">COMPÁRTELO</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 280, svg)
    js += (f'tl.fromTo("#{fid}-ar", {{y: 40, opacity: 0}}, {{y: 0, opacity: 1, duration: .35, ease: "back.out(2.5)"}}, {t0 + .2:.3f});\n'
           f'tl.to("#{fid}-ar", {{y: -14, duration: .3, ease: "sine.inOut", yoyo: true, repeat: {max(1, int((t_out - t0 - .9) / .3) | 1)}}}, {t0 + .6:.3f});\n')
    return html, js


def loop(fid, t, t_out, cx, cy, label):
    """Dos flechas circulares que giran (ayuda mutua / retroalimentación)."""
    svg = (f'<svg class="c" id="{fid}-r" viewBox="0 0 200 200" style="width:220px;height:220px;overflow:visible"><g fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round">'
           f'<path d="M160 100 A60 60 0 0 1 60 145"/><path d="M40 100 A60 60 0 0 1 140 55"/><path d="M128 32 L145 57 L117 66"/><path d="M72 168 L55 143 L83 134"/></g></svg>'
           f'<div class="c" style="top:150px;{LABEL}">{label}</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, svg)
    js += f'tl.fromTo("#{fid}-r", {{rotation: 0}}, {{rotation: 360, duration: {t_out - t0:.3f}, ease: "none"}}, {t0:.3f});\n' + float_(f"#{fid}", t0, t_out)
    return html, js


def brand(fid, t, t_out, cx, cy, img, label):
    """Logo de marca en una baldosa blanca que entra girando en 3D, con su nombre debajo."""
    inner = (f'<div class="c p3" style="width:210px;height:210px"><div class="s3" id="{fid}-s" style="width:210px;height:210px;background:#fff;border-radius:44px;'
             f'box-shadow:0 20px 60px rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center"><img src="{img}" style="width:140px;height:140px;display:block"></div></div>'
             f'<div class="c" style="top:160px;{LABEL};font-size:30px">{label}</div>')
    k_html, k_js = sparks(fid, t + .4, [(-150, -130), (150, -120), (160, 100)])
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, inner + k_html, "{opacity: 0, scale: .5}")
    js += f'tl.fromTo("#{fid}-s", {{rotationY: -180}}, {{rotationY: 0, duration: .8, ease: "power3.out"}}, {t0:.3f});\n' + k_js + float_(f"#{fid}", t0, t_out)
    return html, js


