# Series thumbnail photo (all 50 parts)

Raj chose this photo for every Money Plan thumbnail and Shorts cover (16 Oct 2026): mouth closed, looking into the lens.

- `raj-thumb-photo.jpg`: the original, from `C:\Users\rajpr\OneDrive\Pictures\Camera Roll\WIN_20261016_16_47_55_Pro.jpg` (2560x1440).
- `raj-cutout.png`: the same photo with the room removed (transparent PNG, 2560x1440), made with
  `npx hyperframes@0.8.154 remove-background raj-thumb-photo.jpg -o raj-cutout.png`.
- Both stay on this computer (git-ignored, because the repo is public).

**Using it in a part (copy `videos/ep01/thumbnail/thumb.html` and `cover.html`):**
- Thumbnail 1280x720: `#raj{left:296px;top:-76px;width:1449px;height:815px}`. Raj sits on the right; text and the bar stay left of x≈570.
- Shorts cover 1080x1920: `#raj{left:-775px;top:660px;width:2560px;height:1440px}`. His face is centred under the title.
- Both use a soft cyan glow: `filter:drop-shadow(0 0 28px rgba(10,240,240,.35)) brightness(1.05) contrast(1.06)`.
- Change only the words and numbers per part. Render with `node shot.cjs <puppeteer-core path>` and check the image at 320x180.
