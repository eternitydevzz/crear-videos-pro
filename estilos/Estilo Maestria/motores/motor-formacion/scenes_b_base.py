"""Gráficos a pantalla completa de «Leccion 5 · Preséntate a la comunidad». Reglas comunes en scenes.py.
Maqueta de una publicación de presentación que se rellena con cada dato: mismo diseño (número gigante «0N» + tarjeta con icono y título), para que se lea como una lista.
"""
from scenes import BLUE, LEAD, PRE, RED, snaps, write_scene

CHECK = '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ST = 'fill="none" stroke="#0050E0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
ICON = {
    "heart": f'<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" {ST}/>',
    "ban": f'<circle cx="12" cy="12" r="8.5" {ST}/><path d="M6 6l12 12" {ST}/>',
    "lock": f'<rect x="5" y="11" width="14" height="10" rx="2.5" {ST}/><path d="M8 11V8a4 4 0 0 1 8 0v3" {ST}/><circle cx="12" cy="16" r="1.6" fill="#0050E0"/>',
    "ask": f'<path d="M4 5h16v11H9l-5 4z" {ST}/><path d="M10 8.6a2 2 0 1 1 2.6 1.9c-.5.2-.6.6-.6 1.1M12 13.4v.1" {ST}/>',
    "hands": f'<circle cx="8" cy="8" r="3" {ST}/><circle cx="16" cy="8" r="3" {ST}/><path d="M3 20c.5-3.5 2.5-5.5 5-5.5s4.5 2 5 5.5M11 20c.5-3.5 2.5-5.5 5-5.5s4.5 2 5 5.5" {ST}/>',
    "play": f'<rect x="3" y="5" width="18" height="14" rx="3" {ST}/><path d="M10 9v6l5-3z" fill="#0050E0"/>',
    "doc": f'<path d="M7 3h7l5 5v13H7z" {ST}/><path d="M14 3v5h5M10 12h6M10 16h6" {ST}/>',
    "grid": f'<rect x="4" y="4" width="7" height="7" rx="1.5" {ST}/><rect x="13" y="4" width="7" height="7" rx="1.5" {ST}/><rect x="4" y="13" width="7" height="7" rx="1.5" {ST}/><rect x="13" y="13" width="7" height="7" rx="1.5" fill="#0050E0"/>',
    "globe": f'<circle cx="12" cy="12" r="8.5" {ST}/><path d="M3.5 12h17M12 3.5c2.5 2.6 2.5 14.4 0 17M12 3.5c-2.5 2.6-2.5 14.4 0 17" {ST}/>',
    "levels": f'<path d="M5 19v-4M10 19v-8M15 19v-11M20 19V5" {ST} stroke-width="2.6"/>',
    "bulb": f'<path d="M9 17h6M10 20h4M12 3a6 6 0 0 0-3.5 10.9V16h7v-2.1A6 6 0 0 0 12 3z" {ST}/>',
    "rocket": f'<path d="M12 3c3 2 4.5 5.5 4.5 9.5L14 16h-4l-2.5-3.5C7.5 8.5 9 5 12 3z" {ST}/><circle cx="12" cy="9.5" r="1.6" fill="#0050E0"/><path d="M9 16l-2 4M15 16l2 4" {ST}/>',
    "gem": f'<path d="M6 4h12l3 5-9 11L3 9z" {ST}/><path d="M3 9h18M9 4l3 16 3-16" {ST}/>',
    "user": f'<circle cx="12" cy="8" r="4" {ST}/><path d="M4 21c.6-4.6 3.8-7 8-7s7.4 2.4 8 7" {ST}/>',
    "shake": f'<path d="M3 12l4-4 4 2 3-2 4 1 3 3-6 6-3-2-3 1z" {ST}/><path d="M7 8l4 6M14 8l-3 4" {ST}/>',
    "tool": f'<path d="M14.5 5.5a4 4 0 0 0-5 5L4 16v4h4l5.5-5.5a4 4 0 0 0 5-5l-2.5 2.5-3-.5-.5-3z" {ST}/>',
    "cart": f'<path d="M3 4h2.5l2 11h10l2-7H7" {ST}/><circle cx="9" cy="19" r="1.6" fill="#0050E0"/><circle cx="17" cy="19" r="1.6" fill="#0050E0"/>',
    "clock": f'<circle cx="12" cy="12" r="8.5" {ST}/><path d="M12 7v5l3.5 2" {ST}/>',
    "cal": f'<rect x="4" y="5" width="16" height="15" rx="2.5" {ST}/><path d="M4 10h16M9 3v4M15 3v4" {ST}/>',
    "wave": f'<path d="M7 13V6.5a1.5 1.5 0 0 1 3 0V12M10 11V4.5a1.5 1.5 0 0 1 3 0V11M13 11V5.5a1.5 1.5 0 0 1 3 0V13M16 12V9.5a1.5 1.5 0 0 1 3 0V15a6 6 0 0 1-6 6h-1a6 6 0 0 1-5-2.7L4.5 15a1.5 1.5 0 0 1 2.5-1.6" {ST}/>',
    "link": f'<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1" {ST}/>',
    "brief": f'<rect x="3" y="7" width="18" height="13" rx="2.5" {ST}/><path d="M9 7V5h6v2M3 12h18" {ST}/>',
    "target": f'<circle cx="12" cy="12" r="8.5" {ST}/><circle cx="12" cy="12" r="4.5" {ST}/><circle cx="12" cy="12" r="1.5" fill="#0050E0"/>',
}
svg = lambda k, s, col=None: f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" style="display:block">{ICON[k].replace("#0050E0", col) if col else ICON[k]}</svg>'
BASE_CSS = f"""
#ID .hot{{border-radius:40px;background:radial-gradient(circle at 30% 20%,#2f74ff,{BLUE} 60%,#0038a8);color:#fff;box-shadow:0 40px 100px rgba(0,80,224,.40)}}
#ID .chipw{{display:flex;align-items:center;gap:16px;padding:16px 28px;background:#fff;border-radius:999px;box-shadow:0 22px 50px rgba(16,24,40,.16);white-space:nowrap;font-size:38px;font-weight:700}}
#ID .ok{{display:flex;align-items:center;justify-content:center;width:52px;height:52px;border-radius:50%;background:{BLUE}}}
#ID .ic{{display:flex;align-items:center;justify-content:center;border-radius:30px;background:#e8efff}}
/* serie de reglas */
#ID .rn{{left:170px;top:250px;width:420px;text-align:center}}
#ID .rn .k{{font-family:'Spline',monospace;font-size:34px;letter-spacing:10px;color:#6b7280}}
#ID .rn .n{{display:block;font-size:300px;font-weight:700;letter-spacing:-14px;line-height:.9;color:BLUE}}
#ID .rc{{left:640px;top:250px;width:1110px;height:300px;display:flex;align-items:center;gap:44px;padding:0 60px}}
#ID .rc .t{{font-size:96px;font-weight:700;letter-spacing:-3px;line-height:1}}
#ID .row2{{left:640px;top:600px;display:flex;gap:24px}}
"""


