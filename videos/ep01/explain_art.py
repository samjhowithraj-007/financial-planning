"""Money explainer animations for the Money Plan studio screen (panel units: screen box 926,118 948x848).

Raj's rule (16 Oct 2026): the studio screen is never blank, and whenever he explains with an example the screen shows
an animation of it: buckets filling with coins, a piggy bank, a growing chart, a shield, a house, a wallet emptying.
Every function returns (html, js) for one root-level clip; times are PLAN seconds (warped by build-draft.py like
everything else). All motion is GSAP on the paused timeline (seek-safe), no CSS keyframes.
"""
from html import escape

SX, SY, SW, SH = 926, 118, 948, 848          # the screen box (panel units)
AMBER, CYAN, MAG, WHITE = "#FFB904", "#0AF0F0", "#CD00EE", "rgba(255,255,255,.9)"
E = lambda s: escape(s, quote=False)


def _wrap(eid, t_in, t_out, svg, title, sub, low=False):
    head = '<div class="xa-t">%s</div>' % title if title else ""
    foot = '<div class="xa-s">%s</div>' % sub if sub else ""
    html = ('<div id="%s" class="clip xa%s" data-start="%.2f" data-duration="%.2f" data-track-index="11">%s'
            '<svg class="xa-svg" viewBox="0 0 900 560" width="900" height="560">%s</svg>%s</div>'
            % (eid, " low" if low else "", t_in, t_out - t_in, head, svg, foot))
    js = ["tl.fromTo('#%s',{opacity:0},{opacity:1,duration:.35},%.2f);" % (eid, t_in),
          "tl.to('#%s',{opacity:0,duration:.3},%.2f);" % (eid, t_out - 0.3)]
    return html, js


def _coin(cid, x, y, r=22):
    return ('<g id="%s" transform="translate(%d,%d)"><circle r="%d" fill="%s" stroke="#b37400" stroke-width="4"/>'
            '<text y="9" text-anchor="middle" font-size="%d" font-weight="700" fill="#7a4d00">₹</text></g>' % (cid, x, y, r, AMBER, r))


def buckets(eid, t_in, t_out, labels, fills, title="", sub="", colors=None):
    """Up to 4 buckets; coins drop into each in turn and the water line rises to its fill (0-1)."""
    n = len(labels)
    colors = colors or [CYAN, AMBER, MAG, WHITE][:n]
    gap = 900 / n
    svg, js = [], []
    step = max(0.6, (t_out - t_in - 1.2) / (n * 1.6))
    for k, (lab, f, col) in enumerate(zip(labels, fills, colors)):
        cx = gap * (k + .5)
        x0, x1, y0, y1 = cx - 95, cx + 95, 150, 430            # bucket rim and bottom
        clip = "%s-c%d" % (eid, k)
        svg.append('<clipPath id="%s"><path d="M%d %d L%d %d L%d %d L%d %d Z"/></clipPath>' % (clip, x0, y0, x1, y0, x1 - 30, y1, x0 + 30, y1))
        svg.append('<g clip-path="url(#%s)"><rect id="%s-w%d" x="%d" y="%d" width="190" height="%d" fill="%s" opacity=".85"/></g>'
                   % (clip, eid, k, x0, y0, y1 - y0, col))
        svg.append('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="none" stroke="rgba(255,255,255,.85)" stroke-width="6" stroke-linejoin="round"/>'
                   % (x0, y0, x1, y0, x1 - 30, y1, x0 + 30, y1))
        svg.append('<path d="M%d %d Q%d %d %d %d" fill="none" stroke="rgba(255,255,255,.6)" stroke-width="5"/>' % (x0 + 10, y0, cx, y0 - 90, x1 - 10, y0))
        svg.append('<text x="%d" y="490" text-anchor="middle" font-size="34" font-weight="700" fill="#fff">%s</text>' % (cx, E(lab)))
        t = t_in + 0.6 + k * step * 1.6
        for c in range(3):
            cid = "%s-k%d%d" % (eid, k, c)
            svg.append(_coin(cid, int(cx - 30 + c * 30), -40))
            js.append("tl.fromTo('#%s',{y:-40,opacity:1},{y:%d,duration:.55,ease:'power2.in'},%.2f);" % (cid, 330 - c * 8, t + c * 0.25))
            js.append("tl.to('#%s',{opacity:0,duration:.15},%.2f);" % (cid, t + c * 0.25 + .55))
        js.append("tl.fromTo('#%s-w%d',{attr:{y:%d,height:0}},{attr:{y:%d,height:%d},duration:%.2f,ease:'power1.out'},%.2f);"
                  % (eid, k, y1, y1 - (y1 - y0) * f, (y1 - y0) * f, step * 1.4, t + 0.3))
    html, j0 = _wrap(eid, t_in, t_out, "".join(svg), title, sub)
    return html, j0 + js


