#!/usr/bin/env python3
"""Money Plan Part 1 SHORT (9:16, 1080x1920) for YouTube Shorts, Instagram Reels and Facebook Reels.

Seven lines cut from Raj's long take (short/cut-list.json, flat cut 66.7 s) + a 3.3 s ending. Animations fill the top,
the Hinglish caption sits under them, Raj is a small rounded frame bottom-right (cropped head and shoulders; cropping
is fine in the Short). Usage: python build-short.py yt|ig   -> short/index.html
yt ends with a red Subscribe button, ig (Instagram + Facebook) with a blue Follow button.
"""
import os, sys
from html import escape
from characters import character, CHAR_CSS

HERE = os.path.dirname(os.path.abspath(__file__))
PLAT = sys.argv[1] if len(sys.argv) > 1 else "yt"
OUT = os.path.join(HERE, "short", "index.html")
import json as _json
_CM = _json.load(open(os.path.join(HERE, "short", "cut-map.json")))
FLAT = _CM["flat_duration"]                        # reshoot cut (16 Oct 2026): 7 lines, 67.0 s
END = FLAT + 0.03
DUR = round(END + 3.24, 2)
# the scene times below were written for the v1 cut; M() maps them onto the reshoot cut line by line
OB = [0, 5.74, 12.04, 17.74, 30.08, 39.80, 55.36, 66.76]
NB = [g["flat_start"] for g in _CM["segments"]] + [END]
def M(t):
    for (a0, b0), (a1, b1) in zip(zip(OB, NB), zip(OB[1:], NB[1:])):
        if t <= a1:
            return b0 + (b1 - b0) * (t - a0) / (a1 - a0)
    return NB[-1] + (t - OB[-1])
E = lambda s: escape(s, quote=False)
html, js = [], []
VBOX = (60, 380, 960, 798)     # AI clip box: 1.2:1 like the clips, between the title and the caption (y 1270)

def vid(vid_id, clip, a, b, box=VBOX, skip=0.0):
    """An AI family clip (CapCut, broll/) in the top area; times are v1-cut times, mapped by M()."""
    x, y, w, h = box
    a, b = M(a), M(b)
    html.append('<video id="%s" class="clip aiv" src="assets/broll/%s" muted playsinline data-start="%.2f" data-duration="%.2f" '
                'data-media-start="%.2f" data-track-index="5" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></video>'
                % (vid_id, clip, a, b - a, skip, x, y, w, h))
    js.append("tl.fromTo('#%s',{opacity:0},{opacity:1,duration:.3},%.2f); tl.to('#%s',{opacity:0,duration:.3},%.2f);"
              % (vid_id, a + 10000, vid_id, b - 0.3 + 10000))

def scene(sid, a, b, inner):
    a, b = M(a), M(b)
    html.append('<div id="%s" class="clip scene" data-start="%.2f" data-duration="%.2f" data-track-index="%d">%s</div>'
                % (sid, a, b - a, 1 + len(html) % 2, inner))
    js.append("tl.fromTo('#%s',{opacity:0},{opacity:1,duration:.3},%.2f);" % (sid, a + 10000))
    js.append("tl.to('#%s',{opacity:0,duration:.3},%.2f);" % (sid, b - 0.3 + 10000))

def cap(cid, text, em, a, b):
    a, b = M(a), M(b)
    words = "".join('<span class="w%s">%s</span>' % (" " + c if c else "", E(w))
                    for w, c in [(w, em.get(i, "")) for i, w in enumerate(text.split())])
    html.append('<div id="%s" class="clip cap" data-start="%.2f" data-duration="%.2f" data-track-index="6">%s</div>' % (cid, a, b - a, words))
    js.append("tl.fromTo('#%s .w',{opacity:0,y:20},{opacity:1,y:0,duration:.35,ease:'power2.out',stagger:.05},%.2f);" % (cid, a + 10000))
    js.append("tl.to('#%s',{opacity:0,duration:.25},%.2f);" % (cid, b - 0.25 + 10000))

# ---- A. SMS hook 0.00-5.74
scene("sA", 0.0, 5.74, '''
<div class="hook">₹1 lakh salary. <b class="cyan">Future set?</b></div>
''')
vid("a-v", "01-ai-salary-sms.mp4", 0.05, 5.74)
cap("cA1", "Amit ke phone pe SMS aaya…", {}, 0.1, 2.7)
cap("cA2", "₹1,00,000 credited!", {0: "amber"}, 2.7, 5.6)

