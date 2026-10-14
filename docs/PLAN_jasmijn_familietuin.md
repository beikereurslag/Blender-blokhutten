# Plan — Jasmijn 300x250+300+zijwand "De Familietuin" (2026-06-12)

## 1. Concept & waarom dit origineel is
- Jasmijn heeft de hygge-avond-hero (vuur, avond). Het tweede gezicht: **de zonnige zaterdagmiddag van een gezin**.
- **Scene-idee dat nog nooit is gedaan: de geleefde familietuin.** Picknicktafel met limonade-moment, groot speelgazon, zandbak bij de veranda, vogelbad — een tuin waar kinderen spelen en ouders bijkomen. Persona: De Plattelandsgezin / jonge gezinnen (style-klassiek-familie bestaat al als batch-categorie maar is nooit als hero uitgewerkt).
- Onderscheid t.o.v. Dahlia-oogsttuin (productief) en Lelie-cottage (decoratief weelderig): hier is **het gazon zelf de held** — open speelruimte als verkoopargument, omzoomd door vrolijke borders.
- Lichtmoment: volle zomermiddag met lichte bewolking — nog niet gebruikt (alles tot nu was golden hour, avond of strak daglicht).

## 2. Model-feiten (geprobed 12 jun, `pilots/base/Jasmijn-300x250-300-zijwand.blend`)
- Footprint **6.43 × 2.91 m**, hoogte 2.34 m, plat dak (`flatroof-71-*`).
- Deur **+Y-voorzijde**, X 0.73..2.24; veranda links, pole-0 op (−2.94, 1.18), open naar +Y.
- GLB-camera aanwezig → weg in P1. Materialen leeg → `build_clean_wood`.

## 3. Stijl & materialen (alleen echte producttextures)
Stijlbijbel: **Boerderij/landelijk-licht**, vriendelijk en blank.
- Wanden: `assets/blokhutwinkel-textures/8192/luxehouse-onbehandeld.jpg` (blank, warm, gezinsvriendelijk)
- Balken/palen: `douglas.jpg`
- Deur: `hardhout-deuren-ramen.jpg`
- Dak: `epdm.jpg`, rand `staalpannen-antraciet.jpg`
- Terras onder veranda: `kdi_rabat.jpg` als vlonder-look of klinker `paving_stones_64` (polyhaven textures) — kies in P3 wat het warmst leest
- Géén zwart, géén strakke cor-ten — dit is de toegankelijke gezinslijn.

## 4. Scene-layout (coördinaten; cabin op origin, voorzijde +Y)
| Element | Positie | Detail |
|---|---|---|
| Grasgrond | 30×30 m | **bewust groot open gazon** Y 4..9 vrijhouden — speelruimte is het verhaal |
| Terras | X −3.2..0.5, Y 1.7..4.0 | onder/voor veranda |
| **Picknicktafel (focal)** | (−1.5, 3.0) | `picnic_table_low_poly_gltf`; kan + 2 bekers (cilinders) erop |
| Zandbak | (3.8, 3.2), 1.5×1.5 m | proceduraal: douglas-kader 4 planken + zand (aerial_grass_rock → sand-tint of noise-bump beige) + emmertje weglaten als geen asset overtuigt |
| Vogelbad | (4.8, 6.5) | `assets/sketchfab/decor/birdbaths_gltf` |
| Vogelvoederhuisje | op paal bij border-rechts | `small_wooden_bird_feeder_gltf` (stond recht in Dahlia na fix — zelfde aanpak) |
| Klinkerpad | 0.9 m breed, Y 9.5 → deur | visgraat-look `paving_stones_64` |
| Borders | L+R van gazon, diep 1.2 m | hortensia (`bigleaf_hydrangea`), spiraea, butterfly bush — hoog-laag-ritme |
| Madeliefjes-spikkels | scatter `dandelion_01` dun over gazonranden | leefbaar gras, geen golfbaan |
| Heg perimeter | Y −5.5, X ±9 | GN shrub_03, 1.6 m |
| Bomenringen | 3 ringen 14/18/23 m | birch/maple/pine mix |
| Schaduw-boom | grote esdoorn (6, 4) | `maple_tree_scan` — slagschaduw op gazonrand |

