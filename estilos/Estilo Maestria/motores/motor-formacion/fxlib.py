"""Motions blancos ligados a palabras (pasada 2). build.py llama a fx(wt, END) -> (css, html, js).

Cada motion vive en un .fx centrado en (cx, cy) a un lado del presentador (él ocupa x ≈ 560-1300 al 100 %,
hasta ≈ 1400 al 116 %), por encima de los subtítulos (y < 760). Todo determinista.
"""
# Pasada 2: brillo al 50 % -> halos, anillos, resplandor y destello ya están a la mitad.
LEAD = 0.10  # la animación arranca 0,1 s antes de su palabra (estilo.md §6)

CSS = """
.fx{position:absolute;width:0;height:0;z-index:30;opacity:0}
.fx .c{position:absolute;left:0;top:0;transform:translate(-50%,-50%)}
.fx .p3{perspective:1100px}
.fx .s3{position:relative;transform-style:preserve-3d}
.fx .lay{position:absolute;left:0;top:0;width:100%;height:100%}
.fx .ring{border-radius:50%;border:3px solid rgba(255,255,255,.45);opacity:0}
.fx .glow{border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.22),rgba(255,255,255,0) 65%)}
.fx .shine{position:absolute;inset:0;background:linear-gradient(105deg,rgba(255,255,255,0) 35%,rgba(160,190,255,.5) 50%,rgba(255,255,255,0) 65%);
           background-size:300% 100%;background-position:120% 0;-webkit-mask-size:100% 100%;mask-size:100% 100%}
.fx .num{font-family:'Hanken',sans-serif;font-weight:700;color:#fff;white-space:nowrap;text-shadow:0 6px 30px rgba(0,0,0,.35)}
.fx .spark{width:34px;height:34px}
"""

SPARK = ('<svg class="c spark" id="{id}" viewBox="0 0 24 24" style="left:{x}px;top:{y}px;opacity:0">'
         '<path d="M12 0c.8 6.4 4.8 10.6 12 12-7.2 1.4-11.2 5.6-12 12-.8-6.4-4.8-10.6-12-12C7.2 10.6 11.2 6.4 12 0z" fill="#fff"/></svg>')


def logo(fid, t, t_out, cx, cy, w=300):
    """Logo Maestría: entra girando 360° en 3D con canto (capas grises), anillo de luz y brillo que lo cruza."""
    h = round(w * 312 / 330)
    layers = "".join(f'<img class="lay" src="assets/logos/maestria-gris.png" style="transform:translateZ({-2 * i}px)">' for i in range(1, 9))
    html = (f'<div class="fx" id="{fid}" style="left:{cx}px;top:{cy}px">'
            f'<div class="c glow" id="{fid}-gl" style="width:{w * 1.9:.0f}px;height:{w * 1.9:.0f}px;opacity:0"></div>'
            f'<div class="c ring" id="{fid}-rg" style="width:{w}px;height:{w}px"></div>'
            f'<div class="c p3" style="width:{w}px;height:{h}px"><div class="s3" id="{fid}-s" style="width:{w}px;height:{h}px">{layers}'
            f'<img class="lay" src="assets/logos/maestria-blanco.png" style="transform:translateZ(-18px) rotateY(180deg);backface-visibility:hidden">'
            f'<img class="lay" src="assets/logos/maestria-blanco.png" style="backface-visibility:hidden;filter:drop-shadow(0 0 18px rgba(255,255,255,.28))">'
            f'<div class="shine" id="{fid}-sh" style="-webkit-mask-image:url(assets/logos/maestria-blanco.png);mask-image:url(assets/logos/maestria-blanco.png)"></div>'
            f'</div></div></div>')
    t0 = t - LEAD
    js = f"""
tl.fromTo("#{fid}", {{opacity: 0, scale: .35, y: 40}}, {{opacity: 1, scale: 1, y: 0, duration: .55, ease: "back.out(1.7)"}}, {t0:.3f});
tl.fromTo("#{fid}-s", {{rotationY: -360}}, {{rotationY: 0, duration: 1.15, ease: "power3.out"}}, {t0:.3f});
tl.fromTo("#{fid}-rg", {{scale: .3, opacity: .95}}, {{scale: 1.9, opacity: 0, duration: .8, ease: "power2.out"}}, {t0 + .15:.3f});
tl.fromTo("#{fid}-gl", {{opacity: 0}}, {{opacity: .4, duration: .5, ease: "power2.out"}}, {t0 + .2:.3f});
tl.fromTo("#{fid}-sh", {{backgroundPosition: "120% 0"}}, {{backgroundPosition: "-20% 0", duration: .7, ease: "power2.inOut"}}, {t0 + 1.0:.3f});
tl.to("#{fid}-s", {{rotationY: 14, duration: {(t_out - t0 - 1.15) / 2:.3f}, ease: "sine.inOut", yoyo: true, repeat: 1}}, {t0 + 1.15:.3f});
tl.to("#{fid}", {{opacity: 0, scale: .8, y: -30, duration: .3, ease: "power2.in"}}, {t_out - .3:.3f});
"""
    return html, js


