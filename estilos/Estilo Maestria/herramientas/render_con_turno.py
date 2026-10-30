"""Renderiza un proyecto HyperFrames esperando turno (el Mac tiene 8 GB: solo 1 render a la vez).
Uso: bash ~/.config/crear-videos/py render_con_turno.py <carpeta proyecto> <salida.mp4>"""
import os, shutil, subprocess, sys, time
LOCK = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".render.lock")
proj, out = sys.argv[1], sys.argv[2]
t0 = time.time()
while True:
    try:
        os.mkdir(LOCK); break
    except FileExistsError:
        if time.time() - os.path.getmtime(LOCK) > 1800:  # candado viejo (>30 min): se libera
            os.rmdir(LOCK); continue
        time.sleep(15)
print(f"turno conseguido tras {time.time() - t0:.0f} s", flush=True)
try:
    r = subprocess.run([shutil.which("npx") or "npx", "--yes", "hyperframes@0.8.114", "render", "-o", out, "--quiet", "--workers", "3"], cwd=proj)
    sys.exit(r.returncode)
finally:
    os.rmdir(LOCK)