def piggy(eid, t_in, t_out, title="", sub="", coins=5):
    """A piggy bank; coins drop into the slot and it bounces once."""
    svg = ['<g id="%s-pig" transform="translate(450,330)">' % eid,
           '<ellipse rx="190" ry="140" fill="#F6A6C8"/><ellipse cx="150" cy="-10" rx="55" ry="45" fill="#F48FB9"/>',
           '<circle cx="165" cy="-20" r="8" fill="#7a2c4f"/><circle cx="140" cy="-20" r="8" fill="#7a2c4f"/>',
           '<circle cx="90" cy="-70" r="12" fill="#222"/><path d="M-60 -150 L-20 -110 L-90 -105 Z" fill="#F48FB9"/>',
           '<rect x="-120" y="120" width="40" height="50" rx="10" fill="#F48FB9"/><rect x="60" y="120" width="40" height="50" rx="10" fill="#F48FB9"/>',
           '<rect x="-50" y="-140" width="100" height="16" rx="8" fill="#7a2c4f"/></g>']
    js = []
    for c in range(coins):
        cid = "%s-k%d" % (eid, c)
        svg.append(_coin(cid, 450, -40, 26))
        t = t_in + 0.8 + c * (t_out - t_in - 2) / coins
        js.append("tl.fromTo('#%s',{y:-40,opacity:1},{y:185,duration:.5,ease:'power2.in'},%.2f);" % (cid, t))
        js.append("tl.to('#%s',{opacity:0,duration:.1},%.2f);" % (cid, t + .5))
        js.append("tl.fromTo('#%s-pig',{scale:1},{scale:1.05,duration:.12,yoyo:true,repeat:1,transformOrigin:'50%% 50%%'},%.2f);" % (eid, t + .5))
    html, j0 = _wrap(eid, t_in, t_out, "".join(svg), title, sub)
    return html, j0 + js


def growth(eid, t_in, t_out, title="", sub="", label_end=""):
    """A line chart drawing up and to the right with an amber dot and an end label."""
    pts = [(80, 470), (180, 455), (280, 440), (380, 410), (480, 380), (580, 330), (680, 270), (780, 190), (850, 120)]
    d = "M" + " L".join("%d %d" % p for p in pts)
    svg = ['<line x1="70" y1="480" x2="870" y2="480" stroke="rgba(255,255,255,.5)" stroke-width="4"/>',
           '<line x1="70" y1="480" x2="70" y2="90" stroke="rgba(255,255,255,.5)" stroke-width="4"/>',
           '<path id="%s-l" d="%s" fill="none" stroke="%s" stroke-width="10" stroke-linecap="round" stroke-dasharray="1200" stroke-dashoffset="1200"/>' % (eid, d, CYAN),
           '<circle id="%s-d" cx="850" cy="120" r="18" fill="%s" opacity="0"/>' % (eid, AMBER),
           '<text id="%s-e" x="840" y="80" text-anchor="end" font-size="44" font-weight="700" fill="%s" opacity="0">%s</text>' % (eid, AMBER, E(label_end))]
    js = ["tl.to('#%s-l',{attr:{'stroke-dashoffset':0},duration:%.2f,ease:'power1.inOut'},%.2f);" % (eid, max(1.2, (t_out - t_in) * .55), t_in + .5),
          "tl.to('#%s-d,#%s-e',{opacity:1,duration:.3},%.2f);" % (eid, eid, t_in + .5 + max(1.2, (t_out - t_in) * .55))]
    html, j0 = _wrap(eid, t_in, t_out, "".join(svg), title, sub)
    return html, j0 + js


