# Plan — Dahlia "De Oogsttuin" (2026-06-12)

## Waarom dit concept
- **Dahlia** is de enige van de 8 cabin-lijnen zonder eigen hero-scene (alle 4 varianten alleen batch-previews).
- **Boerderij/landelijk** uit de Garden Style Bible is als stijl nog nooit als hero uitgewerkt (gedaan: modern ×2, japandi, scandi ×2, cottage, mediterraan-warm, hygge-avond).
- **Origineel scene-idee**: een *productieve* tuin — moestuin met kweekbakken en oogst-props — i.p.v. de puur decoratieve siertuinen van alle eerdere scenes. Dahlia's inventaris-stijlmatch is "Modern/boerderij"; het platte dak + open veranda maken het een *moderne* boerderijtuin (warm douglas, geen rode dakpannen verzinnen — alleen echte producttextures).

## Model-analyse (geprobed)
- `pilots/base/Dahlia-250x250-300-zijwand.blend` — 5.92 × 2.9 m, plat dak (EPDM), hoogte 2.34 m.
- Dichte cabine **rechts** (X 0.13..2.83), deur aan **voorzijde +Y** (X 0.73..2.24) met glas + chroom.
- Open veranda/canopy **links** (X -2.84..0.33) met achterwand, linker zijwand en paal op (-2.69, 1.18) — open naar +Y.
- Lege materialen-set zoals Jasmijn → zelfde `build_clean_wood` BOX-mapping aanpak.

## Scene-ontwerp
- **Cabin**: wanden douglas-rabat (honingbruin, echt product), balken/palen douglas, deur hardhout, dakrand staalpannen-antraciet, plat dak EPDM.
- **Compositie** (hero-regels): camera 35 mm op 1.65 m, 3/4 vanaf voor-rechts ±(8, 10); deur op power point rechts, veranda-diepte links open richting camera; horizon op onderste derde; geen kantelende verticalen (shift_y).
- **Voorgrond → deur**: klinkerpad (paving stones) recht naar de deur (boerderij-regel), **rozenboog** over het pad halverwege.
- **Moestuin links-midden**: 3 douglas kweekbakken met donkere mulch + gewassen (sorrel/weed/periwinkle-rijen), rieten mand + schep als oogst-props, vogelvoederhuisje.
- **Veranda**: picknicktafel (boer-tafel) + oude lantaarn, klinker-terras eronder.
- **Borders**: hortensia-look bloeiende drifts (spiraea/roses) rechts bij de deur, klaprozen bij de bakken — asymmetrisch: dicht aan gesloten kant, lucht aan veranda-kant.
- **Erfgrens**: GN-scatter heggen (echte shrub_03-blaadjes, bewezen methode) achter + zijkant.
- **Achtergrond**: 3 ringen bomen (pine/birch/maple) die de lucht occluderen — geen vliegend-eiland.
- **Licht**: spaichingen_hill HDRI (golden hour) + zon ~4500K laag, 30-45° off-axis achter camera; Filmic Medium High Contrast.

## Uitvoering (headless, per fase een script + diag-render + save)
| Fase | Script | Inhoud |
|---|---|---|
| P1 | `build_dahlia_p1.py` | GLB-camera weg, materialen, grasgrond, HDRI+zon, camera |
| P2 | `build_dahlia_p2.py` | GN-heggen + bomenringen + statement-boom |
| P3 | `build_dahlia_p3.py` | Pad, terras, kweekbakken + gewassen |
| P4 | `build_dahlia_p4.py` | Rozenboog, picknicktafel, lantaarn, potten, mand, borders |
| P5 | `build_dahlia_p5.py` | validate_scene + audit + camera-polish + 1080p preview |

Output: `pilots/Dahlia-250x250-300-zijwand/style-boerderij/dahlia_oogsttuin.blend` (+ diag PNGs).
Definitieve hero-render (2560×1440) pas na akkoord van de user.
