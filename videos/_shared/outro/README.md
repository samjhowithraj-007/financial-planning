# Series outro (every Money Plan episode)

`outro.mp4` (30 s, 1080p, silent audio track) is appended after Raj's last word in **every episode**:

1. 0–24 s: a walkthrough of the **Financial Tracker** on samjhowithraj.online (old site; the planner now lives at www.paisasamjhoraj.com/#planner, re-record this walkthrough there) (browser window, cursor click on the tab,
   scroll through household → monthly bucket split → safety check → long-term goals, 5 numbered Hinglish captions,
   then "Bilkul free · private").
2. 24–30 s: **Subscribe** (YouTube @SamjhowithRaj) + **Follow** (Instagram @samjhowithraj, Facebook Samjho with Raj).

In the episode itself, when Raj says "visit karo hamara website", the studio screen shows `assets/tracker-top.jpg`
(the top of the tracker in a browser frame) until his last word. Each episode's `finish.sh` joins the episode render
and `outro.mp4`, then mixes the lo-fi bed over both (the bed comes up under the outro).

**Update it when the tracker changes:** serve the website locally (`python -m http.server 8765` in the website repo),
re-run the capture (`capture/tracker-full.png` + `tracker-boxes.json`, 1440x900 viewport at 2x, dark mode), rebuild
`assets/tracker-full.jpg` / `tracker-top.jpg`, check the cursor targets in `index.html` against `tracker-boxes.json`,
then render: `npx --yes hyperframes@0.8.154 render . --resolution 1080p --video-bitrate 16M --workers 2 -o outro-video.mp4`
and add the silent audio track (see the ep01 session notes / `finish.sh`).
