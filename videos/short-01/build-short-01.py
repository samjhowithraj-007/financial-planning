#!/usr/bin/env python3
"""Paisa Samjho · PART 1/20 SHORT (9:16, 1080x1920): "Salary aati hai… 25 tareekh ko gayab kyun?"

Built on the approved Money Plan Short frame (videos/ep01/build-short.py): animations in the top area, the Hinglish
caption at y 1270, POINT badge left of Raj, Raj head-to-chest in the 484x500 box bottom-right, end card.
Script: C:\\samjhowithraj\\video-research\\money-shorts\\short-01.md (teleprompter "Paisa Samjho 1 (PART 1/20)").

Timing: every time below is a PLAN second (placeholder, written before the take). Once Raj's take is cut,
short/cut-map.json exists and BEATS_ACTUAL (the flat second each beat starts on his voice) re-times everything via M().
Rules (memory shorts-performance-rules): payoff/question in frame 1, <= 45-50 s, captions on, end line
"Part 2 kal, subscribe/follow karo", disclaimer foot note, Every Dawn ducked under the voice (mixed in finish).
Usage: python build-short-01.py yt|ig   -> short/index.html
"""
import os, sys, json
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
PLAT = sys.argv[1] if len(sys.argv) > 1 else "yt"
OUT = os.path.join(HERE, "short", "index.html")
E = lambda s: escape(s, quote=False)

# beat starts (plan seconds): hook, kharche, point 2 (likho), point 3 (dabbe), payoff, site+CTA, end
BEATS_PLAN = [0.0, 4.6, 13.4, 20.4, 33.8, 38.2, 46.0]
CM = os.path.join(HERE, "short", "cut-map.json")
if os.path.exists(CM) and os.path.exists(os.path.join(HERE, "beats.json")):
    BEATS_ACTUAL = json.load(open(os.path.join(HERE, "beats.json")))       # written after the take is transcribed
    FLAT = json.load(open(CM))["flat_duration"]
    HAVE_TAKE = True
else:
    BEATS_ACTUAL, FLAT, HAVE_TAKE = BEATS_PLAN, BEATS_PLAN[-1], False
END = FLAT + 0.03
DUR = round(END + 3.0, 2)
OB, NB = BEATS_PLAN, BEATS_ACTUAL[:len(BEATS_PLAN) - 1] + [END]

def M(t):
    for (a0, b0), (a1, b1) in zip(zip(OB, NB), zip(OB[1:], NB[1:])):
        if t <= a1:
            return b0 + (b1 - b0) * (t - a0) / (a1 - a0)
    return NB[-1] + (t - OB[-1])

html, js = [], []

def scene(sid, a, b, inner, first=False):
    a, b = M(a), M(b)
    html.append('<div id="%s" class="clip scene" data-start="%.2f" data-duration="%.2f" data-track-index="%d">%s</div>'
                % (sid, a, b - a, 1 + len(html) % 2, inner))
    if not first:   # the first scene is visible on frame 1 (payoff/question in frame 1)
        js.append("tl.fromTo('#%s',{opacity:0},{opacity:1,duration:.3},%.2f);" % (sid, a + 10000))
    js.append("tl.to('#%s',{opacity:0,duration:.3},%.2f);" % (sid, b - 0.3 + 10000))

def cap(cid, text, em, a, b):
    a, b = M(a), M(b)
    words = "".join('<span class="w%s">%s</span>' % (" " + c if c else "", E(w))
                    for w, c in [(w, em.get(i, "")) for i, w in enumerate(text.split())])
    html.append('<div id="%s" class="clip cap" data-start="%.2f" data-duration="%.2f" data-track-index="6">%s</div>' % (cid, a, b - a, words))
    js.append("tl.fromTo('#%s .w',{opacity:0,y:20},{opacity:1,y:0,duration:.35,ease:'power2.out',stagger:.05},%.2f);" % (cid, a + 10000))
    js.append("tl.to('#%s',{opacity:0,duration:.25},%.2f);" % (cid, b - 0.25 + 10000))

