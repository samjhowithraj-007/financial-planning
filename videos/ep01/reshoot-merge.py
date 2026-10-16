#!/usr/bin/env python3
"""Join the two halves of the reshoot transcript (run in parallel to save time) into transcript-reshoot.json.
Part A (transcript-reshoot.json.log) covers 0-360 s; part B (transcript-reshoot-b.json.log) was cut from 360 s,
so its times get +360. Log lines look like "[ 18.34- 19.88] text"."""
import re, json

def read(path, off):
    out = []
    for ln in open(path, encoding="utf-8"):
        m = re.match(r"\[\s*([0-9.]+)-\s*([0-9.]+)\]\s?(.*)", ln.rstrip("\n"))
        if m:
            out.append({"start": round(float(m.group(1)) + off, 2), "end": round(float(m.group(2)) + off, 2), "text": m.group(3)})
    return out

a = [c for c in read("transcript-reshoot.json.log", 0) if c["start"] < 360]
b = read("transcript-reshoot-b.json.log", 360)
json.dump(a + b, open("transcript-reshoot.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("A %d chunks to %.1f s, B %d chunks %.1f-%.1f s" % (len(a), a[-1]["end"], len(b), b[0]["start"], b[-1]["end"]))