# ---- B. 31% bachat 5.74-12.04
scene("sB", 5.74, 12.04, '''
<div id="b-fam" class="h" style="left:60px;top:380px;width:960px;height:540px;border-radius:28px;overflow:hidden;box-shadow:0 24px 70px rgba(0,0,0,.55)">
  <img src="assets/img/verma-family.png" style="width:100%;height:100%;object-fit:cover"></div>
<div id="b-bar" class="h" style="left:60px;top:970px;width:960px">
  <div class="sbar"><i style="width:58%;background:rgba(255,255,255,.85)"></i><i style="width:11%;background:#FFB904"></i><i id="b-fut" style="width:31%;background:#0AF0F0"></i></div>
  <div class="slab"><span>Zaroori 58%</span><span class="cyan">Future 31%</span></div></div>
''')
js += ["rise('#b-fam',5.9);", "rise('#b-bar',7.6);"]
cap("cB", "31% bachat: achha start hai", {0: "cyan", 1: "cyan"}, 6.0, 11.9)

# ---- C. kya kaafi hai 12.04-17.74
scene("sC", 12.04, 17.74, '''
<div id="c-q" class="h hook" style="top:225px">Kya ye <b class="mag">sach mein kaafi</b> hai?</div>
''')
vid("c-v", "02-ai-month-end-worry.mp4", 12.1, 17.74, (60, 420, 960, 798))
js += ["rise('#c-q',12.4);"]
cap("cC", "Man mein ek sawaal…", {}, 12.2, 17.6)

# ---- D. 12 lakh 17.74-30.08
scene("sD", 17.74, 30.08, '''
<div id="d-card" class="h card" style="left:60px;top:420px;width:960px;padding:40px 46px">
  <div style="font-size:44px;font-weight:700">Padhai · ₹10,000 × 10 saal</div>
  <div id="d-amt" class="amber" style="font-size:150px;font-weight:700;line-height:1.15">₹0</div>
  <div id="d-dono" class="h chip2">dono bachchon ke liye</div></div>
<div id="d-note" class="h note">Sirf jama rakam · illustrative</div>
''')
js += ["rise('#d-card',18.0);", "count('#d-amt',0,1200000,21.6,1.6);", "rise('#d-dono',26.4);", "rise('#d-note',23.4);"]
cap("cD1", "₹10,000 har mahine, 10 saal…", {0: "amber"}, 17.9, 23.3)
cap("cD2", "= ₹12 lakh jama", {1: "amber", 2: "amber"}, 23.3, 29.9)

# ---- E. sirf jama rakam 30.08-39.80
scene("sE", 30.08, 39.80, '''
<div id="e-x" class="h strike">Final amount</div>
<div id="e-t" class="h big" style="left:60px;top:560px;width:960px;text-align:center">Sirf <b class="cyan">jama rakam</b></div>
<div id="e-p1" class="h pillx" style="left:120px;top:800px">✗ growth</div>
<div id="e-p2" class="h pillx" style="left:400px;top:800px">✗ mehngai</div>
<div id="e-p3" class="h pillx" style="left:700px;top:800px">✗ inflation</div>
<div id="e-ep" class="h chip2" style="position:absolute;left:180px;top:960px">Asli kharcha: Episode 41 &amp; 46</div>
''')
js += ["rise('#e-x',30.3);", "rise('#e-t',30.8);", "rise('#e-p1',34.2);", "rise('#e-p2',35.9);", "rise('#e-p3',37.3);", "rise('#e-ep',38.2);"]
cap("cE1", "Ye sirf jama rakam hai", {2: "cyan", 3: "cyan"}, 30.2, 34.0)
cap("cE2", "Na growth, na mehngai judi", {}, 34.0, 39.6)

# ---- F. 5 goals 39.80-55.36
rows = [("Emergency fund", "Abhi", 43.6), ("Aarav ka college", "2036", 45.2), ("Pihu ka college", "2040", 46.8),
        ("Retirement", "2051", 48.4), ("Apna ghar", "? sapna", 50.0)]
rh = "".join('<div class="prow"><span>%s</span><span>%s</span><span>₹ ____</span><div id="f-m%d" class="pmask"></div></div>'
             % (g, w if "sapna" not in w else '<b class="amber">? sapna</b>', k) for k, (g, w, _) in enumerate(rows))
