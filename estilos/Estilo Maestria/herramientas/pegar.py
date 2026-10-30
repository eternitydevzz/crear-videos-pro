"""Pega tramos re-renderizados en un vídeo base (vídeo por fotograma exacto; el audio del base intacto).
Uso: bash ~/.config/crear-videos/py pegar.py base.mp4 salida.mp4 A1 B1 tramo1.mp4 [A2 B2 tramo2.mp4 ...]   (B = None si llega al final)
Los tramos salen de ventana.py (su segundo 0 = A). Si el tramo cambia sonidos, cambia también el audio aparte
(medir la ganancia y el desfase en un trozo sin efectos e insertarlo con fundidos de 5 ms)."""
import math, subprocess, sys
base, out, rest = sys.argv[1], sys.argv[2], sys.argv[3:]
W = [(float(rest[i]), None if rest[i + 1] == "None" else float(rest[i + 1]), rest[i + 2]) for i in range(0, len(rest), 3)]
cnt = lambda p: int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
F = lambda t: math.ceil(t * 30 - 1e-6)
n = cnt(base)
ins, parts, cur = ["-i", base], [], 0
for k, (a, b, w) in enumerate(W):
    fa, fb = F(a), (F(b) if b else n)
    k0 = round(fa - a * 30)
    ins += ["-i", w]
    parts.append(f"[0:v]trim=start_frame={cur}:end_frame={fa},setpts=PTS-STARTPTS[a{k}]")
    parts.append(f"[{k + 1}:v]trim=start_frame={k0}:end_frame={k0 + fb - fa},setpts=PTS-STARTPTS[b{k}]")
    cur = fb
labels = "".join(f"[a{k}][b{k}]" for k in range(len(W))); segs = 2 * len(W)
if cur < n:
    parts.append(f"[0:v]trim=start_frame={cur}:end_frame={n},setpts=PTS-STARTPTS[z]"); labels += "[z]"; segs += 1
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(parts) + f";{labels}concat=n={segs}:v=1:a=0[v]", "-map", "[v]", "-map", "0:a",
                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-video_track_timescale", "15360", "-c:a", "copy", out], check=True)
print("fotogramas", n, "->", cnt(out))