def shield(eid, t_in, t_out, title="", sub="", items=()):
    """A shield that draws itself, a check pops in, and short items tick in beside it."""
    svg = ['<path id="%s-s" d="M250 80 L400 130 L400 280 Q400 420 250 480 Q100 420 100 280 L100 130 Z" fill="rgba(10,240,240,.14)" '
           'stroke="%s" stroke-width="10" stroke-dasharray="1400" stroke-dashoffset="1400"/>' % (eid, CYAN),
           '<path id="%s-c" d="M180 280 L235 335 L330 220" fill="none" stroke="%s" stroke-width="22" stroke-linecap="round" '
           'stroke-linejoin="round" stroke-dasharray="320" stroke-dashoffset="320"/>' % (eid, AMBER)]
    js = ["tl.to('#%s-s',{attr:{'stroke-dashoffset':0},duration:1.0,ease:'power1.inOut'},%.2f);" % (eid, t_in + .4),
          "tl.to('#%s-c',{attr:{'stroke-dashoffset':0},duration:.5,ease:'power2.out'},%.2f);" % (eid, t_in + 1.4)]
    for k, it in enumerate(items):
        iid = "%s-i%d" % (eid, k)
        svg.append('<text id="%s" x="470" y="%d" font-size="42" font-weight="700" fill="#fff" opacity="0">✓ %s</text>' % (iid, 200 + k * 90, E(it)))
        js.append("tl.fromTo('#%s',{opacity:0,x:-20},{opacity:1,x:0,duration:.35},%.2f);" % (iid, t_in + 1.9 + k * 0.6))
    html, j0 = _wrap(eid, t_in, t_out, "".join(svg), title, sub)
    return html, j0 + js


def house(eid, t_in, t_out, title="", sub="", dashed=True):
    """A house outline that draws itself (dashed = still a dream), with a little window light."""
    dash = ' stroke-dasharray="26 18"' if dashed else ""
    svg = ['<g id="%s-h" opacity="0"><path d="M200 300 L450 110 L700 300" fill="none" stroke="%s" stroke-width="12" stroke-linejoin="round"%s/>' % (eid, AMBER, dash),
           '<rect x="260" y="290" width="380" height="210" fill="rgba(255,185,4,.08)" stroke="%s" stroke-width="10"%s/>' % (AMBER, dash),
           '<rect x="410" y="380" width="80" height="120" fill="none" stroke="%s" stroke-width="8"/>' % AMBER,
           '<rect id="%s-w" x="300" y="330" width="70" height="60" fill="%s" opacity="0"/></g>' % (eid, AMBER)]
    js = ["tl.fromTo('#%s-h',{opacity:0,y:30},{opacity:1,y:0,duration:.6,ease:'power2.out'},%.2f);" % (eid, t_in + .3),
          "tl.to('#%s-w',{opacity:.9,duration:.4},%.2f);" % (eid, t_in + 1.2)]
    html, j0 = _wrap(eid, t_in, t_out, "".join(svg), title, sub)
    return html, j0 + js


def wallet(eid, t_in, t_out, title="", sub="", out_labels=(), low=False):
    """A big wallet with ₹ notes flying out to labelled spends (salary disappearing)."""
    svg = ['<g transform="translate(40,170) scale(1.35)"><rect width="300" height="200" rx="26" fill="#7a5532" stroke="#4d331b" stroke-width="6"/>'
           '<rect x="180" y="70" width="140" height="70" rx="18" fill="#5d3f22"/><circle cx="225" cy="105" r="14" fill="%s"/>'
           '<rect x="20" y="-26" width="200" height="40" rx="8" fill="#7bd389" transform="rotate(-6)"/></g>' % AMBER]
    js = []
    n = max(1, len(out_labels))
    for k, lab in enumerate(out_labels):
        nid = "%s-n%d" % (eid, k)
        ty = 70 + k * (440 / n)
        svg.append('<g id="%s" opacity="0"><rect x="0" y="-38" width="150" height="76" rx="12" fill="#7bd389" stroke="#3e8f52" stroke-width="4"/>'
                   '<text x="75" y="14" text-anchor="middle" font-size="42" font-weight="700" fill="#1d4d27">₹</text>'
                   '<text x="175" y="16" font-size="50" font-weight="700" fill="#fff">%s</text></g>' % (nid, E(lab)))
        t = t_in + 0.6 + k * min(0.9, (t_out - t_in - 1.2) / n)
        js.append("tl.fromTo('#%s',{opacity:0,x:230,y:330,scale:.6},{opacity:1,x:470,y:%d,scale:1,duration:.6,ease:'power2.out'},%.2f);" % (nid, ty, t))
    html, j0 = _wrap(eid, t_in, t_out, "".join(svg), title, sub, low)
    return html, j0 + js


