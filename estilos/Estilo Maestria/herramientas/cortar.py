import json, os, re, subprocess, sys
SRC, OUT = sys.argv[1], sys.argv[2]
M = 0.05
log = subprocess.run(["ffmpeg", "-i", SRC, "-vn", "-af", "silencedetect=noise=-30dB:d=0.3", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC],
                           capture_output=True, text=True).stdout)
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
if len(en) < len(st):  # ffmpeg no escribe el «end» si el vídeo acaba en silencio: ese silencio también se corta
    en.append(dur)
keep, cur = [], 0.0
for s, e in zip(st, en):
    a, b = s + M, e - M
    if a > cur:
        keep.append((round(cur, 3), round(a, 3)))
    cur = max(cur, b)
if cur < dur:
    keep.append((round(cur, 3), round(dur, 3)))
keep = [(a, b) for a, b in keep if b - a > 0.05]
parts, labels = [], []
for i, (a, b) in enumerate(keep):
    d = b - a
    parts.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];")
    parts.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={d-0.01:.3f}:d=0.01[a{i}];")
    labels.append(f"[v{i}][a{i}]")
fc = "".join(parts) + "".join(labels) + f"concat=n={len(keep)}:v=1:a=1[v][a]"
open(OUT + ".fc.txt", "w").write(fc)
json.dump({"tramos": keep, "silencios": list(zip(st, en))}, open(os.path.join(os.path.dirname(os.path.abspath(OUT)), "tramos.json"), "w"), indent=1)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-/filter_complex", OUT + ".fc.txt", "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                "-ar", "48000", OUT], check=True)
print(len(st), "silencios,", len(keep), "tramos, total", round(sum(b - a for a, b in keep), 2), "s")
