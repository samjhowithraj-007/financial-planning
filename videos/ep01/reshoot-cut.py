#!/usr/bin/env python3
"""Part 1 reshoot: pick the takes, write cut-list.json, and re-anchor the storyboard to the new voice.

1. Takes. Raj recorded scene by scene, 2-3 takes each, saying "cut this line" after a fluff. Transcript chunks that say
   the same thing (character-trigram similarity >= SIM) within the next few chunks are takes of one line; the one with
   more energy wins (mean speech loudness in dB + 4 dB per extra syllable per second), the later one on a tie, because
   he usually gets better. Chunks with "cut" in them and stray fragments under 0.45 s go.
2. Pace. Each kept chunk keeps 0.10 s before and 0.16 s after; gaps under 0.30 s stay, longer pauses are cut down.
3. Anchors. The storyboard was anchored to the v1 take (ANCHORS in v1/build-draft.py: plan second -> v1 raw second).
   The v1 and reshoot transcripts are both Devanagari from the same model, so a character-level alignment of the two
   kept texts maps every v1 anchor onto the reshoot. Writes reshoot-anchors.json for build-draft.py.

Usage: python reshoot-cut.py   (needs transcript-reshoot.json, reshoot-16k.wav, v1/ files)
"""
import json, re, wave, difflib, ast
import numpy as np

SIM = 0.42
LOOKAHEAD = 6
HERE = "."

def tri(s):
    s = re.sub(r"[\s\.,!?।…\-]+", "", s)
    return {s[i:i + 3] for i in range(max(0, len(s) - 2))}

def sim(a, b):
    A, B = tri(a), tri(b)
    if not A or not B:
        return 0.0
    return len(A & B) / min(len(A), len(B))

# ---------------------------------------------------------------- energy per chunk
wf = wave.open("reshoot-16k.wav")
audio = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
SR = 16000