def cap_grad(eid, t_in, t_out, title="", sub="", years=""):
    """A graduation cap dropping in with a years tag (education goals)."""
    svg = ['<g id="%s-g" transform="translate(450,250)" opacity="0"><path d="M-260 0 L0 -110 L260 0 L0 110 Z" fill="#1d2433" stroke="%s" stroke-width="8"/>' % (eid, CYAN),
           '<path d="M-150 50 L-150 150 Q0 220 150 150 L150 50" fill="#1d2433" stroke="%s" stroke-width="8"/>' % CYAN,
           '<path d="M200 20 L200 150" stroke="%s" stroke-width="8"/><circle cx="200" cy="160" r="16" fill="%s"/></g>' % (AMBER, AMBER),
           '<text id="%s-y" x="450" y="520" text-anchor="middle" font-size="56" font-weight="700" fill="%s" opacity="0">%s</text>' % (eid, AMBER, E(years))]
    js = ["tl.fromTo('#%s-g',{opacity:0,y:-60},{opacity:1,y:0,duration:.6,ease:'back.out(1.6)'},%.2f);" % (eid, t_in + .3),
          "tl.to('#%s-y',{opacity:1,duration:.35},%.2f);" % (eid, t_in + 1.0)]
    html, j0 = _wrap(eid, t_in, t_out, "".join(svg), title, sub)
    return html, j0 + js


def calendar(eid, t_in, t_out, title="", sub="", days=("1", "25")):
    """A calendar page that flips from the first day to the second."""
    svg = ['<rect x="300" y="90" width="300" height="360" rx="26" fill="#f4f6fa"/><rect x="300" y="90" width="300" height="90" rx="26" fill="%s"/>' % AMBER,
           '<rect x="300" y="150" width="300" height="30" fill="%s"/>' % AMBER,
           '<text x="450" y="150" text-anchor="middle" font-size="40" font-weight="700" fill="#111">TAREEKH</text>',
           '<text id="%s-a" x="450" y="390" text-anchor="middle" font-size="190" font-weight="700" fill="#111">%s</text>' % (eid, days[0]),
           '<text id="%s-b" x="450" y="390" text-anchor="middle" font-size="190" font-weight="700" fill="#E0242E" opacity="0">%s</text>' % (eid, days[1])]
    mid = (t_in + t_out) / 2
    js = ["tl.to('#%s-a',{opacity:0,duration:.3},%.2f);" % (eid, mid), "tl.to('#%s-b',{opacity:1,duration:.3},%.2f);" % (eid, mid + .1)]
    html, j0 = _wrap(eid, t_in, t_out, "".join(svg), title, sub)
    return html, j0 + js


CSS = """
.xa{position:absolute;left:926px;top:118px;width:948px;height:848px;z-index:6;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}
.xa-t{font-size:52px;font-weight:700;text-align:center;line-height:1.15;max-width:860px}
.xa-t b{color:#FFB904}.xa-t i{font-style:normal;color:#0AF0F0}
.xa-s{font-size:32px;color:rgba(255,255,255,.8);text-align:center;max-width:860px}
.xa-svg{display:block}
.xa-idle{position:absolute;left:926px;top:118px;width:948px;height:848px;z-index:2;overflow:hidden;border-radius:16px;pointer-events:none}
.xa.low{justify-content:flex-end;padding-bottom:30px}.xa.low .xa-svg{width:860px;height:535px}
"""


def idle(eid, flat_total, coins=9):
    """Background life for the studio screen: ₹ coins drifting up, behind everything (z 2). Whenever no clip or
    animation covers the screen (a hand-over, a fade) the screen still moves. Positions are flat (+10000)."""
    import random
    rnd = random.Random(7)
    svg, js = [], []
    for k in range(coins):
        cid = "%s-k%d" % (eid, k)
        r = rnd.choice((26, 34, 42, 52))
        x = 60 + k * (830 / (coins - 1))
        svg.append('<g id="%s" opacity=".32"><g transform="translate(%d,0)">%s</g></g>' % (cid, x, _coin(cid + "i", 0, 0, r)))
        dur = rnd.uniform(9, 14)
        y0 = rnd.uniform(-80, 900)                       # start somewhere on the way up, then loop bottom -> top
        first = dur * (y0 + 80) / 980
        rep = int(flat_total / dur) + 1
        js.append("tl.fromTo('#%s',{y:%.0f},{y:-80,duration:%.2f,ease:'none'},10000);" % (cid, y0, first))
        js.append("tl.fromTo('#%s',{y:900},{y:-80,duration:%.2f,ease:'none',repeat:%d,immediateRender:false},%.2f);"
                  % (cid, dur, rep, 10000 + first))
    html = ('<div id="%s" class="clip xa-idle" data-start="0.00" data-duration="%.2f" data-track-index="2">'
            '<svg viewBox="0 0 948 848" width="948" height="848">%s</svg></div>' % (eid, 9999, "".join(svg)))
    return html, js