scene("sF", 39.80, 55.36, '''
<div id="f-paper" class="h paper" style="left:60px;top:380px"><div class="phead">Hamare 5 goals</div>
  <div class="prow pcols"><span>Goal</span><span>Kab</span><span>Kitna</span></div>%s</div>
''' % rh)
js += ["rise('#f-paper',40.0);"]
vid("f-v", "10-ai-write-goals.mp4", 51.2, 55.36, skip=3.0)
js += ["tl.fromTo('#f-m%d',{scaleX:1},{scaleX:0,duration:.9,ease:'power1.inOut'},%.2f);" % (k, t) for k, (_, _, t) in enumerate(rows)]
cap("cF1", "Aaj raat ek kaagaz lo…", {}, 39.9, 44.6)
cap("cF2", "5 goals likho: kab chahiye, kitna", {0: "cyan", 1: "cyan"}, 44.6, 55.2)

# ---- G. website 55.36-66.76
scene("sG", 55.36, 66.76, '''
<div id="g-t" class="h big" style="left:60px;top:300px;width:960px;text-align:center">Free <b class="cyan">Financial Tracker</b></div>
<div id="g-win" class="h webwin" style="left:60px;top:440px"><div class="wbar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i>
  <i style="background:#28c840"></i><span class="wurl">🔒&nbsp;<b>samjhowithraj.online</b>/#tracker</span></div>
  <img id="g-img" src="assets/img/tracker-top.jpg" alt=""></div>
''')
js += ["rise('#g-t',55.6);", "rise('#g-win',56.0);", "tl.to('#g-img',{y:-420,duration:8,ease:'power1.inOut'},57.6);"]
cap("cG1", "Financial planner chahiye?", {1: "cyan"}, 55.5, 60.4)
cap("cG2", "samjhowithraj.online pe free!", {0: "cyan"}, 60.4, 66.6)

# ---- H. ending 66.76-70.0
btn = '<span class="btn red">Subscribe</span>' if PLAT == "yt" else '<span class="btn blue">Follow</span>'
who = '<span class="ico">▶</span><div><div class="endk">YouTube</div><div class="endh">@SamjhowithRaj</div></div>' if PLAT == "yt" else \
      '<span class="ico ig">◎</span><div><div class="endk">Instagram · Facebook</div><div class="endh">@samjhowithraj</div></div>'
html.append('''<div id="sH" class="clip endc" data-start="@@END@@" data-duration="3.24" data-track-index="8">
<div class="endt">Poori series:<br><b class="cyan">50 parts</b></div>
<div id="h-b" class="endb">%s%s</div>
<div class="endw">Part 2: salary <b>gayab kahan</b> hoti hai?</div></div>''' % (who, btn))
js += ["tl.fromTo('#sH',{opacity:0},{opacity:1,duration:.35},66.76);", "rise('#h-b',67.1);",
       "tl.fromTo('#h-b .btn',{scale:1},{scale:1.1,duration:.22,yoyo:true,repeat:5,ease:'power1.inOut'},67.6);"]

money = [M(2.4), M(23.2)]
sounds = "".join('<audio id="cc%d" src="assets/sfx/chaching.mp3" data-start="%.2f" data-duration="1.4" data-track-index="12" data-volume="0.16"></audio>'
                 % (k, t) for k, t in enumerate(money))

