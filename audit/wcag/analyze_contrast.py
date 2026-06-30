"""WCAG-Pixelkontrast: liest Hintergrund-Screenshot (Text ausgeblendet) + JSON (Rects/Farben) von
hero-contrast.mjs und misst pro Element den realen Kontrast (Relativluminanz) Text vs. Hintergrund.
Lauf: python audit/wcag/analyze_contrast.py <bg.png> <data.json> [label]
Bewertung: PASS wenn p90-Hintergrund die Schwelle haelt (4.5 Text / 3.0 large); 'worst' = lichtester Pixel."""
import sys, json
from PIL import Image

def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
def lum_rgb(r, g, b): return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
def contrast(l1, l2):
    a, b = max(l1, l2), min(l1, l2); return (a + 0.05) / (b + 0.05)
def parse_rgb(s):
    nums = s[s.find('(') + 1:s.find(')')].split(','); return tuple(float(x) for x in nums[:3])
def pct(v, p):
    if not v: return 0
    return v[min(len(v) - 1, int(round(p / 100.0 * (len(v) - 1))))]

bg = Image.open(sys.argv[1]).convert('RGB')
data = json.load(open(sys.argv[2], encoding='utf-8'))
label = sys.argv[3] if len(sys.argv) > 3 else ''
dpr = data['dpr']; px = bg.load()
print(f"=== {label}  (dpr={dpr}, bgsize={bg.size}) ===")
for it in data['items']:
    fr, fg, fb = parse_rgb(it['color']); tl = lum_rgb(fr, fg, fb)
    fs = it['fontSize']; fw = it['fontWeight']
    bold = str(fw) in ('700','800','900','bold')
    large = fs >= 24 or (bold and fs >= 18.66); thr = 3.0 if large else 4.5
    x0, y0 = max(0, int(it['x']*dpr)), max(0, int(it['y']*dpr))
    x1 = min(bg.size[0], int((it['x']+it['w'])*dpr)); y1 = min(bg.size[1], int((it['y']+it['h'])*dpr))
    L = [lum_rgb(*px[xx, yy]) for yy in range(y0, y1, 2) for xx in range(x0, x1, 2)]
    if not L: print(f"  {it['sel']:26s} no pixels"); continue
    L.sort(); med, p90, mx = pct(L, 50), pct(L, 90), L[-1]
    cm, c90, cw = contrast(tl, med), contrast(tl, p90), contrast(tl, mx)
    ok = "PASS" if c90 >= thr else ("borderline" if cm >= thr else "FAIL")
    print(f"  {it['sel']:26s} fs={fs:.0f}px {'large' if large else 'small'} thr={thr}  textL={tl:.3f}  "
          f"bgL med={med:.3f}/p90={p90:.3f}/max={mx:.3f}  contrast med={cm:.2f} p90={c90:.2f} worst={cw:.2f}  -> {ok}")
