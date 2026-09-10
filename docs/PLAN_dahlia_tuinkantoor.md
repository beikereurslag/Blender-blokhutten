# Plan — Dahlia 250x250+300+zijwand "Het Tuinkantoor" (2026-06-12)

## 1. Concept & waarom dit origineel is
- Dahlia heeft sinds vandaag de boerderij-oogsttuin-hero. Dit is het **tweede gezicht** van dezelfde cabin: hetzelfde model, totaal andere koper.
- **Scene-idee dat nog nooit is gedaan: werken-vanuit-de-tuin, ochtend.** Een tuinkantoor op een frisse werkdag-ochtend: fiets tegen de wand, bureau zichtbaar door het deurglas, koffie op de veranda, strakke onderhoudsarme tuin. Persona: De Stedelijke Ondernemer (stijlbijbel Modern, 35-55, koopt voor tuinkantoor).
- Onderscheid t.o.v. Lavendel-modern en Zonnebloem-modern (al gedaan): die waren architecturale avond/dag-heroes zonder verhaal. Hier draagt het **woon-werk-verhaal** de scene: de fiets (forens die niet meer forenst), de open laptop, het ochtendlicht.
- Geen enkele eerdere scene gebruikt het fiets-asset of een interieur-werkplek als focal.

## 2. Model-feiten (geprobed 12 jun, `pilots/base/Dahlia-250x250-300-zijwand.blend`)
- Footprint **5.93 × 2.91 m**, hoogte 2.34 m, plat dak (`flatroof-41-*`).
- Deur **+Y-voorzijde**, X 0.73..2.24 (gesloten deel rechts, X 0.13..2.83 binnenvolume), glas + chroom.
- Open veranda links: pole-0 op (−2.69, 1.18), open naar +Y.
- GLB-camera aanwezig → weg in P1. Materialen leeg → `build_clean_wood`.

## 3. Stijl & materialen (alleen echte producttextures)
Stijlbijbel: **Modern strak** — zwart potdeksel, warm houtaccent, géén rvs.
- Wanden gesloten deel: `assets/blokhutwinkel-textures/8192/kdi_potdeksel_zwart.jpg`
- Veranda-binnenwand + plafond: `luxehouse-onbehandeld.jpg` (warmte-break, bewezen two-tone uit Lavendel)
- Balken/palen: `kdi_rabat_fbz_zwart.jpg`
- Deur: `hardhout-deuren-ramen.jpg` (warm accent in zwart vlak — leest premium)
- Dak: `epdm.jpg`, rand `staalpannen-antraciet.jpg`
- Vlonder: `douglas.jpg` donker getint richting ipé (`#3A2F26` mix 0.3), planken haaks op gevel (stijlbijbel: leidt het oog naar binnen)

## 4. Scene-layout (coördinaten; cabin op origin, voorzijde +Y)
| Element | Positie | Detail |
|---|---|---|
| Grasgrond | 30×30 m | strak gemaaid, niet oververzadigd |
| Vlonder | X −3.0..3.0, Y 1.7..4.4 | volle breedte — moderne plint |
| Pad | betonplaten 0.8×0.4 m, Y 4.4..10, 8 mm voeg | `beton.jpg`, recht naar deur |
| **Fiets (focal)** | tegen gesloten wand, (2.6, 1.85), leunend | `assets/3daistudio/bicycle` |
| Werkplek interieur | bureau + stoel achter deurglas, X 1.2..2.0, Y 0.4..1.0 | simpel bureau proceduraal + `modern_arm_chair_01` |
| Koffietafel + stoel veranda | (−1.6, 2.6) | `coffee_table_round_01` + `outdoor_chair_scan_medpoly` |
| Beukenheg-blokken | 2 rechthoekige blokken 1.8×0.6×1.2 m op (−5, 5) en (4.5, 6.5) | GN shrub_03 op box-donor, strak |
| Siergras-drift | 15× Karl-Foerster-look langs pad-oost | `weed_plant_02` hertint strogeel, geclusterd |
| Heg perimeter | Y −5.5 en X ±8.5 | GN shrub_03, 1.7 m |
| Bomenringen | 3 ringen 13/17/22 m | birch + maple, dicht |
| Statement-boom | multi-stam berk (5.5, −1.5) | bewezen Birch-aanpak |

