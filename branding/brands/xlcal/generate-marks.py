# XL Cal marks: the Xperience Levels X mark (from the site's logo, embedded as PNG)
# + "XL CAL" in Montserrat Bold outlines with the logo's blue→green gradient.
# Run from this folder:  python generate-marks.py   (needs fonttools + pillow,
# xl-mark.png = the X mark cropped from the Xperience Levels logo, and
# Montserrat-Bold.ttf). Writes public/*.svg; PNG icons are rendered with rsvg-convert.
import base64, io
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image

NAME = 'XL Cal'
BLUE, GREEN, GREEN_LIGHT = '#4FA3C8', '#01734D', '#2FB27E'   # logo gradient; lighter green for dark UI
TILE = '#0a0a0a'

f = TTFont('Montserrat-Bold.ttf'); gs = f.getGlyphSet(); cmap = f.getBestCmap()
cap = f['OS/2'].sCapHeight

mark = Image.open('xl-mark.png').convert('RGBA')           # 408×506
def mark_uri(h):
    w = round(mark.width * h / mark.height)
    buf = io.BytesIO(); mark.resize((w * 4, h * 4), Image.LANCZOS).save(buf, 'PNG', optimize=True)
    return w, 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

def run(text, x0, track, scale, base):
    d, x = [], x0
    for ch in text:
        g = gs[cmap[ord(ch)]]
        if ch != ' ':
            pen = SVGPathPen(gs); g.draw(TransformPen(pen, (scale, 0, 0, -scale, x, base))); d.append(pen.getCommands())
        x += g.width * scale + track
    return ' '.join(d), x - track

# ── wordmark, 26px tall like cal.diy's: X mark + "XL CAL" ──
H, capPx = 26, 15
mw, muri = mark_uri(H)
s = capPx / cap; track = 0.06 * capPx
text_d, xend = run('XL CAL', mw + 7, track, s, (H + capPx) / 2)
W = round(xend + 0.5, 2)
def wordmark(end):
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink"><title>{NAME}</title>'
            f'<defs><linearGradient id="g" x1="{mw + 7}" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="{BLUE}"/><stop offset="1" stop-color="{end}"/></linearGradient></defs>'
            f'<image width="{mw}" height="{H}" href="{muri}" xlink:href="{muri}"/>'
            f'<path d="{text_d}" fill="url(#g)"/></svg>')

# ── icons: the X mark alone, plain and on a dark tile ──
def mark_svg(size, mark_h, tile, rx):
    w, uri = mark_uri(mark_h)
    x, y = (size - w) / 2, (size - mark_h) / 2
    bg = f'<rect width="{size}" height="{size}" rx="{rx}" fill="{TILE}"/>' if tile else ''
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink"><title>{NAME}</title>{bg}'
            f'<image x="{x}" y="{y}" width="{w}" height="{mark_h}" href="{uri}" xlink:href="{uri}"/></svg>')

# Safari pinned tab must be one flat colour: "XL" outlines
ps = 30 / cap; pd, pend = run('XL', 0, 0, ps, 43)
pin = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 56"><g transform="translate({(56 - pend) / 2} 0)"><path d="{pd}" fill="#000"/></g></svg>'

files = {
  'calcom-logo-white-word.svg': wordmark(GREEN),        # light backgrounds (the main LOGO)
  'cal-logo-word.svg':          wordmark(GREEN),
  'cal-logo-word-black.svg':    wordmark(GREEN),        # OG images
  'cal-logo-word-dark.svg':     wordmark(GREEN_LIGHT),  # dark backgrounds
  'cal-com-icon-white.svg':     mark_svg(56, 40, False, 0),
  'cal-com-icon.svg':           mark_svg(56, 36, True, 12),
  'safari-pinned-tab.svg':      pin,
  '_favicon-master.svg':        mark_svg(512, 360, True, 104),
}
for n, svg in files.items(): open(f'public/{n}', 'w').write(svg)
print(f'wordmark {W}×{H}px')