def coin(fid, t, t_out, cx, cy, d=230, target=100000, num=True):
    """Moneda $ en 3D (canto de 10 capas) que gira 720°, destellos y contador +$0 -> +$100.000 debajo."""
    layers = "".join(f'<div class="lay" style="border-radius:50%;background:#aab4cc;transform:translateZ({-2.4 * i:.1f}px)"></div>' for i in range(1, 11))
    face = (f'<div class="lay" style="border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffffff,#e6ebf7 60%,#c9d3ea);'
            f'box-shadow:inset 0 0 0 8px #fff,inset 0 0 0 14px #d4dcf0;display:flex;align-items:center;justify-content:center">'
            f'<span style="font-family:Hanken,sans-serif;font-weight:700;font-size:{d * .62:.0f}px;color:#0050E0;line-height:1;margin-top:-6px">$</span></div>')
    sparks = "".join(SPARK.format(id=f"{fid}-k{i}", x=x, y=y) for i, (x, y) in enumerate([(-150, -110), (140, -130), (165, 60), (-160, 80)]))
    html = (f'<div class="fx" id="{fid}" style="left:{cx}px;top:{cy}px">'
            f'<div class="c glow" id="{fid}-gl" style="width:{d * 2.2:.0f}px;height:{d * 2.2:.0f}px;opacity:0"></div>'
            f'<div class="c ring" id="{fid}-rg" style="width:{d}px;height:{d}px"></div>'
            f'<div class="c p3" style="width:{d}px;height:{d}px"><div class="s3" id="{fid}-s" style="width:{d}px;height:{d}px">{layers}{face}</div></div>'
            f'{sparks}' + (f'<div class="c num" id="{fid}-n" style="top:{d * .5 + 60:.0f}px;font-size:66px">+$0</div>' if num else '') + '</div>')
    t0 = t - LEAD
    js = f"""
tl.fromTo("#{fid}", {{opacity: 0, scale: .3, y: 60}}, {{opacity: 1, scale: 1, y: 0, duration: .5, ease: "back.out(1.8)"}}, {t0:.3f});
tl.fromTo("#{fid}-s", {{rotationY: -720}}, {{rotationY: 0, duration: 1.3, ease: "power3.out"}}, {t0:.3f});
tl.fromTo("#{fid}-rg", {{scale: .3, opacity: .95}}, {{scale: 2.1, opacity: 0, duration: .8, ease: "power2.out"}}, {t0 + .1:.3f});
tl.fromTo("#{fid}-gl", {{opacity: 0}}, {{opacity: .45, duration: .5, ease: "power2.out"}}, {t0 + .15:.3f});
""" + (f"""(() => {{ const o = {{v: 0}}, el = document.getElementById("{fid}-n");
  tl.fromTo(o, {{v: 0}}, {{v: {target}, duration: 1.0, ease: "power2.out", onUpdate: () => {{ el.textContent = "+$" + Math.round(o.v).toLocaleString("es-ES").replace(/,/g, "."); }} }}, {t0 + .15:.3f}); }})();
tl.fromTo("#{fid}-n", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: .3, ease: "power3.out"}}, {t0 + .15:.3f});
tl.to("#{fid}-n", {{scale: 1.15, duration: .12, ease: "power2.out", yoyo: true, repeat: 1}}, {t0 + 1.15:.3f});
""" if num else "") + f"""
""" + "".join(
        f'tl.fromTo("#{fid}-k{i}", {{scale: 0, opacity: 0, rotation: -45}}, {{scale: 1, opacity: 1, rotation: 0, duration: .25, ease: "back.out(3)"}}, {t0 + .9 + i * .08:.3f});\n'
        f'tl.to("#{fid}-k{i}", {{scale: 0, opacity: 0, duration: .3, ease: "power2.in"}}, {t0 + 1.5 + i * .08:.3f});\n' for i in range(4)) + f"""
tl.to("#{fid}-s", {{rotationY: 18, duration: {(t_out - t0 - 1.3) / 2:.3f}, ease: "sine.inOut", yoyo: true, repeat: 1}}, {t0 + 1.3:.3f});
tl.to("#{fid}", {{opacity: 0, scale: .8, y: -30, duration: .3, ease: "power2.in"}}, {t_out - .3:.3f});
"""
    return html, js


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


