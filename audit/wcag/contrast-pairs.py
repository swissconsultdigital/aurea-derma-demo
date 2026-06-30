"""Deterministische WCAG-Kontraste fuer die AUREA-Token-Paare (echte Verwendungen).
Lauf: python audit/wcag/contrast-pairs.py
Prueft Text/Flaeche-Paare auf soliden Noir-/Hell-Flaechen (1.4.3 Text 4.5:1, 1.4.11 UI 3:1).
Fuer Text UEBER Bild (Hero) siehe hero-contrast.mjs + analyze_contrast.py (Pixelmessung)."""
def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
def lum(hx):
    hx = hx.lstrip('#'); r, g, b = int(hx[0:2],16), int(hx[2:4],16), int(hx[4:6],16)
    return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)
def cr(a, b):
    la, lb = lum(a), lum(b); hi, lo = max(la,lb), min(la,lb)
    return (hi+0.05)/(lo+0.05)

# Tokens aus assets/style-b.css :root (bei Aenderung hier nachziehen)
T = dict(noir='#17130F', noir2='#1E1813', noir3='#271F18', bone='#F3ECDF', bonemut='#C3B7A4',
         gold='#CDA15E', goldsoft='#E6D2AC', light='#ECE5D9', light2='#E3DACB', ink='#1A1611',
         inkmut='#5E564A', lead='#E8E1D4', warn='#F2876A', green='#8FB98A')

# (fg, bg, kontext, threshold) — 4.5 normaler Text, 3.0 large(>=24px)/Nicht-Text-UI
pairs = [
    ('bone','noir','Text auf Seite',4.5), ('bone','noir2','Text auf Surface',4.5), ('bone','noir3','Text auf Panel/Karte',4.5),
    ('bonemut','noir','Muted/Hint',4.5), ('bonemut','noir2','Muted auf Surface',4.5), ('bonemut','noir3','Muted auf Panel',4.5),
    ('gold','noir','Eyebrow/Akzent',4.5), ('gold','noir2','Gold auf Surface',4.5), ('gold','noir3','Gold-Text auf Panel',4.5),
    ('goldsoft','noir','Gold-soft Akzent',4.5), ('goldsoft','noir2','Gold-soft auf Surface',4.5),
    ('lead','noir','Hero-Lead',4.5),
    ('warn','noir','Fehlertext',4.5), ('warn','noir2','Fehlertext Surface',4.5), ('warn','noir3','Fehlertext Panel',4.5),
    ('green','noir3','Badge-Punkt frei (UI)',3.0),
    ('ink','bone','Button-Label Creme',4.5), ('ink','gold','Auf Gold',4.5), ('ink','light','Text auf hell',4.5),
    ('inkmut','light','Muted auf hell',4.5), ('ink','goldsoft','Auf gold-soft',4.5),
    ('gold','noir','Fokusring/UI',3.0), ('gold','noir2','Fokusring Surface/UI',3.0), ('gold','noir3','Fokusring/Border Panel/UI',3.0),
]
print(f"{'FG':9s} {'BG':7s} {'ratio':>6s} {'thr':>4s}  {'':4s} kontext")
fails = 0
for fg, bg, ctx, thr in pairs:
    r = cr(T[fg], T[bg]); ok = 'PASS' if r >= thr else 'FAIL'
    fails += ok == 'FAIL'
    print(f"{fg:9s} {bg:7s} {r:6.2f} {thr:4.1f}  {ok:4s} {ctx}")
print(f"\n== {fails} FAIL(s) ==")