def energy(c):
    x = audio[int(c["start"] * SR):int(c["end"] * SR)]
    if len(x) < 400:
        return -99.0
    fr = x[: len(x) // 320 * 320].reshape(-1, 320)
    rms = np.sqrt((fr ** 2).mean(1))
    voiced = rms[rms > 0.01]
    db = 20 * np.log10(voiced.mean()) if len(voiced) else -60
    syl = len(re.findall(r"[aeiouािीुूेैोौंँ]", c["text"])) / max(0.3, c["end"] - c["start"])
    return db + 4 * syl / 10

T = json.load(open("transcript-reshoot.json", encoding="utf-8"))
T = [c for c in T if c["text"].strip()]
for c in T:
    c["e"] = energy(c)

# Raj read the teleprompter's scene labels aloud ("Scene number 3 Verma family", "6. Goals", "Next scene Sunday hisaab")
LABEL = re.compile(r"seen|scene|intro|goals|सीन|शीन|श़न|नेश्ट|^\s*\d+\s*\.", re.I)
FIRST_LINE = 11.5          # everything before "Mahine ki pehli tareekh" is the slate ("take one, scene hook")
MANUAL_DROP = [(479.8, 481.4), (515.0, 517.1)]   # "Aapka kaam" and the scene 10 label, transcribed as noise
drop = set()
for i, c in enumerate(T):
    t = c["text"].lower()
    # (short chunks are real words: "Aarav" was a 0.3 s chunk, so nothing is dropped for being short)
    if (re.search(r"\bcut\b|कट|कत दिस|कट दिस", t)
            or (LABEL.search(c["text"]) and c["end"] - c["start"] < 3.0) or c["end"] <= FIRST_LINE
            or any(a <= c["start"] and c["end"] <= b for a, b in MANUAL_DROP)):
        drop.add(i)
for i, c in enumerate(T):
    if i in drop:
        continue
    for j in range(i + 1, min(len(T), i + 1 + LOOKAHEAD)):
        if j in drop:
            continue
        if sim(c["text"], T[j]["text"]) >= SIM and len(tri(c["text"])) >= 4:
            loser = i if T[j]["e"] >= c["e"] - 0.5 else j
            drop.add(loser)
            if loser == i:
                break
kept = [c for k, c in enumerate(T) if k not in drop]

ranges = []
for c in kept:
    a, b = max(0.0, c["start"] - 0.10), c["end"] + 0.16
    if ranges and a - ranges[-1][1] < 0.30:
        ranges[-1][1] = max(ranges[-1][1], b)
    else:
        ranges.append([a, b])
src_dur = len(audio) / SR
ranges = [[round(a, 3), round(min(b, src_dur), 3)] for a, b in ranges]
kept_s = sum(b - a for a, b in ranges)
json.dump({"source_duration": round(src_dur, 3), "kept_seconds": round(kept_s, 3),
           "kept": [{"start": a, "end": b} for a, b in ranges]}, open("cut-list.json", "w"), indent=1)

with open("reshoot-takes.log", "w", encoding="utf-8") as f:
    for k, c in enumerate(T):
        f.write("%s %7.2f-%7.2f e=%6.2f %s\n" % ("DROP" if k in drop else "keep", c["start"], c["end"], c["e"], c["text"]))
print("chunks %d, dropped %d, kept %d ranges, %.1f s of %.1f s" % (len(T), len(drop), len(ranges), kept_s, src_dur))

# ---------------------------------------------------------------- anchors: v1 raw time -> reshoot raw time
def char_stream(chunks, keep_ranges):
    text, times = [], []
    for c in chunks:
        if not any(a - 0.2 <= c["start"] and c["end"] <= b + 0.2 for a, b in keep_ranges):
            continue
        s = re.sub(r"[\s\.,!?।…\-]+", "", c["text"])
        for n, ch in enumerate(s):
            text.append(ch)
            times.append(c["start"] + (c["end"] - c["start"]) * (n + 0.5) / max(1, len(s)))
    return "".join(text), times

v1T = json.load(open("v1/transcript-raw.json", encoding="utf-8"))
v1cut = json.load(open("v1/cut-list.json"))
v1txt, v1t = char_stream(v1T, [(g["start"], g["end"]) for g in v1cut["kept"]])
rstxt, rst = char_stream(kept, ranges)
sm = difflib.SequenceMatcher(None, v1txt, rstxt, autojunk=False)
pairs = []  # (v1 time, reshoot time) for matched characters
for a, b, n in sm.get_matching_blocks():
    for k in range(0, n, 2):
        pairs.append((v1t[a + k], rst[b + k]))
pairs.sort()
# keep a monotonic chain (drop matches that run backwards)
chain = []
for p in pairs:
    if not chain or (p[0] > chain[-1][0] and p[1] > chain[-1][1]):
        chain.append(p)
print("matched characters %d of %d (v1) / %d (reshoot), chain %d" % (sum(n for *_, n in sm.get_matching_blocks()),
      len(v1txt), len(rstxt), len(chain)))

src = open("v1/build-draft.py", encoding="utf-8").read()
A = ast.literal_eval(re.search(r"ANCHORS = (\[.*?\])\nWARP", src, re.S).group(1))
xs = np.array([p[0] for p in chain]); ys = np.array([p[1] for p in chain])
new = []
for plan, r in A:
    rr = float(np.interp(r, xs, ys))
    if new and rr <= new[-1][1]:
        rr = new[-1][1] + 0.05
    new.append((plan, round(rr, 2)))
# beats the transcript alignment got wrong, pinned by hand to the reshoot (Raj: ₹12/39 lakh came in after he said them)
MANUAL = {284.6: 389.0, 285.0: 390.4, 286.0: 394.6, 289.0: 399.2, 295.0: 405.0, 298.0: 411.0, 302.0: 414.8,
          305.0: 427.6, 319.6: 439.6, 320.0: 440.0, 321.0: 442.6, 324.0: 446.7}
merged = sorted({**dict(new), **MANUAL}.items())
fixed = []
for plan, rr in merged:
    if fixed and rr <= fixed[-1][1]:
        if plan in MANUAL:                       # a pinned beat wins: drop earlier unpinned points that now run backwards
            while fixed and fixed[-1][1] >= rr and fixed[-1][0] not in MANUAL:
                fixed.pop()
        else:
            continue
    fixed.append((plan, round(rr, 2)))
new = fixed
json.dump(new, open("reshoot-anchors.json", "w"))
print("anchors", len(new), "first", new[:3], "last", new[-3:])
