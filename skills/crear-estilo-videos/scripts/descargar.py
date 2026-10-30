"""Descarga el reel a <estilo>/video.mp4. Primero yt-dlp; si falla, ScrapeCreators (plan B, con la clave del usuario).
Uso: py descargar.py --estilo CARPETA URL
"""
import argparse
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_comun"))
import comun  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--estilo", required=True)
    p.add_argument("url")
    a = p.parse_args()
    estilo = Path(a.estilo)
    estilo.mkdir(parents=True, exist_ok=True)
    destino = estilo / "video.mp4"

    print("1) Probando con yt-dlp…")
    r = comun.correr(["yt-dlp", "-q", "--no-warnings", "--force-overwrites", "-f", "bv*+ba/b",
                      "--merge-output-format", "mp4", "-o", destino, a.url], check=False)
    if r.returncode == 0 and destino.is_file() and destino.stat().st_size > 0:
        print(f"Descargado con yt-dlp: {destino}")
        return 0
    print("yt-dlp falló. Si Instagram lo ha cambiado, actualiza yt-dlp "
          "(Mac: brew upgrade yt-dlp · Windows: winget upgrade yt-dlp.yt-dlp)", file=sys.stderr)

    print("2) Plan B: ScrapeCreators…")
    if not comun.clave():
        comun.fallo(comun.aviso_clave())
    try:
        post = comun.scrapecreators("/v1/instagram/post", a.url)["data"]["xdt_shortcode_media"]
    except Exception as e:  # la API cambia de forma sin avisar: se dice qué pasó
        comun.fallo(f"ScrapeCreators no devolvió el post: {e}")
    media = post
    if post.get("edge_sidecar_to_children"):  # carrusel: el primer vídeo
        media = next((n["node"] for n in post["edge_sidecar_to_children"]["edges"] if n["node"].get("video_url")), post)
    if not media.get("video_url"):
        comun.fallo("El post no tiene vídeo.")
    with urllib.request.urlopen(media["video_url"], timeout=120) as r, open(destino, "wb") as f:
        f.write(r.read())
    if destino.stat().st_size == 0:
        comun.fallo("La descarga por ScrapeCreators salió vacía.")
    print(f"Descargado con ScrapeCreators: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
