# Part 1 reshoot: free stock clips (Pexels)

These 10 clips replace the animated cutaways on the studio screen. Downloaded on 16 Oct 2026.

**Licence:** Pexels License. Free for commercial use (YouTube monetisation included), no attribution required, no watermark. You may not sell the clip on its own. Credit is optional; the description can say "Stock video: Pexels".
Real people appear in these clips, so the upload's "Altered or synthetic content" answer stays **No**.

**Files:**
- Originals: `broll/raw/NN-*.mp4`.
- Conformed copies: `broll/NN-*.mp4`. Each is 1422x1182 to fit the 948x788 screen slot, 30 fps, no audio, with a light grade.
- `build-draft.py` copies the conformed clips to `draft/assets/broll/`.
- All mp4 files are git-ignored. Rebuild a conformed copy with `broll-conform.py --size 1422x1182 --grade`.

**Same family throughout (changed 16 Oct 2026):** wherever the Vermas appear, the clip comes from one Pexels shoot (Anna Pou), so viewers see the same father, mother and son. The full set of 32 clips and the reuse rules are in `../_shared/verma-family/README.md`. The replaced clips are kept in `broll/old/`.

| # | Story moment (line it cuts in on) | Clip | Pexels page | In the draft |
|---|---|---|---|---|
| 1 | Hook: "1 tareekh… SMS aaya" | Amit on his laptop, Aarav drawing (`01-family-9347900`) | https://www.pexels.com/video/9347900/ | place on the reshoot |
| 2 | Hook: "25 tareekh… chup ho gaya" | Worried man at night, face in shadow (`02-month-end-worry`) | https://www.pexels.com/video/7280528/ | place on the reshoot |
| 3 | Hook: Neha asks about fees and the house | Family at the dining table (`03-family-9347903`) | https://www.pexels.com/video/9347903/ | place on the reshoot |
| 4 | Verma family: Lucknow, rented 2BHK | Indian city rooftops at sunset, no people (`04-city-rooftops`) | https://www.pexels.com/video/36159111/ | **v-lko** |
| 5 | ₹1 lakh: kiraya, ration, bills | Family picking vegetables (`05-family-9346225`) | https://www.pexels.com/video/9346225/ | place on the reshoot |
| 6 | "Achaanak nahi, har saal aate hain" | Neha and Aarav at a garland stall (`06-family-9346226`) | https://www.pexels.com/video/9346226/ | **v-diwali** |
| 7 | Goals: Aarav's college | Amit reading with Aarav (`07-family-9346228`) | https://www.pexels.com/video/9346228/ | place on the reshoot |
| 8 | Goals: parents' care | Woman caring for an elderly man; the grandparents are other people (`08-parents-care`) | https://www.pexels.com/video/7522216/ | place on the reshoot |
| 9 | Goals: "Apna ghar: kabhi na kabhi" | The family on their couch at home (`09-family-9346245`) | https://www.pexels.com/video/9346245/ | **v-ghar** |
| 10 | Aapka kaam: write 5 goals | Neha and Aarav writing on paper (`10-family-9347894`) | https://www.pexels.com/video/9347894/ | place on the reshoot |

**How the clips are wired:**
- In `build-draft.py`, `USE_STOCK = True` makes `broll()` play the clip in `STOCK` in place of the drawn scene.
- Setting it to `False` brings the animations back.
- Clips 1–3, 5, 7, 8 and 10 cover moments where the screen currently shows data cards (the SMS, the budget, the goal timeline). They are slotted when the cut is re-timed to the reshoot voice. Each one runs 3–5 s on its line, then the card comes back, so the numbers stay on screen long enough to read.
