"""Escenas del vídeo (estilo nuevo · ficha: estilos/Estilo Maestria/youtube/estilo.md).

Prefijos del id (deciden qué hace la cámara): s = sobre la cara · c = cámara reducida (id con derecha/izquierda/circulo)
· b = cámara en blur detrás · t = pantalla azul (textcards.py) · v = b-roll · g = gráfico claro a pantalla completa.
Reglas: título + objeto = un bloque centrado · cada pieza entra con su palabra · nunca blur vacío · «ding», nunca «success».
Piezas listas en piezas.py (copiadas del vídeo YouTube 2): scene, ph, logo, gin, gout, blur_at, gin_slow, pulse, floaty,
s_card, broll, stats_card, biblio, win, mini_ruta… Ejemplos reales: video YouTube 2/todas las versiones/*/proyecto/scenes_b.py
"""
from scenes import LEAD, PRE, snaps, write_scene
from piezas import kit, ico, ICON, GL, RW, SW, TTL, END


def more(root, wt, words, W, H, out):
    k = kit(root, wt, words, W, H, out)
    scene, ph, logo, gin, gout, blur_at, gin_slow, pulse, floaty = k.scene, k.ph, k.logo, k.gin, k.gout, k.blur_at, k.gin_slow, k.pulse, k.floaty
    s_card, broll, stats_card, biblio, win, WIN_IN, mini_ruta = k.s_card, k.broll, k.stats_card, k.biblio, k.win, k.WIN_IN, k.mini_ruta

    # ================================================================== S01 · cristal a la derecha · «frase que ilustra»
    # c = "s01-ejemplo"
    # s, e = ph("Primera frase") - PRE, ph("Siguiente frase") - PRE
    # L = lambda t: round(max(t - s - LEAD, 0), 3)
    # body, css, js = …                       (copiar una escena parecida de los minutos de YouTube 2)
    # scene(c, s, e, css, body, js, [("whoosh.m4a", 0, 0.2)], bg="none")
