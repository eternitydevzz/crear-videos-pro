"""Comprueba lo que necesita editar-con-estilo (además de lo común) y dice cómo instalar lo que falte.
Uso: py comprobar.py
Sale con 1 si falta algo imprescindible.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_comun"))
import comun  # noqa: E402
import comprobar as comprobar_comun  # noqa: E402

NODE_MINIMO = 22   # HyperFrames necesita Node 22 o más
FILTROS = ["silencedetect", "aselect", "select", "amix"]


def main():
    falta = comprobar_comun.main() != 0
    if comun.herramienta("ffmpeg"):
        filtros = comun.correr(["ffmpeg", "-hide_banner", "-filters"], check=False).stdout
        for f in FILTROS:
            if f" {f} " not in filtros:
                print(f"A este ffmpeg le falta el filtro '{f}'.\n{comun.pista_instalar('ffmpeg')}", file=sys.stderr)
                falta = True
    if comun.herramienta("node"):
        v = comun.correr(["node", "-v"], check=False).stdout.strip()
        m = re.match(r"v(\d+)", v)
        if not m or int(m.group(1)) < NODE_MINIMO:
            print(f"Node.js {v} es viejo: HyperFrames necesita {NODE_MINIMO} o más.\n{comun.pista_instalar('node')}",
                  file=sys.stderr)
            falta = True
    else:
        print(f"FALTA Node.js ({NODE_MINIMO} o más)\n{comun.pista_instalar('node')}", file=sys.stderr)
        falta = True
    if not falta:
        print(f"Para editar también está todo: Node {comun.correr(['node', '-v']).stdout.strip()}. "
              f"Tus vídeos se guardan en {comun.mis_videos()}. Comprueba el plugin de HyperFrames con: claude plugin list")
    return 1 if falta else 0


if __name__ == "__main__":
    sys.exit(main())
