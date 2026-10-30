"""Entrega un vídeo del estilo de formación: render (uno a la vez), intro delante sin recodificar y auditoría.
Uso: bash ~/.config/crear-videos/py entregar.py <carpeta vídeo> <nombre> [--intro INTRO.mp4]
Deja en la carpeta del vídeo: «<nombre> - sin intro.mp4» y, con --intro, «<nombre> - pasada 1.mp4».
El sonido sale TAL CUAL del render: no se lleva a −16 LUFS ni se le pone limitador (decisión del equipo).
Antes era entregar.sh (zsh, solo Mac, con la intro en una carpeta temporal fija).
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2] / "skills" / "_comun"))
import comun  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("carpeta")
    p.add_argument("nombre")
    p.add_argument("--intro", help="vídeo de intro con el mismo formato (códec, resolución, fps y audio)")
    a = p.parse_args()
    base = Path(a.carpeta).resolve()
    render = base / "proyecto" / "renders" / "render-pasada1.mp4"
    render.parent.mkdir(parents=True, exist_ok=True)

    r = subprocess.run([sys.executable, str(AQUI / "render_con_turno.py"), str(base / "proyecto"), str(render)])
    if r.returncode:
        comun.fallo("El render falló (mira el mensaje de arriba)")

    sin_intro = base / f"{a.nombre} - sin intro.mp4"
    comun.correr(["ffmpeg", "-v", "error", "-y", "-i", render, "-c", "copy", "-movflags", "+faststart", sin_intro])
    final = sin_intro
    if a.intro:
        intro = Path(a.intro).resolve()
        if not intro.is_file():
            comun.fallo(f"No existe la intro {intro}")
        final = base / f"{a.nombre} - pasada 1.mp4"
        with tempfile.TemporaryDirectory() as tmp:
            lista = Path(tmp) / "lista.txt"
            lista.write_text(f"file '{intro.as_posix()}'\nfile '{sin_intro.as_posix()}'\n", encoding="utf-8")
            comun.correr(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy",
                          "-movflags", "+faststart", final])
    print(f"== {a.nombre}: duración {comun.ffprobe(final, 'format=duration')} s · {final.name}")
    r = subprocess.run([sys.executable, str(AQUI / "auditar.py"), str(base), str(sin_intro)], capture_output=True,
                       text=True)
    print("\n".join((r.stdout or r.stderr).strip().splitlines()[-2:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
