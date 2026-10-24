#!/usr/bin/env python3
"""Generates the "Alpha x Lion x Luminous Seal" SVG assets for Aseef Ahmed's GitHub profile README.

Palette: obsidian black, gold/amber, with a cool platinum / steel-blue accent used sparingly.
Motion: slow shimmer, gentle glow, line-draw. Static renders show the finished state.
"""
import math, os, random
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

BG = "#08090C"; G1 = "#F5B301"; G2 = "#FFD54A"; G3 = "#E8860C"
INK = "#E8EAED"; MUTED = "#9AA4AF"; LINE = "#262B33"
PLAT = "#C9D1D9"; STEEL = "#3BA3FF"
CARD = "#0F1116"; CARD2 = "#13151B"; DISC = "#16140E"
FONT = "'Segoe UI',Ubuntu,'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"


def common_defs(w, h, uid):
    return f'''
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{G2}"/><stop offset=".5" stop-color="{G1}"/><stop offset="1" stop-color="{G3}"/></linearGradient>
<linearGradient id="goldH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{G3}"/><stop offset=".5" stop-color="{G2}"/><stop offset="1" stop-color="{G3}"/></linearGradient>
<linearGradient id="platH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PLAT}" stop-opacity="0"/><stop offset=".5" stop-color="{PLAT}"/><stop offset="1" stop-color="{PLAT}" stop-opacity="0"/></linearGradient>
<linearGradient id="plat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2F5F8"/><stop offset="1" stop-color="#9AA6B2"/></linearGradient>
<linearGradient id="band" x1="0" x2="1"><stop offset="0" stop-color="#FFF7DA" stop-opacity="0"/><stop offset=".5" stop-color="#FFF7DA" stop-opacity=".7"/><stop offset="1" stop-color="#FFF7DA" stop-opacity="0"/></linearGradient>
<linearGradient id="border" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{G1}" stop-opacity=".8"/><stop offset=".5" stop-color="{PLAT}" stop-opacity=".18"/><stop offset="1" stop-color="{G2}" stop-opacity=".7"/></linearGradient>
<linearGradient id="aL" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{G1}"/><stop offset="1" stop-color="#A85C05"/></linearGradient>
<linearGradient id="aR" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF1B8"/><stop offset=".45" stop-color="{G2}"/><stop offset="1" stop-color="{G1}"/></linearGradient>
<radialGradient id="glowA" cx=".85" cy=".2" r=".6"><stop offset="0" stop-color="{G3}" stop-opacity=".16"/><stop offset="1" stop-color="{G3}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowB" cx=".08" cy="1" r=".55"><stop offset="0" stop-color="{STEEL}" stop-opacity=".07"/><stop offset="1" stop-color="{STEEL}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
  <path d="M32 0 H0 V32" fill="none" stroke="{PLAT}" stroke-opacity=".035" stroke-width="1"/>
</pattern>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<clipPath id="card{uid}"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20"/></clipPath>'''


def frame(w, h, uid, body, extra_defs="", style=""):
    css = f'''<style>
.t{{font-family:{FONT}}} .m{{font-family:{MONO}}}
.pulse{{animation:pulse 4s ease-in-out infinite}} @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}
.float{{animation:flt 9s ease-in-out infinite}} @keyframes flt{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
.flow{{stroke-dasharray:6 12;animation:flow 3.2s linear infinite}} @keyframes flow{{to{{stroke-dashoffset:-36}}}}
{style}</style>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<defs>{common_defs(w, h, uid)}{extra_defs}</defs>{css}
<g clip-path="url(#card{uid})">
<rect width="{w}" height="{h}" fill="{BG}"/>
<rect width="{w}" height="{h}" fill="url(#grid)"/>
<rect width="{w}" height="{h}" fill="url(#glowA)"/>
<rect width="{w}" height="{h}" fill="url(#glowB)"/>
{body}
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="none" stroke="url(#border)" stroke-width="1.4"/>
</svg>'''


def write(name, svg):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)


def text(x, y, s, size=16, fill=INK, weight=400, anchor="start", cls="t", extra=""):
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'


def chip(x, y, label, size=13, h=26, pad=12, cw=7.9, fill="#14130F", stroke=G1, color=G2, anchor="start"):
    w = len(label) * cw * size / 13 + pad * 2
    if anchor == "middle":
        x = x - w / 2
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{stroke}" stroke-opacity=".5"/>'
            + text(x + w / 2, y + h / 2 + size * .36, label, size, color, 600, "middle")), w


_SC = [0]
def uid():
    _SC[0] += 1
    return _SC[0]


def sweep(x0, y0, wd, ht, dist, dur=9):
    """A soft highlight band that crosses once, then rests (slow, refined shimmer)."""
    return (f'<rect x="{x0-240}" y="{y0}" width="200" height="{ht}" fill="url(#band)">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{dist} 0;{dist} 0" keyTimes="0;.45;1" dur="{dur}s" repeatCount="indefinite"/></rect>')


def shine_text(x, y, s, size, weight=800, anchor="start", extra="", width=900, glow=True, fill="url(#gold)"):
    """Gold text with a slow sweeping highlight (static render = plain gold)."""
    cid = f"sh{uid()}"
    t = f'<text x="{x}" y="{y}" class="t" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'
    base = t.replace('<text ', f'<text fill="{fill}" ' + ('filter="url(#glow)" ' if glow else ''), 1)
    x0 = x - (width / 2 if anchor == "middle" else 0)
    return base + f'<clipPath id="{cid}">{t}</clipPath><g clip-path="url(#{cid})">{sweep(x0, y-size, width, size*1.4, width+300)}</g>'


def draw_anim(p, dur=12, begin=0):
    """Line-draw: draws in, holds, then retracts. Static render shows the full line."""
    return (f'stroke-dasharray="{p:.1f}" stroke-dashoffset="0"><animate attributeName="stroke-dashoffset" values="{p:.1f};0;0;{-p:.1f}" '
            f'keyTimes="0;.28;.88;1" dur="{dur}s" begin="-{begin}s" repeatCount="indefinite"/')


def hexpts(r, rot=-90):
    return " ".join(f"{r*math.cos(math.radians(rot+60*i)):.1f},{r*math.sin(math.radians(rot+60*i)):.1f}" for i in range(6))


# ---------------------------------------------------------------- Alpha Group mark
def alpha_mark(cx, cy, s=1.0, anim=True, frame_hex=True, node=True):
    """Original Alpha Group monogram: a faceted, sharp-apex Alpha (two split legs, a platinum
    crossbar that exits as a circuit trace into a steel-blue node), set in a line-drawn hexagon."""
    k = uid()
    o = [f'<g transform="translate({cx} {cy}) scale({s})">']
    if frame_hex:
        p = 6 * 72
        o.append(f'<polygon points="{hexpts(72)}" fill="#0C0D11" fill-opacity=".85" stroke="{G1}" stroke-opacity=".25" stroke-width="1"/>')
        da = draw_anim(p, 14) if anim else 'stroke-dasharray="none"'
        o.append(f'<polygon points="{hexpts(72)}" fill="none" stroke="url(#gold)" stroke-width="2" stroke-linejoin="miter" {da}></polygon>' if anim
                 else f'<polygon points="{hexpts(72)}" fill="none" stroke="url(#gold)" stroke-width="2"/>')
        o.append(f'<polygon points="{hexpts(63)}" fill="none" stroke="{PLAT}" stroke-opacity=".16" stroke-width="1"/>')
        for i in range(6):  # vertex ticks
            a = math.radians(-90 + 60 * i)
            o.append(f'<line x1="{76*math.cos(a):.1f}" y1="{76*math.sin(a):.1f}" x2="{82*math.cos(a):.1f}" y2="{82*math.sin(a):.1f}" stroke="{G2}" stroke-opacity=".7" stroke-width="1.6"/>')
    left = "0,-50 0,-15 -25,42 -42,42"
    right = "1.5,-50 42,42 25,42 1.5,-15"
    o.append(f'<polygon points="{left}" fill="url(#aL)"/>')
    o.append(f'<polygon points="{right}" fill="url(#aR)"/>')
    # crossbar (platinum) spanning the legs
    o.append(f'<polygon points="-28.6,13 29.1,13 32.2,20 -31.7,20" fill="url(#plat)"/>')
    if node:
        trace = "M32 16.5 H42 L50 8 H57"
        o.append(f'<path d="{trace}" fill="none" stroke="{STEEL}" stroke-width="2.2" stroke-linecap="square" stroke-linejoin="miter" opacity=".95"/>')
        na = '<animate attributeName="opacity" values="1;.45;1" dur="4.5s" repeatCount="indefinite"/>' if anim else ""
        o.append(f'<circle cx="59" cy="8" r="3.6" fill="{STEEL}" filter="url(#glow)">{na}</circle>')
    # apex highlight + slow shimmer across the monogram
    if anim:
        o.append(f'<clipPath id="am{k}"><polygon points="{left}"/><polygon points="{right}"/></clipPath>'
                 f'<g clip-path="url(#am{k})"><rect x="-120" y="-60" width="46" height="120" fill="url(#band)" transform="skewX(-18)">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;200 0;200 0" keyTimes="0;.35;1" dur="8s" repeatCount="indefinite" additive="sum"/></rect></g>')
    o.append('</g>')
    return "".join(o)


def alpha_wordmark(x, y, size=56, anchor="start", anim=True, width=560):
    """ALPHA (heavy gold) + GROUP (light platinum), wide tracking."""
    ls = size * .16
    t_alpha = f'<tspan font-weight="800">ALPHA</tspan>'
    t_group = f'<tspan font-weight="300" fill="url(#plat)" dx="{size*.28:.1f}">GROUP</tspan>'
    t = (f'<text x="{x}" y="{y}" class="t" font-size="{size}" text-anchor="{anchor}" letter-spacing="{ls:.1f}" fill="url(#gold)">{t_alpha}{t_group}</text>')
    out = t
    if anim:
        cid = f"wm{uid()}"
        clip = f'<text x="{x}" y="{y}" class="t" font-size="{size}" font-weight="800" text-anchor="{anchor}" letter-spacing="{ls:.1f}">ALPHA</text>'
        x0 = x - (width / 2 if anchor == "middle" else 0)
        out += f'<clipPath id="{cid}">{clip}</clipPath><g clip-path="url(#{cid})">{sweep(x0, y-size, width, size*1.3, width+300, 10)}</g>'
    return out


