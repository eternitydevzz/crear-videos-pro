"""Música por bloques bajo la voz (estilo nuevo, ficha §9). Rehecho a partir de lo usado en YouTube 2.

Uso: bash ~/.config/crear-videos/py musica_bloques.py config.json
Pasos:
  1. Cada bloque: su pista desde «recorte» s; si no llega, se repite desde el segundo 20 con fundido de 3 s.
     Fundidos de 1,5 s entre bloques (0,6 s al empezar) y de 2,5 s al final del último.
  2. Nivelación continua: la música se mide en ventanas de 2 s (ponderación aproximada a LUFS) y se corrige
     suave (~1 s) para que quede siempre a «objetivo_db» de la voz típica. Así no sube ni baja.
  3. Volumen de cada bloque con rampas de 1,5 s en los cortes.
  4. Si el vídeo sigue después de la voz (cierre), la música de ese tramo se iguala a la de los últimos 13 s de voz.
  5. Mezcla: voz + música, alimiter 0,79. Sale un WAV y, si se da «video_salida», el MP4 con el vídeo copiado.
Config (ejemplo en musica_bloques.ejemplo.json): video (con la voz), video_imagen (opcional; por defecto el mismo),
fin (s, opcional), voz_fin (s, opcional: dónde acaba la voz), cortes [inicio de cada bloque], bloques
[{pista, recorte, volumen}], objetivo_db, wav_salida, video_salida.
"""
import json, os, subprocess, sys, numpy as np

SR, FR = 48000, 4800


def lee(f, ch, filtro="anull"):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-af", filtro, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True).stdout
    return np.frombuffer(b, np.float32).reshape(-1, ch).copy()


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())


KW = "highpass=f=60,highshelf=f=1500:g=4"            # aproximación de la ponderación K


def corto(x, win=20):                                  # dB por tramo de 0,1 s, ventana de 2 s
    n = len(x) // FR
    e = (x[:n * FR] ** 2).reshape(n, FR).mean(1)
    return 10 * np.log10(np.convolve(e, np.ones(win) / win, "same") + 1e-12)


def lufs(f, ss, t):
    e = subprocess.run(["ffmpeg", "-nostats", "-ss", str(ss), "-t", str(t), "-i", f, "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return float(e.split("I:")[-1].split("LUFS")[0])


def rms_db(a):
    return 10 * np.log10(np.mean(a ** 2) + 1e-12)


def main(cfg):
    voz_f = cfg["video"]
    fin = cfg.get("fin") or dur(voz_f)
    cortes = cfg["cortes"] + [fin]
    total = int(fin * SR)
    mus = np.zeros((total, 2), np.float32)
    XF = 1.5
    for i, bl in enumerate(cfg["bloques"]):            # 1. montar bloques
        a, b = max(cortes[i] - XF / 2, 0), min(cortes[i + 1] + XF / 2, fin)
        n = int((b - a) * SR)
        p = lee(bl["pista"], 2)[int(bl.get("recorte", 0) * SR):]
        while len(p) < n:                              # repetir desde el segundo 20 con fundido de 3 s
            r = p[int(20 * SR):] if len(p) > 30 * SR else p
            f = int(3 * SR); w = np.linspace(0, 1, f)[:, None]
            p = np.concatenate([p[:-f], p[-f:] * (1 - w) + r[:f] * w, r[f:]])
        seg = p[:n].copy()
        rc = bl.get("recorte", 0)                      # normalizar el trozo usado a −26,5 LUFS antes de nivelar
        seg *= 10 ** ((-26.5 - lufs(bl["pista"], rc, min(n / SR, dur(bl["pista"]) - rc))) / 20)
        fi = int((0.6 if i == 0 else XF) * SR); fo = int(2.5 * SR)
        seg[:fi] *= np.linspace(0, 1, fi)[:, None]; seg[-fo:] *= np.linspace(1, 0, fo)[:, None]
        mus[int(a * SR):int(a * SR) + n] += seg
    tmp = cfg["wav_salida"] + ".bus.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", tmp], input=mus.tobytes(), check=True)

    voz = corto(lee(voz_f, 1, KW)[:, 0])               # 2. nivelación
    m = corto(lee(tmp, 1, KW)[:, 0])
    n = min(len(voz), len(m))
    vfin = int(cfg.get("voz_fin", len(voz) / 10) * 10)
    ref = np.median(voz[:vfin][voz[:vfin] > voz[:vfin].max() - 30])
    on = m > -70
    g = np.clip(ref + cfg.get("objetivo_db", -10) - m, -12, 14)
    g = np.convolve(g, np.ones(10) / 10, "same"); g[~on] = 0
    t = np.arange(len(mus)) / SR
    mus *= (10 ** (np.interp(t * 10, np.arange(len(g)) + .5, g) / 20))[:, None]

    niv = [bl.get("volumen", 1.0) for bl in cfg["bloques"]]   # 3. volumen por bloque
    k = np.zeros(len(mus))
    for i in range(len(niv)): k[(t >= cortes[i]) & (t < cortes[i + 1])] = niv[i]
    for i in range(1, len(niv)):
        c = cortes[i]; s = (t >= c - .75) & (t < c + .75)
        k[s] = niv[i - 1] + (niv[i] - niv[i - 1]) * (t[s] - (c - .75)) / 1.5
    mus *= k[:, None]

    if "voz_fin" in cfg and cfg["voz_fin"] < fin - 3:  # 4. igualar el cierre sin voz
        vf = cfg["voz_fin"]
        d = rms_db(mus[int((vf - 13) * SR):int(vf * SR)]) - rms_db(mus[int((vf + 1) * SR):int(min(vf + 4, fin - 2.6) * SR)])
        up = 10 ** (d / 20); h = np.where(t >= vf + .5, up, 1.0); s = (t >= vf - 1) & (t < vf + .5)
        h[s] = 1 + (up - 1) * (t[s] - (vf - 1)) / 1.5
        mus *= h[:, None]
        print(f"cierre igualado {d:+.1f} dB")

    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", tmp], input=mus.astype(np.float32).tobytes(), check=True)
    for i in range(len(niv)):                          # informe por bloque
        a = cortes[i] + 2; dd = min(28, cortes[i + 1] - a - 1)
        e = subprocess.run(["ffmpeg", "-nostats", "-ss", str(a), "-t", str(dd), "-i", tmp, "-af", "ebur128=framelog=quiet", "-f", "null", "-"], capture_output=True, text=True).stderr
        print(f"bloque {i + 1}: {e.split('I:')[-1].split('LUFS')[0].strip()} LUFS")

    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voz_f, "-i", tmp, "-filter_complex",       # 5. mezcla
                    f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={fin}[v];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[m];"
                    f"[v][m]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.79:attack=5:release=50:level=false,apad=whole_dur={fin},atrim=0:{fin}[a]",
                    "-map", "[a]", "-c:a", "pcm_s16le", cfg["wav_salida"]], check=True)
    os.remove(tmp)
    if cfg.get("video_salida"):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", cfg.get("video_imagen", voz_f), "-i", cfg["wav_salida"], "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", cfg["video_salida"]], check=True)
    print("ok")


main(json.load(open(sys.argv[1])))
