"""Animated explanation cutaways for the studio screen (used where a stock/AI clip was planned).

Each entry: (svg markup sized 948x788, caption, js lines builder). The SVG parts carry ids so the timeline can move them.
"""
from characters import character


def lucknow(bid, t):
    """Evening skyline: buildings rise, windows light up one by one."""
    blds = [(40, 300, 150), (210, 220, 130), (360, 360, 170), (550, 260, 140), (710, 330, 190)]
    svg = ['<rect x="0" y="0" width="948" height="788" fill="#1a1440"/>',
           '<circle cx="780" cy="150" r="60" fill="#FFB904" opacity=".85"/>',
           '<rect x="0" y="690" width="948" height="98" fill="#0d0b22"/>']
    js = []
    for k, (x, h, w) in enumerate(blds):
        y = 690 - h
        win = "".join('<rect class="%s-w" x="%d" y="%d" width="22" height="26" rx="3" fill="#FFE14D" opacity="0"/>'
                      % (bid, x + 18 + c * 38, y + 24 + r * 46) for r in range(h // 46 - 1) for c in range(w // 38))
        svg.append('<g id="%s-b%d"><rect x="%d" y="%d" width="%d" height="%d" fill="#2b2466"/>%s</g>' % (bid, k, x, y, w, h, win))
        js.append("tl.fromTo('#%s-b%d',{y:120,opacity:0},{y:0,opacity:1,duration:.5,ease:'power2.out'},%.2f);" % (bid, k, t + 0.1 + k * 0.12))
    js.append("tl.to('.%s-w',{opacity:1,duration:.15,stagger:.02},%.2f);" % (bid, t + 0.7))
    return "".join(svg), "Lucknow · kiraye ka 2BHK", js


def diwali(bid, t):
    """Three yearly costs drop in: a diya, a school bag, a gift."""
    svg = ['<rect x="0" y="0" width="948" height="788" fill="#20122e"/>']
    items = [("Diwali", '<path d="M-70 20 Q0 90 70 20 Z" fill="#FFB904"/><path d="M0 -60 Q26 -20 0 10 Q-26 -20 0 -60 Z" fill="#FF7A1A"/>'),
             ("Admission", '<rect x="-60" y="-50" width="120" height="110" rx="18" fill="#2F6FDB"/><rect x="-40" y="-75" width="80" height="35" rx="14" fill="none" stroke="#2F6FDB" stroke-width="10"/>'),
             ("Shaadi gifts", '<rect x="-60" y="-40" width="120" height="100" rx="8" fill="#C2367A"/><rect x="-8" y="-40" width="16" height="100" fill="#FFB904"/><rect x="-60" y="0" width="120" height="16" fill="#FFB904"/>')]
    js = []
    for k, (lab, art) in enumerate(items):
        cx = 170 + k * 300
        svg.append('<g transform="translate(%d 380)"><g id="%s-i%d">%s<text y="140" text-anchor="middle" font-size="40" '
                   'font-weight="700" fill="#fff" font-family="DM Sans, sans-serif">%s</text></g></g>' % (cx, bid, k, art, lab))
        js.append("tl.fromTo('#%s-i%d',{opacity:0,y:-60},{opacity:1,y:0,duration:.45,ease:'power2.out'},%.2f);" % (bid, k, t + 0.2 + k * 0.5))
    return "".join(svg), "Ye har saal aate hain", js


def ghar(bid, t):
    """A flat with a FOR SALE board; Amit and Neha look at it, Neha unsure. Left to right, nothing overlapping:
    Amit (x 30-200), Neha (x 210-375), the board (x 405-565), the flat (x 590-910)."""
    svg = ['<rect x="0" y="0" width="948" height="788" fill="#11253a"/>',
           '<rect x="0" y="700" width="948" height="88" fill="#0b1826"/>',
           '<g id="%s-h"><rect x="590" y="250" width="320" height="450" fill="#e8e1d4"/>' % bid +
           "".join('<rect x="%d" y="%d" width="56" height="70" fill="#7fb3e6"/>' % (615 + c * 100, 290 + r * 120) for r in range(3) for c in range(3)) +
           '<rect x="722" y="610" width="56" height="90" fill="#6b4a2b"/></g>',
           '<g id="%s-s"><rect x="479" y="540" width="12" height="160" fill="#6b4a2b"/><rect x="405" y="470" width="160" height="76" rx="8" fill="#E0242E"/>'
           '<text x="485" y="519" text-anchor="middle" font-size="30" font-weight="700" fill="#fff" font-family="DM Sans, sans-serif">FOR SALE</text></g>' % bid,
           '<g transform="translate(30 410)">%s</g>' % character("amit", bid + "-a", 290),
           '<g transform="translate(210 420)">%s</g>' % character("neha", bid + "-n", 280)]
    js = ["tl.fromTo('#%s-h',{opacity:0,y:40},{opacity:1,y:0,duration:.5,ease:'power2.out'},%.2f);" % (bid, t + 0.1),
          "tl.fromTo('#%s-s',{opacity:0,rotation:-8},{opacity:1,rotation:0,duration:.4,ease:'power2.out'},%.2f);" % (bid, t + 0.6),
          "mood('%s-n',%.2f,'sad');" % (bid, t + 1.6)]
    return "".join(svg), "Apna ghar: kab?", js


ART = {"v-lko": lucknow, "v-diwali": diwali, "v-ghar": ghar}
