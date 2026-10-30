"""Adapta fotos para subir como si fueran de un iPhone 18 Pro Max.

Uso:  python3 -I adaptar_fotos.py plan.json <carpeta_destino>

plan.json es una lista; cada foto lleva:
  nombre   nombre de salida sin extensión
  origen   ruta de la foto original
  escena   dia | atardecer | interior | noche   (decide hora, apertura, exposición e ISO)
  fecha    "AAAA-MM-DD" (la hora la elige el script según la escena) o "AAAA-MM-DD HH:MM:SS"
  lugar    opcional: {ciudad, estado, pais, codigo, lat, lon, zona}  (por defecto Newark, NJ)

Qué hace con cada foto:
  - Tamaño original: nunca amplía ni reduce.
  - Reducción de ruido (nlmeans suave) solo si los cuadraditos de compresión pasan de 1,2.
  - JPEG calidad 100 en perfil Display P3 (como un iPhone).
  - Borra todos los metadatos y escribe: Apple / iPhone 18 Pro Max, focal 24 mm (dato de Apple),
    apertura, exposición e ISO variados según la escena, fecha y hora con zona horaria,
    dimensiones reales y ubicación (GPS + IPTC + XMP).
  - Si el original está dentro de la carpeta destino, lo mueve a <destino>_originales.
"""
import json, os, random, shutil, subprocess, sys, tempfile
from datetime import datetime
from zoneinfo import ZoneInfo

# Perfil Display P3 incluido en la skill (CC0, saucecontrol/Compact-ICC-Profiles): igual en Mac y en Windows
P3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "perfiles", "DisplayP3-v4.icc")
SRGB = None   # sin perfil en la foto de origen: se toma como sRGB (el perfil sRGB lo trae Pillow)
UMBRAL_RUIDO = 1.2
MODELO = "iPhone 18 Pro Max"
FOCAL_MM = 24  # cámara principal según apple.com/iphone-18-pro/specs (ƒ/1.48, 1.8, 2.8, 4.0)
NEWARK = dict(ciudad="Newark", estado="New Jersey", pais="United States", codigo="US",
              lat=40.7357, lon=-74.1724, zona="America/New_York")

# apertura, exposiciones posibles (segundos como fracción), rango ISO, horas posibles
ESCENAS = {
    "dia":       ("1.8",  [800, 1000, 1250, 1600, 2000, 2500, 3200, 4000], (50, 64),   (10, 16)),
    "atardecer": ("1.8",  [120, 160, 200, 250, 320, 400, 500, 640],        (50, 160),  (16, 17)),
    "interior":  ("1.8",  [60, 80, 100, 120, 160, 200, 250, 320],          (64, 250),  (10, 16)),
    "noche":     ("1.48", [30, 40, 50, 60, 80, 100],                       (320, 1000), (20, 23)),
}
PATRON_AI = "c2pa|jumb|openai|chatgpt|gpt-image|dall-e|sora|trainedAlgorithmic|watermark|midjourney|gemini"

def run(*a):
    return subprocess.run(a, check=True, capture_output=True, text=True).stdout

def cuadraditos(p):
    import numpy as np
    w, h = map(int, run("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height", "-of", "csv=p=0", p).strip().split(","))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-frames:v", "1", "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], check=True, capture_output=True).stdout
    g = np.frombuffer(raw, np.uint8).reshape(h, w).astype(float)
    d = np.abs(np.diff(g, axis=1))
    return d[:, 7::8].mean() / np.delete(d, np.s_[7::8], axis=1).mean(), w, h

def momento(fecha, escena, zona):
    if len(fecha) > 10:
        dt = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    else:
        h0, h1 = ESCENAS[escena][3]
        dt = datetime.strptime(fecha, "%Y-%m-%d").replace(
            hour=random.randint(h0, h1), minute=random.randint(0, 59), second=random.randint(0, 59))
    dt = dt.replace(tzinfo=ZoneInfo(zona))
    off = dt.strftime("%z")
    return dt.strftime("%Y:%m:%d %H:%M:%S"), f"{off[:3]}:{off[3:]}"

def convertir_a_p3(base, perfil, salida):
    """Lo que antes hacía sips en el Mac: pasa los colores del perfil de origen a Display P3 y guarda JPEG 100."""
    from PIL import Image, ImageCms
    img = Image.open(base)
    img = img.convert("RGBA").convert("RGB") if img.mode in ("P", "LA", "RGBA", "I;16") else img.convert("RGB")
    origen = ImageCms.ImageCmsProfile(perfil) if perfil else ImageCms.createProfile("sRGB")
    destino = ImageCms.ImageCmsProfile(P3)
    img = ImageCms.profileToProfile(img, origen, destino, renderingIntent=ImageCms.Intent.PERCEPTUAL,
                                    outputMode="RGB")
    img.save(salida, "JPEG", quality=100, subsampling=0, icc_profile=destino.tobytes())