def more(root, wt, words, W, H, out):
    def wa(word, after):
        return next(x["s"] for x in words if x["w"] == word and x["s"] >= after - 1e-6)

    def scene(c, s, e, css, body, js, sfx):
        write_scene(root, c, e - s, W, H, BASE_CSS + css, body, js)
        out.append((c, round(s, 3), round(e, 3), [(n, round(s + t, 3), v) for n, t, v in sfx]))

    def rule(c, s, e, num, icon, title, t_num, t_title, chips=(), extra_css="", extra_body="", extra_js="", sfx=(), kind="PRINCIPIO"):
        """Regla N: «0N» gigante + tarjeta con icono y título; chips opcionales [(icono, texto, t)] debajo."""
        L = lambda t: round(max(t - s - LEAD, 0), 3)
        ch = "".join(f'<div class="abs chipw cp" id="ID-p{i}" style="position:relative">{svg(ic, 44)}{tx}</div>' for i, (ic, tx, _) in enumerate(chips))
        body = (f'<div class="abs rn"><span class="k" id="ID-k">{kind}</span><span class="n" id="ID-n">0{num}</span></div>'
                f'<div class="card rc bl" id="ID-c"><span class="ic" style="width:170px;height:170px;flex:none">{svg(icon, 110)}</span><span class="t">{title}</span></div>'
                f'<div class="abs row2">{ch}</div>' + extra_body)
        js = (f'SCENE_IN();\nIN("#ID-k", {L(t_num)}, {{y: 30}});\n'
              f'tl.fromTo("#ID-n", {{scale: 2.4, opacity: 0, "--b": 16}}, {{scale: 1, opacity: 1, "--b": 0, duration: .3, ease: "back.out(1.8)"}}, sn({L(t_num)}));\n'
              f'tl.fromTo("#ID-c", {{x: 260, opacity: 0, rotationY: -40}}, {{x: 0, opacity: 1, rotationY: 0, duration: .4, ease: "back.out(1.5)"}}, sn({L(t_title)}));\n'
              + "".join(f'POP("#ID-p{i}", {L(t)}, {(-1) ** i * 2});\n' for i, (_, _, t) in enumerate(chips)) + extra_js)
        scene(c, s, e, "#ID .cp{opacity:0}\n" + extra_css, body, js,
              [("whoosh.m4a", 0, 0.24), ("impacto.m4a", L(t_num), 0.08), ("pop.mp3", L(t_title), 0.28)]
              + [("click.mp3", L(t), 0.22) for *_, t in chips] + list(sfx))
        return L

    def cards(c, s, e, tag, items, check=True, extra_body="", extra_js="", sfx=()):
        """Fila de tarjetas con icono que entran (y se marcan ✓) con su palabra. items: [(icono, texto, t)]."""
        L = lambda t: round(max(t - s - LEAD, 0), 3)
        n = len(items); w = min(460, (1600 - (n - 1) * 40) // n)
        x0 = (1920 - (n * w + (n - 1) * 40)) // 2
        b = f'<div class="abs mono tag" id="ID-tag">{tag}</div>'
        for i, (ic, nm, _) in enumerate(items):
            b += (f'<div class="card it bl" id="ID-i{i}" style="left:{x0 + i * (w + 40)}px;width:{w}px"><span class="ic" style="width:130px;height:130px">{svg(ic, 80)}</span>'
                  f'<span class="nm">{nm}</span>' + (f'<span class="ok ck" id="ID-k{i}">{CHECK.format(s=34)}</span>' if check else "") + '</div>')
        css = """
#ID .it{top:280px;height:380px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px;text-align:center}
#ID .it .nm{font-size:50px;font-weight:700;letter-spacing:-1px;line-height:1.05}
#ID .ck{position:absolute;right:-20px;top:-20px;width:80px;height:80px;opacity:0}
"""
        js = "SCENE_IN();\nIN(\"#ID-tag\", 0, {y: 40, scale: 1});\n" + "".join(
            f'tl.fromTo("#ID-i{i}", {{y: 120, scale: .8, opacity: 0}}, {{y: 0, scale: 1, opacity: 1, duration: .32, ease: "back.out(1.7)"}}, sn({L(t)}));\n'
            + (f'POP("#ID-k{i}", {L(t)} + .22);\n' if check else "") for i, (_, _, t) in enumerate(items)) + extra_js
        scene(c, s, e, css, b + extra_body, js, [("swish.mp3", 0, 0.24)] + [("click.mp3", L(t), 0.22) for *_, t in items] + list(sfx))
        return L

    def post(c, s, e, done, new, sfx=(), title="Nueva publicación", sub="MaestrIA · Comunidad · Presentaciones", head="user"):
        """Maqueta de la publicación de presentación: filas ya rellenas (done) + filas que entran con su palabra (new)."""
        L = lambda t: round(max(t - s - LEAD, 0), 3)
        rows = done + new
        b = (f'<div class="card post bl" id="ID-p" style="height:{190 + 84 * len(rows)}px;top:{max(110, (860 - 190 - 84 * len(rows)) // 2)}px"><div class="hd"><span class="av">{svg(head, 60, "#fff")}</span>'
             f'<div><div class="nm">{title}</div><div class="mono sub">{sub}</div></div></div>')
        for i, (ic, tx, _) in enumerate(rows):
            b += (f'<div class="row" id="ID-r{i}"><span class="ic" style="width:64px;height:64px;border-radius:18px">{svg(ic, 38)}</span><span class="tx">{tx}</span>'
                  f'<span class="ok ck" id="ID-k{i}">{CHECK.format(s=28)}</span></div>')
        b += "</div>"
        css = """
#ID .post{left:420px;top:110px;width:1080px;height:650px;padding:34px 50px;display:flex;flex-direction:column;gap:12px}
#ID .hd{display:flex;align-items:center;gap:24px;padding-bottom:18px;border-bottom:3px solid #eef0f4;margin-bottom:6px}
#ID .av{display:flex;align-items:center;justify-content:center;width:96px;height:96px;border-radius:50%;background:BLUE}
#ID .hd .nm{font-size:46px;font-weight:700;letter-spacing:-1px}
#ID .hd .sub{font-size:20px;color:#6b7280;margin-top:6px}
#ID .row{display:flex;align-items:center;gap:22px;padding:8px 14px;border-radius:20px}
#ID .row .tx{font-size:40px;font-weight:700;flex:1}
#ID .row .ck{width:46px;height:46px}
"""
        js = "SCENE_IN();\n" + ("IN(\"#ID-p\", 0, {y: 120});\n" if not done else "")
        for i in range(len(rows)):
            if i < len(done):
                continue
            t = L(rows[i][2])
            js += (f'tl.fromTo("#ID-r{i}", {{opacity: 0, x: -60}}, {{opacity: 1, x: 0, duration: .3, ease: "power3.out"}}, sn({t}));\n'
                   f'POP("#ID-k{i}", {t} + .2);\n'
                   f'tl.fromTo("#ID-r{i}", {{backgroundColor: "rgba(0,80,224,0)"}}, {{backgroundColor: "rgba(0,80,224,.08)", duration: .15, yoyo: true, repeat: 1}}, sn({t} + .2));\n')
        scene(c, s, e, "#ID .row .ck{opacity:1}\n" + "".join(f"#ID #ID-k{i}{{opacity:0}}\n" for i in range(len(done), len(rows))) + css, b, js,
              [("pop.mp3", 0, 0.28)] + [("click.mp3", L(t), 0.22) for *_, t in new] + list(sfx))

