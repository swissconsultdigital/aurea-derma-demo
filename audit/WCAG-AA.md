# AUREA — WCAG-2.2-AA-Audit

**Stand:** 1.7.2026 · Mockup-Strecke (index, longevity-b, datenschutz-b, impressum-b).
**Ergebnis:** Keine offenen AA-Verstösse. Kontrast deterministisch + pixelgenau belegt; statische
A11y-Dimensionen per 4-Perspektiven-Gremium auditiert, alle Befunde behoben.

## Methode (wiederholbar)

1. **Text-Kontrast auf soliden Flächen (1.4.3 / 1.4.11):** deterministisch über die Token-Paare —
   `python audit/wcag/contrast-pairs.py`. (Aktuell: **0 Fails**; niedrigster Wert ink-mut/hell 5.77:1.)
2. **Text über Bild (Hero, 1.4.3):** Pixelmessung gegen den realen Hintergrund (Text ausgeblendet,
   CDP-Screenshot) — `node audit/wcag/hero-contrast.mjs <url> <w> <h> bg.png data.json` +
   `python audit/wcag/analyze_contrast.py bg.png data.json`. Eyebrow/H1/Lead bei 360/390 alle ≥AA
   (Eyebrow-Worst 7.5:1 nach Scrim, Lead ≥10:1, H1 ≥9:1).
3. **Statische A11y (Tastatur/Fokus, ARIA/Struktur, Formulare, Reflow/Motion/Targets):** Audit gegen
   die Quelldateien je SC, Befunde mit Datei:Zeile.

## Bereits konform (Auszug)

Native Controls (Slider = echtes `input[type=range]` mit Pfeiltasten), Fokusfallen in Nav-Overlay
**und** Buchungs-Sheet (Tab-Zyklus, ESC, Fokus-Rückgabe, Scroll-Lock, Live-Region), keine positiven
tabindex, je Inhaltsseite eine `h1` mit logischer Gliederung, Landmarks header/nav/footer, `lang="de-CH"`,
eindeutige `<title>`, vollständige Formular-Semantik (label/for, fieldset/legend, aria-required/-invalid/
-describedby, `autocomplete`, role=alert/status), Dialog-Semantik, durchgängiges `prefers-reduced-motion`,
Touch-Ziele ≥44px, Zoom/Reflow bis 320px & 200%.

## Behobene Befunde (1.7.2026)

| SC | Schwere | Befund | Fix |
|---|---|---|---|
| 2.4.3 / 2.4.11 / 4.1.2 | major | Service-Modal `#bmodal` ohne Fokusfalle/-rückgabe | Fokus in Dialog, Tab-Trap, ESC, Fokus zurück an Auslöser (analog Sheet) |
| 1.3.1 | major | Kein `<main>`-Landmark | `<main id="hauptinhalt">` auf allen 4 Seiten |
| 1.3.1 / 2.4.6 | major | Rechtsseiten ohne `<h1>` (Haupttitel war h2) | Datenschutz/Impressum-Titel → `h1`, Abschnitte bleiben h2 |
| 4.1.2 | major | Auswahl-Buttons (Pills/Slots/Slider-Pills) ohne `aria-pressed` | `aria-pressed` an Fach-/Anliegen-/Slot-/Vorher-Nachher-Buttons (Markup + JS) |
| 1.4.11 | major | Formularfeld-Rahmen ~1.5:1 (<3:1) | `--field-line #7C7264` → 3.43:1 vs. Füllung / 3.72:1 vs. Panel |
| 2.4.7 | minor | Feld-`:focus` unterdrückte den 2px-Ring | `:focus-visible` 2px-Goldring zurück |
| 2.4.1 | minor | Kein Skip-Link | „Zum Inhalt springen" → `#hauptinhalt` (alle Seiten) |
| 4.1.2 | minor | Burger ohne initiales `aria-expanded` | `aria-expanded="false"` + `aria-controls` im Markup |
| 4.1.2 | minor | FAQ-Buttons ohne `aria-controls` | id + `aria-controls` + `role=region` zentral per JS |
| 1.1.1 | minor | Dekorative Inline-SVGs ohne `aria-hidden` | Init-Sweep: alle ungelabelten SVGs `aria-hidden`+`focusable=false` (23 Stück) |
| 1.3.1 | minor | Footer-Überschriften h4 nach h2 (h3 übersprungen) | Footer → `h3` |
| 1.4.11 | minor | Slider-Fokusring über Bild evtl. <3:1 | zusätzlicher dunkler Box-Shadow-Halo |

Offen/iterativ (Info, kein AA-Verstoss): native Radio/Checkbox-Rahmen sind UA-abhängig (Zielbrowser
gegenprüfen); Schritt-Zähler-Kreise in px (bei 200% Textzoom unkritisch, einstellig).

## Künftig

Vor jedem Release: `contrast-pairs.py` + die Hero-Pixelmessung laufen lassen; bei Markup-Änderungen die
betroffene A11y-Dimension gegenchecken. WordPress-Theme spiegelt die strukturellen Fixes (siehe STAND.md).
