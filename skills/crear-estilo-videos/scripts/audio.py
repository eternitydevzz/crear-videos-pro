"""Mide el audio con ffmpeg (sin separar pistas, sin identificar música) y dibuja espectrogramas.
Uso: py audio.py --estilo CARPETA
Deja audio/audio.wav, audio/medidas.txt y audio/esp_00.png, esp_01.png… (10 s cada uno).

Lo que esto SÍ da: nivel, pico, silencios, si es casi mono y dibujos del sonido (espectrogramas).
Lo que NO da: no oye nada, no separa voz/música/efectos y no dice si hay música. Los nombres de
los sonidos que se vean en un espectrograma son una interpretación, no una medición.
"""
import argparse
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_comun"))
import comun  # noqa: E402

TRAMO_S = 10   # segundos por espectrograma: legible a 1500 px de ancho


def af(wav, filtro):
    return comun.correr(["ffmpeg", "-nostats", "-i", wav, "-af", filtro, "-f", "null", "-"], check=False).stderr


def rms(wav, filtro):
    m = re.search(r"RMS level dB:\s*(\S+)", af(wav, f"{filtro},astats=metadata=0"))
    return m.group(1) if m else "?"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--estilo", required=True)
    a = p.parse_args()
    estilo = Path(a.estilo)
    v = estilo / "video.mp4"
    if not v.is_file():
        comun.fallo(f"No existe {v}")
    if not comun.ffprobe(v, "stream=codec_type", "a"):
        print("Este vídeo no tiene pista de audio.")
        return 0
    carpeta = estilo / "audio"
    carpeta.mkdir(exist_ok=True)
    wav = carpeta / "audio.wav"
    comun.correr(["ffmpeg", "-loglevel", "error", "-y", "-i", v, "-vn", "-ac", "2", "-ar", "44100", wav])
    dur = float(comun.ffprobe(wav, "format=duration"))

    lineas = [f"Duración del audio: {dur}s", "--- Sonoridad (ebur128) ---"]
    ebu = [l.strip() for l in af(wav, "ebur128=peak=true").splitlines() if re.match(r"\s+(I|LRA|Peak):", l)]
    lineas += ["  " + l for l in ebu[-3:]]
    lineas.append("--- Nivel medio y máximo (volumedetect) ---")
    lineas += ["  " + re.sub(r".*\]\s*", "", l) for l in af(wav, "volumedetect").splitlines()
               if "mean_volume" in l or "max_volume" in l]
    lineas.append("--- Silencios por debajo de -45 dB y de más de 0,1 s ---")
    sil = ["  " + re.sub(r".*silence_", "", l) for l in af(wav, "silencedetect=n=-45dB:d=0.1").splitlines()
           if "silence_start" in l or "silence_end" in l]
    # ffmpeg no escribe el «end» de un silencio que llega hasta el final del audio: se añade para que no falte
    if sil and sil[-1].lstrip().startswith("start"):
        sil.append(f"  end: {dur} (el audio termina en silencio)")
    lineas += sil or ["  ninguno: algo suena siempre (voz, música o ruido de sala)"]
    lineas += ["--- Estéreo: central contra lateral, y energía bajo 60 Hz ---",
               f"  central (L+R)/2:  {rms(wav, 'pan=mono|c0=0.5*c0+0.5*c1')} dB",
               f"  lateral (L-R)/2:  {rms(wav, 'pan=mono|c0=0.5*c0-0.5*c1')} dB   "
               "(más de ~20 dB por debajo del central = casi mono)",
               f"  bajo 60 Hz:       {rms(wav, 'pan=mono|c0=0.5*c0+0.5*c1,lowpass=f=60')} dB"]
    texto = "\n".join(lineas) + "\n"
    (carpeta / "medidas.txt").write_text(texto, encoding="utf-8")
    print(texto, end="")

    n = math.ceil(dur / TRAMO_S)
    for i in range(n):
        comun.correr(["ffmpeg", "-loglevel", "error", "-y", "-ss", i * TRAMO_S, "-t", TRAMO_S, "-i", wav,
                      "-lavfi", "showspectrumpic=s=1500x450:legend=1:scale=log:fscale=log:stop=16000",
                      "-frames:v", "1", "-update", "1", carpeta / f"esp_{i:02d}.png"])
    print(f"Espectrogramas: {n} imágenes (esp_00.png = segundos 0-10, esp_01.png = 10-20…). El eje horizontal de "
          "cada una empieza en 0 s de SU tramo: suma 10 s por cada imagen anterior.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