def adaptar(f, salida, tmp):
    src, escena = f["origen"], f["escena"]
    lugar = {**NEWARK, **f.get("lugar", {})}
    nivel, w, h = cuadraditos(src)

    perfil = os.path.join(tmp, "src.icc")
    with open(perfil, "wb") as fh:
        fh.write(subprocess.run(["exiftool", "-icc_profile", "-b", src], capture_output=True).stdout)
    if os.path.getsize(perfil) == 0:
        perfil = SRGB
    base = src
    if nivel > UMBRAL_RUIDO:
        base = os.path.join(tmp, "limpio.png")
        run("ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "nlmeans=s=1.5:p=7:r=15,format=rgb24",
            "-frames:v", "1", base)
    convertir_a_p3(base, perfil, salida)  # conserva el color de la foto de origen
    run("exiftool", "-q", "-overwrite_original", "-all=", "--icc_profile:all", salida)

    apertura, exps, (iso0, iso1), _ = ESCENAS[escena]
    fecha, tz = momento(f["fecha"], escena, lugar["zona"])
    sub = str(random.randint(100, 999))
    lat, lon = float(lugar["lat"]), float(lugar["lon"])
    tags = {
        "Make": "Apple", "Model": MODELO, "Orientation": "Horizontal (normal)",
        "FocalLength": FOCAL_MM, "FocalLengthIn35mmFormat": FOCAL_MM,
        "FNumber": apertura, "ApertureValue": apertura,
        "ExposureTime": f"1/{random.choice(exps)}", "ISO": random.randint(iso0, iso1),
        "ExposureProgram": "Program AE", "MeteringMode": "Multi-segment", "Flash": "Off, Did not fire",
        "WhiteBalance": "Auto", "SensingMethod": "One-chip color area", "SceneCaptureType": "Standard",
        "ColorSpace": "Uncalibrated", "ExifImageWidth": w, "ExifImageHeight": h,
        "DateTimeOriginal": fecha, "CreateDate": fecha, "ModifyDate": fecha,
        "OffsetTime": tz, "OffsetTimeOriginal": tz, "OffsetTimeDigitized": tz,
        "SubSecTimeOriginal": sub, "SubSecTimeDigitized": sub,
        "GPSLatitude": abs(lat), "GPSLatitudeRef": "N" if lat >= 0 else "S",
        "GPSLongitude": abs(lon), "GPSLongitudeRef": "E" if lon >= 0 else "W",
        "XMP:City": lugar["ciudad"], "XMP:State": lugar["estado"], "XMP:Country": lugar["pais"],
        "XMP:CountryCode": lugar["codigo"], "IPTC:City": lugar["ciudad"], "IPTC:Province-State": lugar["estado"],
        "IPTC:Country-PrimaryLocationName": lugar["pais"], "IPTC:Country-PrimaryLocationCode": lugar["codigo"],
    }
    run("exiftool", "-q", "-q", "-overwrite_original", *[f"-{k}={v}" for k, v in tags.items()], salida)
    run("exiftool", "-q", "-overwrite_original", "-XMP-x:XMPToolkit=", salida)
    return nivel, w, h, fecha, tz, tags

def rastros(p):
    import re
    with open(p, "rb") as fh:
        return len(re.findall(PATRON_AI.encode(), fh.read(), re.I))

if __name__ == "__main__":
    plan, destino = json.load(open(sys.argv[1])), os.path.abspath(sys.argv[2])
    originales = destino + "_originales"
    fallos = 0
    for f in plan:
        src = os.path.abspath(f["origen"])
        if os.path.dirname(src) == destino:  # el original está en la carpeta de subida: apartarlo
            os.makedirs(originales, exist_ok=True)
            nuevo = os.path.join(originales, os.path.basename(src))
            shutil.move(src, nuevo)
            f["origen"] = src = nuevo
        out = os.path.join(destino, f["nombre"] + ".jpg")
        with tempfile.TemporaryDirectory() as tmp:
            nivel, w, h, fecha, tz, t = adaptar(f, out, tmp)
        r = rastros(out)
        fallos += r > 0
        print(f"{f['nombre']:26s} {w}x{h:<5d} {fecha} {tz}  f/{t['FNumber']} {t['ExposureTime']:>7s} ISO {t['ISO']:<4d}"
              f" ruido {nivel:.2f}{' (filtrado)' if nivel > UMBRAL_RUIDO else ''}  rastros AI: {r}")
    print(f"ORIGINALES={originales}")
    sys.exit(1 if fallos else 0)
