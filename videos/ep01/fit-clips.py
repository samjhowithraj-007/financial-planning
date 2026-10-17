#!/usr/bin/env python3
"""Make every AI clip exactly as long as its slot on the studio screen (a video that runs out leaves the screen blank).

Reads the slot lengths from draft/index.html (flat seconds), takes the longest clean take of each clip
(broll/ai/NN-clean-16x9.mp4, family picture already removed), crops it for the screen like the first conform, and:
  - slot <= take: trims it;
  - slot <= 1.5 x take: slows it down (setpts) to fill the slot;
  - longer: plays it forward then backward (ping-pong), slowed if still short.
Writes broll/fit/<slot id>.mp4 (1422x1182, 30 fps, no audio); build-draft.py's stock() uses these when present.
Usage: rm -rf broll/fit draft/assets/broll/fit; python build-draft.py; python fit-clips.py; python build-draft.py
(the slot list is read from a build WITHOUT fit files; with them present the clips are skipped)
"""
import os, re, subprocess, json

PAD = 0.4   # a little longer than the slot (fades overlap the next beat)
# clip file used in the slot -> (clean take, crop/fit filter for the 1422x1182 screen, take start, take end)
SRC = {
    "01-ai-salary-sms.mp4": ("broll/ai/01-clean-16x9.mp4", "fill", None),
    "02-ai-month-end-worry.mp4": ("broll/ai/02-clean-16x9.mp4", "fill", "crop=1150:956:180:90"),
    "03-ai-neha-asks.mp4": ("broll/ai/03-clean-16x9.mp4", "fill", "crop=1299:1080:200:0"),
    "04-ai-lucknow-evening.mp4": ("broll/ai/04-clean-16x9.mp4", "fill", None),
    "05-ai-kirana.mp4": ("broll/ai/05-clean-16x9.mp4", "fill", "crop=1299:1080:150:0"),
    "06-ai-diwali-market.mp4": ("broll/ai/06-clean-16x9.mp4", "fill", "crop=1299:1080:100:0"),
    "07-ai-aarav-study.mp4": ("broll/ai/07-clean-16x9.mp4", "fill", "crop=1299:1080:621:0,trim=0:4.0,setpts=PTS-STARTPTS"),
    "08-ai-parents-care.mp4": ("broll/ai/08-clean-16x9.mp4", "fill", "crop=1299:1080:250:0"),
    "09-ai-apna-ghar.mp4": ("broll/ai/09-clean-16x9.mp4", "fill", "trim=0:6.5,setpts=PTS-STARTPTS"),
    "10-ai-write-goals.mp4": ("broll/ai/10-clean-16x9.mp4", "blur", None),
    "10b-ai-night-writing.mp4": ("broll/ai/10-clean-16x9.mp4", "blur", None),
    "00-ai-family-still.mp4": ("broll/00-ai-family-still.mp4", "as-is", None),
}

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))

html = open("draft/index.html", encoding="utf-8").read()
os.makedirs("broll/fit", exist_ok=True)
report = []
for m in re.finditer(r'<video id="([^"]+)-v" class="clip" src="assets/broll/(?:fit/)?([^"]+)"[^>]*data-duration="([0-9.]+)"', html):
    bid, clip, slot = m.group(1), m.group(2), float(m.group(3))
    if clip not in SRC:
        continue
    src, mode, pre = SRC[clip]
    take = dur(src)
    pre_f = (pre + ",") if pre else ""
    if pre and "trim=0:" in pre:
        take = float(re.search(r"trim=0:([0-9.]+)", pre).group(1))
    target = slot + PAD
    if mode == "blur":
        base = ("[0:v]%sfps=30,split[a][b];[a]scale=1422:1182:force_original_aspect_ratio=increase,crop=1422:1182,boxblur=40:2,"
                "eq=brightness=-0.08[bg];[b]scale=1422:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2" % pre_f)
    elif mode == "as-is":
        base = "[0:v]fps=30"
    else:
        base = "[0:v]%sfps=30,scale=1422:1182:force_original_aspect_ratio=increase:flags=lanczos,crop=1422:1182,eq=contrast=1.03:saturation=0.92" % pre_f
    if target <= take:
        how, chain = "trim", base + ",trim=0:%.3f,setpts=PTS-STARTPTS[v]" % target
    elif target <= take * 1.5:
        f = target / take
        how, chain = "slow x%.2f" % f, base + ",setpts=%.4f*PTS,fps=30,trim=0:%.3f,setpts=PTS-STARTPTS[v]" % (f, target)
    else:
        pp = take * 2
        f = max(1.0, target / pp)
        how = "ping-pong" + (" slow x%.2f" % f if f > 1 else "")
        chain = (base + ",format=yuv420p,split[x][y];[y]reverse[r];[x][r]concat=n=2:v=1:a=0,setpts=%.4f*PTS,fps=30,"
                 "trim=0:%.3f,setpts=PTS-STARTPTS[v]" % (f, target))
    out = "broll/fit/%s.mp4" % bid
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", chain + ";[v]format=yuv420p[o]", "-map", "[o]", "-an",
           "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-g", "15", "-keyint_min", "15", "-sc_threshold", "0",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    report.append((bid, clip, round(slot, 1), round(take, 1), how, round(dur(out), 2)))
    print("%-9s %-28s slot %5.1f take %4.1f -> %-18s %5.2f s" % report[-1])
json.dump(report, open("broll/fit/fit-report.json", "w"), indent=1)
