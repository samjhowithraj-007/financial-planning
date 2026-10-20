# Series outro (every Money Plan episode)

`outro.mp4` (36 s, 1080p, silent audio track) is appended after Raj's last word in **every episode**:

1. 0–21.5 s: a walkthrough of the **Money Planner** on www.paisasamjhoraj.com/#planner (re-recorded 17 Oct 2026 from
   `capture/capture-planner.cjs`; the old samjhowithraj.online version is in `capture/old/`) (browser window, cursor click on the tab,
   scroll through household → monthly bucket split → safety check → long-term goals, captions 1–5).
2. 21.5–27.5 s: **email sign-up** (added 18 Oct 2026). The window crossfades to the homepage (`assets/home-full.jpg`,
   from `capture/capture-signup.cjs`), scrolls to "Get new lessons by email", a yellow highlighter (#FFE14D, multiply)
   sweeps the heading, the cursor goes to the email box and clicks **Notify me** (a ring only; nothing is typed or
   submitted). Caption 6: "Email pe naye lessons, course updates aur discount offers: abhi sign up karo".
3. 27.5–30 s: "Bilkul free · private" (Money Planner, no login).
4. 30–36 s: **Subscribe** (YouTube @PaisaSamjhoRaj) + **Follow** (Instagram @paisasamjhoraj, Facebook Paisa Samjho Raj,
   X @samjhowithraj), 2x2 grid, "Free lessons + email updates: paisasamjhoraj.com". Since 20 Oct 2026 the Money Plan
   series lives on the separate **Paisa Samjho Raj** channel (Raj's platform split, via 💰 Money PM). The Instagram and Facebook
   pages were planned but not yet created on 20 Oct: create them before any episode with this outro is posted.
   The previous end card (Samjho with Raj handles) is kept as `outro-v2.mp4` / `index-v2.html`.

The end of every script also asks viewers to sign up for email updates (course updates and discount offers) at
paisasamjhoraj.com, so the outro picks it up.

In the episode itself, when Raj says "visit karo hamara website", the studio screen shows `assets/tracker-top.jpg`
(the top of the tracker in a browser frame) until his last word. Each episode's `finish.sh` joins the episode render
and `outro.mp4`, then mixes the lo-fi bed over both (the bed comes up under the outro).

**Re-captured 19 Oct 2026** after the fintech redesign (site commit df22b13): planner sections sit ~64 px lower, the
sign-up box moved to y 2992 (`HS` 2615), and the highlighter is now rgba yellow + ring (multiply vanished on the dark site).
The 17–18 Oct version is kept as `outro-v1.mp4`, `index-v1.html`, `assets-v1/` and `capture/old/v1-20261018/`.

**Update it when the site changes** (puppeteer-core is at `C:/Users/rajpr/node_modules/puppeteer-core`):

- Planner: `cd capture && node capture-planner.cjs <puppeteer-core path>` (live site, 1440x900 at 2x, dark, Verma
  example loaded) writes `planner-full.png` + `planner-boxes.json`; rebuild `assets/tracker-full.jpg` /
  `tracker-top.jpg` (scale to 1600 wide) and check the cursor targets in `index.html` against the boxes.
- Sign-up box: `cd capture && node capture-signup.cjs <puppeteer-core path>` (homepage, 1440x900 at 2x, dark; only reads
  the form) writes `home-full.png` + `signup-boxes.json`; rebuild `assets/home-full.jpg`
  (`ffmpeg -i capture/home-full.png -vf scale=1600:-2:flags=lanczos -q:v 3 assets/home-full.jpg`) and update the
  heading / input / button coordinates and `HS` (scroll) in `index.html`.
- Check: `npx --yes hyperframes@0.8.154 snapshot . -o snaps --at 2.3,6,10,15,19,21.8,22.6,23.5,24.4,25.5,26.5,28.5,31,35 --describe false`
- Render: `npx --yes hyperframes@0.8.154 render . --resolution 1080p --video-bitrate 16M --workers 2 -o outro-video.mp4`
- Silent audio track (the episode concat needs an audio stream):
  `ffmpeg -y -i outro-video.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart outro.mp4`