CSS = '''
@font-face{font-family:"DM Sans";src:url(fonts/DMSans-400.woff2) format("woff2");font-weight:400}
@font-face{font-family:"DM Sans";src:url(fonts/DMSans-500.woff2) format("woff2");font-weight:500}
@font-face{font-family:"DM Sans";src:url(fonts/DMSans-700.woff2) format("woff2");font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0a0d14}
body{font-family:"DM Sans",ui-sans-serif,system-ui,sans-serif;color:#fff}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;
  background:radial-gradient(800px 700px at 70% 18%,rgba(10,240,240,.10),transparent 70%),
             radial-gradient(900px 800px at 100% 100%,rgba(0,5,238,.22),transparent 70%),#0a0d14}
.scene{position:absolute;inset:0}.scene>*{position:absolute}
.h{opacity:0}.cyan{color:#0AF0F0}.amber{color:#FFB904}.mag{color:#CD00EE}
#tag{position:absolute;left:0;right:0;top:110px;display:flex;justify-content:center}
#tag span{padding:14px 30px;border-radius:9999px;background:rgba(255,255,255,.1);border:3px solid rgba(255,255,255,.4);font-size:32px;font-weight:700;letter-spacing:.06em}
.hook{left:60px;right:60px;top:230px;text-align:center;font-size:72px;font-weight:700;line-height:1.1}
.big{font-size:84px;font-weight:700;line-height:1.1}
.card{background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.4);border-radius:30px}
.sms{width:520px;padding:24px 30px;border-radius:28px;background:#f4f6fa;color:#111;box-shadow:0 20px 60px rgba(0,0,0,.5)}
.smsh{font-size:24px;font-weight:700;color:#667;letter-spacing:.06em;margin-bottom:6px}
.sms .amber{color:#b37400}
.bub{padding:24px 32px;border-radius:30px;background:#fff;color:#111;font-size:50px;font-weight:700;line-height:1.2;box-shadow:0 18px 50px rgba(0,0,0,.45)}
.bub b{color:#0005EE}
.sbar{display:flex;gap:6px;height:70px;border-radius:16px;overflow:hidden}.sbar i{display:block;height:70px}
.slab{display:flex;justify-content:space-between;font-size:36px;font-weight:700;margin-top:14px}
.chip2{display:inline-block;margin-top:18px;padding:16px 28px;border-radius:16px;background:rgba(17,17,17,.6);border:2px solid rgba(255,255,255,.25);font-size:44px;font-weight:700}
.note{left:60px;right:60px;top:860px;text-align:center;font-size:32px;color:rgba(255,255,255,.75)}
.strike{left:60px;right:60px;top:470px;text-align:center;font-size:56px;font-weight:700;color:rgba(255,255,255,.75);
  text-decoration:line-through;text-decoration-color:#E0242E;text-decoration-thickness:7px}
.pillx{padding:16px 26px;border-radius:9999px;background:rgba(224,36,46,.16);border:3px solid rgba(224,36,46,.7);font-size:40px;font-weight:700}
.paper{width:960px;padding:40px 46px;border-radius:22px;background:#F5F1E8;color:#1b1a17;box-shadow:0 30px 90px rgba(0,0,0,.55)}
.phead{font-size:60px;font-weight:700;border-bottom:6px solid #FFB904;display:inline-block;margin-bottom:20px}
.prow{position:relative;display:grid;grid-template-columns:1.6fr .9fr .8fr;font-size:42px;font-weight:700;padding:18px 0;border-bottom:2px solid rgba(27,26,23,.15)}
.pcols{font-size:30px;color:rgba(27,26,23,.6)}
.paper .amber{color:#9a6400}
.pmask{position:absolute;inset:0;background:#F5F1E8;transform-origin:100% 50%}
.webwin{width:960px;height:760px;border-radius:22px;overflow:hidden;background:#141414;box-shadow:0 0 0 3px rgba(255,255,255,.14),0 30px 90px rgba(0,0,0,.6)}
.wbar{position:absolute;left:0;top:0;right:0;height:64px;background:#24262b;display:flex;align-items:center;gap:10px;padding:0 22px;z-index:2}
.wbar i{width:14px;height:14px;border-radius:50%;display:inline-block}
.wurl{margin-left:18px;height:38px;padding:0 20px;border-radius:19px;background:#15171b;display:flex;align-items:center;font-size:24px;color:rgba(255,255,255,.85)}
#g-img{position:absolute;left:0;top:64px;width:960px}
.cap{position:absolute;left:40px;right:40px;top:1270px;text-align:center;font-size:0;z-index:6}
.cap span{display:inline-block;font-size:62px;font-weight:700;margin:0 .14em;opacity:0;text-shadow:0 4px 18px rgba(0,0,0,.8)}
#cam{position:absolute;left:616px;top:1440px;width:420px;height:420px;border-radius:40px;overflow:hidden;z-index:7;background:#000;
  box-shadow:0 0 0 4px rgba(10,240,240,.55),0 0 40px rgba(10,240,240,.35)}
#cam video{position:absolute;left:-360px;top:22px;width:1000px;height:563px}
.aiv{position:absolute;object-fit:cover;border-radius:28px;opacity:0;z-index:4;box-shadow:0 24px 70px rgba(0,0,0,.55)}
#foot{position:absolute;left:48px;top:1560px;width:530px;font-size:30px;line-height:1.4;color:rgba(255,255,255,.75)}
#foot b{color:#fff}
.endc{position:absolute;inset:0;z-index:20;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:60px;
  background:radial-gradient(800px 700px at 50% 40%,rgba(10,240,240,.14),transparent 70%),#0a0d14}
.endt{font-size:96px;font-weight:700;text-align:center;line-height:1.1}
.endb{display:flex;align-items:center;gap:22px;padding:28px 32px;border-radius:32px;background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.3)}
.endb .ico{width:96px;height:96px;border-radius:24px;display:flex;align-items:center;justify-content:center;font-size:50px;font-weight:700;background:#FF0000;color:#fff}
.endb .ico.ig{background:linear-gradient(135deg,#F58529,#DD2A7B,#8134AF)}
.endk{font-size:30px;color:rgba(255,255,255,.75)}.endh{font-size:46px;font-weight:700}
.btn{font-size:38px;font-weight:700;padding:18px 32px;border-radius:9999px;color:#fff}.btn.red{background:#FF0000}.btn.blue{background:#0095F6}
.endw{font-size:46px;color:rgba(255,255,255,.88)}.endw b{color:#0AF0F0}
''' + CHAR_CSS

