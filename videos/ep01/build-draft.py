#!/usr/bin/env python3
"""Money Plan Part 1, long video DRAFT: writes draft/index.html (1920x1080, 7:00).

Raj stands full body in the left third (a placeholder until the recording exists); every animation lives in the free
right side (x 940-1860) so he is never covered or cropped. All times are the PLANNED scene times from the episode
storyboard; after the recording, T is re-timed to Raj's words. House style: DM Sans 700, cyan key words, amber money,
magenta punchlines, 0.4 s soft entrances, no bounces, Indian digit grouping (12,00,000).

Usage: python build-draft.py   (then: npx --yes hyperframes@0.8.154 check draft)
"""
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "draft", "index.html")
DUR = 420.0

# Scene windows (seconds), from the storyboard in episodes/EP01-*.md
T = {"hook": (0.0, 15.0), "intro": (15.0, 30.0), "family": (30.0, 75.0), "today": (75.0, 105.0),
     "budget": (105.0, 225.0), "goals": (225.0, 285.0), "jama": (285.0, 320.0), "dabba": (320.0, 345.0),
     "kaam": (345.0, 400.0), "end": (400.0, 420.0)}
CHAPTERS = ["Verma family", "Aaj ka paisa", "₹1 lakh kahan jaata hai", "Goals aur deadline", "Sirf jama rakam",
            "Har goal ka dabba", "Aapka kaam"]

L, W = 940, 920          # the animation side: left edge and width
CX = L + W // 2          # its centre

html, js = [], []

def E(s):
    return escape(s, quote=False)

def em(text, idx, cls):
    """Words of `text`; the word numbers in idx get class cls."""
    return " ".join('<span class="%s">%s</span>' % (cls, E(w)) if i in idx else E(w)
                    for i, w in enumerate(text.split()))

def line(sid, text, idx, cls, t_in, t_out, top=930):
    """Lower line (format 2), centred under the animation side; words rise staggered."""
    words = "".join('<span class="w%s">%s</span>' % (" " + cls if i in idx else "", E(w))
                    for i, w in enumerate(text.split()))
    html.append('<div id="%s" class="ll" style="top:%dpx">%s</div>' % (sid, top, words))
    js.append("tl.fromTo('#%s .w',{opacity:0,y:26},{opacity:1,y:0,duration:.4,ease:'power2.out',stagger:.055},%.2f);"
              % (sid, t_in))
    js.append("tl.to('#%s',{opacity:0,duration:.35,ease:'power2.in'},%.2f);" % (sid, t_out))

def tag(sid, n, t_in):
    """Progress tag (format 9b): chapter n of 7, held 5 s."""
    pips = "".join('<i class="pip%s"></i>' % (" on" if k < n else "") for k in range(len(CHAPTERS)))
    html.append('<div id="%s" class="tag h"><span class="dot"></span><span>%d · %s</span><span class="pips">%s</span></div>'
                % (sid, n, E(CHAPTERS[n - 1]), pips))
    js.append("rise('#%s',%.2f); out('#%s',%.2f);" % (sid, t_in, sid, t_in + 5.0))

def scene_open(key, track):
    a, b = T[key]
    html.append('<div id="sc-%s" class="scene clip" data-start="%.2f" data-duration="%.2f" data-track-index="%d">'
                % (key, a, b - a, track))
    js.append("tl.fromTo('#sc-%s',{opacity:0},{opacity:1,duration:.4,ease:'power2.out'},%.2f);" % (key, a))
    if b < DUR:
        js.append("tl.to('#sc-%s',{opacity:0,duration:.35,ease:'power2.in'},%.2f);" % (key, b - 0.4))

def scene_close():
    html.append("</div>")

def chaching(sid, t):
    html.append('<audio id="%s" src="assets/sfx/chaching.mp3" data-start="%.2f" data-duration="1.4" '
                'data-track-index="12" data-volume="0.16"></audio>' % (sid, t))

money_sounds = []
roots = []         # root-level elements: registry sub-compositions, video slots (absolute times)
broll_slots = []   # (id, what the clip shows, in, out) -> BROLL.md

def block(bid, src, cid, t_in, t_out, box, values, track):
    """A HyperFrames registry block mounted inside the studio screen (box = left, top, width, height)."""
    import json as _j
    x, y, w, h = box
    roots.append("<div id=\"%s\" class=\"clip\" data-composition-id=\"%s\" data-composition-src=\"%s\" "
                 "data-start=\"%.2f\" data-duration=\"%.2f\" data-track-index=\"%d\" "
                 "data-variable-values='%s' style=\"position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;z-index:6\"></div>"
                 % (bid, cid, src, t_in, t_out - t_in, track, _j.dumps(values, ensure_ascii=False), x, y, w, h))

def broll(bid, what, t_in, t_out):
    """An explanation cutaway on the studio screen: AI or stock video goes here (placeholder in the draft)."""
    broll_slots.append((bid, what, t_in, t_out))
    roots.append('<div id="%s" class="clip bslot" data-layout-allow-occlusion data-start="%.2f" data-duration="%.2f" data-track-index="5">'
                 '<div class="btag">AI / STOCK VIDEO</div><div class="bwhat">%s</div></div>' % (bid, t_in, t_out - t_in, E(what)))
    js.append("tl.fromTo('#%s',{opacity:0},{opacity:1,duration:.3},%.2f); tl.to('#%s',{opacity:0,duration:.3},%.2f);"
              % (bid, t_in, bid, t_out - 0.3))

