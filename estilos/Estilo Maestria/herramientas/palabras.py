import json, re, sys, difflib, unicodedata
T = sys.argv[1]  # carpeta trabajo
d = json.load(open(f"{T}/cortado_dtw.json"))
tramos = json.load(open(f"{T}/tramos.json"))["tramos"]
cuts, acc = [], 0.0
for a, b in tramos[:-1]:
    acc += b - a
    cuts.append(round(acc, 3))

# 1) tokens -> palabras de Whisper
ws = []
for seg in d["transcription"]:
    for t in seg["tokens"]:
        tx = t["text"]
        if tx.startswith("[_") or not tx.strip():
            continue
        dtw = t["t_dtw"] / 100 - 0.14 if t["t_dtw"] >= 0 else None
        off = t["offsets"]["from"] / 1000
        if tx.startswith(" ") or not ws:
            ws.append({"w": tx.strip(), "dtw": dtw, "off": off})
        else:
            ws[-1]["w"] += tx
for w in ws:
    s = w["dtw"] if w["dtw"] is not None else w["off"]
    # primera palabra tras un corte: usar offsets (regla validada)
    for c in cuts:
        if c - 0.05 <= w["off"] <= c + 0.35 and not any(c - 0.05 <= x["off"] < w["off"] for x in ws if x is not w):
            s = max(w["off"], c)
    w["s"] = round(max(0, s), 2)

def norm(x):
    x = unicodedata.normalize("NFD", x.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(ch for ch in x if unicodedata.category(ch) != "Mn"))

# 2) alinear con el guion corregido
g = open(f"{T}/guion_final.txt").read().split()
A, B = [norm(w["w"]) for w in ws], [norm(x) for x in g]
out = [None] * len(g)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
    for k in range(j2 - j1):
        src = ws[min(i1 + k * max(1, i2 - i1) // max(1, j2 - j1), max(i1, i2 - 1))] if i2 > i1 else None
        out[j1 + k] = src["s"] if src else None
    if tag != "equal":
        print("DIF", tag, " ".join(w["w"] for w in ws[i1:i2]), "->", " ".join(g[j1:j2]))
# rellenar huecos interpolando
for i in range(len(out)):
    if out[i] is None:
        prev = next((out[k] for k in range(i - 1, -1, -1) if out[k] is not None), 0)
        nxt = next((out[k] for k in range(i + 1, len(out)) if out[k] is not None), prev + 0.3)
        out[i] = round((prev + nxt) / 2, 2)
for i in range(1, len(out)):
    if out[i] < out[i - 1]:
        out[i] = out[i - 1]
json.dump([{"w": w, "s": s} for w, s in zip(g, out)], open(f"{T}/palabras.json", "w"), ensure_ascii=False, indent=0)
print(len(g), "palabras; cortes:", cuts)