## 5. Compositie & camera
- 35 mm, 1.65 m, vanaf voor-rechts **(7.0, 9.0, 1.65)**, target (−0.2, 0.6, 1.25).
- Vanaf (+X,+Y): gesloten zwarte deel **links** in beeld met fiets goed leesbaar, veranda met koffietafel rechts-diep.
- Deur + verlicht bureau-interieur op linker power point; fiets net onder de horizonlijn-derde.
- Betonpad start onderin frame → leidt naar deur (leading line).

## 6. Licht & sfeer (frisse ochtend ~08:30)
- HDRI: `assets/polyhaven/hdri/kiara_1_dawn_2k.hdr`, strength 0.9, Z-rotatie zodat zon laag van rechts-achter camera komt (30-45° off-axis).
- Zon: 4800K licht koel-fris, energie 3.0, elevatie ~20° — lange koele schaduwen over het gras, strijklicht op potdeksel-profiel.
- Interieur: 1 area light warm 3000K boven bureau — het "ik zit al te werken"-signaal door het deurglas.
- Filmic, Medium High Contrast, exposure 0.3. Gras NIET oversatureren (amateur-tell).

## 7. Props & asset-paden
- Fiets: `assets/3daistudio/bicycle/` (schaal checken — GLB komt vaak in cm: ×0.01 + grounding)
- Stoel: `assets/sketchfab/furniture/outdoor_chair_scan_medpoly_gltf`
- Koffietafel: `assets/polyhaven/models/coffee_table_round_01_2k.blend`
- Bureau-stoel interieur: `assets/polyhaven/models/modern_arm_chair_01_2k.blend`
- Laptop: proceduraal (2 afgeronde boxen, scherm zwak emissief) — alleen als deurglas-doorkijk het toont; anders koffiemok (cilinder) op verandatafel
- Potplant strak: `potted_plant_01` ×2, symmetrisch bij deur — enige symmetrie in de scene
- Bollard-lampjes: 3× langs pad, `assets/sketchfab/lighting/garden_lamp.blend` (mat zwart hertinten)
- GN-heg + bomen: zelfde bewezen assets als altijd (shrub_03, birch/maple pack)

## 8. Bouwfases (headless, per fase script + save + diag 1280×720/64)
| Fase | Script | Inhoud |
|---|---|---|
| P1 | `build_dahlia_kantoor_p1.py` | GLB-cam weg, two-tone materialen, gras, HDRI+zon, camera |
| P2 | `build_dahlia_kantoor_p2.py` | Perimeter-heg + beukenblokken + bomenringen + statement-berk |
| P3 | `build_dahlia_kantoor_p3.py` | Vlonder + betonplaten-pad + bollards |
| P4 | `build_dahlia_kantoor_p4.py` | Fiets, meubels, interieur-werkplek, grassen-drift, potten |
| P4b | inspectiecams | close-ups: fiets, deurglas-doorkijk, veranda, pad |
| P5 | `build_dahlia_kantoor_p5.py` | validate + audit + 1080p preview |
| P6+ | fixes na feedback → finale | |

## 9. Risico's & fallbacks
- **Fiets-GLB** onbekende kwaliteit/schaal → P4b close-up verplicht; staat hij er raar bij (GLTF importeert regelmatig ondersteboven), dan tegen veranda-paal i.p.v. wand, of helemaal weg en koffietafel wordt focal.
- **Interieur door glas** kan te donker/ruisig zijn → area light feller of bureau dichter bij glas; werkt het niet, dan deur half open (deur-objecten roteerbaar) of interieur laten vallen.
- **Beukenblokken via GN op box**: scatter-dichtheid hoog genoeg dat de box-donor niet doorschijnt; anders donor-mesh een donkergroen basismateriaal geven.
- Karl-Foerster via hertint weed_plant is een benadering → in diag beoordelen; vlekkerig = vervangen door extra beukenblok.

## 10. Validatie & render-trap
- Audit elke fase (cabin-bbox leeg, niets >12 m), full-res crops bij twijfel.
- Anti-empty checklist; let op: pad-materiaal beton moet niet uitgewassen wit renderen (roughness 0.85, albedo dempen).
- Preview 1080p/160 → user-akkoord → finale 2560×1440/240 (playbook-instellingen).

## Output
`pilots/Dahlia-250x250-300-zijwand/style-modern-urban-cottage/dahlia_tuinkantoor.blend` + diag PNGs.
