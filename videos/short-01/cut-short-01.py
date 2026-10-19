"""Cut Paisa Samjho 1 from the take: keep the chosen takes, shrink pauses, speed 1.15x (pitch kept), clean the voice.
Writes short/assets/cam/raj.mp4 (cam crop, 968x1000), short/assets/voice.m4a, short/cut-map.json, beats.json."""
import json, subprocess
SPEED = 1.15
S = [tuple(map(float, l.split())) for l in open("silences.txt")]
SEG = [("hook", 11.60, 20.30), ("p1", 38.05, 49.70), ("p2", 61.65, 74.10), ("p3", 127.55, 153.15),
       ("payoff", 164.70, 169.45), ("end", 176.50, 195.90)]       # rent lead-in (28-38 s) dropped for length
pieces = []
for name, a, b in SEG:
    cur = a
    for s, e in S:
        if s > a and e < b and e - s > 0.32:
            pieces.append((name, cur, s + 0.10)); cur = e - 0.10
    pieces.append((name, cur, b))
flat, beats, cmap = 0.0, {}, []
for name, a, b in pieces:
    beats.setdefault(name, flat / SPEED)
    cmap.append({"raw": [a, b], "flat": [flat / SPEED, (flat + b - a) / SPEED]})
    flat += b - a
FLAT = flat / SPEED
# clean voice on the full raw first (noise profile from the silent gap 153.6-158.8 s), then cut
clean = ("highpass=f=80,asendcmd=c='153.6 afftdn sn start;158.8 afftdn sn stop',afftdn=nr=14:nf=-42:tn=1,"
         "agate=threshold=0.012:ratio=2:range=0.25:attack=8:release=180")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "raw/IMG_6740.MOV", "-vn", "-af", clean, "-ar", "48000", "-ac", "1", "work-clean.wav"], check=True)
fv, fa, cv, ca = [], [], "", ""
for k, (n, a, b) in enumerate(pieces):
    fv.append("[0:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS[v%d]" % (a, b, k))
    fa.append("[1:a]atrim=%.3f:%.3f,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=%.3f:d=0.02[a%d]" % (a, b, max(0, b - a - 0.02), k))
    cv += "[v%d]" % k; ca += "[a%d]" % k
fc = ";".join(fv + fa) + ";%sconcat=n=%d:v=1:a=0,setpts=PTS/%s,crop=1080:1115:0:720,scale=968:1000:flags=lanczos,fps=30[v];" % (cv, len(pieces), SPEED) \
     + "%sconcat=n=%d:v=0:a=1,atempo=%s[a]" % (ca, len(pieces), SPEED)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "raw/short01-capcut.mp4.mp4", "-i", "work-clean.wav", "-filter_complex", fc,
                "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", "short/assets/cam/raj.mp4",
                "-map", "[a]", "-c:a", "pcm_s16le", "work-voice-cut.wav"], check=True)
# one fixed gain to -15 LUFS (measured, not dynamic loudnorm)
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", "work-voice-cut.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float([l for l in m.splitlines() if l.strip().startswith("I:")][-1].split()[1])
g = -15 - I
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "work-voice-cut.wav", "-af", "volume=%.2fdB,alimiter=limit=0.89" % g, "-c:a", "aac", "-b:a", "256k", "short/assets/voice.m4a"], check=True)
json.dump({"speed": SPEED, "flat_duration": FLAT, "pieces": cmap}, open("short/cut-map.json", "w"), indent=1)
json.dump([beats[n] for n in ("hook", "p1", "p2", "p3", "payoff", "end")], open("beats.json", "w"))
print("pieces %d, flat %.2f s, integrated %.1f LUFS -> gain %+.1f dB" % (len(pieces), FLAT, I, g))
print("beats", [round(beats[n], 2) for n in beats])
