# Verma family footage library (all 50 parts)

These are 32 stock clips of one Indian family from a single shoot. They play the Vermas on the studio screen in every episode.

- **Who's in it:** father (Amit), mother (Neha) and son (Aarav). No little girl, so the drawn characters stand in for Pihu when all four are needed.
- **Source:** [Anna Pou on Pexels](https://www.pexels.com/@anna-pou/). Each clip's page is `https://www.pexels.com/video/<id>/`.
- **Licence:** Pexels License. Free for commercial and monetised use, no credit required, no limit on reuse across episodes. You may not resell the clips on their own.
- **On upload:** these are real people, so "Altered or synthetic content" is **No**. The description can say "Stock video: Pexels (Anna Pou)".
- **Downloaded:** 16 Oct 2026.

**Files:**
- `raw/<id>.mp4`: the Pexels HD originals. 31 are portrait 1080x1920; 9346291 is 1280x720 landscape. All are 10 s.
- `screen/<id>.mp4`: copies conformed for the studio-screen slot. 1422x1182, 30 fps, no audio, light grade. Portrait clips are cropped at 40% from the top so the faces stay in frame.
- `screen/<id>.mp4.sheet.png`: the first, middle and last frame of each clip.
- All mp4 files are git-ignored (they stay on this computer).
- To re-crop a clip:
  `python broll-conform.py --in raw/<id>.mp4 --out <ep>/broll/<name>.mp4 --size 1422x1182 --grade --vf "crop=iw:iw/1.203:0:(ih-iw/1.203)*0.4"`
  Change `0.4` to move the window up or down.

## Rules for using the library
1. **Show the family once or twice per episode, not on every cutaway.** Topic moments (bank, insurance, hospital, tax) need other footage: stock without clear faces (hands, documents, a city) or animations.
2. **Don't reuse the previous episode's clips.** Check the "Used in" column below.
3. **Flags:** clips marked 🇮🇳 have Indian-flag bunting (an Independence Day shoot). They're fine for home and family moments. Avoid them in Diwali, tax-season or other festival episodes.
4. **Street:** the market clips (🏙) were shot on a foreign street. The crop keeps the stalls; avoid any re-crop that shows the crosswalk or signs.
5. **Log every use:** add the part number to "Used in" whenever an episode uses a clip.

## Catalogue
| Id | Who | Scene | Good for | Notes | Used in |
|---|---|---|---|---|---|
| 9346214 | Amit, Neha | Couple at a fruit stall, from behind | ration, groceries | 🏙 | |
| 9346215 | Neha, Aarav | Mother and son at a market stall | kids' expenses, shopping | 🏙 | |
| 9346216 | all 3 | Family laughing at a festive stall | festival shopping, yearly expenses | 🏙 | |
| 9346218 | all 3 | Produce stand, Neha checks her phone | budget while shopping | 🏙 | |
| 9346223 | Amit, Neha | Picking limes | ration, inflation | 🏙 | |
| 9346225 | all 3 | Family picking onions and vegetables | ration, monthly expenses | 🏙 | Part 1 |
| 9346226 | Neha, Aarav | Flower and garland stall on a street corner | festivals, yearly expenses | 🏙 street visible | Part 1 |
| 9346228 | Amit, Aarav | Father reading a book with his son | education, college fund | | Part 1 |
| 9346231 | Aarav (hands) | Child picking toys at a stall | kids' wants, impulse buys | 🏙 | |
| 9346237 | Amit, Aarav | Father and son on a tablet | screen time, online spend | | |
| 9346238 | Amit, Aarav | Son on a phone, father watching | UPI, phone, gadgets | | |
| 9346241 | Amit, Aarav | Son on a tablet on dad's lap | learning, edtech fees | | |
| 9346245 | all 3 | Family smiling on the couch (portrait) | family intro, home, goals | | Part 1 |
| 9346247 | Neha, Aarav | Mother and son in the kitchen | household, cooking | | |
| 9346258 | all 3 | Festive meal at the table | celebration, milestones | 🇮🇳 | |
| 9346260 | Neha, Aarav | Mother and son eating | daily life | 🇮🇳 | |
| 9346261 | Aarav | Son eating | kids' expenses | | |
| 9346267 | (hands) | Indian thali close-up | food budget | | |
| 9346270 | Amit | Amit eating alone | Amit's moment, calm | | |
| 9346271 | Amit, Aarav | Father and son laughing on the couch | family time, insurance "why" | | |
| 9346272 | Neha, Aarav | Mother and son, sweets on the table | festivals, sweets | | |
| 9346273 | all 3 | Family on the couch, wide | family security, insurance | | |
| 9346274 | Neha, Aarav | Mother serving her son | household care | 🇮🇳 | |
| 9346275 | Amit, Aarav | Son smiling, Amit behind | children's future | | |
| 9346287 | Amit, Aarav | Father hugging his son | protection, term insurance | 🇮🇳 flag wrap | |
| 9346291 | all 3 | Amit on a laptop, Neha and Aarav drawing (landscape 720p) | working from home, side income | 🇮🇳 | |
| 9347892 | all 3 | Family on the couch waving flags | (Independence Day only) | 🇮🇳 | |
| 9347894 | Neha, Aarav | Mother and son drawing on paper | writing goals, planning | | Part 1 |
| 9347900 | Amit, Aarav | Amit on a laptop, Aarav drawing | salary, checking accounts | 🇮🇳 | Part 1 |
| 9347903 | all 3 | Family at the dining table | family talk, "Neha asks" | 🇮🇳 | Part 1 |
| 9347905 | all 3 | Family in festive clothes, smiling | family intro, celebration | | |
| 9347909 | Neha | Woman dancing with a flag | (Independence Day only) | 🇮🇳 | |
