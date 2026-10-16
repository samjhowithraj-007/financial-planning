# Part 1 reshoot: free stock clips (Pexels)

These 10 clips replace the animated cutaways on the studio screen. Downloaded on 16 Oct 2026.

**Licence:** Pexels License. Free for commercial use (YouTube monetisation included), no attribution required, no watermark. You may not sell the clip on its own. Credit is optional; the description can say "Stock video: Pexels".
Real people appear in these clips, so the upload's "Altered or synthetic content" answer stays **No**.

**Files:**
- Originals: `broll/raw/NN-*.mp4`.
- Conformed copies: `broll/NN-*.mp4`. Each is 1422x1182 to fit the 948x788 screen slot, 30 fps, no audio, with a light grade.
- `build-draft.py` copies the conformed clips to `draft/assets/broll/`.
- All mp4 files are git-ignored. Rebuild a conformed copy with `broll-conform.py --size 1422x1182 --grade`.

| # | Story moment (line it cuts in on) | Clip | Pexels page | Length | In the draft |
|---|---|---|---|---|---|
| 1 | Hook: "1 tareekh… SMS aaya" | Smiling man on the phone | https://www.pexels.com/video/7581309/ | 9.9 s | place on the reshoot |
| 2 | Hook: "25 tareekh… chup ho gaya" | Worried man at night with phone | https://www.pexels.com/video/7280528/ | 10 s (from 2 s) | place on the reshoot |
| 3 | Hook: Neha asks about fees and the house | Mother and son at the dining table | https://www.pexels.com/video/9347903/ | 10 s (portrait, centre crop) | place on the reshoot |
| 4 | Verma family: Lucknow, rented 2BHK | Indian city rooftops at sunset | https://www.pexels.com/video/36159111/ | 6.0 s (portrait, centre crop) | **v-lko** |
| 5 | ₹1 lakh: kiraya, ration, bills | Busy Indian kirana store | https://www.pexels.com/video/39688924/ | 10 s (from 2 s) | place on the reshoot |
| 6 | "Achaanak nahi, har saal aate hain" | Diwali-lit street, Jaipur | https://www.pexels.com/video/34580723/ | 10 s (from 2 s) | **v-diwali** |
| 7 | Goals: Aarav's college | Indian college campus walkway | https://www.pexels.com/video/36878014/ | 11.6 s | place on the reshoot |
| 8 | Goals: parents' care | Woman caring for an elderly man | https://www.pexels.com/video/7522216/ | 9.0 s | place on the reshoot |
| 9 | Goals: "Apna ghar: kabhi na kabhi" | Couple with a baby viewing a flat | https://www.pexels.com/video/7578020/ | 8.9 s | **v-ghar** |
| 10 | Aapka kaam: write 5 goals | Hand writing in a notebook by lamplight | https://www.pexels.com/video/39425735/ | 9.8 s | place on the reshoot |

**How the clips are wired:**
- In `build-draft.py`, `USE_STOCK = True` makes `broll()` play the clip in `STOCK` in place of the drawn scene.
- Setting it to `False` brings the animations back.
- Clips 1–3, 5, 7, 8 and 10 cover moments where the screen currently shows data cards (the SMS, the budget, the goal timeline). They are slotted when the cut is re-timed to the reshoot voice. Each one runs 3–5 s on its line, then the card comes back, so the numbers stay on screen long enough to read.