# ---------------------------------------------------------------------------------------------- 1. Hook
scene_open("hook", 1)
html.append('''
<div id="h-cal" class="card h" style="left:%dpx;top:230px;width:290px;height:330px;padding:0;overflow:hidden">
  <div style="height:78px;background:#FFB904;color:#111;font-size:34px;font-weight:700;display:flex;align-items:center;justify-content:center;letter-spacing:.08em">TAREEKH</div>
  <div id="h-d1" style="position:absolute;left:0;right:0;top:100px;text-align:center;font-size:190px;font-weight:700;line-height:1">1</div>
  <div id="h-d25" class="h" style="position:absolute;left:0;right:0;top:100px;text-align:center;font-size:190px;font-weight:700;line-height:1">25</div>
</div>
<div id="h-amt" class="h big amber" style="left:%dpx;top:250px;font-size:116px">₹0</div>
<div id="h-aayi" class="h" style="left:%dpx;top:395px;font-size:46px;font-weight:700">Salary aayi!</div>
<div id="h-q1" class="pill h" style="left:%dpx;top:300px">College fees<b class="amber">?</b></div>
<div id="h-q2" class="pill h" style="left:%dpx;top:420px">Apna ghar<b class="amber">?</b></div>
<div id="h-q3" class="pill h" style="left:%dpx;top:540px">Retirement<b class="amber">?</b></div>
''' % (L + 20, L + 360, L + 365, L + 365, L + 365, L + 365))
js += ["rise('#h-cal',0.3);", "rise('#h-amt',1.1);", "count('#h-amt',0,100000,1.2,1.4);", "rise('#h-aayi',5.2);",
       "tl.to('#h-d1',{opacity:0,duration:.35},7.0);", "tl.fromTo('#h-d25',{opacity:0},{opacity:1,duration:.4},7.1);",
       "out('#h-amt',7.0); out('#h-aayi',7.0);",
       "rise('#h-q1',7.6); rise('#h-q2',8.3); rise('#h-q3',9.0);"]
money_sounds.append(2.6)
broll("v-hook", "Month-end: a father checks his bank SMS, worried", 9.7, 11.5)
line("h-l1", "Shuruaat kahan se karein?", {1, 2}, "cyan", 11.6, 14.4)
scene_close()

# ---------------------------------------------------------------------------------------------- 2. Series intro
scene_open("intro", 2)
dots = "".join('<i class="sd%s"></i>' % (" first" if k == 0 else "") for k in range(50))
html.append('''
<div id="i-eye" class="h eyebrow" style="left:%dpx;top:250px;width:%dpx;text-align:center">PART 1 / 50</div>
<div id="i-t1" class="h title" style="left:%dpx;top:330px;width:%dpx;text-align:center;font-size:74px">Middle-Class Family Ka</div>
<div id="i-t2" class="h title cyan" style="left:%dpx;top:425px;width:%dpx;text-align:center;font-size:112px">Money Plan</div>
<div id="i-sub" class="h" style="left:%dpx;top:560px;width:%dpx;text-align:center;font-size:38px;color:rgba(255,255,255,.82)">Budget se investment tak, ghar se retirement tak</div>
<div id="i-dots" class="h" style="left:%dpx;top:660px;width:%dpx;text-align:center;font-size:0">%s</div>
''' % (L, W, L, W, L, W, L, W, L + 160, W - 320, dots))
js += ["rise('#i-eye',15.3);", "rise('#i-t1',15.6);", "rise('#i-t2',16.0);", "rise('#i-sub',17.2);",
       "rise('#i-dots',18.4);",
       "tl.fromTo('#i-dots .first',{backgroundColor:'rgba(255,255,255,.18)',boxShadow:'0 0 0 rgba(10,240,240,0)'},"
       "{backgroundColor:'#0AF0F0',boxShadow:'0 0 18px rgba(10,240,240,.9)',duration:.4},19.2);"]
scene_close()

# ---------------------------------------------------------------------------------------------- 3. Verma family
scene_open("family", 1)
tag("f-tag", 1, 30.2)
people = [("A", "Amit", "35", "#0AF0F0", 36.0), ("N", "Neha", "33", "#0AF0F0", 38.0),
          ("Aa", "Aarav", "8 saal", "#FFB904", 41.0), ("P", "Pihu", "4 saal", "#FFB904", 43.0)]
html.append('<div id="f-title" class="h title" style="left:%dpx;top:170px;width:%dpx;text-align:center">Verma family</div>' % (L, W))
html.append('<div id="f-where" class="h" style="left:%dpx;top:275px;width:%dpx;text-align:center;font-size:38px;color:rgba(255,255,255,.85)">'
            '<span class="cyan">●</span> Lucknow · kiraye ka 2BHK</div>' % (L, W))
for k, (ini, name, age, col, t) in enumerate(people):
    x = L + 40 + k * 215
    html.append('<div id="f-p%d" class="h" style="left:%dpx;top:370px;width:200px;text-align:center">'
                '<div class="av" style="border-color:%s">%s</div>'
                '<div style="font-size:40px;font-weight:700;margin-top:16px">%s</div>'
                '<div style="font-size:30px;color:rgba(255,255,255,.75)">%s</div></div>' % (k, x, col, ini, name, age))
    js.append("rise('#f-p%d',%.2f);" % (k, t))
html.append('<div id="f-inc" class="card h" style="left:%dpx;top:660px;width:640px;height:150px;text-align:center;padding-top:14px">'
            '<div id="f-incv" class="amber" style="font-size:78px;font-weight:700;line-height:1.1">₹0</div>'
            '<div style="font-size:28px;color:rgba(255,255,255,.78)">har mahine · ghar ki kul take-home</div></div>' % (CX - 320))
html.append('<div id="f-ex" class="chip h" style="left:%dpx;top:836px;width:520px">Example family ·&nbsp;<b class="mag">asli nahi</b></div>' % (CX - 260))
broll("v-lko", "Lucknow apartment buildings, evening", 33.6, 36.0)
js += ["rise('#f-title',31.0);", "rise('#f-where',33.0);", "rise('#f-inc',48.0);",
       "count('#f-incv',0,100000,48.2,1.4);", "rise('#f-ex',56.0);", "out('#f-ex',59.6);"]
money_sounds.append(49.6)
line("f-l1", "Bilkul hamari-aapki jaisi family", {1}, "cyan", 60.0, 66.0)
scene_close()

# ---------------------------------------------------------------------------------------------- 4. Aaj ka paisa
scene_open("today", 2)
tag("t-tag", 2, 75.2)
tiles = [("t-s", "Savings account", "₹0", 76.5, 60000), ("t-e", "Amit ka EPF", "₹0", 78.5, 400000),
         ("t-h", "Health cover", "Company policy", 80.5, None), ("t-k", "Karz", "₹0", 82.5, None)]
