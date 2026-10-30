"""Lo que antes hacía sips en el Mac, igual en Windows: redimensiona a 1080 de ancho y guarda JPEG.
Uso: py imagen.py ENTRADA SALIDA ALTO [CALIDAD]   (imprime el tamaño original como «ANCHOxALTO»)
     py imagen.py --medir ENTRADA                  (imprime «ANCHO ALTO»)
Abre PNG, JPG, WEBP, TIFF y HEIC. No convierte colores: copia los píxeles tal cual, como sips -z.
"""
import sys

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()
ANCHO = 1080   # ancho de las imágenes de Instagram


def main():
    if sys.argv[1] == "--medir":
        with Image.open(sys.argv[2]) as img:
            print(img.width, img.height)
        return 0
    entrada, salida, alto = sys.argv[1], sys.argv[2], int(sys.argv[3])
    calidad = int(sys.argv[4]) if len(sys.argv) > 4 else 92
    with Image.open(entrada) as img:
        w, h = img.size
        img = img.convert("RGB").resize((ANCHO, alto), Image.LANCZOS)
        img.save(salida, "JPEG", quality=calidad)
    print(f"{w}x{h}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
