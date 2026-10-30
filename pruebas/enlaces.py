"""Comprueba que todos los enlaces relativos de los .md del repo apuntan a algo que existe.
Uso: py pruebas/enlaces.py   (desde cualquier carpeta). Sale con 1 si hay enlaces rotos.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

RAIZ = Path(__file__).resolve().parents[1]
ENLACE = re.compile(r"\]\(([^)\s]+)\)")
IGNORAR = {"PLAN.md"}   # interno: no se sube


def main():
    rotos = 0
    for md in sorted(RAIZ.rglob("*.md")):
        if md.name in IGNORAR or "node_modules" in md.parts:
            continue
        for n, linea in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            for destino in ENLACE.findall(linea):
                if re.match(r"(https?:|mailto:|#)", destino):
                    continue
                ruta = unquote(destino.split("#", 1)[0])
                if ruta and not (md.parent / ruta).exists():
                    print(f"ROTO {md.relative_to(RAIZ)}:{n} -> {destino}")
                    rotos += 1
    print("Enlaces: todo bien" if not rotos else f"Enlaces rotos: {rotos}")
    return 1 if rotos else 0


if __name__ == "__main__":
    sys.exit(main())
