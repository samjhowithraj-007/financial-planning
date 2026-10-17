#!/usr/bin/env python3
"""Find moments where the studio screen is blank (Raj's rule: the screen always shows a clip, picture or animation).
Reads snaps/scan/frame-*-at-<t>s.png, crops the screen's inner area (x 980-1870, y 70-860 on the 1920x1080 frame),
and calls it blank when almost nothing in it differs from the empty screen colour.
Usage: python screen-scan.py  -> prints blank runs (flat seconds)."""
import glob, re, subprocess, numpy as np

rows = []
for f in sorted(glob.glob("snaps/scan/frame-*-at-*s.png"), key=lambda p: float(re.search(r"at-([0-9.]+)s", p).group(1))):
    t = float(re.search(r"at-([0-9.]+)s", f).group(1))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", "crop=890:790:980:70,scale=178:158,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).astype(np.float32)
    busy = float((np.abs(a - np.median(a)) > 18).mean())   # share of pixels that are not the empty screen
    rows.append((t, busy, float(np.median(a))))
blank = [t for t, b, m in rows if m < 45 and b < 0.02]
sparse = [t for t, b, m in rows if m < 45 and 0.02 <= b < 0.07]
runs = []
for t in blank:
    if runs and t - runs[-1][1] <= 2.1:
        runs[-1][1] = t
    else:
        runs.append([t, t])
for t, b, m in rows:
    print("%6.1f %5.3f %4.0f %s" % (t, b, m, "BLANK" if t in blank else ("sparse" if t in sparse else "")))
print("\nblank runs:", [(round(a - 1, 1), round(b + 1, 1)) for a, b in runs])

import sys, json
if "--windows" in sys.argv:          # empty seconds -> padded flat windows for the idle coins
    w = []
    for t in blank:
        a, b = max(0.0, t - 0.3), t + 0.3
        if w and a <= w[-1][1] + 0.4:
            w[-1][1] = b
        else:
            w.append([a, b])
    json.dump([[round(a, 2), round(b, 2)] for a, b in w], open("idle-windows.json", "w"))
    print("idle windows:", w)
