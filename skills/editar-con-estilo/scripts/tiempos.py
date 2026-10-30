"""Tiempos por palabra del vídeo ya cortado, con whisper.cpp.

Uso: py tiempos.py --trabajo CARPETA/trabajo [--guion GUION.txt] [--idioma es|en] [--modelo RUTA]

- Lee CARPETA/trabajo/voz.wav (lo deja cortar_silencios.py).
- Detecta solo si se habla en español o en inglés (o usa --idioma).
- Usa los tiempos por token de whisper.cpp alineados con DTW (más exactos que los de cada frase): el inicio
  de cada palabra es el momento en que empieza a sonar, que es donde tiene que aparecer su animación.
- Deja CARPETA/trabajo/palabras.json.
- Con --guion, compara lo que se oye con el guion y lista dónde NO coinciden. No decide quién tiene razón:
  eso se le pregunta al usuario.
"""
import argparse, difflib, json, os, re, shutil, subprocess, sys, tempfile, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_comun"))
import comun  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--trabajo", required=True)
ap.add_argument("--guion")
ap.add_argument("--idioma", choices=["es", "en"])
ap.add_argument("--modelo", default=os.environ.get("WHISPER_MODELO", str(comun.MODELO_WHISPER)))
a = ap.parse_args()

voz = os.path.join(a.trabajo, "voz.wav")
if not os.path.isfile(voz):
    sys.exit(f"No existe {voz}: ejecuta primero cortar_silencios.py")
if not os.path.isfile(a.modelo):
    sys.exit(f"No existe el modelo de Whisper {a.modelo}: ejecuta comprobar.py")
whisper = comun.herramienta("whisper-cli")
if not whisper:
    sys.exit("No encuentro whisper-cli: ejecuta comprobar.py")

tmpdir = tempfile.mkdtemp(prefix="tiempos-")
wav16 = os.path.join(tmpdir, "voz16k.wav")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", voz, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav16], check=True)

# 1. Idioma
idioma = a.idioma
if not idioma:
    r = subprocess.run([whisper, "-m", a.modelo, "-f", wav16, "-l", "auto", "-dl"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"auto-detected language:\s*(\w+)", r.stderr + r.stdout)
    detectado = m.group(1) if m else None
    if detectado in ("es", "en"):
        idioma = detectado
        print(f"Idioma detectado: {'español' if idioma == 'es' else 'inglés'}")
    else:
        idioma = "es"
        print(f"AVISO: Whisper detectó «{detectado or 'nada'}», que no es español ni inglés. Uso español; si no es correcto, repite con --idioma en.")

# 2. Transcripción con tiempos por token (DTW si el modelo es uno de los conocidos)
base = os.path.join(tmpdir, "salida")
m = re.match(r"ggml-(tiny|base|small|medium|large-v[123]|large-v3-turbo)(\.en)?\.bin$", os.path.basename(a.modelo))
dtw = None
if m:
    dtw = m.group(1).replace("large-v", "large.v").replace("large.v3-turbo", "large.v3.turbo") + (m.group(2) or "")
cmd = [whisper, "-m", a.modelo, "-f", wav16, "-l", idioma, "-ojf", "-of", base, "-np"]
r = subprocess.run(cmd + (["-dtw", dtw] if dtw else []), capture_output=True, text=True, encoding="utf-8", errors="replace")
if r.returncode != 0 and dtw:
    print("AVISO: este whisper-cli no aceptó DTW; sigo sin él (los tiempos serán algo menos exactos).")
    dtw = None
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
if r.returncode != 0 or not os.path.isfile(base + ".json"):
    sys.exit("whisper-cli falló:\n" + (r.stderr or r.stdout)[-1500:])
datos = json.load(open(base + ".json", encoding="utf-8", errors="replace"))
shutil.rmtree(tmpdir, ignore_errors=True)

# 3. Tokens → palabras. Un token que empieza con espacio abre una palabra nueva.
palabras = []
for seg in datos.get("transcription", []):
    for tok in seg.get("tokens", []):
        texto = tok.get("text", "")
        if not texto or texto.startswith("[_") or texto.startswith("<|"):
            continue
        ini = tok["offsets"]["from"] / 1000
        fin = tok["offsets"]["to"] / 1000
        t_dtw = tok.get("t_dtw", -1)
        momento = t_dtw / 100 if dtw and t_dtw is not None and t_dtw >= 0 else ini
        if texto.startswith(" ") or not palabras:
            palabras.append({"texto": texto.strip(), "inicio": momento, "fin": fin})
        else:
            palabras[-1]["texto"] += texto
            palabras[-1]["fin"] = fin
palabras = [p for p in palabras if p["texto"] and not re.fullmatch(r"[\[\(].*[\]\)]", p["texto"])]  # fuera [Música], (risas)…

# El fin de cada palabra no pasa del inicio de la siguiente. Las que quedan sin duración se marcan.
for i, p in enumerate(palabras):
    if i + 1 < len(palabras):
        p["fin"] = min(p["fin"], palabras[i + 1]["inicio"])
    if p["fin"] - p["inicio"] < 0.04:
        p["fin"] = p["inicio"] + 0.04
        p["revisar"] = True
    p["inicio"], p["fin"] = round(p["inicio"], 3), round(p["fin"], 3)

def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^\w]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))

# 4. Comparación con el guion (si hay)
diferencias = []
if a.guion:
    guion = re.findall(r"\S+", open(a.guion, encoding="utf-8").read())
    A = [norm(p["texto"]) for p in palabras]
    B = [norm(w) for w in guion]
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                palabras[i1 + k]["guion"] = guion[j1 + k]  # el texto de los subtítulos sale del guion, palabra por palabra
        else:
            seg = palabras[i1]["inicio"] if i1 < len(palabras) else (palabras[-1]["fin"] if palabras else 0)
            diferencias.append({"segundo": seg, "se_oye": " ".join(p["texto"] for p in palabras[i1:i2]) or "(nada)",
                                "dice_el_guion": " ".join(guion[j1:j2]) or "(nada)"})

salida = os.path.join(a.trabajo, "palabras.json")
json.dump({"idioma": idioma, "fuente": f"whisper.cpp ({os.path.basename(a.modelo)}{', DTW ' + dtw if dtw else ''})",
           "nota": "inicio = cuando empieza a sonar la palabra (en el vídeo YA CORTADO). 'revisar' = Whisper la dio pegada a otra: comprueba su tiempo.",
           "palabras": palabras, "diferencias_con_guion": diferencias},
          open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"{len(palabras)} palabras · {sum(1 for p in palabras if p.get('revisar'))} para revisar · escrito {salida}")
if a.guion:
    if diferencias:
        print(f"\n{len(diferencias)} sitios donde el audio NO coincide con el guion (pregunta al usuario qué se dice de verdad):")
        for d in diferencias:
            print(f"  {d['segundo']:7.2f} s · se oye: «{d['se_oye']}» · guion: «{d['dice_el_guion']}»")
    else:
        print("El audio coincide con el guion palabra por palabra.")