page = '''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="vendor/gsap.min.js"></script><style>%s</style></head><body>
<div id="stage" data-composition-id="short" data-start="0" data-duration="%.2f" data-fps="30" data-width="1080" data-height="1920">
<div id="tag"><span>MONEY PLAN · <b class="cyan">PART 1</b> / 50</span></div>
%s
<div id="cam" class="clip" data-start="0" data-duration="%.2f" data-track-index="3"><video id="camv" src="assets/cam/raj.mp4" muted playsinline
  class="clip" data-start="0" data-duration="%.2f" data-track-index="4"></video></div>
<div id="foot">Educational example<br><b>Financial advice nahi</b> · numbers illustrative</div>
<audio id="voice" src="assets/voice.m4a" data-start="0" data-duration="%.2f" data-track-index="10" data-volume="1"></audio>
%s
</div>
<script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
const OB=@@OB@@, NB=@@NB@@;
function W(t){ if(typeof t!=='number') return t; if(t>=10000) return t-10000;
  for(let i=1;i<OB.length;i++){ if(t<=OB[i]) return NB[i-1]+(NB[i]-NB[i-1])*(t-OB[i-1])/(OB[i]-OB[i-1]); }
  return NB[NB.length-1]+(t-OB[OB.length-1]); }
for (const k of ['to','fromTo','set']) { const f=tl[k].bind(tl);
  tl[k]=(...a)=>{ const n=a.length-1; if(typeof a[n]==='number') a[n]=W(a[n]); return f(...a); }; }
function rise(s,t){ tl.fromTo(s,{opacity:0,y:26},{opacity:1,y:0,duration:.4,ease:'power2.out'},t); }
function blink(s,t){ tl.to(s,{scaleY:.1,duration:.07,ease:'none'},t); tl.to(s,{scaleY:1,duration:.09,ease:'none'},t+.07); }
function mood(c,t,m){ tl.to('#'+c+'-'+(m==='sad'?'happy':'sad'),{opacity:0,duration:.2},t); tl.to('#'+c+'-'+m,{opacity:1,duration:.2},t+.1); }
function write(s,t){ tl.to(s,{rotation:-9,duration:.12,yoyo:true,repeat:7,ease:'none'},t); }
function inr(n){ const s=String(Math.round(n)); if(s.length<=3) return s; return s.slice(0,-3).replace(/\\B(?=(\\d{2})+(?!\\d))/g,',')+','+s.slice(-3); }
function count(s,a,b,t,d){ const el=document.querySelector(s); const p={v:a}; el.textContent='₹'+inr(a);
  tl.to(p,{v:b,duration:d||1.4,ease:'power2.out',onUpdate:()=>{ el.textContent='₹'+inr(p.v); }},t); }
tl.fromTo('#cam',{opacity:0,y:40},{opacity:1,y:0,duration:.4,ease:'power2.out'},.1);
tl.to('#cam',{opacity:0,duration:.3},66.6);
tl.to('#foot',{opacity:0,duration:.3},66.6);
%s
tl.to({}, { duration: %.2f }, 0);
window.__timelines["short"] = tl;
</script></body></html>''' % (CSS, DUR, "\n".join(html), FLAT, FLAT, FLAT, sounds, "\n".join(js), DUR)
page = page.replace("@@OB@@", _json.dumps(OB)).replace("@@NB@@", _json.dumps(NB)).replace("@@END@@", "%.2f" % END)
open(OUT, "w", encoding="utf-8").write(page)
print("wrote", OUT, PLAT)
