"""The Verma family as flat SVG characters (Money Plan series), so the same faces return in every episode.

character(kind, cid, height, phone=False) -> an <svg> string. kind: amit | neha | aarav | pihu.
Animatable parts carry ids: #<cid>-eyes (blink: scaleY), #<cid>-happy and #<cid>-sad (swap mouths with opacity),
#<cid>-arm (the right arm, rotates from the shoulder). CSS for .ch-part must be on the page (CHAR_CSS below).
"""

SKIN = {"amit": "#C68A5C", "neha": "#D9A070", "aarav": "#C68A5C", "pihu": "#D9A070"}
TOP = {"amit": "#2F6FDB", "neha": "#C2367A", "aarav": "#F2A71B", "pihu": "#FF7BB0"}
BOTTOM = {"amit": "#2B2F3A", "neha": "#5B2A4C", "aarav": "#2E4A7A", "pihu": "#FF7BB0"}
HAIR = "#1E1A18"

CHAR_CSS = (".ch-part{transform-box:fill-box;transform-origin:50% 50%}"
            ".ch-arm{transform-box:fill-box;transform-origin:50% 6%}")


def character(kind, cid, height, phone=False):
    skin, top, bottom = SKIN[kind], TOP[kind], BOTTOM[kind]
    w = round(height * 200 / 340)
    p = []
    # legs and shoes (Pihu's frock covers most of hers)
    p.append('<rect x="70" y="232" width="26" height="88" rx="11" fill="%s"/>' % (skin if kind == "pihu" else bottom))
    p.append('<rect x="104" y="232" width="26" height="88" rx="11" fill="%s"/>' % (skin if kind == "pihu" else bottom))
    p.append('<ellipse cx="81" cy="322" rx="19" ry="8" fill="#1a1a1a"/><ellipse cx="119" cy="322" rx="19" ry="8" fill="#1a1a1a"/>')
    # Neha's hair falls behind the body
    if kind == "neha":
        p.append('<path d="M52 82 Q50 26 100 26 Q150 26 148 82 L154 172 Q132 160 126 120 L74 120 Q68 160 46 172 Z" fill="%s"/>' % HAIR)
    # body
    if kind == "pihu":
        p.append('<path d="M70 128 L130 128 L156 262 L44 262 Z" fill="%s"/>' % top)
        p.append('<rect x="60" y="250" width="80" height="14" rx="7" fill="#ffffff" opacity=".55"/>')
    elif kind == "neha":
        p.append('<path d="M60 130 Q100 118 140 130 L150 270 L50 270 Z" fill="%s"/>' % top)
        p.append('<path d="M60 130 Q100 118 140 130 L136 150 Q100 140 64 150 Z" fill="#FFB904" opacity=".85"/>')
    else:
        p.append('<rect x="58" y="128" width="84" height="116" rx="26" fill="%s"/>' % top)
        if kind == "amit":
            p.append('<path d="M86 128 L100 150 L114 128 Z" fill="#ffffff" opacity=".9"/>')
        if kind == "aarav":
            p.append('<text x="100" y="196" text-anchor="middle" font-size="34" font-weight="700" fill="#1a1a1a" '
                     'font-family="DM Sans, sans-serif">8</text>')
    # left arm (still) and right arm (can wave or hold a phone)
    p.append('<rect x="36" y="134" width="22" height="94" rx="11" fill="%s"/><circle cx="47" cy="230" r="11" fill="%s"/>' % (top, skin))
    arm = '<rect x="142" y="134" width="22" height="94" rx="11" fill="%s"/><circle cx="153" cy="230" r="11" fill="%s"/>' % (top, skin)
    if phone:
        arm = ('<rect x="142" y="134" width="22" height="70" rx="11" fill="%s"/>' % top +
               '<rect x="128" y="168" width="22" height="58" rx="11" fill="%s" transform="rotate(-38 139 172)"/>' % top +
               '<rect x="104" y="168" width="26" height="44" rx="5" fill="#121418" stroke="#3a3f4a" stroke-width="2"/>'
               '<rect x="108" y="173" width="18" height="30" rx="2" fill="#0AF0F0" opacity=".85"/>'
               '<circle cx="112" cy="206" r="9" fill="%s"/>' % skin)
    if kind == "aarav":
        arm += '<rect x="158" y="150" width="11" height="100" rx="5" fill="#D9A35B" transform="rotate(14 163 150)"/>'
    p.append('<g id="%s-arm" class="ch-arm">%s</g>' % (cid, arm))
    if kind == "pihu":
        p.append('<g transform="translate(18 196)"><circle cx="18" cy="14" r="16" fill="#B07A4C"/><circle cx="6" cy="0" r="7" fill="#B07A4C"/>'
                 '<circle cx="30" cy="0" r="7" fill="#B07A4C"/><circle cx="12" cy="12" r="2.5" fill="#1a1a1a"/>'
                 '<circle cx="24" cy="12" r="2.5" fill="#1a1a1a"/></g>')   # her teddy
    # neck, head, ears
    p.append('<rect x="90" y="110" width="20" height="24" fill="%s"/>' % skin)
    p.append('<circle cx="56" cy="82" r="8" fill="%s"/><circle cx="144" cy="82" r="8" fill="%s"/>' % (skin, skin))
    p.append('<circle cx="100" cy="78" r="44" fill="%s"/>' % skin)
    # hair
    if kind in ("amit", "aarav"):
        p.append('<path d="M55 78 Q54 30 100 30 Q146 30 145 78 Q134 50 100 50 Q68 50 55 78 Z" fill="%s"/>' % HAIR)
    if kind == "neha":
        p.append('<path d="M55 84 Q54 30 100 30 Q146 30 145 84 Q132 50 100 50 Q68 50 55 84 Z" fill="%s"/>' % HAIR)
        p.append('<circle cx="100" cy="28" r="17" fill="%s"/><circle cx="100" cy="62" r="3.5" fill="#E0242E"/>' % HAIR)
    if kind == "pihu":
        p.append('<path d="M56 80 Q56 32 100 32 Q144 32 144 80 Q130 54 100 56 Q70 54 56 80 Z" fill="%s"/>' % HAIR)
        p.append('<circle cx="48" cy="62" r="15" fill="%s"/><circle cx="152" cy="62" r="15" fill="%s"/>' % (HAIR, HAIR))
        p.append('<circle cx="56" cy="56" r="5" fill="#FF7BB0"/><circle cx="144" cy="56" r="5" fill="#FF7BB0"/>')
    # face: eyes (blink), glasses for Amit, cheeks, two mouths
    p.append('<g id="%s-eyes" class="ch-part"><ellipse cx="84" cy="80" rx="5" ry="6.5" fill="#1b1b1b"/>'
             '<ellipse cx="116" cy="80" rx="5" ry="6.5" fill="#1b1b1b"/></g>' % cid)
    if kind == "amit":
        p.append('<g fill="none" stroke="#1b1b1b" stroke-width="3"><circle cx="84" cy="80" r="13"/><circle cx="116" cy="80" r="13"/>'
                 '<path d="M97 80 L103 80"/></g>')
    p.append('<circle cx="74" cy="96" r="6" fill="#E46A6A" opacity=".25"/><circle cx="126" cy="96" r="6" fill="#E46A6A" opacity=".25"/>')
    p.append('<path id="%s-happy" d="M86 100 Q100 113 114 100" fill="none" stroke="#5A2A1A" stroke-width="4" stroke-linecap="round"/>' % cid)
    p.append('<path id="%s-sad" d="M88 108 Q100 97 112 108" fill="none" stroke="#5A2A1A" stroke-width="4" stroke-linecap="round" opacity="0"/>' % cid)
    return ('<svg width="%d" height="%d" viewBox="0 0 200 340" aria-label="%s">%s</svg>'
            % (w, height, kind.capitalize(), "".join(p)))