# ---------------------------------------------------------------- lion crest
def lion(cx, cy, s=1.0, anim=True, crown=True):
    """Original geometric lion head: faceted face, two-ring mane, crowned with the Alpha mark."""
    out = [f'<g transform="translate({cx} {cy}) scale({s})">']
    out.append(f'<circle r="150" fill="{G3}" opacity=".14" filter="url(#soft)"/>')
    rays = []
    n = 20
    for i in range(n):
        a = 2 * math.pi * i / n
        a1, a2 = a - math.pi / n * .78, a + math.pi / n * .78
        r0, r1 = 92, (142 if i % 2 == 0 else 126)
        p = [(r0 * math.cos(a1), r0 * math.sin(a1)), (r1 * math.cos(a), r1 * math.sin(a)), (r0 * math.cos(a2), r0 * math.sin(a2))]
        rays.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in p)}" fill="url(#maneA)" stroke="{G2}" stroke-opacity=".3" stroke-width=".8"/>')
    rot = '<animateTransform attributeName="transform" type="rotate" values="0;360" dur="140s" repeatCount="indefinite"/>' if anim else ""
    out.append(f'<g>{"".join(rays)}{rot}</g>')
    rh = []
    m = 16
    for i in range(m):
        a = 2 * math.pi * i / m + .2
        aa, ab = a - math.pi / m * .9, a + math.pi / m * .9
        pts = [(74 * math.cos(a), 74 * math.sin(a)), (96 * math.cos(aa), 96 * math.sin(aa)), (112 * math.cos(a), 112 * math.sin(a)), (96 * math.cos(ab), 96 * math.sin(ab))]
        rh.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="url(#maneB)" stroke="{BG}" stroke-width="1.2"/>')
    rot2 = '<animateTransform attributeName="transform" type="rotate" values="360;0" dur="200s" repeatCount="indefinite"/>' if anim else ""
    out.append(f'<g>{"".join(rh)}{rot2}</g>')
    ring_anim = '<animate attributeName="stroke-opacity" values=".85;.35;.85" dur="6s" repeatCount="indefinite"/>' if anim else ""
    out.append(f'<circle r="86" fill="none" stroke="{G2}" stroke-width="1.4" stroke-opacity=".85">{ring_anim}</circle>')
    out.append(f'<polygon points="-50,-58 -60,-92 -26,-72" fill="{G3}" stroke="{G2}" stroke-width="1"/>')
    out.append(f'<polygon points="50,-58 60,-92 26,-72" fill="{G3}" stroke="{G2}" stroke-width="1"/>')
    out.append(f'<polygon points="-47,-64 -54,-84 -33,-71" fill="#5A3305"/>')
    out.append(f'<polygon points="47,-64 54,-84 33,-71" fill="#5A3305"/>')
    head = "0,-80 -48,-64 -64,-22 -56,24 -32,62 0,80 32,62 56,24 64,-22 48,-64"
    out.append(f'<polygon points="{head}" fill="url(#face)" stroke="{G2}" stroke-width="1.5"/>')
    out.append(f'<polygon points="0,-80 -22,-42 0,-12 22,-42" fill="{G2}" opacity=".9"/>')
    out.append(f'<polygon points="-48,-64 -22,-42 -64,-22" fill="{G1}" opacity=".85"/>')
    out.append(f'<polygon points="48,-64 22,-42 64,-22" fill="{G3}" opacity=".85"/>')
    out.append(f'<polygon points="-64,-22 -46,-14 -56,24" fill="{G3}" opacity=".9"/>')
    out.append(f'<polygon points="64,-22 46,-14 56,24" fill="#C46F08" opacity=".9"/>')
    out.append(f'<polygon points="-56,24 -32,30 -32,62" fill="#C46F08"/>')
    out.append(f'<polygon points="56,24 32,30 32,62" fill="#A85C05"/>')
    out.append(f'<polyline points="-48,-30 -18,-24 0,-14 18,-24 48,-30" fill="none" stroke="#5A3305" stroke-width="2.4" stroke-linejoin="round"/>')
    for sx in (-1, 1):
        out.append(f'<g transform="translate({sx*29} -16)"><polygon points="{sx*-15},-4 {sx*15},-1 {sx*9},6 {sx*-13},3" fill="#1A0F02"/><polygon points="{sx*-4},-2.5 {sx*5},-1 {sx*3},3 {sx*-4},2" fill="#FFF3B0" filter="url(#glow)"/></g>')
    out.append(f'<polygon points="0,-12 -14,10 14,10" fill="{G1}"/>')
    out.append(f'<polygon points="-14,10 14,10 0,26" fill="#2A1703"/>')
    out.append(f'<polygon points="-14,10 0,26 -2,44 -30,34" fill="#FFE9A3"/>')
    out.append(f'<polygon points="14,10 0,26 2,44 30,34" fill="#F7D774"/>')
    out.append(f'<polyline points="-16,46 0,40 16,46" fill="none" stroke="#2A1703" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(f'<polygon points="-16,52 0,80 16,52 0,58" fill="{G3}"/>')
    for (x, y) in [(-20, 32), (-24, 38), (-16, 37), (20, 32), (24, 38), (16, 37)]:
        out.append(f'<circle cx="{x}" cy="{y}" r="1.3" fill="#7A4A06"/>')
    # Alpha mark as the crest's crown
    if crown:
        out.append(alpha_mark(0, -122, .36, anim, frame_hex=True, node=False))
    out.append('</g>')
    return "".join(out)


LION_DEFS = f'''
<linearGradient id="maneA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{G2}"/><stop offset=".55" stop-color="{G3}"/><stop offset="1" stop-color="#7A3E04"/></linearGradient>
<linearGradient id="maneB" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#B65F05"/><stop offset="1" stop-color="{G1}"/></linearGradient>
<linearGradient id="face" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{G2}"/><stop offset="1" stop-color="{G3}"/></linearGradient>'''


def circuit(points, color=STEEL, op=.35, node_end=True, anim=True, dur=10, begin=0):
    d = "M" + " L".join(f"{x} {y}" for x, y in points)
    p = sum(math.dist(points[i], points[i + 1]) for i in range(len(points) - 1))
    o = f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1.3" ' + (draw_anim(p, dur, begin) + '></path>' if anim else '/>')
    if node_end:
        x, y = points[-1]
        o += f'<circle cx="{x}" cy="{y}" r="2.6" fill="{color}" opacity=".8"/>'
        x, y = points[0]
        o += f'<rect x="{x-2.5}" y="{y-2.5}" width="5" height="5" fill="none" stroke="{color}" stroke-opacity=".6"/>'
    return o


# ---------------------------------------------------------------- luminous seal motif (original art)
# A floating Alpha capstone with a glowing eye, a line-engraved pyramid, slow light rays, a
# rotating seal ring with Roman numerals and Karachi coordinates, and compass geometry.
COORDS = "24.8607° N · 67.0011° E"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

SEAL_DEFS = f'''
<radialGradient id="aura" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFF3C4" stop-opacity=".5"/><stop offset=".35" stop-color="{G1}" stop-opacity=".16"/><stop offset="1" stop-color="{G1}" stop-opacity="0"/></radialGradient>
<linearGradient id="ray" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFF3C4" stop-opacity=".5"/><stop offset=".5" stop-color="{G2}" stop-opacity=".14"/><stop offset="1" stop-color="{G1}" stop-opacity="0"/></linearGradient>
<linearGradient id="pyrL" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A2C0A"/><stop offset="1" stop-color="#15110A"/></linearGradient>
<linearGradient id="pyrR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#231A06"/><stop offset="1" stop-color="#0D0B07"/></linearGradient>
<radialGradient id="iris" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFF7DA"/><stop offset=".3" stop-color="{G2}"/><stop offset=".75" stop-color="{G3}"/><stop offset="1" stop-color="#6A3604"/></radialGradient>'''

CAP_K = 54 / 94  # capstone / pyramid side slope (dx per dy)


def eye(cx, cy, w, anim=True):
    """Original almond eye: engraved iris rings, dark pupil, soft breathing glow."""
    k = uid(); a = w * .26
    almond = f"M{-w/2:.1f} 0 Q0 {-2*a:.1f} {w/2:.1f} 0 Q0 {2*a:.1f} {-w/2:.1f} 0Z"
    o = [f'<g transform="translate({cx} {cy})">']
    ga = '<animate attributeName="opacity" values=".55;1;.55" dur="6s" repeatCount="indefinite"/>' if anim else ""
    o.append(f'<circle r="{w*.95:.1f}" fill="url(#aura)" opacity=".8">{ga}</circle>')
    o.append(f'<clipPath id="ey{k}"><path d="{almond}"/></clipPath>')
    o.append(f'<path d="{almond}" fill="#0B0906"/>')
    o.append(f'<g clip-path="url(#ey{k})">')
    ir = w * .2
    o.append(f'<circle r="{ir:.1f}" fill="url(#iris)"/>')
    rot = f'<animateTransform attributeName="transform" type="rotate" values="0;360" dur="40s" repeatCount="indefinite"/>' if anim else ""
    o.append(f'<circle r="{ir*.78:.1f}" fill="none" stroke="#7A4A06" stroke-width="{w*.012:.2f}" stroke-dasharray="{w*.018:.2f} {w*.022:.2f}">{rot}</circle>')
    o.append(f'<circle r="{ir:.1f}" fill="none" stroke="#5A3305" stroke-width="{w*.014:.2f}"/>')
    pa = f'<animate attributeName="r" values="{w*.075:.1f};{w*.06:.1f};{w*.075:.1f}" dur="7s" repeatCount="indefinite"/>' if anim else ""
    o.append(f'<circle r="{w*.075:.1f}" fill="#120B02">{pa}</circle>')
    o.append(f'<circle cx="{-w*.05:.1f}" cy="{-w*.05:.1f}" r="{w*.028:.1f}" fill="#FFFDF2" opacity=".95"/>')
    o.append('</g>')
    o.append(f'<path d="{almond}" fill="none" stroke="url(#gold)" stroke-width="{max(w*.04,0.8):.2f}" stroke-linejoin="round"/>')
    o.append('</g>')
    return "".join(o)


def capstone(cx, cy, s=1.0, anim=True, with_eye=True):
    """Alpha Group capstone: the Α letterform as a floating, faceted gold capstone (apex,
    split legs, platinum crossbar) with a glowing eye set in its upper body."""
    k = uid()
    left = "0,-62 -54,32 -16,32 0,0"; right = "0,-62 0,0 16,32 54,32"
    o = [f'<g transform="translate({cx} {cy}) scale({s})">']
    ga = '<animate attributeName="opacity" values=".7;1;.7" dur="6s" repeatCount="indefinite"/>' if anim else ""
    o.append(f'<circle cy="-14" r="110" fill="url(#aura)">{ga}</circle>')
    o.append(f'<polygon points="{left}" fill="url(#aL)"/><polygon points="{right}" fill="url(#aR)"/>')
    # banknote-style engraving on the faces
    o.append(f'<clipPath id="cp{k}"><polygon points="{left}"/><polygon points="{right}"/></clipPath><g clip-path="url(#cp{k})">')
    o.append("".join(f'<line x1="-60" y1="{y}" x2="60" y2="{y}" stroke="#6A3A04" stroke-opacity="{.22 if y < 0 else .3}" stroke-width=".7"/>' for y in range(-56, 34, 4)))
    o.append(f'<rect x="0" y="-70" width="60" height="110" fill="#5A3305" opacity=".18"/>')
    if anim:
        o.append(f'<rect x="-120" y="-70" width="40" height="110" fill="url(#band)" transform="skewX(-18)">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;220 0;220 0" keyTimes="0;.35;1" dur="9s" repeatCount="indefinite" additive="sum"/></rect>')
    o.append('</g>')
    o.append(f'<polygon points="-44,12 44,12 48.5,19 -48.5,19" fill="url(#plat)"/>')
    o.append(f'<path d="M0 -62 L-54 32 H-16 L0 0 L16 32 H54 Z" fill="none" stroke="#FFF3C4" stroke-opacity=".55" stroke-width="1" stroke-linejoin="miter"/>')
    if with_eye:
        o.append(eye(0, -24, 40, anim))
    o.append('</g>')
    return "".join(o)


def pyramid_body(cx, apex_y, top_y, base_y, anim=True, course=14):
    """Truncated, line-engraved pyramid whose sides continue the capstone's slope."""
    k = uid()
    ht = (top_y - apex_y) * CAP_K; hb = (base_y - apex_y) * CAP_K
    L = f"{cx-ht:.1f},{top_y} {cx:.1f},{top_y} {cx:.1f},{base_y} {cx-hb:.1f},{base_y}"
    R = f"{cx:.1f},{top_y} {cx+ht:.1f},{top_y} {cx+hb:.1f},{base_y} {cx:.1f},{base_y}"
    o = [f'<polygon points="{L}" fill="url(#pyrL)"/><polygon points="{R}" fill="url(#pyrR)"/>']
    o.append(f'<clipPath id="pb{k}"><polygon points="{L}"/><polygon points="{R}"/></clipPath><g clip-path="url(#pb{k})">')
    row = 0
    y = top_y + course
    while y < base_y:
        o.append(f'<line x1="{cx-hb}" y1="{y:.1f}" x2="{cx+hb}" y2="{y:.1f}" stroke="{G1}" stroke-opacity=".32" stroke-width=".8"/>')
        off = (course * 1.9) * (.5 if row % 2 else 0)
        xx = cx - hb + off
        while xx < cx + hb:
            o.append(f'<line x1="{xx:.1f}" y1="{y-course:.1f}" x2="{xx:.1f}" y2="{y:.1f}" stroke="{G1}" stroke-opacity=".16" stroke-width=".7"/>')
            xx += course * 1.9
        y += course; row += 1
    # fine engraved shading on the shadow face
    for i in range(0, int(hb * 2 + (base_y - top_y)), 5):
        o.append(f'<line x1="{cx + i:.1f}" y1="{top_y}" x2="{cx + i - (base_y-top_y)*.6:.1f}" y2="{base_y}" stroke="#000" stroke-opacity=".22" stroke-width=".7"/>')
    o.append('</g>')
    outline = f"M{cx-ht:.1f} {top_y} H{cx+ht:.1f} L{cx+hb:.1f} {base_y} H{cx-hb:.1f} Z"
    p = 2 * ht + 2 * hb + 2 * math.dist((ht, top_y), (hb, base_y))
    o.append(f'<path d="{outline}" fill="none" stroke="{G1}" stroke-opacity=".25" stroke-width="1"/>')
    o.append(f'<path d="{outline}" fill="none" stroke="url(#gold)" stroke-width="1.6" stroke-linejoin="miter" ' + (draw_anim(p, 16) + '></path>' if anim else '/>'))
    o.append(f'<line x1="{cx}" y1="{top_y}" x2="{cx}" y2="{base_y}" stroke="{G2}" stroke-opacity=".28" stroke-width=".8"/>')
    return "".join(o)


def light_rays(cx, cy, n=36, r0=40, r1=230, anim=True, dur=180, op=1.0):
    o = [f'<g transform="translate({cx} {cy})" opacity="{op}"><g>']
    for i in range(n):
        a = 360 * i / n
        ln = r1 if i % 2 == 0 else r1 * .72
        wd = 2.6 if i % 2 == 0 else 1.6
        o.append(f'<polygon points="{r0},{-wd/2} {ln:.0f},0 {r0},{wd/2}" fill="url(#ray)" transform="rotate({a:.1f})"/>')
    if anim:
        o.append(f'<animateTransform attributeName="transform" type="rotate" values="0;360" dur="{dur}s" repeatCount="indefinite"/>')
        o.append('<animate attributeName="opacity" values=".65;1;.65" dur="8s" repeatCount="indefinite"/>')
    o.append('</g></g>')
    return "".join(o)


def seed_geometry(cx, cy, r, op=.08):
    """Compass construction: seed-of-life circles, bounding circle and hexagon."""
    o = [f'<g transform="translate({cx} {cy})" fill="none" stroke="{PLAT}" stroke-opacity="{op}" stroke-width="1">']
    o.append(f'<circle r="{r}"/>')
    for i in range(6):
        a = math.radians(60 * i - 90)
        o.append(f'<circle cx="{r*math.cos(a):.1f}" cy="{r*math.sin(a):.1f}" r="{r}"/>')
    o.append(f'<circle r="{2*r}"/><polygon points="{hexpts(2*r)}"/>')
    o.append(f'<line x1="{-2.3*r:.0f}" y1="0" x2="{2.3*r:.0f}" y2="0" stroke-dasharray="2 6"/><line x1="0" y1="{-2.3*r:.0f}" x2="0" y2="{2.3*r:.0f}" stroke-dasharray="2 6"/>')
    o.append('</g>')
    return "".join(o)


def seal_ring(cx, cy, R, label, anim=True, dur=240, numerals=True):
    """Engraved rotating seal ring: legend on a circular path, ticks, Roman numerals."""
    k = uid(); rt = R - 12
    o = [f'<g transform="translate({cx} {cy})"><g>']
    o.append(f'<circle r="{R}" fill="none" stroke="{G1}" stroke-opacity=".45" stroke-width="1.2"/>')
    o.append(f'<circle r="{R-22}" fill="none" stroke="{PLAT}" stroke-opacity=".22" stroke-width="1"/>')
    o.append(f'<path id="rp{k}" d="M{-rt} 0 A{rt} {rt} 0 1 1 {rt} 0 A{rt} {rt} 0 1 1 {-rt} 0" fill="none"/>')
    o.append(f'<text class="m" font-size="{max(R*.05,8.5):.1f}" fill="{PLAT}" fill-opacity=".6" letter-spacing="{R*.016:.1f}"><textPath href="#rp{k}" startOffset="0">{esc(label)}</textPath></text>')
    for i in range(120):
        a = math.radians(3 * i)
        big = i % 10 == 0
        r2 = R - 22 - (9 if big else 4)
        o.append(f'<line x1="{(R-22)*math.cos(a):.1f}" y1="{(R-22)*math.sin(a):.1f}" x2="{r2*math.cos(a):.1f}" y2="{r2*math.sin(a):.1f}" stroke="{G2 if big else PLAT}" stroke-opacity="{.6 if big else .25}" stroke-width="{1.2 if big else .8}"/>')
    if numerals:
        for i, rn in enumerate(ROMAN):
            a = math.radians(30 * i - 90); rr = R - 44
            o.append(f'<text x="{rr*math.cos(a):.1f}" y="{rr*math.sin(a)+3.5:.1f}" font-family="Georgia,\'Times New Roman\',serif" font-size="{max(R*.05,8):.1f}" fill="{G2}" fill-opacity=".55" text-anchor="middle" transform="rotate({30*i} {rr*math.cos(a):.1f} {rr*math.sin(a):.1f})">{rn}</text>')
    if anim:
        o.append(f'<animateTransform attributeName="transform" type="rotate" values="0;-360" dur="{dur}s" repeatCount="indefinite"/>')
    o.append('</g></g>')
    return "".join(o)


def emblem(cx, cy, s=1.0, anim=True, ring_label=None, with_lion=True):
    """Full blended crest in local coords (ring radius 212): seal ring, compass geometry,
    light rays, engraved pyramid, guardian lion, and the floating Alpha capstone with eye."""
    R = 212
    lab = ring_label or f"SOFTWARE · DATA · AI · EDUCATION · KARACHI · {COORDS} · "
    k = uid()
    o = [f'<g transform="translate({cx} {cy}) scale({s})">']
    o.append(f'<circle r="{R-8}" fill="{G3}" opacity=".10" filter="url(#soft)"/>')
    o.append(seed_geometry(0, -10, 52, .07))
    o.append(f'<clipPath id="em{k}"><circle r="{R-24}"/></clipPath><g clip-path="url(#em{k})">')
    o.append(light_rays(0, -128, 40, 30, 260, anim))
    o.append('</g>')
    o.append(seal_ring(0, 0, R, lab * 2, anim))
    apex = -180
    o.append(pyramid_body(0, apex, -72, 128, anim))
    # ground line with engraved hatch
    o.append(f'<line x1="-188" y1="128" x2="188" y2="128" stroke="url(#goldH)" stroke-width="1.4"/>')
    o.append("".join(f'<line x1="{x}" y1="132" x2="{x-6}" y2="140" stroke="{G1}" stroke-opacity=".28" stroke-width=".8"/>' for x in range(-150, 156, 9)))
    if with_lion:
        o.append(lion(0, 34, .5, anim, crown=False))
    fl = '<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="8s" repeatCount="indefinite" additive="sum"/>' if anim else ""
    o.append(f'<g>{capstone(0, -118, 1.0, anim)}{fl}</g>')
    o.append('</g>')
    return "".join(o)


def mini_capstone(cx, cy, s=.3, anim=True):
    return (f'<g transform="translate({cx} {cy}) scale({s})">' + light_rays(0, -20, 16, 30, 120, anim, 120, .8)
            + capstone(0, 0, 1.0, anim) + '</g>')


# ---------------------------------------------------------------- header
def header():
    W, H = 1200, 480
    body = []
    LX, LY = 966, 244
    random.seed(11)
    for i in range(16):
        x = 32 * random.randint(1, 36); y = 32 * random.randint(1, 14)
        d = random.uniform(8, 14); b = random.uniform(0, 10)
        col = random.choice([PLAT, G2, STEEL])
        body.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{col}" opacity=".1"><animate attributeName="opacity" values=".08;.6;.08" dur="{d:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>')
    body.append(circuit([(LX + 212, LY - 60), (1172, LY - 60), (1172, 40)], color=G1, op=.28, dur=12, begin=4, node_end=False))
    body.append(circuit([(LX + 200, LY + 80), (1180, LY + 80)], dur=12, begin=7))
    body.append(emblem(LX, LY, .97))
    # left column
    body.append(mini_capstone(74, 82, .2) + text(100, 90, "SOFTWARE  ·  DATA  ·  AI  ·  EDUCATION", 13.5, PLAT, 600, extra='letter-spacing="4"'))
    body.append(shine_text(58, 170, "ASEEF AHMED", 72, 800, extra='letter-spacing="3"', width=620))
    body.append(f'<rect x="60" y="190" width="430" height="2" fill="{LINE}"/>')
    body.append(f'<rect x="60" y="189" width="430" height="4" rx="2" fill="url(#goldH)"><animate attributeName="width" values="0;430;430;0" keyTimes="0;.3;.88;1" dur="12s" repeatCount="indefinite"/></rect>')
    body.append(alpha_mark(78, 232, .27, node=True))
    body.append(text(108, 240, "Founder, Alpha Group", 23, G2, 700, extra='letter-spacing=".5"'))
    body.append(text(60, 276, "Software Engineer  ·  Data Scientist  ·  Senior Manager Academics", 19, INK, 600))
    roles = ["Data Science  ·  AI & ML  ·  LLMs  ·  RAG  ·  Agentic AI",
             "Big Data  ·  Apache Hadoop  ·  Apache Spark",
             "MERN Stack  ·  .NET Core  ·  Python  ·  R  ·  C#",
             "Trainer  ·  Motivational Speaker  ·  Faculty Capacity Builder"]
    n = len(roles); dur = n * 4
    for i, r in enumerate(roles):
        s0 = i / n; s1 = (i + 1) / n; f = .04
        if i == 0:
            kt = [0, s1 - f, s1, 1 - f, 1]; vals = [1, 1, 0, 0, 1]
        else:
            kt = [0, s0, s0 + f, s1 - f, s1, 1]; vals = [0, 0, 1, 1, 0, 0]
        init = "1" if i == 0 else "0"
        body.append(f'<g opacity="{init}"><text x="60" y="316" class="m" font-size="16" fill="{PLAT}"><tspan fill="{STEEL}">&gt;_ </tspan>{esc(r)}</text>'
                    f'<animate attributeName="opacity" values="{";".join(map(str, vals))}" keyTimes="{";".join(f"{k:.3f}" for k in kt)}" dur="{dur}s" repeatCount="indefinite"/></g>')
    x = 60
    for lab in ["Alpha Group", "Aptech Learning", "Contour Software", "MS Data Science · NED UET"]:
        hl = lab == "Alpha Group"
        c, w = chip(x, 344, lab, 13, fill=("#1C1708" if hl else "#121418"), stroke=(G1 if hl else PLAT), color=(G2 if hl else PLAT))
        body.append(c); x += w + 10
    body.append(text(60, 412, "Building software, data and AI solutions — and the engineers of tomorrow.", 15, MUTED, 400, extra='font-style="italic"'))
    body.append(f'<text x="60" y="444" class="m" font-size="12" fill="{MUTED}" letter-spacing="2"><tspan fill="{G1}">◆</tspan>  KARACHI  ·  {COORDS}</text>')
    write("header.svg", frame(W, H, "h", "".join(body), LION_DEFS + SEAL_DEFS))


# ---------------------------------------------------------------- section banner
def guilloche(x0, x1, cy, amp=9, anim=True):
    """Banknote-style interlaced sine band that drifts slowly."""
    k = uid(); w = x1 - x0
    o = [f'<clipPath id="gu{k}"><rect x="{x0}" y="{cy-amp-4}" width="{w}" height="{2*amp+8}"/></clipPath><g clip-path="url(#gu{k})">']
    per = 40
    for j, (ph, col, op) in enumerate([(0, G1, .5), (per / 3, PLAT, .22), (2 * per / 3, G2, .35)]):
        pts = []
        xx = x0 - per * 2
        while xx <= x1 + per:
            pts.append(f"{xx:.1f},{cy + amp * math.sin(2 * math.pi * (xx - x0 + ph) / per):.2f}")
            xx += 2
        an = f'<animateTransform attributeName="transform" type="translate" values="0 0;{per} 0" dur="{9+j*3}s" repeatCount="indefinite"/>' if anim else ""
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="1">{an}</polyline>')
    o.append('</g>')
    return "".join(o)


def banner(fname, num, title, sub):
    W, H = 1200, 96
    b = []
    rn = ROMAN[int(num) - 1]
    b.append(f'<text x="112" y="68" font-family="Georgia,\'Times New Roman\',serif" font-size="44" font-weight="700" fill="none" stroke="{G1}" stroke-opacity=".6" stroke-width="1.2" text-anchor="end">{rn}</text>')
    b.append(mini_capstone(144, 52, .24))
    b.append(shine_text(178, 48, title, 30, 800, extra='letter-spacing="1"', width=520, glow=False))
    b.append(text(179, 74, sub, 14.5, MUTED, 400))
    b.append(guilloche(800, 1132, 47.75))
    b.append(f'<text x="1132" y="80" class="m" font-size="10.5" fill="{MUTED}" text-anchor="end" letter-spacing="1.5">§ {rn}  ·  {COORDS}</text>')
    b.append(eye(1152, 47.75, 26))
    write(fname, frame(W, H, "b" + num, "".join(b), SEAL_DEFS))


# ---------------------------------------------------------------- Alpha Group brand card
def alpha_card():
    W, H = 1200, 420
    b = []
    MX, MY = 214, 210
    b.append(f'<circle cx="{MX}" cy="{MY}" r="150" fill="{G3}" opacity=".10" filter="url(#soft)"/>')
    b.append(f'<g transform="translate({MX} {MY})"><circle r="168" fill="none" stroke="{PLAT}" stroke-opacity=".14" stroke-dasharray="2 9"><animateTransform attributeName="transform" type="rotate" values="0;360" dur="150s" repeatCount="indefinite"/></circle>'
             f'<circle r="184" fill="none" stroke="{G1}" stroke-opacity=".12"/></g>')
    b.append(circuit([(MX + 150, MY + 70), (MX + 175, MY + 95), (410, MY + 95)], dur=12, begin=3))
    b.append(circuit([(MX - 140, MY - 80), (MX - 160, MY - 100), (30, MY - 100)], color=G1, op=.3, dur=12, begin=7))
    b.append(alpha_mark(MX, MY, 1.95))
    # divider
    b.append(f'<line x1="420" y1="56" x2="420" y2="364" stroke="url(#platH)" stroke-opacity=".5"/>')
    X = 456
    b.append(text(X, 82, "SOFTWARE HOUSE", 13, STEEL, 700, extra='letter-spacing="5"'))
    b.append(alpha_wordmark(X - 2, 150, 62, width=420))
    b.append(f'<rect x="{X}" y="172" width="{1150-X}" height="1.5" fill="{LINE}"/>')
    b.append(f'<rect x="{X}" y="171.5" width="{1150-X}" height="2.5" fill="url(#goldH)"><animate attributeName="width" values="0;{1150-X};{1150-X};0" keyTimes="0;.3;.88;1" dur="12s" repeatCount="indefinite"/></rect>')
    b.append(f'<text x="{X}" y="206" class="t" font-size="17" font-weight="600" fill="{INK}"><tspan fill="{G2}" font-weight="700">Founder</tspan>  ·  Aseef Ahmed</text>')
    b.append(text(X, 232, "Software development, data & AI solutions, and training.", 15, MUTED, 400))
    tiles = [("code", "Software Development"), ("ai", "Data & AI Solutions"), ("lead", "Training")]
    widths, gap = [254, 234, 172], 17
    x = X - widths[0] - gap
    for i, (ic, t) in enumerate(tiles):
        x = x + (widths[i-1] if i else widths[0]) + gap if i else X; tw = widths[i]; y = 270
        b.append(f'<g class="float" style="animation-delay:-{i*1.5:.1f}s">')
        b.append(f'<rect x="{x}" y="{y}" width="{tw}" height="82" rx="14" fill="{CARD}" stroke="{G1}" stroke-opacity=".32"/>')
        b.append(f'<rect x="{x+16}" y="{y}" width="{tw-32}" height="2" fill="url(#goldH)" opacity=".8"/>')
        b.append(f'<circle cx="{x+40}" cy="{y+41}" r="22" fill="{DISC}" stroke="{G1}" stroke-opacity=".45"/>')
        b.append(f'<g transform="translate({x+40} {y+41}) scale(.55) translate({-x-40} {-y-41})">{icon(ic, x+40, y+41)}</g>')
        b.append(text(x + 72, y + 47, t, 14.5, "#FFFFFF", 650))
        b.append('</g>')
    write("alpha-group.svg", frame(W, H, "ag", "".join(b)))


# ---------------------------------------------------------------- journey timeline
def journey():
    W, H = 1200, 800
    items = [
        ("2019 – 2023", "Sir Syed University (SSUET)", "BS Software Engineering", ["Full scholarship", "FYP: Brain Tumor Detection (ML), A+"], "EDUCATION"),
        ("Mar – Aug 2022", "Bank Alfalah Limited", "Associate Engineer (Intern)", ["Banking & financial services", "Six-month engineering internship"], "INTERNSHIP"),
        ("Jan 2023 – Present", "Contour Software", "Software Engineer & Scrum Master", ["Node.js · Express · MongoDB", "ASP.NET Core MVC (C#) · Python ML"], "NOW"),
        ("Sep 2023 – Dec 2024", "Aptech North Karachi", "Faculty Member", ["Taught 150+ students", "Trained 5 faculty every 3 months"], "ACADEMIA"),
        ("Jan 2025 – Present", "Aptech Learning", "Senior Manager Academics", ["Centre academics & operations", "Faculty training · capacity building"], "NOW"),
        ("Nov 2025 – Present", "NED UET", "MS Data Science", ["Coursework complete", "Thesis in progress: HeatFlood Sentinel"], "RESEARCH"),
    ]
    b = []
    cw, ch = 360, 196
    xs = [36, 420, 804]
    ys = [70, 330]
    WY, WH = 592, 168
    cy0, cy1, cy2 = ys[0] + ch / 2, ys[1] + ch / 2, WY + WH / 2
    R = xs[2] + cw + 8; L = xs[0] - 8
    path = (f"M{xs[0]-24} {cy0} H{R} C{R+18} {cy0} {R+18} {cy1} {R} {cy1} H{L} "
            f"C{L-18} {cy1} {L-18} {cy2} {L} {cy2} H{L+60}")
    b.append(f'<path d="{path}" fill="none" stroke="{LINE}" stroke-width="2.5"/>')
    b.append(f'<path d="{path}" fill="none" stroke="url(#goldH)" stroke-width="2.5" class="flow" opacity=".75"/>')
    b.append(f'<circle cx="0" cy="0" r="5" fill="#FFF3C4" filter="url(#glow)" opacity=".9"><animateMotion dur="16s" repeatCount="indefinite" path="{path}"/></circle>')
    b.append(text(44, 44, "From scholarship engineer to founder and academic leader — every step, in order.", 15, MUTED, 400, extra='font-style="italic"'))

    def tag_pill(x, y, tag, right):
        tw = len(tag) * 8.3 + 20
        now = tag == "NOW"
        o = f'<rect x="{right-tw}" y="{y}" width="{tw}" height="22" rx="11" fill="{G1 if now else "#15161B"}" stroke="{G1 if now else PLAT}" stroke-opacity=".55"' + (' class="pulse"' if now else '') + '/>'
        return o + text(right - tw / 2, y + 15, tag, 11, BG if now else PLAT, 800, "middle", extra='letter-spacing="1"')

    for i, (date, org, role, lines, tag) in enumerate(items):
        x = xs[i % 3]; y = ys[i // 3]
        if i // 3 == 1:
            x = xs[2 - (i % 3)]
        b.append(f'<g class="float" style="animation-delay:-{i*1.3:.1f}s">')
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{CARD}" stroke="{G1}" stroke-opacity=".3"/>')
        b.append(f'<rect x="{x}" y="{y}" width="5" height="{ch}" rx="2.5" fill="url(#gold)"/>')
        b.append(f'<text x="{x+24}" y="{y+34}" class="m" font-size="13" fill="{G3}" font-weight="700">{esc(date)}</text>')
        b.append(tag_pill(x, y + 18, tag, x + cw - 16))
        b.append(text(x + 24, y + 70, org, 20, "#FFFFFF", 700))
        b.append(text(x + 24, y + 98, role, 15.5, G2, 600))
        b.append(f'<line x1="{x+24}" y1="{y+116}" x2="{x+cw-24}" y2="{y+116}" stroke="{LINE}"/>')
        for k, l in enumerate(lines):
            b.append(f'<rect x="{x+27}" y="{y+140+k*26-7}" width="6" height="6" transform="rotate(45 {x+30} {y+140+k*26-4})" fill="{G1}"/>')
            b.append(text(x + 42, y + 140 + k * 26, l, 14, INK, 400))
        b.append('</g>')
    # current venture: wide Alpha Group card closes the path
    x, y, w = xs[0], WY, xs[2] + cw - xs[0]
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{WH}" rx="18" fill="#100F0C" stroke="url(#border)" stroke-width="1.6"/>')
    b.append(f'<rect x="{x}" y="{y}" width="5" height="{WH}" rx="2.5" fill="url(#gold)"/>')
    b.append(alpha_mark(x + 96, y + WH / 2, .78))
    tx = x + 196
    b.append(f'<text x="{tx}" y="{y+40}" class="m" font-size="13" fill="{STEEL}" font-weight="700" letter-spacing="2">CURRENT VENTURE</text>')
    b.append(tag_pill(x, y + 22, "NOW", x + w - 22))
    b.append(alpha_wordmark(tx - 1, y + 88, 34, anim=True, width=300))
    b.append(f'<text x="{tx}" y="{y+122}" class="t" font-size="17" font-weight="500" fill="{INK}"><tspan fill="{G2}" font-weight="700">Founder</tspan>  ·  Own software house</text>')
    b.append(f'<line x1="{x+640}" y1="{y+56}" x2="{x+640}" y2="{y+WH-30}" stroke="{LINE}"/>')
    for k, l in enumerate(["Software development", "Data & AI solutions", "Training"]):
        yy = y + 78 + k * 28
        b.append(f'<rect x="{x+668}" y="{yy-8}" width="6" height="6" transform="rotate(45 {x+671} {yy-5})" fill="{G1}"/>')
        b.append(text(x + 686, yy, l, 15, INK, 400))
    write("journey.svg", frame(W, H, "j", "".join(b)))


# ---------------------------------------------------------------- expertise pillars
def icon(kind, x, y):
    s = f'stroke="{G2}" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    g = f'<g transform="translate({x} {y})">'
    if kind == "ai":  # neural net
        nodes = [(-18, -14), (-18, 14), (0, -20), (0, 0), (0, 20), (18, -8), (18, 10)]
        edges = [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (3, 6), (4, 6)]
        g += "".join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[c][0]}" y2="{nodes[c][1]}" stroke="{G1}" stroke-opacity=".6" stroke-width="1.4"/>' for a, c in edges)
        g += "".join(f'<circle cx="{nx}" cy="{ny}" r="4" fill="{G2}"><animate attributeName="r" values="4;5.5;4" dur="{1.6+i*.2:.1f}s" repeatCount="indefinite"/></circle>' for i, (nx, ny) in enumerate(nodes))
    elif kind == "data":  # cylinder stack
        for k in range(3):
            yy = -16 + k * 12
            g += f'<ellipse cx="0" cy="{yy}" rx="18" ry="6" {s}/>'
        g += f'<path d="M-18 -16 V16 M18 -16 V16" {s}/><path d="M-18 16 A18 6 0 0 0 18 16" {s}/>'
    elif kind == "code":
        g += f'<path d="M-10 -14 L-22 0 L-10 14 M10 -14 L22 0 L10 14 M4 -18 L-4 18" {s}/>'
    elif kind == "bi":
        for k, hh in enumerate([14, 24, 18, 30]):
            g += f'<rect x="{-20+k*11}" y="{16-hh}" width="7" height="{hh}" rx="2" fill="{G1 if k%2 else G2}"><animate attributeName="height" values="{hh};{hh*.6:.0f};{hh}" dur="{2+k*.3:.1f}s" repeatCount="indefinite"/><animate attributeName="y" values="{16-hh};{16-hh*.6:.0f};{16-hh}" dur="{2+k*.3:.1f}s" repeatCount="indefinite"/></rect>'
        g += f'<path d="M-24 18 H24" {s}/>'
    elif kind == "teach":  # mic + spark
        g += f'<rect x="-7" y="-20" width="14" height="24" rx="7" {s}/><path d="M-14 -2 A14 14 0 0 0 14 -2 M0 12 V20 M-8 20 H8" {s}/>'
    elif kind == "phone":
        g += f'<rect x="-12" y="-22" width="24" height="44" rx="5" {s}/><path d="M-4 -16 H4" {s}/><circle cx="0" cy="15" r="2.2" fill="{G2}"/>'
    elif kind == "lead":
        g += f'<circle cx="0" cy="-8" r="7" {s}/><path d="M-13 14 A13 11 0 0 1 13 14" {s}/><circle cx="-18" cy="-2" r="4.5" {s}/><circle cx="18" cy="-2" r="4.5" {s}/>'
    return g + '</g>'


def expertise():
    W, H = 1200, 560
    pillars = [
        ("ai", "Data Science & AI", ["Machine Learning", "Deep Learning", "LLMs & RAG", "Agentic AI", "Generative AI"]),
        ("data", "Data Engineering", ["Big Data", "Apache Hadoop", "Apache Spark", "SQL Server · MySQL", "MongoDB"]),
        ("code", "Software Engineering", ["MERN Stack", "ASP.NET Core MVC", "Python · R · C#", "JavaScript ES6+", "Dart · Git"]),
        ("bi", "Analytics & BI", ["Data Analysis", "Tableau", "Power BI", "Dashboards", "Python & R stats"]),
        ("teach", "Teaching & Leadership", ["Any course, any level", "Curriculum design", "Faculty training", "eProject supervision", "Motivational speaker"]),
    ]
    b = []
    cw, gap = 214, 13
    x0 = (W - (5 * cw + 4 * gap)) / 2
    for i, (ic, title, items) in enumerate(pillars):
        x = x0 + i * (cw + gap); y = 40
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{cw}" height="480" rx="18" fill="{CARD}" stroke="{G1}" stroke-opacity=".3"/>')
        # top bar shimmer
        b.append(f'<rect x="{x+18:.1f}" y="{y}" width="{cw-36}" height="3" rx="1.5" fill="url(#goldH)"/>')
        cx = x + cw / 2
        b.append(f'<circle cx="{cx:.1f}" cy="{y+78}" r="40" fill="{DISC}" stroke="{G1}" stroke-opacity=".5"/>')
        b.append(f'<circle cx="{cx:.1f}" cy="{y+78}" r="47" fill="none" stroke="{G2}" stroke-opacity=".6" stroke-dasharray="3 7"><animateTransform attributeName="transform" type="rotate" values="0 {cx:.1f} {y+78};360 {cx:.1f} {y+78}" dur="{18+i*3}s" repeatCount="indefinite"/></circle>')
        b.append(icon(ic, round(cx, 1), y + 78))
        b.append(text(cx, y + 160, title, 15, "#FFFFFF", 700, "middle"))
        b.append(f'<rect x="{cx-22:.1f}" y="{y+174}" width="44" height="2" fill="{G1}"/>')
        for k, it in enumerate(items):
            yy = y + 198 + k * 52
            b.append(f'<rect x="{x+16:.1f}" y="{yy}" width="{cw-32}" height="38" rx="10" fill="{CARD2}" stroke="{G1}" stroke-opacity=".28"/>')
            b.append(f'<polygon points="{x+30:.1f},{yy+19} {x+35:.1f},{yy+14} {x+40:.1f},{yy+19} {x+35:.1f},{yy+24}" fill="{G1}"/>')
            b.append(text(x + 44, yy + 24, it, 13, INK, 500))
    write("expertise.svg", frame(W, H, "e", "".join(b)))


# ---------------------------------------------------------------- featured project
def featured():
    W, H = 1200, 410
    b = []
    b.append(chip(48, 40, "FEATURED · MS THESIS · NED UET", 12, 26, 14, 7.8, G1, G1, BG)[0])
    b.append(shine_text(48, 112, "HeatFlood Sentinel", 50, 800, width=520))
    b.append(text(50, 148, "A scalable Big Data + deep learning framework for heatwave and", 18, INK, 500))
    b.append(text(50, 174, "flash-flood forecasting and detection across Pakistan.", 18, INK, 500))
    bullets = ["Real ERA5 reanalysis data · 2015–2022 · 20 cities",
               "XGBoost · LSTM · SARIMA · ConvLSTM model suite",
               "Kafka / Spark streaming design with local fallback",
               "FastAPI service + 10-page dashboard with live Open-Meteo feed"]
    for k, t in enumerate(bullets):
        yy = 214 + k * 32
        b.append(f'<polygon points="52,{yy-5} 58,{yy-11} 64,{yy-5} 58,{yy+1}" fill="{G1}"/>')
        b.append(text(76, yy, t, 15.5, INK, 400))
    # emblem right: medallion with sun over flood waves
    mx, my, mr = 1010, 190, 128
    b.append(f'<circle cx="{mx}" cy="{my}" r="{mr+26}" fill="{G3}" opacity=".16" filter="url(#soft)"/>')
    b.append(f'<clipPath id="med"><circle cx="{mx}" cy="{my}" r="{mr}"/></clipPath>')
    b.append(f'<g clip-path="url(#med)"><rect x="{mx-mr}" y="{my-mr}" width="{2*mr}" height="{2*mr}" fill="url(#sky)"/>')
    rays = "".join(f'<line x1="{44*math.cos(a):.1f}" y1="{44*math.sin(a):.1f}" x2="{60*math.cos(a):.1f}" y2="{60*math.sin(a):.1f}" stroke="{G2}" stroke-width="4" stroke-linecap="round"/>' for a in [i * math.pi / 8 for i in range(16)])
    b.append(f'<g transform="translate({mx} {my-30})"><g>{rays}<animateTransform attributeName="transform" type="rotate" values="0;360" dur="30s" repeatCount="indefinite"/></g>'
             f'<circle r="34" fill="url(#gold)"><animate attributeName="r" values="34;37;34" dur="3s" repeatCount="indefinite"/></circle></g>')
    for k, (op, dy, d) in enumerate([(.95, 0, 4), (.7, 22, 5.5), (.5, 44, 7)]):
        y0 = my + 40 + dy
        wave = f"M{mx-mr-100} {y0} q25 -12 50 0 " + " ".join(["t50 0"] * 9) + f" V{my+mr} H{mx-mr-100} Z"
        col = ["#2B7FC4", "#1F5F96", "#16476F"][k]
        b.append(f'<path d="{wave}" fill="{col}" opacity="{op}"><animateTransform attributeName="transform" type="translate" values="0 0;100 0;0 0" dur="{d}s" repeatCount="indefinite"/></path>')
    b.append('</g>')
    b.append(f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="none" stroke="url(#gold)" stroke-width="3"/>')
    b.append(f'<circle cx="{mx}" cy="{my}" r="{mr+12}" fill="none" stroke="{G1}" stroke-opacity=".5" stroke-dasharray="2 9"><animateTransform attributeName="transform" type="rotate" values="0 {mx} {my};360 {mx} {my}" dur="40s" repeatCount="indefinite"/></circle>')
    b.append(text(mx, my + mr + 36, "HEAT  ·  FLOOD  ·  FORECAST", 12, G1, 700, "middle", extra='letter-spacing="3"'))
    tech = ["Python", "Kafka", "Spark", "Delta Lake", "XGBoost", "LSTM", "ConvLSTM", "FastAPI"]
    x = 48
    for t in tech:
        c, w = chip(x, 352, t, 12, 26, 11)
        b.append(c); x += w + 8
    extra = f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A1A06"/><stop offset=".6" stop-color="#5A3305"/><stop offset="1" stop-color="#0B0B0F"/></linearGradient>'
    write("featured-heatflood.svg", frame(W, H, "f", "".join(b), extra))


# ---------------------------------------------------------------- HeatFlood Sentinel data-flow diagram
def heatflood_flow():
    W, H = 1200, 540
    b = []
    b.append(text(44, 50, "HEATFLOOD SENTINEL  ·  DATA FLOW", 14, G1, 800, extra='letter-spacing="3"'))
    b.append(text(44, 74, "From reanalysis and live weather to forecasts and alerts — a medallion lakehouse pipeline.", 14.5, MUTED, 400, extra='font-style="italic"'))
    CY = 290
    cols = [36, 200, 364, 528, 712, 896, 1040]
    bw = 132
    # node helper
    def node(x, y, w, h, title, sub, accent=G1):
        o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{CARD}" stroke="{accent}" stroke-opacity=".55"/>'
        o += f'<rect x="{x+14}" y="{y}" width="{w-28}" height="3" rx="1.5" fill="url(#goldH)" opacity=".85"/>'
        o += text(x + w / 2, y + h / 2 - 2, title, 15.5, "#FFFFFF", 700, "middle")
        o += text(x + w / 2, y + h / 2 + 18, sub, 11.5, MUTED, 400, "middle")
        return o
    # stage numerals
    for i, x in enumerate(cols):
        w = 124 if i == 6 else (164 if i in (3, 4) else bw)
        b.append(f'<text x="{x + w/2:.0f}" y="122" font-family="Georgia,\'Times New Roman\',serif" font-size="15" fill="{G2}" fill-opacity=".6" text-anchor="middle">{ROMAN[i]}</text>')
        b.append(f'<line x1="{x + w/2 - 18:.0f}" y1="130" x2="{x + w/2 + 18:.0f}" y2="130" stroke="{G1}" stroke-opacity=".35"/>')
    paths = []  # (d, color, dur, n)
    # sources
    b.append(node(cols[0], CY - 120, bw, 74, "ERA5", "reanalysis · batch"))
    b.append(node(cols[0], CY + 46, bw, 74, "Open-Meteo", "live forecast feed", STEEL))
    b.append(node(cols[1], CY - 45, bw, 90, "Kafka", "ingestion topics"))
    b.append(node(cols[2], CY - 45, bw, 90, "Spark", "structured streaming"))
    # Delta medallion
    dx, dw = cols[3], 164
    b.append(f'<rect x="{dx}" y="{CY-118}" width="{dw}" height="236" rx="14" fill="{CARD}" stroke="{G1}" stroke-opacity=".55"/>')
    b.append(text(dx + dw / 2, CY - 92, "Delta Lake", 15.5, "#FFFFFF", 700, "middle"))
    for k, (tier, col, note) in enumerate([("BRONZE", "#B4712A", "raw ingest"), ("SILVER", PLAT, "cleaned · joined"), ("GOLD", G1, "features · labels")]):
        yy = CY - 72 + k * 62
        b.append(f'<rect x="{dx+14}" y="{yy}" width="{dw-28}" height="50" rx="10" fill="{CARD2}" stroke="{col}" stroke-opacity=".75"/>')
        b.append(f'<rect x="{dx+14}" y="{yy}" width="5" height="50" rx="2.5" fill="{col}"/>')
        b.append(text(dx + 32, yy + 22, tier, 12.5, col, 800, extra='letter-spacing="2"'))
        b.append(text(dx + 32, yy + 39, note, 11.5, MUTED, 400))
        if k < 2:
            b.append(f'<path d="M{dx+dw/2} {yy+50} V{yy+62}" stroke="{G2}" stroke-width="1.6" class="flow"/>')
    # models
    mx, mw = cols[4], 164
    b.append(f'<rect x="{mx}" y="{CY-118}" width="{mw}" height="236" rx="14" fill="{CARD}" stroke="{G1}" stroke-opacity=".55"/>')
    b.append(text(mx + mw / 2, CY - 92, "Models", 15.5, "#FFFFFF", 700, "middle"))
    for k, m in enumerate(["LSTM", "ConvLSTM", "XGBoost", "SARIMA"]):
        yy = CY - 74 + k * 47
        b.append(f'<rect x="{mx+16}" y="{yy}" width="{mw-32}" height="36" rx="18" fill="#14130F" stroke="{G1}" stroke-opacity=".45"/>')
        b.append(text(mx + mw / 2, yy + 23, m, 13.5, G2, 650, "middle"))
        b.append(f'<circle cx="{mx+30}" cy="{yy+18}" r="3" fill="{G1}"><animate attributeName="opacity" values=".3;1;.3" dur="3s" begin="-{k*.75:.2f}s" repeatCount="indefinite"/></circle>')
    b.append(node(cols[5], CY - 45, bw, 90, "FastAPI", "forecast & alert API"))
    b.append(node(cols[6], CY - 120, 124, 74, "Dashboard", "maps · trends"))
    b.append(node(cols[6], CY + 46, 124, 74, "Alerts", "heat · flood", "#E8860C"))
    # edges
    e = []
    e.append((f"M{cols[0]+bw} {CY-83} C{cols[0]+bw+20} {CY-83} {cols[1]-20} {CY-15} {cols[1]} {CY-15}", G2, 4.5))
    e.append((f"M{cols[0]+bw} {CY+83} C{cols[0]+bw+20} {CY+83} {cols[1]-20} {CY+15} {cols[1]} {CY+15}", STEEL, 4.5))
    e.append((f"M{cols[1]+bw} {CY} H{cols[2]}", G2, 2.6))
    e.append((f"M{cols[2]+bw} {CY} H{dx}", G2, 2.6))
    e.append((f"M{dx+dw} {CY} H{mx}", G2, 2.6))
    e.append((f"M{mx+mw} {CY} H{cols[5]}", G2, 2.6))
    e.append((f"M{cols[5]+bw} {CY-15} C{cols[5]+bw+8} {CY-15} {cols[6]-8} {CY-83} {cols[6]} {CY-83}", G2, 3))
    e.append((f"M{cols[5]+bw} {CY+15} C{cols[5]+bw+8} {CY+15} {cols[6]-8} {CY+83} {cols[6]} {CY+83}", "#E8860C", 3))
    for i, (d, col, dur) in enumerate(e):
        b.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="2.4"/>')
        b.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity=".7" stroke-width="2" class="flow"/>')
        for j in range(3):
            b.append(f'<circle r="3.6" fill="{col}" filter="url(#glow)" opacity="0"><animateMotion dur="{dur}s" begin="{-(dur*j/3)-i*.37:.2f}s" repeatCount="indefinite" path="{d}"/>'
                     f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="{dur}s" begin="{-(dur*j/3)-i*.37:.2f}s" repeatCount="indefinite"/></circle>')
    # legend
    ly = 478
    b.append(f'<line x1="44" y1="{ly-28}" x2="1156" y2="{ly-28}" stroke="{LINE}"/>')
    lg = [(G2, "batch · reanalysis 2015–2022, 20 cities"), (STEEL, "live · Open-Meteo forecast feed"), ("#E8860C", "alerts · heatwave & flash-flood")]
    x = 44
    for col, lab in lg:
        b.append(f'<circle cx="{x+6}" cy="{ly-4}" r="5" fill="{col}" filter="url(#glow)"/>')
        b.append(text(x + 20, ly + 1, lab, 13, PLAT, 500)); x += 20 + len(lab) * 7.2 + 40
    b.append(text(1156, ly + 1, "MS thesis · NED UET", 13, MUTED, 500, "end", extra='font-style="italic"'))
    b.append(eye(1150, 50, 30))
    write("heatflood-flow.svg", frame(W, H, "hf", "".join(b), SEAL_DEFS))


# ---------------------------------------------------------------- focus areas sunburst
FOCUS = [
    ("Data Science & AI", ["Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "scikit-learn"]),
    ("GenAI · LLMs · RAG · Agentic", ["LLMs", "RAG", "Agentic AI", "Generative AI"]),
    ("Data Engineering & Big Data", ["Hadoop", "Spark", "Kafka", "SQL Server", "MySQL", "MongoDB"]),
    ("Full-stack MERN & .NET", ["React", "Node.js", "Express", "ASP.NET Core", "C#", "Flutter"]),
    ("Analytics & BI", ["Tableau", "Power BI", "Pandas", "NumPy", "R"]),
    ("Teaching & Leadership", ["Any course", "Curriculum", "Faculty training", "eProjects", "Speaking"]),
]
FOCUS_COLORS = ["#FFD54A", "#F5B301", "#E8860C", "#C9D1D9", "#3BA3FF", "#D9A441"]


def _arc(cx, cy, r0, r1, a0, a1):
    f = lambda r, a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    large = 1 if a1 - a0 > 180 else 0
    p0, p1, p2, p3 = f(r1, a0), f(r1, a1), f(r0, a1), f(r0, a0)
    return (f"M{p0[0]:.1f} {p0[1]:.1f} A{r1} {r1} 0 {large} 1 {p1[0]:.1f} {p1[1]:.1f} "
            f"L{p2[0]:.1f} {p2[1]:.1f} A{r0} {r0} 0 {large} 0 {p3[0]:.1f} {p3[1]:.1f} Z")


def focus():
    W, H = 1200, 580
    b = []
    CX, CY = 300, 296
    n = len(FOCUS); cyc = 4 * n
    b.append(f'<circle cx="{CX}" cy="{CY}" r="250" fill="{G3}" opacity=".08" filter="url(#soft)"/>')
    b.append(seed_geometry(CX, CY, 62, .06))
    b.append(seal_ring(CX, CY, 268, ("SIX FOCUS AREAS · " + COORDS + " · ") * 3, dur=300, numerals=False))
    for i, ((dom, tools), col) in enumerate(zip(FOCUS, FOCUS_COLORS)):
        a0 = -90 + i * 60 + .8; a1 = -90 + (i + 1) * 60 - .8
        s0 = i / n; s1 = (i + 1) / n
        kt = "0;%.3f;%.3f;%.3f;%.3f;1" % (max(s0 - .001, 0), s0 + .02, s1 - .02, s1) if i else None
        hl = (f'<animate attributeName="opacity" values=".55;.55;1;1;.55;.55" keyTimes="0;{max(s0,.0001):.3f};{s0+.02:.3f};{s1-.02:.3f};{s1:.3f};1" dur="{cyc}s" repeatCount="indefinite"/>')
        b.append(f'<g opacity=".55">{hl}')
        b.append(f'<path d="{_arc(CX, CY, 78, 150, a0, a1)}" fill="{col}" fill-opacity=".85" stroke="{BG}" stroke-width="1.5"/>')
        am = math.radians((a0 + a1) / 2)
        b.append(f'<text x="{CX + 114*math.cos(am):.1f}" y="{CY + 114*math.sin(am) + 7:.1f}" font-family="Georgia,\'Times New Roman\',serif" font-size="21" font-weight="700" fill="{BG}" text-anchor="middle">{ROMAN[i]}</text>')
        m = len(tools); span = (a1 - a0) / m
        for j, t in enumerate(tools):
            t0 = a0 + j * span + .6; t1 = a0 + (j + 1) * span - .6
            b.append(f'<path d="{_arc(CX, CY, 156, 238, t0, t1)}" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-opacity=".55" stroke-width="1"/>')
            tm = (t0 + t1) / 2; rr = 197
            x = CX + rr * math.cos(math.radians(tm)); y = CY + rr * math.sin(math.radians(tm))
            rot = tm if -90 <= tm <= 90 else tm + 180
            fs = 10.5 if len(t) <= 10 else (9.6 if len(t) <= 13 else 8.8)
            b.append(f'<text x="{x:.1f}" y="{y:.1f}" class="t" font-size="{fs}" font-weight="600" fill="#F2F4F7" text-anchor="middle" dominant-baseline="central" transform="rotate({rot:.1f} {x:.1f} {y:.1f})">{esc(t)}</text>')
        b.append('</g>')
    # rotating highlight sweep ring
    b.append(f'<g transform="translate({CX} {CY})"><path d="{_arc(0, 0, 242, 248, -90, -30)}" fill="url(#gold)"><animateTransform attributeName="transform" type="rotate" values="0;60;60;120;120;180;180;240;240;300;300;360" keyTimes="0;.03;.1667;.1967;.3333;.3633;.5;.53;.6667;.6967;.8333;.8633" dur="{cyc}s" repeatCount="indefinite" calcMode="linear"/></path></g>')
    b.append(f'<circle cx="{CX}" cy="{CY}" r="72" fill="#0B0A07" stroke="{G1}" stroke-opacity=".5"/>')
    b.append(mini_capstone(CX, CY + 8, .52))
    # legend
    LX = 640
    b.append(text(LX, 64, "FOCUS AREAS", 14, G1, 800, extra='letter-spacing="3"'))
    b.append(text(LX, 88, "Where my work lives — each area with the tools behind it.", 14.5, MUTED, 400, extra='font-style="italic"'))
    for i, ((dom, tools), col) in enumerate(zip(FOCUS, FOCUS_COLORS)):
        y = 116 + i * 72
        s0 = i / n; s1 = (i + 1) / n
        hl = f'<animate attributeName="stroke-opacity" values=".18;.18;.8;.8;.18;.18" keyTimes="0;{max(s0,.0001):.3f};{s0+.02:.3f};{s1-.02:.3f};{s1:.3f};1" dur="{cyc}s" repeatCount="indefinite"/>'
        b.append(f'<rect x="{LX}" y="{y}" width="520" height="60" rx="12" fill="{CARD}" stroke="{col}" stroke-opacity=".18">{hl}</rect>')
        b.append(f'<rect x="{LX}" y="{y}" width="5" height="60" rx="2.5" fill="{col}"/>')
        b.append(f'<text x="{LX+40}" y="{y+38}" font-family="Georgia,\'Times New Roman\',serif" font-size="20" font-weight="700" fill="{col}" text-anchor="middle">{ROMAN[i]}</text>')
        b.append(text(LX + 68, y + 26, dom, 16, "#FFFFFF", 700))
        b.append(text(LX + 68, y + 47, "  ·  ".join(tools), 12.5, MUTED, 400))
    b.append(text(LX, 560, "Areas are drawn equal: a map of focus, not a score.", 12, MUTED, 400, extra='font-style="italic" fill-opacity=".8"'))
    write("focus.svg", frame(W, H, "fo", "".join(b), SEAL_DEFS))


# ---------------------------------------------------------------- career timeline (Gantt)
CAREER = [
    ("SSUET", "BS Software Engineering · scholarship", (2019, 12), (2023, 4), False),
    ("Bank Alfalah", "Associate Engineer (Intern)", (2022, 3), (2022, 8), False),
    ("Contour Software", "Software Engineer & Scrum Master", (2023, 1), None, False),
    ("Aptech North Karachi", "Faculty Member", (2023, 9), (2024, 12), False),
    ("Aptech Learning", "Senior Manager Academics", (2025, 1), None, False),
    ("NED UET", "MS Data Science · thesis in progress", (2025, 11), None, False),
    ("Alpha Group", "Founder · current", None, None, True),
]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def to_roman(n):
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    o = ""
    for v, s_ in vals:
        while n >= v:
            o += s_; n -= v
    return o


def career_timeline_svg(now):
    """Animated Gantt of verified career dates. `now` is a datetime (PKT); the NOW line and
    open-ended bars are drawn up to it, so the chart stays current when regenerated."""
    W = 1200; rows = len(CAREER); RH = 50; Y0 = 150
    H = Y0 + rows * RH + 64
    y0 = 2019; y1 = max(2027, now.year + 1)
    X0, X1 = 330, 1150
    xm = lambda y, m: X0 + (X1 - X0) * ((y - y0) + (m - 1) / 12) / (y1 - y0)
    xnow = X0 + (X1 - X0) * ((now.year - y0) + (now.month - 1 + (now.day - 1) / 31) / 12) / (y1 - y0)
    b = []
    b.append(text(44, 48, "CAREER TIMELINE", 14, G1, 800, extra='letter-spacing="3"'))
    b.append(text(44, 72, "Study, industry, academia and enterprise — overlapping, by year.", 14.5, MUTED, 400, extra='font-style="italic"'))
    for y in range(y0, y1 + 1):
        x = xm(y, 1)
        b.append(f'<line x1="{x:.1f}" y1="{Y0-14}" x2="{x:.1f}" y2="{Y0+rows*RH}" stroke="{PLAT}" stroke-opacity=".08"/>')
        b.append(text(x, Y0 - 34, str(y), 13, PLAT, 700, "middle", cls="m"))
        b.append(f'<text x="{x:.1f}" y="{Y0-19}" font-family="Georgia,\'Times New Roman\',serif" font-size="9.5" fill="{G2}" fill-opacity=".55" text-anchor="middle" letter-spacing="1">{to_roman(y)}</text>')
    for i, (org, role, st, en, venture) in enumerate(CAREER):
        y = Y0 + i * RH
        if i % 2 == 0:
            b.append(f'<rect x="30" y="{y}" width="1140" height="{RH}" fill="#FFFFFF" fill-opacity=".018"/>')
        b.append(text(44, y + 22, org, 15, G2 if venture else "#FFFFFF", 700))
        b.append(text(44, y + 40, role, 12, MUTED, 400))
        cy = y + RH / 2
        if venture:
            b.append(f'<line x1="{X0}" y1="{cy}" x2="{xnow-14:.1f}" y2="{cy}" stroke="{G1}" stroke-opacity=".25" stroke-dasharray="2 6"/>')
            b.append(mini_capstone(round(xnow, 1), cy + 3, .17))
            b.append(text(xnow - 22, cy + 4, "Founder · now", 12, G2, 700, "end"))
            continue
        xs = xm(*st); ongoing = en is None
        xe = xnow if ongoing else xm(en[0], en[1]) + (X1 - X0) / (12 * (y1 - y0))
        w = xe - xs
        lab = f"{MONTHS[st[1]-1]} {st[0]} – " + ("present" if ongoing else f"{MONTHS[en[1]-1]} {en[0]}")
        begin = i * .35
        anim = (f'<animate attributeName="width" values="0;{w:.1f};{w:.1f};0" keyTimes="0;.12;.9;1" dur="16s" begin="-{15.99-begin:.2f}s" repeatCount="indefinite"/>')
        fill = "url(#goldH)" if ongoing else "url(#gold)"
        b.append(f'<rect x="{xs:.1f}" y="{cy-9}" width="{w:.1f}" height="18" rx="9" fill="{fill}" fill-opacity="{1 if ongoing else .78}">{anim}</rect>')
        if ongoing:
            b.append(f'<circle cx="{xe:.1f}" cy="{cy}" r="6" fill="#FFF3C4" filter="url(#glow)" class="pulse"/>')
        tw = len(lab) * 6.6 + 16
        if w > tw:
            b.append(text(xs + 10, cy + 4, lab, 11, BG, 700, cls="m"))
        elif ongoing:
            b.append(text(xs - 10, cy + 4, lab, 11, PLAT, 600, "end", cls="m"))
        else:
            b.append(text(xe + 10, cy + 4, lab, 11, PLAT, 600, cls="m"))
    # NOW line
    b.append(f'<line x1="{xnow:.1f}" y1="{Y0-10}" x2="{xnow:.1f}" y2="{Y0+rows*RH+8}" stroke="{STEEL}" stroke-width="1.4" stroke-dasharray="4 5" class="flow"/>')
    b.append(chip(xnow, Y0 + rows * RH + 14, f"NOW · {MONTHS[now.month-1]} {now.year}", 11.5, 24, 10, 7.6, "#0E1A26", STEEL, "#9FD0FF", "middle")[0])
    return frame(W, H, "ct", "".join(b), SEAL_DEFS)


# ---------------------------------------------------------------- other projects
def projects():
    W, H = 1200, 470
    cards = [
        ("ai", "Earth Climate Agency", "Climate-focused AI/ML application", ["AI/ML", "Flask", "Big Data"]),
        ("bi", "Stock Market Prediction", "Machine-learning price forecasting", ["Machine Learning", "Python"]),
        ("code", "Fitness Tracker", "Full-stack fitness tracking app", ["MongoDB", "Express", "React", "Node.js"]),
        ("phone", "Currency Converter", "Mobile currency conversion app", ["Mobile"]),
        ("ai", "Brain Tumor Detection", "BS final-year project · graded A+", ["Machine Learning", "FYP", "A+"]),
    ]
    b = []
    # 3 + 2 layout
    cw, chh = 360, 190
    pos = [(42, 40), (420, 40), (798, 40), (231, 252), (609, 252)]
    for i, ((ic, t, d, tags), (x, y)) in enumerate(zip(cards, pos)):
        b.append(f'<g class="float" style="animation-delay:-{i*1.1:.1f}s">')
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" rx="16" fill="{CARD}" stroke="{G1}" stroke-opacity=".35"/>')
        b.append(f'<circle cx="{x+44}" cy="{y+48}" r="26" fill="{DISC}" stroke="{G1}" stroke-opacity=".5"/>')
        b.append(f'<g transform="translate({x+44} {y+48}) scale(.62) translate({-x-44} {-y-48})">{icon(ic, x+44, y+48)}</g>')
        b.append(text(x + 84, y + 44, t, 19, "#FFFFFF", 700))
        b.append(text(x + 84, y + 66, d, 13.5, MUTED, 400))
        b.append(f'<line x1="{x+22}" y1="{y+100}" x2="{x+cw-22}" y2="{y+100}" stroke="{LINE}"/>')
        xx = x + 22
        for tg in tags:
            c, w = chip(xx, y + 120, tg, 12, 26, 10)
            b.append(c); xx += w + 8
        b.append(f'<rect x="{x+22}" y="{y+chh-14}" width="{cw-44}" height="2" rx="1" fill="url(#goldH)" opacity=".7"/>')
        b.append('</g>')
    write("projects.svg", frame(W, H, "p", "".join(b)))


# ---------------------------------------------------------------- achievements
def achievements():
    W, H = 1200, 300
    items = [("TechWiz Winners", "with my students", "2024 & 2025", "Aptech worldwide tech competition"),
             ("Google AI Primer", "ML · DL · Data Science", "2024", "Certification"),
             ("MERN Stack Trainer", "Contour Software", "2023", "Internal certification"),
             ("Java & JavaScript", "300-hour certificates", "SSUET", "Sir Syed University")]
    b = []
    cw, gap = 262, 20
    x0 = (W - (4 * cw + 3 * gap)) / 2
    for i, (t, s, yr, note) in enumerate(items):
        x = x0 + i * (cw + gap); y = 36; cx = x + cw / 2
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{cw}" height="228" rx="18" fill="{CARD}" stroke="{G1}" stroke-opacity=".35"/>')
        # medal
        b.append(f'<g transform="translate({cx:.1f} {y+62})"><polygon points="-14,-34 -4,-6 4,-6 14,-34" fill="{G3}"/>'
                 f'<circle r="24" fill="url(#gold)" stroke="#FFF3C4" stroke-width="1.5"/><circle r="17" fill="none" stroke="#7A4A06" stroke-width="1.4"/>'
                 f'<polygon points="0,-10 3,-3 10,-3 4.5,1.5 6.5,9 0,4.5 -6.5,9 -4.5,1.5 -10,-3 -3,-3" fill="#7A4A06"/>'
                 f'<circle r="24" fill="none" stroke="#FFF7DA" stroke-width="2" stroke-dasharray="10 140"><animateTransform attributeName="transform" type="rotate" values="0;360" dur="{4+i}s" repeatCount="indefinite"/></circle></g>')
        b.append(text(cx, y + 126, t, 18, "#FFFFFF", 700, "middle"))
        b.append(text(cx, y + 150, s, 14, INK, 400, "middle"))
        b.append(chip(cx, y + 166, yr, 12.5, 24, 12, anchor="middle")[0])
        b.append(text(cx, y + 212, note, 12.5, MUTED, 400, "middle"))
    write("achievements.svg", frame(W, H, "a", "".join(b)))


# ---------------------------------------------------------------- teaching
def teaching():
    W, H = 1200, 420
    tiles = [("code", "Programming", "Any language · any level"), ("code", "Web & MERN", "Full-stack JavaScript ES6+"),
             ("code", ".NET Core & C#", "ASP.NET Core MVC"), ("phone", "Mobile Apps", "Dart · Flutter"),
             ("ai", "AI / ML & GenAI", "ML · DL · LLMs · RAG"), ("data", "Big Data", "Hadoop · Spark"),
             ("bi", "Data & BI", "Tableau · Power BI · R"), ("lead", "Faculty Training", "Workshops · curriculum")]
    b = []
    tw, th, gx, gy = 268, 112, 16, 16
    x0 = (W - (4 * tw + 3 * gx)) / 2
    for i, (ic, t, s) in enumerate(tiles):
        x = x0 + (i % 4) * (tw + gx); y = 32 + (i // 4) * (th + gy)
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{tw}" height="{th}" rx="14" fill="{CARD}" stroke="{G1}" stroke-opacity=".3"/>')
        b.append(f'<circle cx="{x+46:.1f}" cy="{y+th/2}" r="26" fill="{DISC}" stroke="{G1}" stroke-opacity=".45"/>')
        b.append(f'<g transform="translate({x+46:.1f} {y+th/2}) scale(.62) translate({-x-46:.1f} {-y-th/2})">{icon(ic, round(x+46,1), y+th/2)}</g>')
        b.append(text(x + 86, y + 50, t, 17, "#FFFFFF", 700))
        b.append(text(x + 86, y + 74, s, 13, MUTED, 400))
    # ribbon
    y = 302
    b.append(f'<rect x="{x0:.1f}" y="{y}" width="{4*tw+3*gx}" height="86" rx="16" fill="{CARD2}" stroke="url(#border)"/>')
    b.append(text(x0 + 28, y + 36, "eProject supervision", 17, G2, 700))
    b.append(text(x0 + 28, y + 62, "PHP · MERN · Flutter · Big Data · AI — guiding students from idea to demo day", 14.5, INK, 400))
    b.append(text(x0 + 4 * tw + 3 * gx - 28, y + 36, "150+ students taught", 17, G2, 700, "end"))
    b.append(text(x0 + 4 * tw + 3 * gx - 28, y + 62, "as Faculty Member, 2023–2024", 14, MUTED, 400, "end"))
    write("teaching.svg", frame(W, H, "t", "".join(b)))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1200, 330
    b = []
    b.append(emblem(600, 92, .36, ring_label=f"ALPHA GROUP · KARACHI · {COORDS} · "))
    b.append(shine_text(600, 218, "“Lead with courage. Teach with heart. Build with data.”", 26, 700, "middle", extra='font-style="italic"', width=760, glow=False))
    b.append(text(600, 248, "— Aseef Ahmed  ·  Founder, Alpha Group", 15, MUTED, 500, "middle"))
    b.append(f'<line x1="120" y1="282" x2="1080" y2="282" stroke="{LINE}"/>')
    b.append(f'<rect x="120" y="281.2" width="960" height="1.6" fill="url(#goldH)"><animate attributeName="width" values="0;960;960;0" keyTimes="0;.3;.88;1" dur="12s" repeatCount="indefinite"/></rect>')
    b.append(guilloche(140, 460, 282, 5)); b.append(guilloche(740, 1060, 282, 5))
    b.append(circuit([(120, 282), (96, 306), (40, 306)], dur=12, begin=1))
    b.append(circuit([(1080, 282), (1104, 306), (1160, 306)], dur=12, begin=1))
    b.append(f'<rect x="520" y="270" width="160" height="24" fill="{BG}"/>')
    b.append(text(600, 287, "MMXXVI · KARACHI", 11, PLAT, 600, "middle", cls="m", extra='letter-spacing="3" fill-opacity=".7"'))
    write("footer.svg", frame(W, H, "ft", "".join(b), LION_DEFS + SEAL_DEFS))


if __name__ == "__main__":
    header(); alpha_card(); journey(); expertise(); featured(); heatflood_flow(); focus(); projects(); achievements(); teaching(); footer()
    for f, n, t, s in [("sec-about.svg", "01", "About Me", "Engineer, data scientist, founder and educator."),
                       ("sec-alpha.svg", "02", "Alpha Group", "My software house: software, data & AI solutions, and training."),
                       ("sec-journey.svg", "03", "Journey", "Industry, academia, research and enterprise — in order."),
                       ("sec-expertise.svg", "04", "Expertise", "Five pillars I build, analyse and teach with."),
                       ("sec-stack.svg", "05", "Tech Arsenal", "Languages, frameworks and platforms in daily use."),
                       ("sec-projects.svg", "06", "Featured Work", "Thesis research, live data and selected builds."),
                       ("sec-achievements.svg", "07", "Achievements", "Wins and certifications along the way."),
                       ("sec-teaching.svg", "08", "Teaching & Mentorship", "What I teach, train and supervise."),
                       ("sec-analytics.svg", "09", "GitHub Analytics", "Live cards refreshed every 6 hours, plus GitHub widgets.")]:
        banner(f, n, t, s)
    print("done", sorted(os.listdir(OUT)))