def sparks(fid, t, pts):
    html = "".join(SPARK.format(id=f"{fid}-k{i}", x=x, y=y) for i, (x, y) in enumerate(pts))
    js = "".join(f'tl.fromTo("#{fid}-k{i}", {{scale: 0, opacity: 0, rotation: -45}}, {{scale: 1, opacity: 1, rotation: 0, duration: .25, ease: "back.out(3)"}}, {t + i * .07:.3f});\n'
                 f'tl.to("#{fid}-k{i}", {{scale: 0, opacity: 0, duration: .3, ease: "power2.in"}}, {t + .6 + i * .07:.3f});\n' for i in range(len(pts)))
    return html, js


def lock(fid, t, t_open, t_out, cx, cy):
    """Candado blanco que entra girando y se abre con su palabra; pastilla «ACCESO» debajo."""
    svg = (f'<svg class="c" viewBox="0 0 200 220" style="width:200px;height:220px;overflow:visible">'
           f'<g id="{fid}-sh"><path d="M55 100 V65 a45 45 0 0 1 90 0 V100" {SW} stroke-width="16"/></g>'
           f'<rect x="25" y="95" width="150" height="115" rx="26" fill="#fff"/>'
           f'<circle cx="100" cy="145" r="15" fill="#0050E0"/><rect x="93" y="150" width="14" height="32" rx="7" fill="#0050E0"/></svg>')
    pill = (f'<div class="c" id="{fid}-pl" style="top:170px;padding:10px 26px;border:2px solid rgba(255,255,255,.8);border-radius:40px;{LABEL};opacity:0">ACCESO</div>')
    k_html, k_js = sparks(fid, t_open + .1, [(-130, -90), (125, -110), (140, 40)])
    html, js, t0 = box(fid, t, t_out, cx, cy, 240, svg + pill + k_html, "{opacity: 0, scale: .4, rotationY: -180}")
    js += (f'tl.fromTo("#{fid}-sh", {{y: 0, rotation: 0}}, {{y: -26, rotation: -18, transformOrigin: "145px 100px", duration: .35, ease: "back.out(3)"}}, {t_open - LEAD:.3f});\n'
           f'tl.fromTo("#{fid}-pl", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: .3, ease: "power3.out"}}, {t_open:.3f});\n' + k_js + float_(f"#{fid}", t0, t_out))
    return html, js


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