## 5. Compositie & camera
- 35 mm, 1.65 m, vanaf voor-rechts **(8.0, 10.0, 1.65)**, target (−0.3, 0.8, 1.2).
- Vanaf (+X,+Y): cabin links-midden, gazon als open midden, picknicktafel onder veranda rechts-diep.
- Deur op power point; pad start onderin frame, buigt licht (gezinstuin mag zachter dan moderne rechte lijn — boerderij-regel "recht naar deur" hier bewust iets gebogen, het blijft leesbaar als route).
- Voorgrond: border-bloemen onscherp onderin (f/5.6) — kijkt de tuin ín.

## 6. Licht & sfeer (zomermiddag, licht bewolkt ~14:00)
- HDRI: `assets/polyhaven/hdri/kloofendal_48d_partly_cloudy_puresky_2k.hdr`, strength 1.0.
- Zon: 5200K neutraal-warm, energie 3.5, elevatie ~48° MAAR 35-40° off-axis zodat schaduwen modelleren (noon-flatness vermijden; stijl-research: middagzon is risico → de wolkjes en boomschaduw breken het).
- Esdoorn werpt schaduwpartij over gazonrand = diepte in het open groen (dode-zone-breker, compositieregel).
- Filmic, Medium High Contrast, exposure 0.3; gras-albedo dempen.

## 7. Props & asset-paden
- Picknicktafel: `assets/sketchfab/furniture/picnic_table_low_poly_gltf` (in Dahlia stond hij eerst op de kop — P4b close-up verplicht!)
- Vogelbad: `assets/sketchfab/decor/birdbaths_gltf`
- Voederhuisje: `assets/sketchfab/decor/small_wooden_bird_feeder_gltf`
- Hortensia: `assets/sketchfab/flowering_bushes/bigleaf_hydrangea_vgztealha_ue_raw`
- Spiraea: `goldmound_spiraea_red_flowering_gltf`; vlinderstuik: `multi_color_butterfly_bush_gltf`
- Madeliefjes: `assets/polyhaven/models/dandelion_01_2k.blend` (cluster-donor fix gebruiken — NOOIT _duplicate_collection_at direct!)
- Wasgoed aan lijn (optioneel sfeer-plus): lijn = curve tussen 2 palen, 3 doeken = subdivided planes met wave-modifier — ALLEEN houden als de P4b-crop overtuigt
- GN-heg: shrub_03; bomen: birch pack + maple + pine trio

## 8. Bouwfases (headless, per fase script + save + diag 1280×720/64)
| Fase | Script | Inhoud |
|---|---|---|
| P1 | `build_jasmijn_fam_p1.py` | GLB-cam weg, blanke materialen, gras, HDRI+zon, camera |
| P2 | `build_jasmijn_fam_p2.py` | Heg + bomenringen + schaduw-esdoorn |
| P3 | `build_jasmijn_fam_p3.py` | Klinkerpad, terras, zandbak-kader |
| P4 | `build_jasmijn_fam_p4.py` | Picknicktafel, vogelbad, voederhuisje, borders, madeliefjes, evt. waslijn |
| P4b | inspectiecams | close-ups: tafel, zandbak, borders, deurzone |
| P5 | `build_jasmijn_fam_p5.py` | validate + audit + 1080p preview |
| P6+ | fixes na feedback → finale | |

## 9. Risico's & fallbacks
- **Zandbak-zand** proceduraal kan als beton lezen → noise-bump + lichte oneffenheid in rand; leest het fout, dan zandbak vervangen door tweede zitje/speelkleed (plane + stoffen kleur).
- **Waslijn-doeken** zijn experimenteel → strikt optioneel, weglaten bij twijfel.
- **Open gazon = dode-zone-risico** (compositieregel) → boomschaduw + madeliefjes-spikkels + maailijn-suggestie (subtiele kleurbanen in gras-shader) breken het vlak.
- Picknicktafel/voederhuisje GLTF-oriëntatie → bekende valkuil, P4b verplicht.
- Geen speelgoed-assets aanwezig — NIET verzinnen met blokkerige DIY-meshes (anti-pattern); het verhaal werkt via zandbak + tafel + open gazon.

## 10. Validatie & render-trap
- Audit per fase; anti-empty checklist; let extra op: geen identieke-hoogte-struiken op rij (amateur-tell) — borders in hoog-laag-ritme.
- Preview 1080p/160 → user-akkoord → finale 2560×1440/240 (playbook).

## Output
`pilots/Jasmijn-300x250-300-zijwand/style-klassiek-familie/jasmijn_familietuin.blend` + diag PNGs.