def pt(pid, n, text, a, b):
    a, b = M(a), M(b)
    html.append('<div id="%s" class="clip pt" data-start="%.2f" data-duration="%.2f" data-track-index="9">'
                '<div class="pn">POINT %d / 3</div><div class="px">%s</div></div>' % (pid, a, b - a, n, text))
    js.append("tl.fromTo('#%s',{opacity:0,x:-30},{opacity:1,x:0,duration:.35,ease:'power2.out'},%.2f);" % (pid, a + 10000.1))
    js.append("tl.to('#%s',{opacity:0,duration:.25},%.2f);" % (pid, b - 0.25 + 10000))

def at(t):      # a plan second as an absolute (flat) GSAP position
    return M(t) + 10000

# ---- A. hook 0 - 4.6: "1 tareekh ₹1 lakh… 25 tareekh ₹0?" (visible on frame 1) ---------------------------------
scene("sA", 0.0, 4.6, '''
<div class="hook" style="opacity:1">1 tareekh <b class="amber">₹1 lakh</b>…<br>25 tareekh <b class="red">₹0?</b></div>
<div id="a-cal" class="cal" style="left:110px;top:520px"><div class="calh">TAREEKH</div>
  <div id="a-d" class="cald">1</div></div>
<div id="a-bank" class="bank" style="left:470px;top:560px"><div class="bankh">BANK BALANCE</div>
  <div id="a-bal" class="bankv amber">₹1,00,000</div><div class="bankbar"><i id="a-bar"></i></div></div>
''', first=True)
js.append("dcount('#a-d',1,25,%.2f,3.2);" % at(0.6))
js.append("count('#a-bal',100000,0,%.2f,3.2);" % at(0.6))
js.append("tl.fromTo('#a-bar',{scaleX:1},{scaleX:0,duration:3.2,ease:'power2.in'},%.2f);" % at(0.6))
js.append("tl.to('#a-bal',{color:'#E0242E',duration:.3},%.2f);" % at(3.6))
cap("cA", "Paisa gaya kahan?", {1: "amber", 2: "amber"}, 0.2, 4.5)

# ---- B. chhote kharche 4.6 - 13.4: ₹50 chai, ₹200 delivery, ₹99 subscription pile up --------------------------
items = [("☕", "Chai", 50, 6.0), ("🛵", "Delivery", 200, 7.4), ("📺", "Subscription", 99, 8.8),
         ("🍪", "Snacks", 80, 9.8), ("🚕", "Auto", 120, 10.6), ("☕", "Chai", 50, 11.3)]