for k, (tid, lab, val, t, n) in enumerate(tiles):
    x = L + 20 + (k % 2) * 450
    y = 170 + (k // 2) * 200
    vcls = "amber" if n is not None else ("cyan" if tid == "t-k" else "")
    check = ' <span class="cyan" style="font-size:32px">✓ koi karz nahi</span>' if tid == "t-k" else ""
    html.append('<div id="%s" class="card h" style="left:%dpx;top:%dpx;width:430px;height:176px;padding:22px 28px">'
                '<div style="font-size:28px;color:rgba(255,255,255,.75)">%s</div>'
                '<div id="%sv" class="%s" style="font-size:%dpx;font-weight:700;margin-top:6px;white-space:nowrap">%s%s</div></div>'
                % (tid, x, y, E(lab), tid, vcls, 64 if n is not None or tid == "t-k" else 52, val, check))
    js.append("rise('#%s',%.2f);" % (tid, t))
    if n is not None:
        js.append("count('#%sv',0,%d,%.2f,1.2);" % (tid, n, t + 0.2))
js.append("tl.to('#t-e,#t-h,#t-k',{opacity:.38,duration:.4},88.0);")
html.append('''
<div id="t-cmp" class="h" style="left:%dpx;top:600px;width:880px">
  <div class="rowlab">Savings <span class="amber">₹60,000</span></div>
  <div class="track"><div id="t-b1" class="bar" style="width:%dpx;background:#FFB904"></div></div>
  <div class="rowlab" style="margin-top:22px">1 mahine ka zaroori kharch <span class="amber">₹58,000</span></div>
  <div class="track"><div id="t-b2" class="bar" style="width:%dpx;background:rgba(255,255,255,.85)"></div></div>
</div>
<div id="t-one" class="chip h" style="left:%dpx;top:830px;width:460px"><b class="amber">≈ sirf 1 mahina</b></div>
''' % (L + 20, int(860 * 60 / 60), int(860 * 58 / 60), CX - 230))
js += ["rise('#t-cmp',88.4);", "grow('#t-b1',88.8);", "grow('#t-b2',89.6);", "rise('#t-one',91.0);", "out('#t-one',94.6);"]
line("t-l1", "Buffer sirf ek mahine ka", {2, 3}, "amber", 95.0, 104.0)
scene_close()

# ---------------------------------------------------------------------------------------------- 5. ₹1 lakh kahan jaata hai
scene_open("budget", 1)
tag("b-tag", 3, 105.2)
html.append('<div id="b-title" class="h" style="left:%dpx;top:150px;width:%dpx;text-align:center;font-size:56px;font-weight:700">'
            '<span class="amber">₹1,00,000</span> har mahine</div>' % (L, W))
BW = 880
segs = [("b-s1", 58, "rgba(255,255,255,.88)", 107.5), ("b-s2", 6, "#FFB904", 151.0),
        ("b-s3", 5, "rgba(255,185,4,.55)", 158.0), ("b-s4", 31, "#0AF0F0", 181.0)]
x = 0
bar = []
for sid, pct, col, t in segs:
    w = round(BW * pct / 100)
    bar.append('<div id="%s" class="seg" style="left:%dpx;width:%dpx;background:%s"></div>' % (sid, x, w - 4, col))
    js.append("grow('#%s',%.2f,.7);" % (sid, t))
    x += w
html.append('<div id="b-bar" class="h" style="left:%dpx;top:250px;width:%dpx;height:84px;border-radius:16px;'
            'background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.18)">%s</div>' % (L + 20, BW, "".join(bar)))
html.append('<div id="b-lab1" class="h seglab" style="left:%dpx;top:350px">Zaroori <span class="amber">₹58,000</span> · 58%%</div>' % (L + 20))
html.append('<div id="b-lab4" class="h seglab" style="left:%dpx;top:350px;width:%dpx;text-align:right">Future <span class="cyan">₹31,000</span> · 31%%</div>' % (L + 20, BW))
js += ["rise('#b-title',105.4);", "rise('#b-bar',106.6);", "rise('#b-lab1',132.0);"]
# essentials: a white data card (Pranjal style), the yellow marker moves to each row as it is said
ess = [("Kiraya", 18000, 110.0), ("Ration", 14000, 114.0), ("Bills", 4000, 118.0),
       ("Transport", 6000, 121.0), ("School", 10000, 124.0), ("Health", 6000, 128.0), ("Zaroori total", 58000, 132.0)]
rows_html = ""
for k, (lab, amt, t) in enumerate(ess):
    total = k == len(ess) - 1
    rows_html += ('<div class="drow%s"><div id="b-hl%d" class="dhl"></div><span>%s</span><span>₹%s</span></div>'
                  % (" dtot" if total else "", k, lab, format(amt, ",")))
    nxt = ess[k + 1][1 + 1] if not total else 148.6
    js.append("tl.fromTo('#b-hl%d',{scaleX:0,opacity:1},{scaleX:1,duration:.35,ease:'power2.out'},%.2f);" % (k, t))
    js.append("tl.to('#b-hl%d',{opacity:0,duration:.25},%.2f);" % (k, nxt - 0.1))
html.append('<div id="b-data" class="h dcard" style="left:%dpx;top:400px"><div class="dhead"><span>Verma family · har mahine</span>'
            '<span>₹</span></div>%s</div>' % (L + 20, rows_html))
js += ["rise('#b-data',109.4);", "out('#b-data',149.0);"]
line("b-l1", "Har mahine ka pakka kharcha", {3}, "cyan", 138.0, 148.0)
# annual + fun
html.append('<div id="b-ann" class="card h" style="left:%dpx;top:440px;width:880px;height:170px;padding:22px 30px">'
            '<div style="font-size:46px;font-weight:700">Saal bhar ke kharche <span class="amber">₹6,000</span></div>'
            '<div style="font-size:32px;color:rgba(255,255,255,.78);margin-top:10px">Diwali · admission · shaadi ke gifts</div></div>' % (L + 20))
html.append('<div id="b-fun" class="card h" style="left:%dpx;top:640px;width:880px;height:110px;padding:22px 30px">'
            '<div style="font-size:46px;font-weight:700">Masti <span class="amber">₹5,000</span></div></div>' % (L + 20))
js += ["rise('#b-ann',152.0);", "rise('#b-fun',159.0);", "out('#b-ann,#b-fun',179.0);"]
broll("v-diwali", "Family shopping for Diwali; school admission desk", 165.0, 170.0)
line("b-l2", "Ye har saal aate hain", {2, 3}, "cyan", 165.0, 178.0)
# future: three pots, heights by amount
pots = [("Emergency", 8000, 186.0), ("Retirement", 13000, 190.0), ("Padhai", 10000, 194.0)]
for k, (lab, amt, t) in enumerate(pots):
    x = L + 60 + k * 290
    h = round(260 * amt / 13000)
    html.append('<div id="b-p%d" class="h" style="left:%dpx;top:430px;width:230px;height:400px">'
                '<div class="jar"><div id="b-pf%d" class="jarfill" style="height:%dpx"></div></div>'
                '<div style="text-align:center;font-size:34px;font-weight:700;margin-top:14px">%s</div>'
                '<div class="amber" style="text-align:center;font-size:40px;font-weight:700">₹%s</div></div>'
                % (k, x, k, h, lab, format(amt, ",")))
    js.append("rise('#b-p%d',%.2f); tl.fromTo('#b-pf%d',{scaleY:0},{scaleY:1,duration:.8,ease:'power2.out'},%.2f);" % (k, t, k, t + 0.2))
js.append("rise('#b-lab4',182.0);")
js.append("out('#b-p0,#b-p1,#b-p2,#b-bar,#b-lab1,#b-lab4,#b-title',198.8);")
block("x-donut", "compositions/components/chart-story.html", "chart-story", 199.2, 224.6, (L + 20, 130, 880, 760),
      {"type": "donut", "data": "58, 6, 5, 31", "labels": "Zaroori, Saal bhar, Masti, Future", "emphasize": 3,
       "unit": "%", "accent": "green", "exit": "none"}, 7)
line("b-l3", "31% bachat: achha start hai", {0, 1}, "cyan", 200.0, 210.0)
html.append('<div id="b-q" class="chip h" style="left:%dpx;top:920px;width:560px">Par kya ye&nbsp;<b class="mag">kaafi</b>&nbsp;hai?</div>' % (CX - 280))
js += ["rise('#b-q',212.0);", "out('#b-q',223.8);"]
scene_close()

# ---------------------------------------------------------------------------------------------- 6. Goals aur deadline
scene_open("goals", 2)
tag("g-tag", 4, 225.2)
AX0, AX1, AY = L + 60, L + 860, 640
def gx(years):
    return AX0 + (AX1 - AX0) * years / 25
html.append('<div id="g-axis" class="h" style="left:%dpx;top:%dpx;width:%dpx;height:4px;background:rgba(255,255,255,.7);border-radius:2px"></div>'
            % (AX0, AY, AX1 - AX0))
for k, (yrs, lab) in enumerate([(0, "Abhi"), (10, "10 saal"), (14, "14 saal"), (25, "25 saal")]):
    html.append('<div id="g-t%d" class="h ticklab" style="left:%dpx;top:%dpx">%s</div>' % (k, gx(yrs) - 80, AY + 18, lab))
    js.append("rise('#g-t%d',%.2f);" % (k, 226.6 + k * 0.15))
goals = [("Emergency fund", 0, 150, 228.0, "cyan"), ("Insurance check", 0, 250, 232.0, "cyan"),
         ("Aarav ka college", 10, 350, 238.0, ""), ("Pihu ka college", 14, 450, 244.0, ""),
         ("Retirement", 25, 150, 256.0, "")]
for k, (lab, yrs, top, t, tone) in enumerate(goals):
    x = gx(yrs) - 12 if yrs < 20 else gx(yrs) - 270
    border = "#0AF0F0" if tone == "cyan" else "rgba(255,255,255,.5)"
    html.append('<div id="g-g%d" class="card h goal" style="left:%dpx;top:%dpx;border-color:%s">%s</div>' % (k, x, top, border, lab))
    html.append('<div id="g-s%d" class="h" style="left:%dpx;top:%dpx;width:3px;height:%dpx;background:%s"></div>'
                % (k, gx(yrs) - 1, top + 80, AY - top - 80, border))
    js.append("rise('#g-g%d',%.2f); rise('#g-s%d',%.2f);" % (k, t, k, t + 0.1))
js.append("grow('#g-axis',226.0,.8);")
html.append('<div id="g-par" class="h" style="left:%dpx;top:%dpx;width:%dpx;height:46px;border-radius:12px;background:rgba(255,185,4,.16);'
            'border:2px solid rgba(255,185,4,.6);font-size:28px;font-weight:700;display:flex;align-items:center;padding-left:18px">'
            'Parents ki care: <span class="amber" style="margin-left:10px">kabhi bhi</span></div>' % (AX0, AY + 70, AX1 - AX0))
html.append('<div id="g-ghar" class="h goal" style="left:%dpx;top:%dpx;border:3px dashed rgba(255,185,4,.8);border-radius:20px;'
            'background:rgba(255,185,4,.06)">Apna ghar:&nbsp;<span class="amber">kabhi na kabhi?</span></div>' % (gx(9), AY + 140))
broll("v-ghar", "A couple looking at a flat for sale", 248.6, 253.0)
js += ["rise('#g-ghar',253.4);", "rise('#g-par',262.0);"]
line("g-l1", "Har goal ki apni deadline", {3, 4}, "cyan", 268.0, 283.0, top=950)
scene_close()

# ---------------------------------------------------------------------------------------------- 7. Sirf jama rakam
scene_open("jama", 1)
tag("j-tag", 5, 285.2)
for k, (lab, n, sub, t) in enumerate([("Padhai · ₹10,000 × 10 saal", 1200000, "dono bachchon ke liye", 286.0),
                                      ("Retirement · ₹13,000 × 25 saal", 3900000, "EPF alag se", 295.0)]):
    top = 170 + k * 300
    html.append('<div id="j-c%d" class="card h" style="left:%dpx;top:%dpx;width:880px;height:270px;padding:24px 34px">'
                '<div style="font-size:36px;font-weight:700;color:rgba(255,255,255,.88)">%s</div>'
                '<div id="j-v%d" class="amber" style="font-size:118px;font-weight:700;line-height:1.15">₹0</div>'
                '<div style="font-size:30px;color:rgba(255,255,255,.75)">%s</div></div>' % (k, L + 20, top, E(lab), k, sub))
    js.append("rise('#j-c%d',%.2f); count('#j-v%d',0,%d,%.2f,1.6);" % (k, t, k, n, t + 3.0))
    money_sounds.append(t + 4.6)
html.append('<div id="j-cap" class="h" style="left:%dpx;top:790px;width:880px;text-align:center;font-size:28px;'
            'color:rgba(255,255,255,.8)">Sirf jama rakam: growth aur mehngai shamil nahi · <b>Illustrative</b></div>' % (L + 20))
html.append('<div id="j-ep" class="chip h" style="left:%dpx;top:880px;width:680px">Asli kharcha kitna?&nbsp;<b class="cyan">Episode 41 &amp; 46</b></div>' % (CX - 340))
js += ["rise('#j-cap',289.0);", "rise('#j-ep',305.0);"]
scene_close()

# ---------------------------------------------------------------------------------------------- 8. Har goal ka dabba
scene_open("dabba", 2)
tag("d-tag", 6, 320.2)
for k, (when, goal, t) in enumerate([("1 saal", "Emergency", 321.0), ("10–14 saal", "College", 322.5), ("25 saal", "Retirement", 324.0)]):
    x = L + 60 + k * 290
    html.append('<div id="d-j%d" class="h" style="left:%dpx;top:170px;width:230px">'
                '<div class="jar" style="height:200px"><div class="jarfill" style="height:%dpx"></div></div>'
                '<div class="cyan" style="text-align:center;font-size:36px;font-weight:700;margin-top:12px">%s</div>'
                '<div style="text-align:center;font-size:30px;color:rgba(255,255,255,.8)">%s</div></div>'
                % (k, x, 60 + k * 50, when, goal))
    js.append("rise('#d-j%d',%.2f);" % (k, t))
terms = [("Goal", 328.0, ""), ("+", 328.8, "op"), ("Deadline", 329.6, ""), ("=", 330.4, "op"), ("Plan", 331.2, "mag")]
html.append('<div id="d-eq" class="h eq" style="left:%dpx;top:520px;width:880px">%s</div>'
            % (L + 20, "".join('<span id="d-q%d" class="%s">%s</span>' % (k, c, s) for k, (s, _, c) in enumerate(terms))))
js.append("tl.set('#d-eq',{opacity:1},327.8);")
js += ["tl.fromTo('#d-q%d',{opacity:0,y:26},{opacity:1,y:0,duration:.4,ease:'power2.out'},%.2f);" % (k, t) for k, (_, t, _) in enumerate(terms)]
html.append('<!-- d-o1 class="card h step" style="left:%dpx;top:680px"><b class="cyan">1</b> Pehle safety<div class="stepsub">emergency fund · insurance · mehnga karz nahi</div></div> -->' % (L + 20))
html.append('<!-- d-o2 class="card h step" style="left:%dpx;top:680px"><b class="cyan">2</b> Phir lambe goals<div class="stepsub">college · ghar · retirement</div></div> -->' % (L + 470))
js.append("out('#d-j0,#d-j1,#d-j2,#d-eq',333.6);")
block("x-safety", "compositions/components/marker-checklist-card.html", "marker-checklist-card", 334.0, 344.6, (L + 20, 120, 880, 780),
      {"top": "SABSE", "mid": "PEHLE", "circled": "SAFETY", "rest": "!", "l1": "EMERGENCY", "v1": "FUND", "l2": "INSURANCE", "v2": "CHECK",
       "l3": "KARZ", "v3": "NAHI"}, 7)
scene_close()

# ---------------------------------------------------------------------------------------------- 9. Aapka kaam
scene_open("kaam", 1)
tag("k-tag", 7, 345.2)
rows = [("Emergency fund", "Abhi", 350.0, ""), ("Aarav ka college", "2036", 354.0, ""), ("Pihu ka college", "2040", 358.0, ""),
        ("Retirement", "2051", 362.0, ""), ("Apna ghar", "?", 366.0, "sapna")]
rh = "".join('<div class="prow" id="k-r%d"><span>%s</span><span>%s</span><span>₹ ______</span>'
             '<div id="k-m%d" class="pmask"></div></div>' % (k, g, w if not s else '<b class="amber">? sapna</b>', k)
             for k, (g, w, _, s) in enumerate(rows))
html.append('<div id="k-paper" class="h paper" style="left:%dpx;top:160px">'
            '<div class="phead">Hamare 5 goals</div>'
            '<div class="prow pcols"><span>Goal</span><span>Kab</span><span>Kitna (andaaza)</span></div>%s</div>' % (L + 40, rh))
broll("v-write", "A hand writing a goals list in a notebook", 345.4, 349.6)
js.append("rise('#k-paper',349.7);")
js += ["tl.fromTo('#k-m%d',{scaleX:1},{scaleX:0,duration:1.0,ease:'power1.inOut'},%.2f);" % (k, t) for k, (_, _, t, _) in enumerate(rows)]
line("k-l1", "Kab chahiye + lagbhag kitna", {0, 1, 3, 4}, "cyan", 375.0, 385.0)
html.append('<div id="k-chip" class="chip h" style="left:%dpx;top:920px;width:620px">Saal nahi? Toh abhi&nbsp;<b class="mag">sapna</b>&nbsp;hai</div>' % (CX - 310))
js += ["rise('#k-chip',386.0);", "out('#k-chip',398.0);"]
scene_close()

# ---------------------------------------------------------------------------------------------- 10. End
scene_open("end", 2)
html.append('''
<div id="e-eye" class="h eyebrow" style="left:%dpx;top:170px;width:%dpx;text-align:center">AGLA PART 2</div>
<div id="e-t" class="h" style="left:%dpx;top:230px;width:%dpx;text-align:center;font-size:60px;font-weight:700;line-height:1.15">Salary aati hai, phir <span class="cyan">gayab kahan</span> hoti hai?</div>
<div id="e-c" class="chip h" style="left:%dpx;top:430px;width:700px">Comment: aapka&nbsp;<b class="cyan">sabse bada goal</b>?</div>
<div id="e-web" class="h" style="left:%dpx;top:560px;width:%dpx;text-align:center;font-size:40px;font-weight:700">Free notes: <span class="cyan">samjhowithraj.online</span></div>
<div id="e-dis" class="h" style="left:%dpx;top:630px;width:%dpx;text-align:center;font-size:28px;color:rgba(255,255,255,.72)">Educational example · financial advice nahi</div>
<div id="e-sb" class="h sbar" style="left:%dpx;top:740px">
  <div class="sbav"><img src="assets/img/raj-mark.png" alt=""></div>
  <div><div style="font-size:42px;font-weight:700;line-height:1.05">Samjho with Raj</div>
  <div style="font-size:23px;color:rgba(255,255,255,.85)">Middle-Class Family Ka Money Plan · 50 parts</div></div>
  <div id="e-btn" class="sbbtn">Subscribe</div>
</div>
''' % (L, W, L + 20, W - 40, CX - 350, L, W, L, W, L + 70))
js += ["rise('#e-eye',400.3);", "rise('#e-t',400.6);", "rise('#e-c',404.0);", "rise('#e-web',407.0);", "rise('#e-dis',408.0);",
       "rise('#e-sb',410.0);",
       "tl.fromTo('#e-btn',{scale:1},{scale:1.08,duration:.22,yoyo:true,repeat:5,ease:'power1.inOut'},410.6);"]
scene_close()

# disclaimer card (2 s, after the hook visual)
roots.append('<div id="o-disc" class="clip disc" data-start="3.00" data-duration="2.00" data-track-index="9">'
             '<div class="dtitle">Educational example</div><div class="dsub">Financial advice nahi · numbers illustrative hain · '
             'apni situation ke hisaab se decide karein</div></div>')
js.append("tl.fromTo('#o-disc',{opacity:0},{opacity:1,duration:.25},3.0); tl.to('#o-disc',{opacity:0,duration:.25},4.75);")

# name lower-third, left of Raj's feet (never over the body)
roots.append('<div id="o-name" class="clip lt3" data-start="16.00" data-duration="4.60" data-track-index="9">'
             '<div class="ltbar"></div><div><div class="ltname">RAJ</div><div class="ltsub">Samjho with Raj</div></div></div>')
js.append("tl.fromTo('#o-name',{opacity:0,x:-40},{opacity:1,x:0,duration:.4,ease:'power2.out'},16.0); out('#o-name',20.2);")

# section cards #1..#7 on the studio screen, 2.2 s at each chapter start
SECTIONS = [("family", "Verma family kaun hai?"), ("today", "Aaj unke paas kya hai?"), ("budget", "₹1 lakh kahan jaata hai?"),
            ("goals", "Kaunsa goal kab?"), ("jama", "Kitna jama hoga?"), ("dabba", "Paisa kaise baantein?"),
            ("kaam", "Aapko kya karna hai?")]
for n, (key, q) in enumerate(SECTIONS, 1):
    a = T[key][0]
    roots.append('<div id="o-sec%d" class="clip secard" data-start="%.2f" data-duration="2.60" data-track-index="10">'
                 '<div class="secn">#%d</div><div class="secq">%s</div></div>' % (n, a, n, E(q)))
    js.append("tl.fromTo('#o-sec%d',{opacity:0},{opacity:1,duration:.3},%.2f); tl.to('#o-sec%d',{opacity:0,duration:.3},%.2f);"
              % (n, a + 0.1, n, a + 2.3))

# white keyword labels next to Raj's head (one at a time, 2-4 s); a struck label = "X nahi, Y"
KW = [("o-kw1", "Sirf 1 mahina", None, 97.0, 100.5), ("o-kw2", "Kaafi?", None, 213.0, 216.5),
      ("o-kw3", "Deadline!", None, 268.5, 272.0), ("o-kw4", "Sirf jama", "Final amount", 309.0, 313.0),
      ("o-kw5", "Sapna ≠ Goal", None, 388.0, 391.5),
      ("o-kw6", "Mushkil!", None, 277.0, 281.0), ("o-kw7", "Pehle safety", None, 340.0, 343.5)]
for kid, word, struck, a, b in KW:
    top = '<div class="kwx">%s</div>' % E(struck) if struck else ""
    roots.append('<div id="%s" class="clip kwbox" data-start="%.2f" data-duration="%.2f" data-track-index="11">%s<div class="kw">%s</div></div>'
                 % (kid, a, b - a, top, E(word)))
    js.append("rise('#%s',%.2f); out('#%s',%.2f);" % (kid, a, kid, b - 0.35))

for k, t in enumerate(money_sounds):
    chaching("sfx-cc%d" % k, t)

# ---------------------------------------------------------------------------------------------- placeholder (left third)
placeholder = '''
<svg id="ph" width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;left:0;top:0">
  <rect x="250" y="96" width="652" height="944" rx="28" fill="none" stroke="rgba(255,255,255,.16)" stroke-width="3" stroke-dasharray="14 12"/>
  <g fill="rgba(10,240,240,.06)" stroke="rgba(10,240,240,.6)" stroke-width="4" stroke-dasharray="12 10" stroke-linejoin="round">
    <circle cx="576" cy="212" r="64"/>
    <path d="M470 312 Q576 284 682 312 L700 600 L652 610 L640 1000 L592 1000 L580 660 L572 660 L560 1000 L512 1000 L500 610 L452 600 Z"/>
    <path d="M478 330 L360 470 L318 560 L346 572 L392 494 L486 420 Z"/>
    <path d="M674 330 L792 470 L834 560 L806 572 L760 494 L666 420 Z"/>
  </g>
  <text x="576" y="70" text-anchor="middle" font-size="27" font-weight="700" fill="rgba(10,240,240,.85)" letter-spacing="3">RAJ YAHAN · FULL BODY</text>
  <text x="576" y="1066" text-anchor="middle" font-size="21" fill="rgba(255,255,255,.5)">placeholder · CapCut studio room · haath aur pair kabhi crop nahi honge</text>
</svg>'''

CSS = '''
@font-face{font-family:"DM Sans";src:url(fonts/DMSans-400.woff2) format("woff2");font-weight:400}
@font-face{font-family:"DM Sans";src:url(fonts/DMSans-500.woff2) format("woff2");font-weight:500}
@font-face{font-family:"DM Sans";src:url(fonts/DMSans-700.woff2) format("woff2");font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#07090d}
body{font-family:"DM Sans",ui-sans-serif,system-ui,sans-serif;color:#fff}
#stage{--brand:#0AF0F0;--fg:#ffffff;--bg:#0a0d14;position:relative;width:1920px;height:1080px;overflow:hidden;
  background:radial-gradient(900px 700px at 78% 22%,rgba(10,240,240,.10),transparent 70%),
             radial-gradient(1100px 800px at 100% 100%,rgba(0,5,238,.22),transparent 70%),
             radial-gradient(800px 600px at 8% 90%,rgba(205,0,238,.08),transparent 70%),#0a0d14}
#grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.045) 2px,transparent 2px),
  linear-gradient(90deg,rgba(255,255,255,.045) 2px,transparent 2px);background-size:96px 96px}
.scene{position:absolute;left:0;top:0;width:1920px;height:1080px}
.scene>*{position:absolute}
.h{opacity:0}
.cyan{color:#0AF0F0}.amber{color:#FFB904}.mag{color:#CD00EE}
.card{background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.4);border-radius:26px;box-shadow:0 24px 80px rgba(0,0,0,.38)}
.big{font-weight:700;letter-spacing:-.015em;white-space:nowrap}
.title{font-size:96px;font-weight:700;letter-spacing:-.015em;line-height:1.05;-webkit-text-stroke:1.5px currentColor}
.eyebrow{font-size:34px;font-weight:700;letter-spacing:.22em;color:#0AF0F0}
.pill{height:92px;padding:0 34px;border-radius:9999px;background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.4);
  display:flex;align-items:center;font-size:50px;font-weight:700;white-space:nowrap}
.pill b{margin-left:6px}
.chip{height:96px;border-radius:16px;background:rgba(17,17,17,.6);border:2px solid rgba(255,255,255,.2);display:flex;align-items:center;
  justify-content:center;font-size:46px;font-weight:700;white-space:nowrap}
.ll{position:absolute;left:940px;width:920px;text-align:center;font-size:0;white-space:nowrap}
.ll span{display:inline-block;font-size:60px;font-weight:700;letter-spacing:-.015em;margin:0 .14em;opacity:0}
.tag{right:60px;top:44px;height:66px;padding:0 26px;border-radius:9999px;background:rgba(255,255,255,.1);border:3px solid rgba(255,255,255,.45);
  display:flex;align-items:center;gap:14px;font-size:32px;font-weight:700;white-space:nowrap}
.tag .dot{width:16px;height:16px;border-radius:50%;background:#0AF0F0;box-shadow:0 0 14px #0AF0F0}
.pips{display:flex;gap:7px;margin-left:6px}.pips i{width:12px;height:12px;border-radius:50%;background:rgba(255,255,255,.25)}.pips i.on{background:#0AF0F0}
.sd{display:inline-block;width:14px;height:14px;border-radius:50%;background:rgba(255,255,255,.18);margin:6px}
.av{width:170px;height:170px;margin:0 auto;border-radius:50%;border:6px solid;display:flex;align-items:center;justify-content:center;
  font-size:64px;font-weight:700;background:rgba(255,255,255,.06)}
.rowlab{font-size:34px;font-weight:700;margin-bottom:10px}
.track{width:860px;height:40px;border-radius:12px;background:rgba(255,255,255,.08)}
.bar{height:40px;border-radius:12px;transform-origin:0 50%}
.seg{position:absolute;top:6px;height:68px;border-radius:12px;transform-origin:0 50%}
.seglab{font-size:36px;font-weight:700;white-space:nowrap}
.row{height:96px;padding:0 30px;display:flex;align-items:center;justify-content:space-between;font-size:42px;font-weight:700}
.jar{position:relative;width:230px;height:290px;border:4px solid rgba(255,255,255,.6);border-top:none;border-radius:0 0 40px 40px;overflow:hidden;
  background:rgba(255,255,255,.04)}
.jarfill{position:absolute;left:0;right:0;bottom:0;background:linear-gradient(#0AF0F0,rgba(10,240,240,.45));transform-origin:50% 100%}
.ticklab{width:160px;text-align:center;font-size:30px;font-weight:700;color:rgba(255,255,255,.85)}
.goal{height:80px;padding:0 22px;display:flex;align-items:center;font-size:34px;font-weight:700;white-space:nowrap}
.eq{display:flex;justify-content:center;gap:28px;font-size:80px;font-weight:700;height:120px;align-items:center;border-radius:26px;
  background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.4)}
.eq span{opacity:0}.eq .op{color:rgba(255,255,255,.6)}
.step{width:430px;height:150px;padding:22px 28px;font-size:42px;font-weight:700}
.stepsub{font-size:24px;font-weight:500;color:rgba(255,255,255,.78);margin-top:10px}
.paper{width:840px;padding:34px 40px;border-radius:18px;background:#F5F1E8;color:#1b1a17;box-shadow:0 30px 90px rgba(0,0,0,.55)}
.phead{font-size:52px;font-weight:700;border-bottom:5px solid #FFB904;display:inline-block;margin-bottom:18px}
.prow{position:relative;display:grid;grid-template-columns:1.5fr .7fr 1.1fr;font-size:36px;font-weight:700;padding:16px 0;
  border-bottom:2px solid rgba(27,26,23,.15)}
.pcols{font-size:26px;color:rgba(27,26,23,.6);letter-spacing:.06em}
.paper .amber{color:#9a6400}
.pmask{position:absolute;inset:0;background:#F5F1E8;transform-origin:100% 50%}
.sbar{height:132px;padding:0 22px 0 18px;border-radius:9999px;background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.22);
  box-shadow:0 24px 80px rgba(0,0,0,.5);display:flex;align-items:center;gap:22px;white-space:nowrap}
.sbav{width:100px;height:100px;border-radius:50%;overflow:hidden;background:#111;flex:none}.sbav img{width:100px;height:100px;display:block}
.sbbtn{margin-left:10px;background:#FF0000;color:#fff;font-weight:700;font-size:32px;padding:16px 30px;border-radius:9999px}
#screen{position:absolute;left:920px;top:112px;width:960px;height:800px;border-radius:22px;background:rgba(6,9,15,.82);
  border:6px solid #1c2230;box-shadow:0 0 0 2px rgba(255,255,255,.12),0 30px 90px rgba(0,0,0,.6)}
#screenfx{position:absolute;left:926px;top:118px;width:948px;height:788px;border-radius:16px;pointer-events:none;z-index:9;
  background:linear-gradient(115deg,rgba(255,255,255,.07) 0%,transparent 30%),repeating-linear-gradient(0deg,rgba(0,0,0,.08) 0 1px,transparent 1px 3px)}
.bslot{position:absolute;left:926px;top:118px;width:948px;height:788px;border-radius:16px;z-index:8;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:18px;padding:60px;text-align:center;
  background:repeating-linear-gradient(135deg,rgba(255,185,4,.10) 0 18px,rgba(255,185,4,.03) 18px 36px),#111520}
.btag{font-size:30px;font-weight:700;letter-spacing:.2em;color:#FFB904}
.bwhat{font-size:46px;font-weight:700;line-height:1.2}
.disc{position:absolute;inset:0;z-index:30;opacity:0;background:#0b0d12;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px}
.dtitle{font-size:72px;font-weight:700;color:#FFB904}
.dsub{font-size:34px;color:rgba(255,255,255,.85);max-width:1300px;text-align:center;line-height:1.35}
.lt3{position:absolute;left:40px;top:930px;z-index:12;display:flex;align-items:center;gap:18px;padding:12px 26px 12px 16px;border-radius:14px;
  background:rgba(10,13,20,.85)}
.ltbar{width:8px;height:78px;border-radius:4px;background:#0AF0F0;box-shadow:0 0 14px rgba(10,240,240,.8)}
.ltname{font-size:46px;font-weight:700;letter-spacing:.06em;line-height:1}
.ltsub{font-size:26px;color:rgba(255,255,255,.8);margin-top:6px}
.secard{position:absolute;left:926px;top:118px;width:948px;height:788px;border-radius:16px;z-index:7;background:#EEF1F5;color:#10131a;
  display:flex;flex-direction:column;justify-content:center;padding:0 90px;
  background-image:linear-gradient(rgba(16,19,26,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(16,19,26,.05) 2px,transparent 2px);background-size:64px 64px}
.secn{font-size:150px;font-weight:700;line-height:1;color:#0005EE}
.secq{font-size:66px;font-weight:700;margin-top:18px;line-height:1.15}
.kwbox{position:absolute;left:670px;top:132px;z-index:12;display:flex;flex-direction:column;align-items:flex-start;gap:8px}
.kw{background:#fff;color:#0b0b0b;font-size:40px;font-weight:700;padding:8px 22px;border-radius:14px;white-space:nowrap;box-shadow:0 10px 30px rgba(0,0,0,.45)}
.kwx{background:#fff;color:#0b0b0b;font-size:30px;font-weight:700;padding:4px 16px;border-radius:10px;white-space:nowrap;
  text-decoration:line-through;text-decoration-color:#E0242E;text-decoration-thickness:5px}
.dcard{width:880px;border-radius:18px;background:#fff;color:#111;padding:18px 26px 14px;box-shadow:0 30px 90px rgba(0,0,0,.55)}
.dhead{display:flex;justify-content:space-between;font-size:26px;font-weight:700;color:#555;letter-spacing:.04em;padding:0 14px 10px;
  border-bottom:3px solid #111}
.drow{position:relative;display:flex;justify-content:space-between;font-size:38px;font-weight:700;padding:8px 14px;border-bottom:1px solid #e3e3e3}
.drow span{position:relative}
.dtot{border-bottom:none;border-top:3px solid #111;margin-top:4px}
.dhl{position:absolute;inset:4px 0;background:#FFE14D;border-radius:8px;transform-origin:0 50%}
#draftmark{position:absolute;right:40px;bottom:22px;font-size:20px;color:rgba(255,255,255,.6);letter-spacing:.08em}
'''

page = '''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<script src="vendor/gsap.min.js"></script>
<style>%s</style></head>
<body>
<div id="stage" data-composition-id="main" data-start="0" data-duration="%.2f" data-fps="30" data-width="1920" data-height="1080">
<div id="grid"></div>
%s
<div id="screen"></div>
%s
<div id="screenfx"></div>
<div id="draftmark">DRAFT 2 · finance style · timed to the plan, not the voice</div>
%s
<audio id="bed" src="assets/audio/bed.mp3" data-start="0" data-duration="%.2f" data-track-index="11" data-volume="0.35"></audio>
</div>
<script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
function rise(s,t){ tl.fromTo(s,{opacity:0,y:26},{opacity:1,y:0,duration:.4,ease:'power2.out'},t); }
function out(s,t){ tl.to(s,{opacity:0,duration:.35,ease:'power2.in'},t); }
function grow(s,t,d){ tl.fromTo(s,{scaleX:0},{scaleX:1,duration:d||.6,ease:'power2.out'},t); }
function inr(n){ const s=String(Math.round(n)); if(s.length<=3) return s;
  return s.slice(0,-3).replace(/\\B(?=(\\d{2})+(?!\\d))/g,',')+','+s.slice(-3); }
function count(s,a,b,t,d){ const el=document.querySelector(s); const p={v:a}; el.textContent='₹'+inr(a);
  tl.to(p,{v:b,duration:d||1.4,ease:'power2.out',onUpdate:()=>{ el.textContent='₹'+inr(p.v); }},t); }
%s
tl.to({}, { duration: %.2f }, 0);
window.__timelines["main"] = tl;
</script>
</body></html>
''' % (CSS, DUR, placeholder, "\n".join(html), "\n".join(roots), DUR, "\n".join(js), DUR)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
NL = chr(10)
md = ["# Part 1: explanation cutaways (AI or stock video on the studio screen)", "",
      "Draft slots, timed to the plan. Each needs a source chosen and approved before anything is generated or downloaded.", "",
      "| Slot | Shows | In | Out | Length |", "|---|---|---|---|---|"]
md += ["| %s | %s | %.1f s | %.1f s | %.1f s |" % (bid, what, a, b, b - a) for bid, what, a, b in broll_slots]
with open(os.path.join(HERE, "BROLL.md"), "w", encoding="utf-8") as f:
    f.write(NL.join(md) + NL)
print("wrote %s (%d elements, %d timeline lines, %d money sounds)" % (OUT, len(html), len(js), len(money_sounds)))
