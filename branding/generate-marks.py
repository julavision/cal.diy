from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

f = TTFont('RussoOne.ttf'); gs = f.getGlyphSet(); cmap = f.getBestCmap()
upm = f['head'].unitsPerEm; cap = getattr(f['OS/2'], 'sCapHeight', 0) or int(upm * .7)
RED = '#e3142b'
NAME, INK_PART, RED_PART = 'VisCal', 'VIS', 'CAL'   # the product name; INK_PART + RED_PART = wordmark

def run(text, x0, track, scale, base):
    """paths for `text`, starting at x0 (px), baseline at `base` (px). Returns (d, x_end)."""
    d, x = [], x0
    for ch in text:
        g = cmap[ord(ch)]; glyph = gs[g]
        pen = SVGPathPen(gs)
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x, base)))
        d.append(pen.getCommands())
        x += glyph.width * scale + track
    return ' '.join(d), x - track

def ink_bounds(text):
    xs, ys = [], []
    for ch in text:
        bp = BoundsPen(gs); gs[cmap[ord(ch)]].draw(bp)
        if bp.bounds: ys += [bp.bounds[1], bp.bounds[3]]
    return min(ys), max(ys)

# ── wordmark: INK_PART (ink) + RED_PART (red), cap height 20px, 26px tall like cal.diy's ──
H = 26; capPx = 18; s = capPx / cap; track = upm * 0.035 * s
base = (H + capPx) / 2
d1, xa = run(INK_PART, 0, track, s, base)
d2, xb = run(RED_PART, xa + track, track, s, base)
W = round(xb + 0.5, 2)
def wordmark(ink):
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">'
            f'<title>{NAME}</title><path d="{d1}" fill="{ink}"/><path d="{d2}" fill="{RED}"/></svg>')

# ── icon: "V." centred in 56×56 ──
def vdot(size, capPx, dx=0):
    s = capPx / cap; tr = upm * 0.02 * s
    wv = gs[cmap[ord('V')]].width * s; wd = gs[cmap[ord('.')]].width * s
    x0 = (size - (wv + tr + wd)) / 2 + dx; base = (size + capPx) / 2
    dv, xv = run('V', x0, 0, s, base); dd, _ = run('.', xv + tr, 0, s, base)
    return dv, dd
dv, dd = vdot(56, 30, dx=1)
icon_plain = f'<svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg"><title>{NAME}</title><path d="{dv}" fill="#111111"/><path d="{dd}" fill="{RED}"/></svg>'
icon_tile  = f'<svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg"><title>{NAME}</title><rect width="56" height="56" rx="12" fill="#0a0a0a"/><path d="{dv}" fill="#fafafa"/><path d="{dd}" fill="{RED}"/></svg>'
# favicon master: tile edge-to-edge, bigger glyph so it reads at 16px
fv, fd = vdot(512, 300, dx=8)
fav = f'<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><rect width="512" height="512" rx="104" fill="#0a0a0a"/><path d="{fv}" fill="#fafafa"/><path d="{fd}" fill="{RED}"/></svg>'
pin = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 56"><path d="{dv} {dd}" fill="#000"/></svg>'

files = {
  'calcom-logo-white-word.svg': wordmark('#111111'),   # dark text, light backgrounds (the main LOGO)
  'cal-logo-word.svg':          wordmark('#111111'),
  'cal-logo-word-black.svg':    wordmark('#000000'),   # OG images
  'cal-logo-word-dark.svg':     wordmark('#fafafa'),   # light text, dark backgrounds
  'cal-com-icon-white.svg':     icon_plain,
  'cal-com-icon.svg':           icon_tile,
  'safari-pinned-tab.svg':      pin,
  '_favicon-master.svg':        fav,
}
for n, svg in files.items(): open(f'out/{n}', 'w').write(svg)
print(f'wordmark {W}×{H}px  (upm {upm}, cap {cap})')