def live(fid, t, t_out, cx, cy):
    """Pantalla de clase con ▶ y la insignia «● EN VIVO» latiendo (rojo de estilo.md)."""
    inner = (f'<div class="c" id="{fid}-m" style="width:320px;height:200px;border:5px solid #fff;border-radius:24px;background:rgba(255,255,255,.08)"></div>'
             f'<div class="c" style="top:118px;width:120px;height:6px;border-radius:3px;background:#fff"></div>'
             f'<svg class="c" id="{fid}-pl" viewBox="0 0 100 100" style="width:90px;height:90px;opacity:0"><circle cx="50" cy="50" r="48" fill="#fff"/>'
             f'<path d="M40 30 L72 50 L40 70z" fill="#0050E0"/></svg>'
             f'<div class="c" id="{fid}-lv" style="left:-95px;top:-128px;display:flex;align-items:center;gap:10px;padding:8px 18px;border-radius:30px;background:#E5484D;{LABEL};font-size:22px;letter-spacing:3px;opacity:0">'
             f'<i id="{fid}-d" style="display:block;width:12px;height:12px;border-radius:50%;background:#fff"></i>EN VIVO</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 320, inner, "{opacity: 0, scale: .6, rotationX: 70}", k=1.15)
    n = int((t_out - t0 - .6) / .3)
    js += (f'tl.fromTo("#{fid}-pl", {{opacity: 0, scale: 0}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(3)"}}, {t0 + .3:.3f});\n'
           f'tl.fromTo("#{fid}-lv", {{opacity: 0, scale: 0}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(2.5)"}}, {t0 + .45:.3f});\n'
           f'tl.to("#{fid}-d", {{opacity: .2, duration: .15, yoyo: true, repeat: {n * 2 - 1 if n > 0 else 1}}}, {t0 + .6:.3f});\n' + float_(f"#{fid}", t0, t_out, 8))
    return html, js


def big(fid, t, t_out, cx, cy, text, label, t_pulse=None, size=280):
    """Número o cifra gigante que cae de golpe con temblor y destellos."""
    k_html, k_js = sparks(fid, t + .15, [(-150, -120), (150, -110), (160, 90), (-150, 100)])
    inner = (f'<div class="c num" id="{fid}-n" style="font-size:{size}px;line-height:1">{text}</div>'
             + (f'<div class="c" id="{fid}-lb" style="top:{size * .62:.0f}px;{LABEL};opacity:0">{label}</div>' if label else "") + k_html)
    html, js, t0 = box(fid, t, t_out, cx, cy, 280, inner, "{opacity: 0}")
    js += (f'tl.fromTo("#{fid}-n", {{scale: 2.8, opacity: 0}}, {{scale: 1, opacity: 1, duration: .3, ease: "back.out(1.8)"}}, {t0:.3f});\n'
           + "".join(f'tl.to("#{fid}", {{x: {x}, duration: .05, ease: "none"}}, {t0 + .28 + i * .05:.3f});\n' for i, x in enumerate([14, -12, 8, 0]))
           + (f'tl.fromTo("#{fid}-lb", {{opacity: 0, y: 16}}, {{opacity: 1, y: 0, duration: .3, ease: "power3.out"}}, {t0 + .35:.3f});\n' if label else "")
           + k_js + float_(f"#{fid}-n", t0, t_out, 8))
    if t_pulse:
        js += f'tl.to("#{fid}-n", {{scale: 1.18, duration: .12, ease: "power2.out", yoyo: true, repeat: 1}}, {t_pulse - LEAD:.3f});\n'
    return html, js


def flag(fid, t, t_out, cx, cy):
    """Bandera de EE. UU. en blanco: las franjas se dibujan, las estrellas aparecen y ondea."""
    W_, H_ = 300, 180
    stripes = "".join(f'<div class="{fid}-st" style="position:absolute;left:0;top:{i * H_ / 7:.1f}px;width:100%;height:{H_ / 7:.1f}px;background:#fff;transform-origin:0 50%"></div>'
                      for i in range(0, 7, 2))
    stars = "".join(f'<div class="{fid}-sr" style="position:absolute;left:{16 + c * 24 + (r % 2) * 12}px;top:{12 + r * 18}px;width:7px;height:7px;border-radius:50%;background:#0050E0"></div>'
                    for r in range(5) for c in range(5 - (r % 2)))
    inner = (f'<div class="c p3" style="width:{W_}px;height:{H_}px"><div class="s3" id="{fid}-f" style="width:{W_}px;height:{H_}px;border:4px solid #fff;border-radius:8px;overflow:hidden">'
             f'{stripes}<div id="{fid}-cn" style="position:absolute;left:0;top:0;width:{W_ * .42:.0f}px;height:{H_ * 4 / 7:.0f}px;background:#fff">{stars}</div></div></div>'
             f'<div class="c" id="{fid}-lb" style="top:{H_ / 2 + 50:.0f}px;{LABEL};opacity:0">ESTADOS UNIDOS</div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 320, inner)
    js += (f'tl.fromTo(".{fid}-st", {{scaleX: 0}}, {{scaleX: 1, duration: .35, ease: "power3.out", stagger: .06}}, {t0 + .1:.3f});\n'
           f'tl.fromTo("#{fid}-cn", {{scale: 0, transformOrigin: "0 0"}}, {{scale: 1, duration: .3, ease: "back.out(2)"}}, {t0 + .3:.3f});\n'
           f'tl.fromTo(".{fid}-sr", {{scale: 0}}, {{scale: 1, duration: .15, ease: "back.out(3)", stagger: .015}}, {t0 + .45:.3f});\n'
           f'tl.fromTo("#{fid}-lb", {{opacity: 0, y: 16}}, {{opacity: 1, y: 0, duration: .3, ease: "power3.out"}}, {t0 + .4:.3f});\n')
    d = (t_out - t0 - .6) / 4
    js += f'tl.fromTo("#{fid}-f", {{rotationY: 0, skewY: 0}}, {{rotationY: 16, skewY: -3, duration: {d:.3f}, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, {t0 + .6:.3f});\n'
    return html, js


def install(fid, t, t_done, t_out, cx, cy):
    """Tarjeta «INSTALANDO…» con barra que se llena, % que cuenta y ✓ al terminar."""
    inner = (f'<div class="c" style="width:360px;height:150px;border:3px solid rgba(255,255,255,.85);border-radius:28px;background:rgba(255,255,255,.08)"></div>'
             f'<div class="c" id="{fid}-tx" style="left:-55px;top:-30px;{LABEL};font-size:24px">INSTALANDO</div>'
             f'<div class="c num" id="{fid}-pc" style="left:120px;top:-30px;font-size:30px">0%</div>'
             f'<div class="c" style="top:22px;width:300px;height:16px;border-radius:8px;background:rgba(255,255,255,.25)"></div>'
             f'<div class="c" style="top:22px;width:300px;height:16px"><div id="{fid}-br" style="width:100%;height:100%;border-radius:8px;background:#fff;transform-origin:0 50%;transform:scaleX(0)"></div></div>'
             f'<svg class="c" id="{fid}-ok" viewBox="0 0 100 100" style="left:170px;top:-75px;width:80px;height:80px;opacity:0"><circle cx="50" cy="50" r="48" fill="#fff"/>'
             f'<path d="M28 52 L44 67 L73 36" fill="none" stroke="#0050E0" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 340, inner, "{opacity: 0, scale: .5, rotationX: -60}", k=1.3)
    dur = t_done - t0 - .2
    js += (f'tl.fromTo("#{fid}-br", {{scaleX: 0}}, {{scaleX: 1, duration: {dur:.3f}, ease: "power1.inOut"}}, {t0 + .2:.3f});\n'
           f'(() => {{ const o = {{v: 0}}, el = document.getElementById("{fid}-pc");\n'
           f'  tl.fromTo(o, {{v: 0}}, {{v: 100, duration: {dur:.3f}, ease: "power1.inOut", onUpdate: () => {{ el.textContent = Math.round(o.v) + "%"; }} }}, {t0 + .2:.3f}); }})();\n'
           f'tl.set("#{fid}-tx", {{textContent: "LISTO"}}, {t_done:.3f});\n'
           f'tl.fromTo("#{fid}-ok", {{opacity: 0, scale: 0, rotation: -30}}, {{opacity: 1, scale: 1, rotation: 0, duration: .3, ease: "back.out(3)"}}, {t_done:.3f});\n'
           + float_(f"#{fid}", t0, t_out, 8))
    return html, js


def coin_face(d, grad=True):
    bg = "radial-gradient(circle at 35% 30%,#ffffff,#e6ebf7 60%,#c9d3ea)" if grad else "linear-gradient(135deg,#ffffff,#d9e0f0)"
    return (f'<div class="lay" style="border-radius:50%;background:{bg};box-shadow:inset 0 0 0 {d * .035:.0f}px #fff,inset 0 0 0 {d * .06:.0f}px #d4dcf0;'
            f'display:flex;align-items:center;justify-content:center"><span style="font-family:Hanken,sans-serif;font-weight:700;font-size:{d * .62:.0f}px;color:#0050E0;line-height:1;margin-top:-{d * .025:.0f}px">$</span></div>')


def rain(fid, t, t_out, cx, cy):
    """Monedas $ que caen girando en 3D y se apilan (con rebote)."""
    d = 100
    spots = [(-90, 150), (20, 150), (130, 150), (-35, 50), (75, 50), (20, -50)]  # pila: 3 + 2 + 1
    coins = ""
    for i, (x, y) in enumerate(spots):
        edge = "".join(f'<div class="lay" style="border-radius:50%;background:#aab4cc;transform:translateZ({-2 * k}px)"></div>' for k in range(1, 6))
        coins += (f'<div class="c p3" id="{fid}-c{i}" style="left:{x}px;top:{y - 60}px;width:{d}px;height:{d}px">'
                  f'<div class="s3" id="{fid}-s{i}" style="width:{d}px;height:{d}px">{edge}{coin_face(d, False)}</div></div>')
    html, js, t0 = box(fid, t, t_out, cx, cy, 300, coins, "{opacity: 0}")
    for i in range(len(spots)):
        ti = t0 + i * .12
        js += (f'tl.fromTo("#{fid}-c{i}", {{y: -520, opacity: 0}}, {{y: 0, opacity: 1, duration: .55, ease: "bounce.out"}}, {ti:.3f});\n'
               f'tl.fromTo("#{fid}-s{i}", {{rotationY: {-540 if i % 2 else 540}}}, {{rotationY: 0, duration: .7, ease: "power2.out"}}, {ti:.3f});\n')
    return html, js


def confetti(t, n=70):
    """Confeti suave que sale DETRÁS del presentador (va entre el vídeo y su recorte persona-inicio.webm). Física precalculada, sin azar en el navegador."""
    seed = [11]
    def r(a, b):
        seed[0] = (seed[0] * 1103515245 + 12345) % 2**31
        return a + (b - a) * seed[0] / 2**31
    cols = ["#ffffff", "#ffffff", "#dbe6ff", "#a9c3ff", "#f4f7ff"]
    html, js = "", ""
    for i in range(n):
        side = -1 if i % 2 == 0 else 1
        ox, oy = 960 + side * r(160, 260), r(560, 680)
        w, h = (r(10, 14), r(16, 26)) if i % 3 else (r(11, 14),) * 2
        rad = "50%" if i % 3 == 0 else "2px"
        t0 = t + i * .006
        up, fall = r(.5, .75), r(1.5, 2.0)
        vx, vy = side * r(140, 560), r(360, 600)  # que no salga por arriba del cuadro
        html += (f'<div id="cf{i}" style="position:absolute;left:{ox:.0f}px;top:{oy:.0f}px;width:{w:.0f}px;height:{h:.0f}px;border-radius:{rad};'
                 f'background:{cols[i % len(cols)]};opacity:0"></div>')
        js += (f'tl.set("#cf{i}", {{opacity: {r(.6, .95):.2f}}}, {t0:.3f});\n'
               f'tl.fromTo("#cf{i}", {{x: 0, y: 0, rotation: 0}}, {{x: {vx * .75:.0f}, y: {-vy:.0f}, rotation: {side * r(180, 400):.0f}, duration: {up:.2f}, ease: "power2.out"}}, {t0:.3f});\n'
               f'tl.to("#cf{i}", {{x: {vx * .75 + side * r(40, 160):.0f}, y: {-vy + r(380, 640):.0f}, rotation: {side * r(600, 1100):.0f}, duration: {fall:.2f}, ease: "sine.in"}}, {t0 + up:.3f});\n'
               f'tl.to("#cf{i}", {{rotationX: 180, duration: .35, ease: "sine.inOut", yoyo: true, repeat: 5}}, {t0 + up * .5:.3f});\n'
               f'tl.to("#cf{i}", {{opacity: 0, duration: .5, ease: "power1.in"}}, {min(t0 + up + fall - .5, 2.9):.3f});\n')
    return f'<div id="confeti" style="position:absolute;inset:0;pointer-events:none">{html}</div>', js


def fx(wt, END):
    items = [
        logo("f-logo1", wt("comunidad.", 1), 8.6, 1620, 390, 360),
        lock("f-lock", wt("acceso"), wt("exclusivo"), 11.3, 300, 380),
        chip("f-chip", wt("inteligencia"), 14.5, 1620, 380),
        speed("f-speed", wt("avanza"), 17.6, 270, 400),
        live("f-live", wt("clase"), 22.0, 1620, 380),
        big("f-five", wt("cinco"), 22.7, 300, 360, "5", "SISTEMAS AI"),
        flag("f-flag", wt("Estados"), 25.1, 1620, 360),
        coin("f-coin", wt("$100.000"), 28.1, 300, 380),
        install("f-inst", wt("fácil", 1), wt("instalar") + .45, 31.0, 1590, 380),
        big("f-free", wt("gratis."), 34.0, 300, 360, "$0", "GRATIS", t_pulse=wt("gratis?"), size=240),
        rain("f-rain", wt("hacer"), 37.95, 1620, 330),
        logo("f-logo2", wt("Así"), END + .3, 300, 390, 360),
    ]
    return CSS, "\n".join(h for h, _ in items), "".join(j for _, j in items)
