"""Une renders/trozoN.mp4 de un proyecto en un MP4 final: cada trozo se recorta a sus fotogramas exactos (según B de trozos.sh),
el audio de cada trozo se recorta a la misma duración, y el volumen se iguala a ~-16,5 LUFS (sin loudnorm: ganancia fija + limitador).
Uso: bash ~/.config/crear-videos/py unir_trozos.py <carpeta proyecto> <salida.mp4>"""
import json, re, subprocess, sys
from pathlib import Path
P, OUT = Path(sys.argv[1]), sys.argv[2]
B = [float(x) for x in re.search(r'^B=\((.*)\)', (P / "renders/trozos.sh").read_text(), re.M).group(1).split()]
F = [round(b * 30) for b in B]
n = len(B) - 1
ins = sum((["-i", str(P / f"renders/trozo{i + 1}.mp4")] for i in range(n)), [])
def fc(gain, video=True):
    v = "".join(f"[{i}:v]trim=end_frame={F[i + 1] - F[i]},setpts=PTS-STARTPTS[v{i}];" for i in range(n))
    a = "".join(f"[{i}:a]atrim=end={(F[i + 1] - F[i]) / 30:.6f},asetpts=N/SR/TB[a{i}];" for i in range(n))
    return ((v if video else "") + a + ("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,setpts=N/30/TB[v];" if video else "")
            + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,volume={gain:.2f}dB,alimiter=limit=0.79:attack=5:release=50:level=false[a]")
lufs = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-nostats", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)[-1])
tmp = OUT + ".medida.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc(0, False), "-map", "[a]", tmp], check=True)
g = -16.5 - lufs(tmp)
Path(tmp).unlink()
subprocess.run(["nice", "ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc(g), "-map", "[v]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-video_track_timescale", "15360", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", OUT], check=True)
fr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=nb_frames", "-of", "csv=p=0", OUT], capture_output=True, text=True).stdout.split()
print(f"ganancia {g:+.1f} dB · fotogramas {fr} (esperados {F[-1]}) · {lufs(OUT):.1f} LUFS")