pile = "".join('<div id="b-k%d" class="kchip h" style="left:%dpx;top:%dpx"><span>%s</span>%s <b>₹%d</b></div>'
               % (k, 70 + (k % 2) * 490, 820 - (k // 2) * 140, ic, lab, amt) for k, (ic, lab, amt, _) in enumerate(items))
scene("sB", 4.6, 13.4, '''
<div class="hook" style="top:230px">Chhote kharche,<br><b class="mag">bada bill</b></div>
%s
<div id="b-tot" class="h ktot">Total: <b id="b-totv" class="amber">₹0</b></div>
''' % pile)
run = 0
for k, (ic, lab, amt, t) in enumerate(items):
    js.append("tl.fromTo('#b-k%d',{opacity:0,y:-260,rotation:%d},{opacity:1,y:0,rotation:0,duration:.55,ease:'bounce.out'},%.2f);"
              % (k, (-8, 7, -5, 6, -7, 5)[k], at(t)))
js.append("rise('#b-tot',%.2f);" % at(6.2))
for k, (ic, lab, amt, t) in enumerate(items):
    js.append("count('#b-totv',%d,%d,%.2f,.5);" % (run, run + amt, at(t + 0.3)))
    run += amt
cap("cB1", "₹50 ki chai, ₹200 ka delivery…", {0: "amber", 4: "amber"}, 4.7, 9.0)
cap("cB2", "chupchap bada bill ban jaate hain", {3: "mag", 4: "mag"}, 9.0, 13.3)
pt("p1", 1, "Hisaab sirf <b>dimaag</b> mein = problem", 4.6, 13.4)

# ---- C. 30 din, har kharcha likho 13.4 - 20.4: a diary filling line by line -----------------------------------
lines = [("1 Oct", "Chai", "₹50"), ("1 Oct", "Sabzi", "₹180"), ("2 Oct", "Delivery", "₹200"), ("3 Oct", "Recharge", "₹299"),
         ("4 Oct", "Auto", "₹120"), ("5 Oct", "Chai", "₹50")]
rows = "".join('<div id="c-r%d" class="drow h"><span>%s</span><span>%s</span><b>%s</b></div>' % ((k,) + l) for k, l in enumerate(lines))
scene("sC", 13.4, 20.4, '''
<div class="hook" style="top:230px"><b class="cyan">30 din</b>, har kharcha <b class="amber">likho</b></div>
<div id="c-dia" class="diary h" style="left:110px;top:420px"><div class="dhead">Mera kharcha · 30 din</div>%s
  <div id="c-pen" class="pen"></div></div>
<div id="c-tip" class="h chip2" style="position:absolute;left:180px;top:1130px">₹10 ka bhi · notes ya diary</div>
''' % rows)
js.append("rise('#c-dia',%.2f);" % at(13.6))
for k in range(len(lines)):
    js.append("tl.fromTo('#c-r%d',{opacity:0,x:-20},{opacity:1,x:0,duration:.3},%.2f);" % (k, at(14.3 + k * 0.8)))
    js.append("tl.to('#c-pen',{x:560,y:%d,duration:.75,ease:'none'},%.2f);" % (122 + k * 74, at(14.3 + k * 0.8)))
js.append("rise('#c-tip',%.2f);" % at(18.6))
cap("cC", "Sirf 30 din, har kharcha likho", {1: "cyan", 2: "cyan", 5: "amber"}, 13.5, 20.3)
pt("p2", 2, "<b>30 din</b>, har kharcha likho", 13.4, 20.4)

# ---- D. 3 dabbe 20.4 - 33.8: jars fill ₹58,000 / ₹11,000 / ₹31,000 (Illustrative) -----------------------------
jars = [("Zaroori", 58000, .58, "#F5F1E8", 23.2), ("Saal ke kharche\n+ masti", 11000, .11 * 2.2, "#FFB904", 25.6),
        ("Future", 31000, .31 * 1.7, "#0AF0F0", 28.0)]
jh = ""
for k, (lab, amt, fill, col, t) in enumerate(jars):
    x = 70 + k * 320
    jh += ('<div id="d-j%d" class="jar h" style="left:%dpx;top:520px"><div class="jarlid"></div><div class="jarbody">'
           '<div id="d-f%d" class="jarfill" style="height:%dpx;background:%s"></div></div>'
           '<div id="d-v%d" class="jarv" style="color:%s">₹0</div><div class="jarl">%s</div></div>'
           % (k, x, k, int(min(1, fill) * 400), col, k, col if k else "#fff", E(lab).replace("\n", "<br>")))
scene("sD", 20.4, 33.8, '''
<div class="hook" style="top:230px"><b class="amber">3 dabbe</b> mein daalo</div>
<div class="h verm" id="d-verm">Verma family · ₹1,00,000 / mahina</div>
%s
<div id="d-ill" class="h illus">Illustrative</div>
''' % jh)
js.append("rise('#d-verm',%.2f);" % at(21.0))
for k, (lab, amt, fill, col, t) in enumerate(jars):
    js.append("rise('#d-j%d',%.2f);" % (k, at(21.4 + k * 0.3)))
    js.append("tl.fromTo('#d-f%d',{scaleY:0},{scaleY:1,duration:1.4,ease:'power2.out'},%.2f);" % (k, at(t)))
    js.append("count('#d-v%d',0,%d,%.2f,1.4);" % (k, amt, at(t)))
js.append("rise('#d-ill',%.2f);" % at(23.4))
cap("cD1", "Zaroori ₹58,000 · Saal ₹11,000", {1: "amber", 3: "amber"}, 20.5, 27.4)
cap("cD2", "Future ₹31,000: control aata hai", {0: "cyan", 1: "cyan"}, 27.4, 33.7)
pt("p3", 3, "<b>3 dabbe</b>: zaroori · saal · future", 20.4, 33.8)

# ---- E. payoff 33.8 - 38.2 --------------------------------------------------------------------------------------
scene("sE", 33.8, 38.2, '''
<div id="e-t" class="h big" style="left:60px;top:520px;width:960px;text-align:center">Jo kharcha <b class="cyan">dikhta</b> hai,<br>wahi <b class="amber">kam</b> hota hai</div>
<div id="e-eye" class="h" style="left:0;right:0;top:340px;text-align:center;font-size:150px">👀</div>
''')
js += ["rise('#e-eye',%.2f);" % at(33.9), "rise('#e-t',%.2f);" % at(34.2)]
cap("cE", "Yaad rakhna!", {}, 33.9, 38.1)

# ---- F. website + CTA 38.2 - 46.0 ------------------------------------------------------------------------------
scene("sF", 38.2, 46.0, '''
<div id="f-t" class="h big" style="left:60px;top:300px;width:960px;text-align:center">Free <b class="cyan">Money Planner</b></div>
<div id="f-win" class="h webwin" style="left:60px;top:440px"><div class="wbar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i>
  <i style="background:#28c840"></i><span class="wurl">🔒&nbsp;<b>paisasamjhoraj.com</b>/#planner</span></div>
  <div class="wview"><img id="f-img" src="assets/img/planner-top.jpg" alt=""><div id="f-hl" class="hl"></div></div></div>
''')
js += ["rise('#f-t',%.2f);" % at(38.4), "rise('#f-win',%.2f);" % at(38.7),
       "tl.fromTo('#f-hl',{scaleX:0},{scaleX:1,duration:.5,ease:'power2.out'},%.2f);" % at(39.6),
       "tl.to('#f-img',{y:-420,duration:4,ease:'power1.inOut'},%.2f);" % at(41.2),
       "tl.to('#f-hl',{opacity:0,duration:.3},%.2f);" % at(41.0)]
cap("cF1", "Apne numbers daalo, free!", {3: "cyan"}, 38.3, 42.0)
cap("cF2", "paisasamjhoraj.com", {0: "cyan"}, 42.0, 45.9)
_cta = "Part 2 kal 👉<small>Subscribe karo · zaroorat ya pressure?</small>" if PLAT == "yt" else \
       "Part 2 kal 👉<small>Follow karo · zaroorat ya pressure?</small>"
html.append('<div id="p6" class="clip cta" data-start="%.2f" data-duration="%.2f" data-track-index="9">%s</div>' % (M(41.6), M(46.0) - M(41.6), _cta))
js.append("tl.fromTo('#p6',{opacity:0,scale:.9},{opacity:1,scale:1,duration:.35,ease:'back.out(1.6)'},%.2f);" % (at(41.6) + 0.1))
js.append("tl.fromTo('#p6',{scale:1},{scale:1.05,duration:.3,yoyo:true,repeat:3,ease:'power1.inOut'},%.2f);" % at(42.6))

# ---- G. end card (3 s after his last word) -----------------------------------------------------------------------
btn = '<span class="btn red">Subscribe</span>' if PLAT == "yt" else '<span class="btn blue">Follow</span>'
who = '<span class="ico">▶</span><div><div class="endk">YouTube</div><div class="endh">@SamjhowithRaj</div></div>' if PLAT == "yt" else \
      '<span class="ico ig">◎</span><div><div class="endk">Instagram · Facebook</div><div class="endh">@samjhowithraj</div></div>'
html.append('''<div id="sH" class="clip endc" data-start="%.2f" data-duration="3.00" data-track-index="8">
<div class="endt">Part 2 <b class="cyan">kal</b>:<br>zaroorat ya <b class="amber">pressure?</b></div>
<div id="h-b" class="endb">%s%s</div>
<div class="endw">Free Money Planner: <b>paisasamjhoraj.com</b></div></div>''' % (END, who, btn))
js += ["tl.fromTo('#sH',{opacity:0},{opacity:1,duration:.35},%.2f);" % (END + 10000), "rise('#h-b',%.2f);" % (END + 10000.3),
       "tl.fromTo('#h-b .btn',{scale:1},{scale:1.1,duration:.22,yoyo:true,repeat:5,ease:'power1.inOut'},%.2f);" % (END + 10000.8)]

cam = ('<video id="camv" src="assets/cam/raj.mp4" muted playsinline class="clip" data-start="0" data-duration="%.2f" data-track-index="4"></video>' % FLAT
       if HAVE_TAKE else '<div class="camph">Raj · your take<br>goes here</div>')

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
.h{opacity:0}.cyan{color:#0AF0F0}.amber{color:#FFB904}.mag{color:#E04CF0}.red{color:#FF4D4D}
#tag{position:absolute;left:0;right:0;top:110px;display:flex;justify-content:center;z-index:9}
#tag span{padding:14px 30px;border-radius:9999px;background:rgba(255,255,255,.1);border:3px solid rgba(255,255,255,.4);font-size:32px;font-weight:700;letter-spacing:.06em}
.hook{left:60px;right:60px;top:210px;text-align:center;font-size:76px;font-weight:700;line-height:1.1}
.big{font-size:84px;font-weight:700;line-height:1.15}
.cal{width:300px;height:330px;border-radius:30px;background:#f4f6fa;color:#111;overflow:hidden;box-shadow:0 24px 70px rgba(0,0,0,.55)}
.calh{height:84px;background:#FFB904;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:700;letter-spacing:.08em}
.cald{text-align:center;font-size:200px;font-weight:700;line-height:240px}
.bank{width:520px;padding:30px 36px;border-radius:30px;background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.35)}
.bankh{font-size:30px;font-weight:700;letter-spacing:.08em;color:rgba(255,255,255,.75)}
.bankv{font-size:96px;font-weight:700;line-height:1.2}
.bankbar{height:26px;border-radius:13px;background:rgba(255,255,255,.12);overflow:hidden;margin-top:14px}
.bankbar i{display:block;height:100%;background:linear-gradient(90deg,#0AF0F0,#FFB904);transform-origin:0 50%}
.kchip{display:flex;align-items:center;gap:12px;width:450px;padding:24px 22px;border-radius:26px;background:#f4f6fa;color:#111;
  font-size:38px;font-weight:700;box-shadow:0 18px 50px rgba(0,0,0,.5)}
.kchip span{font-size:56px}.kchip b{margin-left:auto;color:#b37400}
.ktot{left:60px;right:60px;top:1080px;text-align:center;font-size:72px;font-weight:700}
.diary{width:860px;height:640px;padding:36px 46px;border-radius:24px;background:#F5F1E8;color:#1b1a17;box-shadow:0 30px 90px rgba(0,0,0,.55);
  background-image:repeating-linear-gradient(transparent 0 73px,rgba(70,110,170,.25) 73px 75px);background-position:0 46px}
.dhead{font-size:46px;font-weight:700;color:#7a2c2c;border-bottom:5px solid #FFB904;display:inline-block;margin-bottom:22px}
.drow{display:grid;grid-template-columns:1fr 1.4fr .8fr;font-size:44px;height:74px;align-items:center;color:#1b2a4a}
.drow b{text-align:right;color:#9a3b00}
.pen{position:absolute;left:40px;top:110px;width:160px;height:20px;border-radius:10px;background:#FFB904;transform:rotate(-35deg);box-shadow:0 6px 16px rgba(0,0,0,.35)}
.chip2{display:inline-block;padding:16px 28px;border-radius:16px;background:rgba(17,17,17,.6);border:2px solid rgba(255,255,255,.25);font-size:44px;font-weight:700}
.verm{left:60px;right:60px;top:400px;text-align:center;font-size:40px;color:rgba(255,255,255,.8)}
.jar{width:300px;text-align:center}
.jarlid{width:200px;height:34px;margin:0 auto;border-radius:12px;background:#7d8590}
.jarbody{position:relative;width:260px;height:420px;margin:0 auto;border:8px solid rgba(255,255,255,.75);border-top:none;border-radius:0 0 50px 50px;overflow:hidden;background:rgba(255,255,255,.05)}
.jarfill{position:absolute;left:0;right:0;bottom:0;transform-origin:50% 100%;opacity:.9}
.jarv{font-size:60px;font-weight:700;margin-top:18px}
.jarl{font-size:34px;font-weight:700;color:rgba(255,255,255,.85);line-height:1.15;margin-top:6px}
.illus{left:770px;top:450px;padding:10px 20px;border-radius:12px;background:#FFB904;color:#111;font-size:30px;font-weight:700;transform:rotate(4deg)}
.webwin{width:960px;height:720px;border-radius:22px;overflow:hidden;background:#141414;box-shadow:0 0 0 3px rgba(255,255,255,.14),0 30px 90px rgba(0,0,0,.6)}
.wbar{position:absolute;left:0;top:0;right:0;height:64px;background:#24262b;display:flex;align-items:center;gap:10px;padding:0 22px;z-index:2}
.wbar i{width:14px;height:14px;border-radius:50%;display:inline-block}
.wurl{margin-left:18px;height:38px;padding:0 20px;border-radius:19px;background:#15171b;display:flex;align-items:center;font-size:24px;color:rgba(255,255,255,.85)}
.wview{position:absolute;left:0;right:0;top:64px;bottom:0;overflow:hidden}
#f-img{position:absolute;left:-150px;top:0;width:1440px}
.hl{position:absolute;left:255px;top:62px;width:151px;height:62px;border-radius:10px;background:rgba(255,225,77,.38);transform-origin:0 50%;
  box-shadow:0 0 0 3px rgba(255,225,77,.9)}
.cap{position:absolute;left:40px;right:40px;top:1270px;text-align:center;font-size:0;z-index:6}
.cap span{display:inline-block;font-size:62px;font-weight:700;margin:0 .14em;opacity:0;text-shadow:0 4px 18px rgba(0,0,0,.8)}
#cam{position:absolute;left:556px;top:1380px;width:484px;height:500px;border-radius:40px;overflow:hidden;z-index:7;background:#000;
  box-shadow:0 0 0 4px rgba(10,240,240,.55),0 0 40px rgba(10,240,240,.35)}
#cam video{position:absolute;left:0;top:0;width:484px;height:500px}
.camph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;font-size:40px;color:rgba(255,255,255,.45);
  background:repeating-linear-gradient(45deg,#0d1117 0 24px,#111723 24px 48px)}
#foot{position:absolute;left:48px;top:1790px;width:480px;font-size:24px;line-height:1.35;color:rgba(255,255,255,.65)}
#foot b{color:#fff}
.pt{position:absolute;left:48px;top:1390px;width:480px;padding:22px 26px;border-radius:26px;background:rgba(255,255,255,.07);border:3px solid rgba(10,240,240,.55);z-index:6;opacity:0}
.pt .pn{font-size:30px;font-weight:700;color:#0AF0F0;letter-spacing:.06em}
.pt .px{font-size:44px;font-weight:700;line-height:1.12;margin-top:8px}
.pt .px b{color:#FFB904}
.cta{position:absolute;left:48px;top:1390px;width:480px;padding:22px 26px;border-radius:26px;background:#FF0000;z-index:6;opacity:0;font-size:44px;font-weight:700;line-height:1.15}
.cta small{display:block;font-size:26px;font-weight:500;opacity:.9;margin-top:6px}
.endc{position:absolute;inset:0;z-index:20;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:60px;
  background:radial-gradient(800px 700px at 50% 40%,rgba(10,240,240,.14),transparent 70%),#0a0d14}
.endt{font-size:92px;font-weight:700;text-align:center;line-height:1.1}
.endb{display:flex;align-items:center;gap:22px;padding:28px 32px;border-radius:32px;background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.3)}
.endb .ico{width:96px;height:96px;border-radius:24px;display:flex;align-items:center;justify-content:center;font-size:50px;font-weight:700;background:#FF0000;color:#fff}
.endb .ico.ig{background:linear-gradient(135deg,#F58529,#DD2A7B,#8134AF)}
.endk{font-size:30px;color:rgba(255,255,255,.75)}.endh{font-size:46px;font-weight:700}
.btn{font-size:38px;font-weight:700;padding:18px 32px;border-radius:9999px;color:#fff}.btn.red{background:#FF0000}.btn.blue{background:#0095F6}
.endw{font-size:44px;color:rgba(255,255,255,.88)}.endw b{color:#0AF0F0}
'''

page = '''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="vendor/gsap.min.js"></script><style>%s</style></head><body>
<div id="stage" data-composition-id="short" data-start="0" data-duration="%.2f" data-fps="30" data-width="1080" data-height="1920">
<div id="tag"><span>PAISA SAMJHO · <b class="cyan">PART 1</b> / 20</span></div>
%s
<div id="cam">%s</div>
<div id="foot">Financial education, <b>advice nahi</b><br>Verma family fictional (AI) · illustrative</div>
%s
</div>
<script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
function W(t){ return (typeof t==='number' && t>=10000) ? t-10000 : t; }
for (const k of ['to','fromTo','set']) { const f=tl[k].bind(tl);
  tl[k]=(...a)=>{ const n=a.length-1; if(typeof a[n]==='number') a[n]=W(a[n]); return f(...a); }; }
function rise(s,t){ tl.fromTo(s,{opacity:0,y:26},{opacity:1,y:0,duration:.4,ease:'power2.out'},t); }
function inr(n){ const s=String(Math.round(n)); if(s.length<=3) return s; return s.slice(0,-3).replace(/\\B(?=(\\d{2})+(?!\\d))/g,',')+','+s.slice(-3); }
function count(s,a,b,t,d){ const el=document.querySelector(s); const p={v:a}; el.textContent='₹'+inr(a);
  tl.to(p,{v:b,duration:d||1.4,ease:'power2.out',onUpdate:()=>{ el.textContent='₹'+inr(p.v); }},t); }
function dcount(s,a,b,t,d){ const el=document.querySelector(s); const p={v:a};
  tl.to(p,{v:b,duration:d,ease:'power1.in',onUpdate:()=>{ el.textContent=String(Math.round(p.v)); }},t); }
tl.to('#cam',{opacity:0,duration:.3},%.2f);
tl.to('#foot',{opacity:0,duration:.3},%.2f);
%s
tl.to({}, { duration: %.2f }, 0);
window.__timelines["short"] = tl;
</script></body></html>''' % (CSS, DUR, "\n".join(html), cam,
       ('<audio id="voice" src="assets/voice.m4a" data-start="0" data-duration="%.2f" data-track-index="10" data-volume="1"></audio>' % FLAT) if HAVE_TAKE else "",
       END + 10000 - 0.2, END + 10000 - 0.2, "\n".join(js), DUR)
open(OUT, "w", encoding="utf-8").write(page)
print("wrote", OUT, PLAT, "take" if HAVE_TAKE else "placeholder timings", "%.1f s" % DUR)
